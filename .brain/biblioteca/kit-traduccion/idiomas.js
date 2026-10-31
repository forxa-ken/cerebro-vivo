/* Idiomas y textos del proyecto (kit de traducción, spec 057).
   Formato JSON estricto (comillas dobles, sin comas finales): lo lee también el test de paridad.
   Para añadir un idioma: una línea en "idiomas" y un bloque nuevo en "textos" con las mismas claves. */
window.KIT_I18N = {
  "claveGuardado": "mi_proyecto_lang",
  "porDefecto": "es",
  "iguales_permitidos": ["form.enviar"],
  "idiomas": {"es": "Español", "en": "English", "pt": "Português"},
  "textos": {
    "es": {
      "app.titulo": "Mi proyecto",
      "app.bienvenida": "Bienvenido",
      "app.descripcion": "Esta página cambia de idioma sin recargar.",
      "form.buscar": "Buscar…",
      "form.enviar": "Enviar"
    },
    "en": {
      "app.titulo": "My project",
      "app.bienvenida": "Welcome",
      "app.descripcion": "This page changes language without reloading.",
      "form.buscar": "Search…",
      "form.enviar": "Send"
    },
    "pt": {
      "app.titulo": "Meu projeto",
      "app.bienvenida": "Bem-vindo",
      "app.descripcion": "Esta página muda de idioma sem recarregar.",
      "form.buscar": "Pesquisar…",
      "form.enviar": "Enviar"
    }
  }
};
