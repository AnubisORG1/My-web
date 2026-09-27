import os
import re

files = [
    "paquete-basico.html",
    "paquete-profesional.html",
    "paquete-empresarial.html",
    "paquete-tienda.html"
]

css_injection = '''
        /* Custom Glassmorphism Scrollbar */
        .glass-scrollbar::-webkit-scrollbar {
            height: 6px;
        }
        .glass-scrollbar::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            margin: 0 4px;
        }
        .glass-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        /* Firefox support */
        .glass-scrollbar {
            scrollbar-width: thin;
            scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.05);
        }
'''

js_old = "activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });"
js_new = """
                    // Horizontal scroll only to prevent vertical page jumps (mini zoom/cut-off effect)
                    const bar = activeBtn.parentElement;
                    const scrollLeft = activeBtn.offsetLeft - (bar.offsetWidth / 2) + (activeBtn.offsetWidth / 2);
                    bar.scrollTo({ left: scrollLeft, behavior: 'smooth' });
"""

for filename in files:
    if not os.path.exists(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Inject CSS into existing <style> block
    if '.glass-scrollbar' not in html:
        # Find the end of the <style> block we added earlier
        html = html.replace('</style>', css_injection + '\n    </style>')
        
    # Replace scrollbar-hide with glass-scrollbar on the template-bar
    html = html.replace('scrollbar-hide snap-x" id="template-bar"', 'glass-scrollbar snap-x pb-3 px-1" id="template-bar"')
    
    # Fix the JS scrollIntoView bug
    html = html.replace(js_old, js_new)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filename}")
