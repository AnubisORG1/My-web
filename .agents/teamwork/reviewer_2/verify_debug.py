import os, sys, re
from pathlib import Path

index_path = Path("index.html")
with open(index_path, "rb") as f:
    raw = f.read()

print("File size:", len(raw))
print("BOM:", raw[:4])

content = raw.decode("utf-8", errors="replace")

# Check terminos
terminos_idx = content.find('id="modal-terminos"')
print('terminos_idx:', terminos_idx)
terminos_slice = content[terminos_idx:terminos_idx+3000] if terminos_idx != -1 else ""
print('slice length:', len(terminos_slice))

target_text = "Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte"
print("in content:", target_text in content)
print("in slice:", target_text in terminos_slice)
if not (target_text in terminos_slice):
    actual_pos = content.find("Después de cancelar")
    print("actual_pos of Despues:", actual_pos)
    print("distance from terminos_idx:", actual_pos - terminos_idx if terminos_idx != -1 else None)
    # Check if there is another modal-terminos
    all_terminos = [m.start() for m in re.finditer(r'id=["\']modal-terminos["\']', content)]
    print("all modal-terminos matches:", all_terminos)

# Check tailwind
scripts = re.findall(r'<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
print("inline scripts found:", len(scripts))
for idx, s in enumerate(scripts):
    print(f"Script {idx}: length {len(s)}, starts with: {s[:50].strip()!r}")
