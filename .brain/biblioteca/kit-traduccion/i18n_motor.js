/**
 * Motor de idiomas del kit de traducción (spec 057).
 * Lee la configuración de `window.KIT_I18N` (archivo idiomas.js) y no contiene textos propios.
 * Atributos: data-i18n (texto), data-i18n-html, data-i18n-placeholder, data-i18n-title, data-i18n-aria.
 * Selector automático: cualquier <select data-i18n-selector> se rellena con los idiomas de la lista.
 */
(function () {
    var C = window.KIT_I18N || {};
    var textos = C.textos || {};
    var idiomas = C.idiomas || {};
    var clave = C.claveGuardado || "kit_lang";
    var base = textos[C.porDefecto] ? C.porDefecto : Object.keys(textos)[0] || "es";
    var actual = base;

    try {
        var guardado = localStorage.getItem(clave);
        if (guardado && textos[guardado]) actual = guardado;
    } catch (e) { /* sin almacenamiento: se usa el idioma por defecto */ }

    function buscar(lang, key) {
        var dic = textos[lang];
        return dic && Object.prototype.hasOwnProperty.call(dic, key) ? dic[key] : null;
    }

    // Idioma actual -> idioma por defecto -> texto de respaldo -> la propia clave
    function t(key, respaldo) {
        if (!key) return respaldo || "";
        var v = buscar(actual, key);
        if (v === null) v = buscar(base, key);
        return v !== null ? v : (respaldo || key);
    }

    function aplicar(selector, atributo, destino) {
        document.querySelectorAll(selector).forEach(function (el) {
            var texto = t(el.getAttribute(atributo));
            if (texto !== el.getAttribute(atributo)) destino(el, texto);
        });
    }

    function prepararSelectores() {
        document.querySelectorAll("select[data-i18n-selector]").forEach(function (sel) {
            if (!sel.options.length) {
                Object.keys(idiomas).forEach(function (cod) {
                    var op = document.createElement("option");
                    op.value = cod;
                    op.textContent = idiomas[cod];
                    sel.appendChild(op);
                });
                sel.addEventListener("change", function () { setIdioma(sel.value); });
            }
            sel.value = actual;
        });
    }

    function actualizar() {
        aplicar("[data-i18n]", "data-i18n", function (el, x) { el.textContent = x; });
        aplicar("[data-i18n-html]", "data-i18n-html", function (el, x) { el.innerHTML = x; });
        aplicar("[data-i18n-placeholder]", "data-i18n-placeholder", function (el, x) { el.setAttribute("placeholder", x); });
        aplicar("[data-i18n-title]", "data-i18n-title", function (el, x) { el.setAttribute("title", x); });
        aplicar("[data-i18n-aria]", "data-i18n-aria", function (el, x) { el.setAttribute("aria-label", x); });
        prepararSelectores();
        document.documentElement.setAttribute("lang", actual);
        window.dispatchEvent(new CustomEvent("kit:lang_changed", { detail: { lang: actual } }));
    }

    function setIdioma(lang) {
        if (!textos[lang]) return;
        actual = lang;
        try { localStorage.setItem(clave, lang); } catch (e) { /* no se pudo recordar: no es grave */ }
        actualizar();
    }

    window.KitI18n = { t: t, setIdioma: setIdioma, getIdioma: function () { return actual; }, idiomas: idiomas, actualizar: actualizar };

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", actualizar);
    else actualizar();
})();
