import os
import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the section background
html = html.replace('<section id="dudas" class="py-24 bg-white border-t border-zinc-100">', 
                    '<section id="dudas" class="py-24 bg-zinc-950 relative overflow-hidden">\n            <div class="absolute top-0 left-1/4 w-96 h-96 bg-red-600/20 rounded-full blur-3xl opacity-50 pointer-events-none"></div>\n            <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-orange-600/10 rounded-full blur-3xl opacity-50 pointer-events-none"></div>')

# Replace text colors in the header
html = html.replace('<h2 class="text-4xl font-extrabold text-black mb-4">Preguntas Frecuentes</h2>', 
                    '<h2 class="text-4xl font-extrabold text-white mb-4 relative z-10">Preguntas Frecuentes</h2>')
html = html.replace('<p class="text-xl text-zinc-500">Todo transparente. Si tienes otra duda, mándame WhatsApp.</p>', 
                    '<p class="text-xl text-zinc-400 relative z-10">Todo transparente. Si tienes otra duda, mándame WhatsApp.</p>')
html = html.replace('<div class="space-y-4">', '<div class="space-y-4 relative z-10">')

# Replace the `<details>` items
html = html.replace('class="bg-zinc-50 border border-zinc-200 rounded-2xl group overflow-hidden"', 
                    'class="bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl group overflow-hidden"')

# Remove any `open` attribute that might have been left with the old classes just in case:
html = html.replace('class="bg-zinc-50 border border-zinc-200 rounded-2xl group overflow-hidden" open>', 
                    'class="bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl group overflow-hidden" open>')

# Replace the summary and answer texts inside FAQs
html = html.replace('text-black text-lg">\n                            <span>', 'text-white text-lg">\n                            <span>')
html = html.replace('border-zinc-200/50', 'border-white/10')
html = html.replace('text-zinc-600 leading-relaxed', 'text-zinc-300 leading-relaxed')

# Fix the specific "Nota" pill
html = html.replace('bg-zinc-200 px-2 py-1 rounded text-zinc-700', 'bg-white/10 px-2 py-1 rounded text-zinc-400')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    print("Updated index.html")

# 2. Update subpages
files = [
    "paquete-basico.html",
    "paquete-profesional.html",
    "paquete-empresarial.html",
    "paquete-tienda.html"
]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the section containing "Preguntas Frecuentes sobre"
    # We will use regex to capture the section start and inject blobs
    # The structure is: `<section class="py-16 bg-white border-t border-zinc-100">\n            <div class="max-w-3xl mx-auto px-6">\n                <h2 class="text-2xl font-extrabold text-black mb-8 text-center">Preguntas Frecuentes`
    
    pattern = re.compile(r'<section class="py-16 bg-white border-t border-zinc-100">(\s*<div class="max-w-3xl mx-auto px-6">\s*<h2 class="text-2xl font-extrabold text-black mb-8 text-center">Preguntas Frecuentes)')
    
    replacement = r'<section class="py-16 bg-zinc-950 relative overflow-hidden">\n            <div class="absolute top-0 left-0 w-72 h-72 bg-red-600/20 rounded-full blur-3xl opacity-50 pointer-events-none"></div>\n            <div class="absolute bottom-0 right-0 w-72 h-72 bg-orange-600/10 rounded-full blur-3xl opacity-50 pointer-events-none"></div>\1'
    
    html = pattern.sub(replacement, html)
    
    # Replace header color
    html = html.replace('<h2 class="text-2xl font-extrabold text-black mb-8 text-center">Preguntas Frecuentes', 
                        '<h2 class="text-2xl font-extrabold text-white mb-8 text-center relative z-10">Preguntas Frecuentes')
    
    # Add z-10 to the wrapper
    html = html.replace('<div class="space-y-6">', '<div class="space-y-6 relative z-10">')
    
    # Replace the items
    html = html.replace('<div class="border-b border-zinc-200 pb-4">', '<div class="bg-white/5 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-6">')
    html = html.replace('<h4 class="font-bold text-black', '<h4 class="font-bold text-white')
    html = html.replace('<p class="text-sm text-zinc-600">', '<p class="text-sm text-zinc-300">')
    
    # Fix the small pill
    html = html.replace('bg-zinc-100 px-1.5 py-0.5 rounded text-zinc-500', 'bg-white/10 px-1.5 py-0.5 rounded text-zinc-400')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Updated {filename}")
