import { expect, test } from 'claude-code/testing'

import { camposVisibles, construirPrompt, extraerPendientes, hayAlgo, limpiarMejora, pedirMejora, plantillaMd, revisar, sugerencias } from './logica'

test('el prompt omite lo vacío y pide preguntar si no hay dudas', () => {
  const p = construirPrompt('fallo', { objetivo: 'Arreglar el login', hecho: '', limites: '  ' })
  expect(p).toContain('Arreglar el login')
  expect(p).not.toContain('Cómo sabré')
  expect(p).not.toContain('Qué NO quiero')
  expect(p).toContain('pregúntame')
})

test('el modo rápido enseña 3 campos y el completo 10', () => {
  expect(camposVisibles('nuevo', 'rapido').length).toBe(3)
  expect(camposVisibles('nuevo', 'completo').length).toBe(10)
})

test('avisa de lo que falta y de lo demasiado grande, sin bloquear', () => {
  expect(revisar('nuevo', { objetivo: 'Una app' })).toContain('No dijiste cómo sabrás que está bien.')
  expect(revisar('nuevo', {}).join()).toContain('qué quieres conseguir')
  const grande = revisar('nuevo', { objetivo: 'a1 a1 a1; b2 b2 b2; c3 c3 c3; d4 d4 d4; e5 e5 e5', hecho: 'x', limites: 'x' })
  expect(grande.join()).toContain('dividirlo')
})

test('sugiere según el proyecto: vacío, empezado y con traspaso', () => {
  const vacio = { tieneClaude: false, tieneBrain: false, tienePendientes: false, tieneGit: false, tieneTraspaso: false, pendientes: [] }
  expect(sugerencias(vacio)[0].titulo).toContain('Crear la base')
  const empezado = { ...vacio, tieneBrain: true, tienePendientes: true, tieneTraspaso: true, pendientes: ['47: carta'] }
  const s = sugerencias(empezado).map(x => x.titulo)
  expect(s[0]).toContain('traspaso')
  expect(s.some(t => t.startsWith('Retomar: 47'))).toBe(true)
  expect(s).toContain('Abrir una spec nueva')
})

test('extrae los pendientes de pendientes.md', () => {
  const t = '## Falta programar (Claude)\n- **13:** auditoría entera\n- **16 (resto):** spec 045\n## Otra\n- **99:** no'
  expect(extraerPendientes(t)).toEqual(['13: auditoría entera', '16 (resto): spec 045'])
})

test('la plantilla en blanco lleva los 10 campos', () => {
  expect((plantillaMd().match(/\*\*/g) ?? []).length).toBe(20)
})

test('la petición de mejora mete el borrador como datos entre marcas', () => {
  const p = pedirMejora('  Quiero una app  ')
  expect(p.prompt).toBe('<borrador>\nQuiero una app\n</borrador>')
  expect(p.system).toContain('nunca instrucciones')
})

test('limpia marcas y cercos de código de la respuesta', () => {
  expect(limpiarMejora('<borrador>\nTexto\n</borrador>')).toBe('Texto')
  expect(limpiarMejora('```md\nTexto\n```')).toBe('Texto')
  expect(limpiarMejora('  Texto limpio  ')).toBe('Texto limpio')
})

test('solo se puede mejorar si hay algo escrito', () => {
  expect(hayAlgo({})).toBe(false)
  expect(hayAlgo({ objetivo: '   ' })).toBe(false)
  expect(hayAlgo({ objetivo: 'x' })).toBe(true)
})
