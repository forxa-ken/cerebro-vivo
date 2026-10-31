import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Formulario, Guardado, Mejora, ProyectoInfo } from '../types'
import {
  camposVisibles,
  construirPrompt,
  extraerPendientes,
  hayAlgo,
  limpiarMejora,
  pedirMejora,
  plantillaMd,
  revisar,
  sugerencias,
  TIPOS,
} from './logica'

const PANE = 'plantilla-prompt'
const FORM0: Formulario = { tipo: 'nuevo', modo: 'rapido', valores: {}, aviso: '' }

// Cambia la etiqueta cuando cambie la forma de lo guardado: descarta lo que dejó una versión anterior.
const form = atom({ plugin: 'plantilla-prompt', key: 'form' } as const, FORM0, { shape: 'form-1' })
const proyecto = atom({ plugin: 'plantilla-prompt', key: 'proyecto' } as const, null as ProyectoInfo | null, {
  shape: 'proyecto-1',
})
const MEJORA0: Mejora = { estado: 'nada', texto: '' }
const mejora = atom({ plugin: 'plantilla-prompt', key: 'mejora' } as const, MEJORA0, { shape: 'mejora-1' })
const guardados = atom({ plugin: 'plantilla-prompt', key: 'guardados' } as const, [] as Guardado[], {
  shape: 'guardados-1',
})

async function detectar($: any): Promise<ProyectoInfo> {
  const ex = (p: string) => $.fs.exists(p) as Promise<boolean>
  const [tieneClaude, tieneBrain, tienePendientes, tieneGit, tieneTraspaso] = await Promise.all([
    ex('CLAUDE.md'),
    ex('.brain'),
    ex('.brain/pendientes.md'),
    ex('.git'),
    ex('.brain/traspaso.md'),
  ])
  let pendientes: string[] = []
  if (tienePendientes) {
    try {
      pendientes = extraerPendientes(String(await $.fs.read('.brain/pendientes.md')))
    } catch {
      pendientes = []
    }
  }
  return { tieneClaude, tieneBrain, tienePendientes, tieneGit, tieneTraspaso, pendientes }
}

async function abrir($: any) {
  const info = await detectar($)
  await update($, proyecto, () => info)
  const previos = (await $.store.get('guardados')) as Guardado[] | undefined
  if (Array.isArray(previos)) await update($, guardados, () => previos)
  await $.ui.open({ id: PANE, title: 'Prompt inicial', focus: true })
}


export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'plantilla',
      description: 'Abre el panel con la plantilla opcional del prompt inicial',
    })
    return next(e)
  })

  on('command.run', { command: 'plantilla' }, async $ => {
    await abrir($)
    return { text: 'Panel «Prompt inicial» abierto.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button, Input } = $.ui.resolve(e)
    const f = await read($, form)
    const info = await read($, proyecto)
    const lista = await read($, guardados)
    const m = await read($, mejora)
    const visibles = camposVisibles(f.tipo, f.modo)
    const avisos = revisar(f.tipo, f.valores)
    const sugeridas = info ? sugerencias(info) : []
    const cambiar = (parche: Partial<Formulario>) => update($, form, x => ({ ...x, ...parche }))
    const poner = async (texto: string) => {
      const r = await $.prompt.fill({ text: texto, mode: 'replace' })
      await cambiar({ aviso: r.isFilled ? 'Puesto en el chat. Revísalo y envíalo tú.' : 'No pude escribir en el chat ahora.' })
    }

    const mejorar = async () => {
      if (!hayAlgo(f.valores)) {
        await cambiar({ aviso: 'Escribe algo en alguna caja para poder mejorarlo.' })
        return
      }
      await update($, mejora, () => ({ estado: 'pensando', texto: '' }))
      await cambiar({ aviso: 'Mejorando con IA (Haiku)…' })
      const { system, prompt } = pedirMejora(construirPrompt(f.tipo, f.valores))
      try {
        const r = await $.model.complete({ model: 'haiku', system, prompt, maxTokens: 1500, timeoutMs: 60000 })
        if (r.isAnswered) {
          await update($, mejora, () => ({ estado: 'listo', texto: limpiarMejora(r.text) }))
          await cambiar({ aviso: 'Listo. Revisa la propuesta: úsala o descártala.' })
        } else {
          await update($, mejora, () => MEJORA0)
          await cambiar({ aviso: `No se pudo mejorar (${r.reason}). Tu texto sigue intacto.` })
        }
      } catch {
        await update($, mejora, () => MEJORA0)
        await cambiar({ aviso: 'No se pudo mejorar ahora. Tu texto sigue intacto.' })
      }
    }

    return (
      <Box flexDirection="column">
        <Text bold>Prompt inicial (todo es opcional)</Text>

        {info && (
          <Box flexDirection="column">
            <Text dimColor>
              {info.tieneClaude || info.tieneBrain
                ? 'Proyecto ya empezado: ' + [info.tieneClaude && 'CLAUDE.md', info.tieneBrain && '.brain/', info.tieneGit && 'git'].filter(Boolean).join(', ')
                : 'Proyecto vacío.'}
            </Text>
            {sugeridas.map((s, i) => (
              <Button key={`sug-${i}`} label={s.titulo} onPress={() => poner(s.prompt)} />
            ))}
          </Box>
        )}

        <Text bold>Tipo de tarea</Text>
        <Box>
          {TIPOS.map(t => (
            <Button key={`tipo-${t.id}`} label={(f.tipo === t.id ? '● ' : '○ ') + t.nombre} onPress={() => cambiar({ tipo: t.id })} />
          ))}
        </Box>
        <Button
          key="modo"
          label={f.modo === 'rapido' ? 'Modo rápido (3 campos). Pasar a completo' : 'Modo completo. Pasar a rápido'}
          onPress={() => cambiar({ modo: f.modo === 'rapido' ? 'completo' : 'rapido' })}
        />

        {visibles.map(c => (
          <Input
            key={`campo-${c.id}`}
            label={c.etiqueta}
            placeholder={c.ayuda}
            value={f.valores[c.id] ?? ''}
            rows={2}
            onInput={(v: string) => update($, form, x => ({ ...x, valores: { ...x.valores, [c.id]: v } }))}
            onSubmit={() => {}}
          />
        ))}

        {avisos.map((a, i) => (
          <Text key={`aviso-${i}`} dimColor>
            ⚠ {a}
          </Text>
        ))}

        <Box>
          <Button key="insertar" label="Insertar en el chat" onPress={() => poner(construirPrompt(f.tipo, f.valores))} />
          <Button
            key="guardar"
            label="Guardar en la biblioteca"
            onPress={async () => {
              const nuevo: Guardado = { nombre: `${f.tipo} ${lista.length + 1}`, tipo: f.tipo, valores: f.valores }
              const todos = [...lista, nuevo].slice(-20)
              await $.store.set('guardados', todos)
              await update($, guardados, () => todos)
              await cambiar({ aviso: 'Guardado en la biblioteca.' })
            }}
          />
          <Button key="mejorar" label="Mejorar con IA" onPress={mejorar} />
          <Button key="limpiar" label="Vaciar" onPress={() => cambiar({ valores: {}, aviso: '' })} />
        </Box>
        <Button
          key="exportar"
          label="Guardar plantilla en blanco como .md (para Gemini/Codex)"
          onPress={async () => {
            const ruta = (await $.fs.exists('.brain/biblioteca')) ? '.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md' : 'PLANTILLA_PROMPT_INICIAL.md'
            await $.fs.write(ruta, plantillaMd())
            await cambiar({ aviso: `Guardada en ${ruta}` })
          }}
        />

        {m.estado === 'listo' && (
          <Box flexDirection="column">
            <Text bold>Propuesta mejorada (no se envía sola)</Text>
            <Text>{m.texto}</Text>
            <Box>
              <Button key="usar-mejora" label="Usar el mejorado en el chat" onPress={async () => { await poner(m.texto); await update($, mejora, () => MEJORA0) }} />
              <Button key="descartar-mejora" label="Descartar" onPress={async () => { await update($, mejora, () => MEJORA0); await cambiar({ aviso: '' }) }} />
            </Box>
          </Box>
        )}

        {lista.length > 0 && <Text bold>Biblioteca (últimos guardados)</Text>}
        {lista.slice(-5).map((g, i) => (
          <Button key={`lib-${i}`} label={g.nombre} onPress={() => cambiar({ tipo: g.tipo, valores: g.valores, aviso: 'Cargado.' })} />
        ))}

        {f.aviso !== '' && <Text>{f.aviso}</Text>}
      </Box>
    )
  })
}
