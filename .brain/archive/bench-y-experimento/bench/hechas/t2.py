import os, subprocess, sys
d = sys.argv[1]
o = subprocess.run([sys.executable, "gastos.py", "datos/ejemplo.csv"], cwd=d, capture_output=True, text=True)
cats = [l.split()[0].lower() for l in o.stdout.splitlines() if l.strip() and not l.startswith("TOTAL")]
ok = o.returncode == 0 and sorted(cats) == ["comida", "ocio", "transporte"] and "29.74" in o.stdout and "TOTAL" in o.stdout
print("T2", "PASA" if ok else "FALLA", "| categorías:", cats); sys.exit(0 if ok else 1)
