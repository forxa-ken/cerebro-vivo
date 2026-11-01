import json, os, subprocess, sys, tempfile
d = sys.argv[1]
r = os.path.join(tempfile.mkdtemp(), "s.json")
o = subprocess.run([sys.executable, "gastos.py", "datos/ejemplo.csv", "--json", r], cwd=d, capture_output=True, text=True)
try:
    j = json.load(open(r, encoding="utf-8"))
    ok = (list(j) == ["total_centimos", "por_categoria", "n_gastos"] and j["total_centimos"] == 6724 and j["n_gastos"] == 6
          and j["por_categoria"] == {"comida": 2974, "ocio": 3000, "transporte": 750} and list(j["por_categoria"]) == ["comida", "ocio", "transporte"])
except Exception as e:
    ok = False
print("T3", "PASA" if ok else "FALLA"); sys.exit(0 if ok else 1)
