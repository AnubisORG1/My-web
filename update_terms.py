import os
import re

files = [
    "paquete-basico.html",
    "paquete-profesional.html",
    "paquete-empresarial.html",
    "paquete-tienda.html"
]

new_faq_subpage = '''
        <div class="border-b border-zinc-200 pb-4">
            <h4 class="font-bold text-black mb-2 flex items-center gap-2"><i data-lucide="eye" class="w-4 h-4 text-red-600"></i> ¿Puedo ver una demostración antes de pagar?</h4>
            <p class="text-sm text-zinc-600">Sí. Mándanos tu info básica por WhatsApp y te enviaremos una previsualización de tu página sin costo ni compromiso. Si te gusta, procedemos al trato.<br>
            <span class="text-[11px] font-mono bg-zinc-100 px-1.5 py-0.5 rounded text-zinc-500 mt-2 inline-block">*Esta prueba inicial es 100% independiente y no te descuenta "vueltas de revisión" de tu plan.</span></p>
        </div>
'''

for filename in files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
        
    if '¿Puedo ver una demostración' not in html:
        # inject exactly after `<div class="space-y-6">`
        html = re.sub(r'(<div class="space-y-6">\s*)', r'\1' + new_faq_subpage + '\n', html, count=1)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Updated {filename}")
