#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ventana del instalador del kit de arranque (spec 055). Pide los datos, instala y comprueba con `instalar.py`.

Se abre con doble clic en `instalar_kit.bat`. Solo `tkinter` (viene con Python). La lógica (validar, resumen,
ejecutar, recordar datos) está fuera de la ventana para poder probarla sin pantalla."""

import importlib.util
import json
import os
import threading

AQUI = os.path.dirname(os.path.abspath(__file__))
PREFERENCIAS = os.path.join(AQUI, "preferencias.json")  # solo en este equipo (ignorado por Git)
_espec = importlib.util.spec_from_file_location("instalar", os.path.join(AQUI, "instalar.py"))
kit = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(kit)

NIVELES = {
    "ligero": "Ligero: índice, pendientes y registro (proyecto pequeño o de pocos días).",
    "medio": "Medio: + reglas, decisiones, hechos y specs (semanas, varios chats).",
    "completo": "Completo: + guardianes, avisos automáticos, secretos y pruebas (meses, dinero o datos de usuarios).",
}
NOMBRES_IA = {"claude": "Claude", "gemini": "Antigravity / Gemini", "codex": "GPT Codex"}


def cargar_preferencias():
    try:
        with open(PREFERENCIAS, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def guardar_preferencias(datos):
    try:
        with open(PREFERENCIAS, "w", encoding="utf-8") as f:
            json.dump({k: datos[k] for k in ("dueno", "idioma", "pruebas") if datos.get(k)}, f, ensure_ascii=False)
    except Exception:
        pass  # recordar los datos es una comodidad: si falla, no se avisa


def validar(datos):
    """{campo: mensaje} con lo que falta o está mal; vacío si todo está bien."""
    errores = {}
    if not (datos.get("destino") or "").strip():
        errores["destino"] = "Elige la carpeta del proyecto."
    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "Escribe el nombre del proyecto."
    if not datos.get("ias"):
        errores["ias"] = "Marca al menos una IA."
    if datos.get("nivel") not in kit.NIVELES:
        errores["nivel"] = "Elige un nivel."
    return errores


def argumentos(datos):
    return dict(destino=datos["destino"].strip(), nombre=datos["nombre"].strip(), dueno=(datos.get("dueno") or "").strip() or "el dueño",
                idioma=(datos.get("idioma") or "").strip() or "español",
                pruebas=(datos.get("pruebas") or "").strip() or "python -m unittest discover tests",
                ias=list(datos["ias"]), nivel=datos["nivel"], traduccion=bool(datos.get("traduccion")))


def texto_resumen(datos):
    """Frase de confirmación con lo que se crearía (sin escribir nada)."""
    a = argumentos(datos)
    hechos = kit.instalar(simular=True, **a)
    t = "Se instalará el nivel %s en:\n%s\n\nSe crearán %d archivo(s)." % (a["nivel"], os.path.abspath(a["destino"]), len(hechos["creados"]))
    if hechos["respetados"]:
        t += "\n%d ya existen y NO se tocarán." % len(hechos["respetados"])
    return t + "\n\n¿Continuar?"


def _lineas(resultados):
    return ["%s %s: %s" % ("✅" if bien else "❌", nombre, frase) for nombre, bien, frase in resultados]


def ejecutar(datos, git_init=True):
    """Instala y comprueba. Devuelve (líneas para mostrar, todo_ok)."""
    a = argumentos(datos)
    hechos = kit.instalar(git_init=git_init, **a)
    guardar_preferencias(a)
    lineas = ["Kit instalado (nivel %s): %d archivo(s) creados, %d ya existían y no se tocaron." % (a["nivel"], len(hechos["creados"]), len(hechos["respetados"]))]
    lineas += ["- " + t for t in hechos["avisos"]]
    ok = True
    if a["nivel"] == "completo":
        resultados = kit.comprobar(a["destino"])
        ok = all(bien for _, bien, _ in resultados)
        lineas += [""] + _lineas(resultados)
        lineas.append("\nSiguiente paso: reiniciar Claude Code en esa carpeta." if ok else "\nRevisa los ❌ antes de empezar a trabajar.")
    return lineas, ok


def comprobar(datos):
    resultados = kit.comprobar((datos.get("destino") or "").strip())
    return _lineas(resultados), all(bien for _, bien, _ in resultados)


def abrir_ventana():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError:  # Mac/Linux: algunos Python no traen tkinter (spec 013)
        print("Falta tkinter, la parte gráfica de Python. Instálalo (Mac: `brew install python-tk`) o usa el instalador "
              "por línea de comandos: python3 .brain/biblioteca/kit-arranque/instalar.py DESTINO --nombre N --dueno D --idioma I")
        return

    pref = cargar_preferencias()
    raiz = tk.Tk()
    raiz.title("Instalar Cerebro Vivo en un proyecto nuevo")
    raiz.minsize(700, 700)
    marco = ttk.Frame(raiz, padding=14)
    marco.pack(fill="both", expand=True)
    marco.columnconfigure(1, weight=1)

    v = {"destino": tk.StringVar(), "nombre": tk.StringVar(), "dueno": tk.StringVar(value=pref.get("dueno", "")),
         "idioma": tk.StringVar(value=pref.get("idioma", "español")),
         "pruebas": tk.StringVar(value=pref.get("pruebas", "python -m unittest discover tests")),
         "nivel": tk.StringVar(value="completo"), "git": tk.BooleanVar(value=True), "traduccion": tk.BooleanVar(value=False)}
    ias = {k: tk.BooleanVar(value=(k == "claude")) for k in NOMBRES_IA}
    errores = {}

    def fila(n, etiqueta, ayuda, widget):
        ttk.Label(marco, text=etiqueta).grid(row=n, column=0, sticky="nw", pady=(8, 0), padx=(0, 10))
        widget.grid(row=n, column=1, sticky="ew", pady=(8, 0))
        ttk.Label(marco, text=ayuda, foreground="#666").grid(row=n + 1, column=1, columnspan=2, sticky="w")
        errores[etiqueta] = ttk.Label(marco, text="", foreground="#b00020")
        errores[etiqueta].grid(row=n + 2, column=1, columnspan=2, sticky="w")

    carpeta = ttk.Frame(marco)
    carpeta.columnconfigure(0, weight=1)
    ttk.Entry(carpeta, textvariable=v["destino"]).grid(row=0, column=0, sticky="ew")

    def examinar():
        elegida = filedialog.askdirectory(title="Carpeta del proyecto nuevo")
        if elegida:
            v["destino"].set(os.path.normpath(elegida))
            if not v["nombre"].get():
                v["nombre"].set(os.path.basename(os.path.normpath(elegida)))
    ttk.Button(carpeta, text="Examinar…", command=examinar).grid(row=0, column=1, padx=(6, 0))
    fila(0, "Carpeta del proyecto", "Puede estar vacía o ya tener archivos: nunca se pisa nada.", carpeta)
    fila(3, "Nombre del proyecto", "Se usa en los índices y en los chats («Nombre #1»).", ttk.Entry(marco, textvariable=v["nombre"]))
    fila(6, "Tu nombre", "Con él te hablará la IA. Se recuerda para la próxima vez.", ttk.Entry(marco, textvariable=v["dueno"]))
    fila(9, "Idioma", "Idioma de las respuestas de la IA.", ttk.Combobox(marco, textvariable=v["idioma"], values=["español", "English", "português"]))
    fila(12, "Comando de pruebas", "Lo que se ejecuta tras cada cambio para comprobar que todo sigue bien.", ttk.Entry(marco, textvariable=v["pruebas"]))
    caja = ttk.Frame(marco)
    for k, nombre in NOMBRES_IA.items():
        ttk.Checkbutton(caja, text=nombre, variable=ias[k]).pack(side="left", padx=(0, 12))
    fila(15, "IA que usarás", "Cada IA lee su propio índice de entrada.", caja)
    niv = ttk.Frame(marco)
    for k in NIVELES:
        ttk.Radiobutton(niv, text=k.capitalize(), value=k, variable=v["nivel"]).pack(side="left", padx=(0, 12))
    fila(18, "Nivel", NIVELES["completo"], niv)
    ayuda_nivel = marco.grid_slaves(row=19, column=1)[0]
    v["nivel"].trace_add("write", lambda *_: ayuda_nivel.config(text=NIVELES.get(v["nivel"].get(), "")))
    ttk.Checkbutton(marco, text="Crear el repositorio Git si no existe (activa el bloqueo de secretos al hacer commit)",
                    variable=v["git"]).grid(row=21, column=0, columnspan=3, sticky="w", pady=(10, 0))

    ttk.Checkbutton(marco, text="Añadir idiomas español / inglés / portugués (kit de traducción, opcional)",
                    variable=v["traduccion"]).grid(row=22, column=0, columnspan=3, sticky="w", pady=(4, 0))

    salida = tk.Text(marco, height=11, wrap="word", state="disabled", background="#f7f7f7")
    salida.grid(row=24, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
    marco.rowconfigure(24, weight=1)

    def mostrar(lineas):
        salida.config(state="normal")
        salida.delete("1.0", "end")
        salida.insert("end", "\n".join(lineas))
        salida.config(state="disabled")

    def datos():
        return {"destino": v["destino"].get(), "nombre": v["nombre"].get(), "dueno": v["dueno"].get(), "idioma": v["idioma"].get(),
                "pruebas": v["pruebas"].get(), "nivel": v["nivel"].get(), "ias": [k for k, b in ias.items() if b.get()],
                "traduccion": v["traduccion"].get()}

    campos = {"destino": "Carpeta del proyecto", "nombre": "Nombre del proyecto", "ias": "IA que usarás", "nivel": "Nivel"}

    def hay_errores(d):
        for e in errores.values():
            e.config(text="")
        mal = validar(d)
        for campo, msg in mal.items():
            errores[campos[campo]].config(text=msg)
        return bool(mal)

    botones = []

    def en_hilo(funcion, d):
        for b in botones:
            b.config(state="disabled")
        mostrar(["Trabajando…"])

        resultado = []  # el hilo solo deja aquí su resultado; la ventana lo recoge desde su propio hilo (Tk no es seguro entre hilos)

        def trabajo():
            try:
                resultado.append(funcion(d)[0])
            except Exception as e:
                resultado.append(["❌ No se pudo completar: %s" % e])

        def recoger():
            if resultado:
                mostrar(resultado[0])
                for b in botones:
                    b.config(state="normal")
            else:
                raiz.after(150, recoger)
        threading.Thread(target=trabajo, daemon=True).start()
        raiz.after(150, recoger)

    def instalar_click():
        d = datos()
        if hay_errores(d):
            return
        if messagebox.askyesno("Confirmar", texto_resumen(d)):
            en_hilo(lambda x: ejecutar(x, git_init=v["git"].get()), d)

    def comprobar_click():
        d = datos()
        if not d["destino"].strip():
            hay_errores(d)
            return
        en_hilo(comprobar, d)

    barra = ttk.Frame(marco)
    barra.grid(row=23, column=0, columnspan=3, sticky="ew", pady=(14, 0))
    botones += [ttk.Button(barra, text="Instalar", command=instalar_click), ttk.Button(barra, text="Solo comprobar", command=comprobar_click)]
    for b in botones:
        b.pack(side="left", padx=(0, 8))
    ttk.Button(barra, text="Cerrar", command=raiz.destroy).pack(side="right")
    return raiz, v, ias, datos, en_hilo, mostrar


if __name__ == "__main__":
    abrir_ventana()[0].mainloop()
