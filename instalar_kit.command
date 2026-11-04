#!/bin/sh
# Abre la ventana para instalar Cerebro Vivo en un proyecto nuevo (Mac; spec 013). Doble clic.
# Si no se abre: en Terminal, `chmod +x instalar_kit.command` una vez.
cd "$(dirname "$0")" || exit 1
if [ -x "venv/bin/python" ]; then PY="venv/bin/python"; elif command -v python3 >/dev/null 2>&1; then PY="python3"; else
  echo "No encuentro Python 3. Instálalo desde https://www.python.org/downloads/ y vuelve a abrir este archivo."; read -r _; exit 1
fi
"$PY" -c "import tkinter" 2>/dev/null || { echo "Falta tkinter (Mac: brew install python-tk). Alternativa: python3 .brain/biblioteca/kit-arranque/instalar.py DESTINO --nombre N --dueno D --idioma I"; read -r _; exit 1; }
exec "$PY" ".brain/biblioteca/kit-arranque/instalar_gui.py"
