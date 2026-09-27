import sys

with open(r'c:\Users\joshu\OneDrive\Desktop\My web\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines, 1):
    low = line.lower()
    for kw in ['id="paquetes"', 'id="precios"', 'paquetes', 'básica', 'profesional', 'mantenimiento', 'soporte', 'sla', '250', '800', 'mensual', 'días hábiles', 'dias habiles', 'tiempo de respuesta']:
        if kw in low:
            print(f"{idx}: {line.strip()[:120]}")
            break
