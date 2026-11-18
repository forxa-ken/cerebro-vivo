import subprocess, sys
o = subprocess.run([sys.executable, "gastos.py", "datos/ejemplo.csv", "--min", "10"], cwd=sys.argv[1], capture_output=True, text=True)
s = o.stdout
ok = o.returncode == 0 and "42.50" in s and "30.00" in s and "12.50" in s and "Transporte" not in s
print("T1", "PASA" if ok else "FALLA"); sys.exit(0 if ok else 1)
