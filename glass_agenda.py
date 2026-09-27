import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace Section
html = html.replace('<section id="cotizacion" class="py-24 bg-white border-t border-zinc-100">',
                    '<section id="cotizacion" class="py-32 bg-zinc-950 relative overflow-hidden">\n            <!-- Apple Glass Gradients -->\n            <div class="absolute top-1/4 left-0 w-96 h-96 bg-red-600/30 rounded-full blur-[120px] pointer-events-none"></div>\n            <div class="absolute bottom-1/4 right-0 w-96 h-96 bg-orange-600/20 rounded-full blur-[120px] pointer-events-none"></div>')

# 2. Replace Header
html = html.replace('<h2 class="text-3xl md:text-4xl font-bold text-black mb-4">Agenda tu proyecto</h2>',
                    '<h2 class="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight relative z-10">Agenda tu proyecto</h2>')
html = html.replace('<p id="form-desc" class="text-zinc-600">Cuéntame sobre tu proyecto completando este formulario. Te contactaré directo por WhatsApp.</p>',
                    '<p id="form-desc" class="text-lg text-zinc-400 relative z-10">Cuéntame sobre tu proyecto completando este formulario. Te contactaré directo por WhatsApp.</p>')

# 3. Replace Form Container
html = html.replace('<div class="bg-white rounded-3xl p-8 border border-zinc-200 shadow-xl shadow-zinc-100/50 relative overflow-hidden">',
                    '<div class="bg-white/5 backdrop-blur-3xl rounded-[2.5rem] p-8 md:p-12 border border-white/10 shadow-2xl relative overflow-hidden z-10">')
html = html.replace('<div id="form-decor-glow" class="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none"></div>', '')

# 4. Replace Labels
html = html.replace('class="block text-sm font-semibold text-zinc-800 mb-2"',
                    'class="block text-sm font-medium text-zinc-300 mb-2"')

# 5. Replace Inputs (text, select, textarea)
old_input = 'class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors"'
new_input = 'class="w-full bg-black/20 border border-white/10 rounded-2xl px-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-white/30 focus:bg-white/5 transition-all"'
html = html.replace(old_input, new_input)

# Replace textarea specifically if it has resize-none
old_textarea = 'class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors resize-none"'
new_textarea = 'class="w-full bg-black/20 border border-white/10 rounded-2xl px-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-white/30 focus:bg-white/5 transition-all resize-none"'
html = html.replace(old_textarea, new_textarea)

# Replace Package select (it had font-medium)
old_package = 'class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors font-medium"'
new_package = 'class="w-full bg-black/20 border border-white/10 rounded-2xl px-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-white/30 focus:bg-white/5 transition-all font-medium"'
html = html.replace(old_package, new_package)

# 6. Replace Google Business Block
html = html.replace('<div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100">',
                    '<div class="bg-blue-900/20 backdrop-blur-md p-5 rounded-2xl border border-blue-500/30">')
html = html.replace('<svg class="w-4 h-4 text-blue-600"', '<svg class="w-4 h-4 text-blue-400"')
html = html.replace('class="w-full bg-white border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black transition-colors mb-2"',
                    'class="w-full bg-black/30 border border-blue-500/30 rounded-2xl px-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-blue-400 transition-all mb-2"')

# 7. Replace Summary Block
html = html.replace('<div class="bg-black text-white p-6 rounded-2xl mt-4 hidden shadow-xl" id="summary-block">',
                    '<div class="bg-white/10 backdrop-blur-2xl border border-white/20 text-white p-6 rounded-3xl mt-6 hidden shadow-2xl" id="summary-block">')
html = html.replace('border-b border-zinc-800 pb-2', 'border-b border-white/10 pb-2')
html = html.replace('border-t border-zinc-800', 'border-t border-white/10')

# 8. Replace Form Error Alert
html = html.replace('<div id="form-error-alert" class="hidden p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm font-semibold flex items-center gap-2 shadow-sm">',
                    '<div id="form-error-alert" class="hidden p-4 bg-red-900/30 backdrop-blur-md border border-red-500/30 rounded-2xl text-red-200 text-sm font-semibold flex items-center gap-2 shadow-sm">')

# 9. Form submit text styling at bottom
html = html.replace('<p class="text-xs text-zinc-500 text-center mt-3 flex items-center justify-center gap-1.5">',
                    '<p class="text-xs text-zinc-400 text-center mt-4 flex items-center justify-center gap-1.5">')
html = html.replace('<button type="button" onclick="openModal(\'privacidad\')" class="text-zinc-600 underline hover:text-black transition-colors ml-1">',
                    '<button type="button" onclick="openModal(\'privacidad\')" class="text-zinc-300 underline hover:text-white transition-colors ml-1">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    print("Done")
