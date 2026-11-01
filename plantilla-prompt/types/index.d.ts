export type Guardado = { nombre: string; tipo: string; valores: Record<string, string> }
export type Formulario = { tipo: string; modo: 'rapido' | 'completo'; valores: Record<string, string>; aviso: string }
export type Mejora = { estado: 'nada' | 'pensando' | 'listo'; texto: string }
export type ProyectoInfo = {
  tieneClaude: boolean
  tieneBrain: boolean
  tienePendientes: boolean
  tieneGit: boolean
  tieneTraspaso: boolean
  pendientes: string[]
}

declare module 'claude-code' {
  interface PluginState {
    'plantilla-prompt': {
      form: Shaped<Formulario>
      proyecto: Shaped<ProyectoInfo | null>
      guardados: Shaped<Guardado[]>
      mejora: Shaped<Mejora>
    }
  }
}
