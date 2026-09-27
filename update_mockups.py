import os
import re

# Data structure containing the rich HTML mockups for each slide
packages_data = {
    "paquete-basico.html": {
        "id": "basico",
        "slides": [
            # Slide 1: Cafeteria Minimalista
            """
            <div class="snap-center shrink-0 w-full h-full relative">
                <img src="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover brightness-50" alt="Fondo Cafe">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full">
                        <span class="text-white font-serif italic text-lg">Café Noir</span>
                        <div class="flex gap-3 text-white/80 text-[9px] uppercase tracking-widest">
                            <span>Origen</span><span>Menú</span><span>Visítanos</span>
                        </div>
                    </div>
                    <div class="text-center">
                        <h3 class="text-white font-serif text-3xl mb-2">El arte del café,<br>en tu taza.</h3>
                        <p class="text-white/70 text-[10px] mb-4">Granos seleccionados de Veracruz.</p>
                        <button class="bg-white text-black px-5 py-2 rounded-full text-xs font-bold hover:bg-zinc-200 transition-colors">Ver Menú Digital</button>
                    </div>
                    <div class="flex gap-2">
                        <div class="bg-white/10 backdrop-blur-sm border border-white/20 p-2 rounded-lg flex-1 text-center"><i data-lucide="map-pin" class="w-3 h-3 text-white mx-auto mb-1"></i><span class="text-white text-[8px] block">Centro Histórico</span></div>
                        <div class="bg-white/10 backdrop-blur-sm border border-white/20 p-2 rounded-lg flex-1 text-center"><i data-lucide="clock" class="w-3 h-3 text-white mx-auto mb-1"></i><span class="text-white text-[8px] block">7am - 9pm</span></div>
                    </div>
                </div>
            </div>
            """,
            # Slide 2: Taller Mecánico Urbano
            """
            <div class="snap-center shrink-0 w-full h-full relative">
                <img src="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover brightness-[0.3]" alt="Fondo Taller">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full border-b border-white/10 pb-2">
                        <span class="text-yellow-500 font-black tracking-tighter text-xl uppercase">RACING<span class="text-white">PRO</span></span>
                        <div class="bg-yellow-500 text-black text-[9px] font-bold px-2 py-1 rounded">URGENCIAS 24/7</div>
                    </div>
                    <div>
                        <div class="w-8 h-1 bg-yellow-500 mb-3"></div>
                        <h3 class="text-white font-black text-2xl uppercase leading-none mb-2">Expertos en<br>Motores.</h3>
                        <p class="text-zinc-400 text-[10px] mb-4">Afinación, Frenos y Diagnóstico por Computadora.</p>
                        <button class="bg-yellow-500 text-black px-4 py-2 text-xs font-black uppercase hover:bg-yellow-400 transition-colors flex items-center gap-2">
                            <i data-lucide="wrench" class="w-3 h-3"></i> Cotizar Servicio
                        </button>
                    </div>
                    <div class="flex gap-2">
                        <div class="bg-zinc-900 border border-zinc-700 p-2 text-center w-full"><span class="text-white text-[9px] font-bold block">Ubicación GPS</span></div>
                        <div class="bg-green-600 p-2 text-center w-full"><span class="text-white text-[9px] font-bold block">WhatsApp</span></div>
                    </div>
                </div>
            </div>
            """,
            # Slide 3: Estética / Spa Elegante
            """
            <div class="snap-center shrink-0 w-full h-full relative">
                <img src="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover brightness-75" alt="Fondo Spa">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between bg-gradient-to-t from-pink-900/60 to-transparent">
                    <div class="flex justify-between items-center w-full">
                        <span class="text-white font-light tracking-widest text-sm uppercase">Lumière</span>
                        <i data-lucide="menu" class="w-5 h-5 text-white"></i>
                    </div>
                    <div class="text-center mt-auto mb-4">
                        <h3 class="text-white font-light text-2xl mb-1">Tu momento de<br>relajación absoluta.</h3>
                        <p class="text-white/80 text-[10px] font-light">Skin Care • Masajes • Beauty</p>
                    </div>
                    <button class="w-full bg-pink-100 text-pink-900 py-3 rounded text-xs font-semibold tracking-widest uppercase hover:bg-white transition-colors">
                        Agendar Cita
                    </button>
                </div>
            </div>
            """
        ]
    },
    "paquete-profesional.html": {
        "id": "pro",
        "slides": [
            # Slide 1: Consultorio Médico
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-zinc-50">
                <img src="https://images.unsplash.com/photo-1638202993928-7267aad84c31?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover opacity-20" alt="Fondo Medico">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full bg-white shadow-sm p-2 rounded-lg">
                        <span class="text-blue-600 font-bold text-sm flex items-center gap-1"><i data-lucide="activity" class="w-4 h-4"></i> MediCare</span>
                        <div class="flex gap-2 text-zinc-500 text-[9px] font-semibold">
                            <span>Especialidades</span><span>Pacientes</span>
                        </div>
                    </div>
                    <div class="bg-white/80 backdrop-blur-md p-4 rounded-xl border border-white shadow-lg mt-4">
                        <span class="text-blue-600 text-[8px] font-bold uppercase tracking-widest mb-1 block">Atención Especializada</span>
                        <h3 class="text-zinc-900 font-bold text-xl mb-2 leading-tight">Salud y bienestar<br>para tu familia.</h3>
                        <p class="text-zinc-500 text-[10px] mb-3">Agenda tu consulta presencial o por videollamada con nuestros especialistas.</p>
                        <div class="flex gap-2">
                            <button class="bg-blue-600 text-white px-3 py-2 rounded text-[10px] font-bold flex-1 shadow-md shadow-blue-600/30">Portal de Pacientes</button>
                            <button class="bg-zinc-100 text-zinc-600 px-3 py-2 rounded text-[10px] font-bold border border-zinc-200">Doctores</button>
                        </div>
                    </div>
                    <div class="flex justify-around items-center bg-white shadow-sm rounded-lg p-2 mt-auto">
                        <div class="text-center"><i data-lucide="phone" class="w-4 h-4 text-blue-600 mx-auto"></i><span class="text-[7px] text-zinc-500 block font-bold mt-1">Llamar</span></div>
                        <div class="w-px h-6 bg-zinc-200"></div>
                        <div class="text-center"><i data-lucide="map" class="w-4 h-4 text-blue-600 mx-auto"></i><span class="text-[7px] text-zinc-500 block font-bold mt-1">Ubicación</span></div>
                        <div class="w-px h-6 bg-zinc-200"></div>
                        <div class="text-center"><i data-lucide="calendar" class="w-4 h-4 text-blue-600 mx-auto"></i><span class="text-[7px] text-zinc-500 block font-bold mt-1">Citas</span></div>
                    </div>
                </div>
            </div>
            """,
            # Slide 2: Despacho Legal Corporativo
            """
            <div class="snap-center shrink-0 w-full h-full relative">
                <img src="https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover brightness-[0.4]" alt="Fondo Abogados">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between border-8 border-white/5 m-2">
                    <div class="text-center pt-2">
                        <span class="text-white font-serif text-lg tracking-widest uppercase border-b border-amber-600/50 pb-1 inline-block">Mendoza & Asoc.</span>
                    </div>
                    <div>
                        <h3 class="text-white font-serif text-2xl mb-2">Defensa y<br>Estrategia Legal.</h3>
                        <p class="text-zinc-300 text-[10px] font-light leading-relaxed mb-4 max-w-[80%]">Más de 20 años de experiencia protegiendo el patrimonio de empresas y particulares.</p>
                        <button class="border border-amber-600 text-amber-500 px-4 py-2 text-[10px] uppercase tracking-widest hover:bg-amber-600 hover:text-white transition-colors">Solicitar Asesoría</button>
                    </div>
                </div>
            </div>
            """,
            # Slide 3: Agencia / Portafolio
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-black">
                <div class="absolute inset-0 bg-gradient-to-br from-violet-600 via-fuchsia-600 to-orange-600 opacity-40"></div>
                <div class="relative z-10 p-6 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full">
                        <div class="w-6 h-6 rounded bg-white text-black flex items-center justify-center font-black text-xs">A.</div>
                        <span class="text-white font-bold text-[10px] px-2 py-1 border border-white/20 rounded-full">Proyectos</span>
                    </div>
                    <div>
                        <h3 class="text-white font-black text-4xl tracking-tighter leading-none mb-3">Creamos<br>el futuro.</h3>
                        <div class="flex gap-2">
                            <span class="text-[9px] bg-white/20 text-white px-2 py-1 rounded-full">Branding</span>
                            <span class="text-[9px] bg-white/20 text-white px-2 py-1 rounded-full">Marketing</span>
                            <span class="text-[9px] bg-white/20 text-white px-2 py-1 rounded-full">UX/UI</span>
                        </div>
                    </div>
                    <button class="w-full bg-white text-black py-3 rounded-xl text-xs font-black flex items-center justify-between px-4 hover:scale-105 transition-transform">
                        Ver Portafolio <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>
            """
        ]
    },
    "paquete-empresarial.html": {
        "id": "emp",
        "slides": [
            # Slide 1: Bienes Raíces Premium
            """
            <div class="snap-center shrink-0 w-full h-full relative">
                <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover brightness-75" alt="Fondo Inmueble">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center bg-white/90 backdrop-blur-md p-2 rounded-lg shadow-xl">
                        <span class="text-zinc-900 font-serif font-bold text-xs uppercase tracking-widest">LUXE REALTY</span>
                        <i data-lucide="search" class="w-4 h-4 text-zinc-600"></i>
                    </div>
                    
                    <div class="bg-white/95 backdrop-blur-xl p-4 rounded-2xl shadow-2xl mt-auto">
                        <span class="bg-zinc-900 text-white text-[8px] uppercase tracking-widest px-2 py-1 rounded mb-2 inline-block">Propiedad Destacada</span>
                        <h3 class="text-zinc-900 font-serif text-lg leading-tight mb-1">Villa Serena, Los Cabos</h3>
                        <p class="text-zinc-500 text-[10px] mb-3"><i data-lucide="map-pin" class="w-3 h-3 inline"></i> Frente al mar • 4 Hab • Alberca</p>
                        
                        <div class="bg-zinc-100 rounded-lg p-2 mb-3 flex justify-between items-center">
                            <span class="text-zinc-900 font-bold text-sm">$2.5M USD</span>
                            <span class="text-[9px] text-zinc-500 uppercase">En venta</span>
                        </div>
                        
                        <button class="w-full bg-zinc-900 text-white py-2 rounded-lg text-[10px] uppercase tracking-widest font-bold hover:bg-black transition-colors">
                            Ver Detalles
                        </button>
                    </div>
                </div>
            </div>
            """,
            # Slide 2: Constructora / Industrial
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-zinc-900">
                <img src="https://images.unsplash.com/photo-1541888086225-f64112e56cc1?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-overlay grayscale" alt="Fondo Construccion">
                <div class="relative z-10 p-5 h-full flex flex-col">
                    <div class="border-l-4 border-yellow-500 pl-3 mb-6 mt-2">
                        <span class="text-white font-black text-xl tracking-tighter">BUILD<span class="text-yellow-500">CORP</span></span>
                    </div>
                    
                    <div class="mt-auto">
                        <h3 class="text-white font-black text-3xl uppercase leading-none mb-3">Ingeniería<br>que perdura.</h3>
                        <div class="grid grid-cols-2 gap-2 mb-4">
                            <div class="bg-zinc-800/80 border border-zinc-700 p-2 rounded text-center">
                                <span class="text-yellow-500 font-black text-lg block">15+</span>
                                <span class="text-zinc-400 text-[7px] uppercase">Años Exp.</span>
                            </div>
                            <div class="bg-zinc-800/80 border border-zinc-700 p-2 rounded text-center">
                                <span class="text-yellow-500 font-black text-lg block">200</span>
                                <span class="text-zinc-400 text-[7px] uppercase">Proyectos</span>
                            </div>
                        </div>
                        <button class="w-full bg-yellow-500 text-black py-3 text-xs font-black uppercase hover:bg-yellow-400 transition-colors shadow-[4px_4px_0_0_#fff]">
                            Cotizar Proyecto
                        </button>
                    </div>
                </div>
            </div>
            """,
            # Slide 3: Corporativo / Tech B2B
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-[#0B0F19]">
                <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-900/40 via-[#0B0F19] to-[#0B0F19]"></div>
                <div class="relative z-10 p-6 h-full flex flex-col">
                    <div class="flex justify-between items-center mb-10">
                        <span class="text-white font-bold tracking-tight flex items-center gap-1"><i data-lucide="hexagon" class="w-4 h-4 text-blue-500"></i> NexusData</span>
                        <i data-lucide="menu" class="w-5 h-5 text-zinc-500"></i>
                    </div>
                    
                    <div>
                        <span class="text-blue-500 text-[9px] font-bold uppercase tracking-widest mb-2 block border border-blue-500/30 w-fit px-2 py-1 rounded-full bg-blue-500/10">Enterprise Solutions</span>
                        <h3 class="text-white font-bold text-2xl leading-tight mb-3">Escala tus<br>operaciones con IA.</h3>
                        <p class="text-zinc-400 text-[10px] mb-6">Plataforma integral de gestión de datos para empresas de alto rendimiento.</p>
                        
                        <div class="flex gap-3">
                            <button class="bg-blue-600 text-white px-4 py-2 rounded text-[10px] font-bold hover:bg-blue-500 transition-colors shadow-lg shadow-blue-600/20">Solicitar Demo</button>
                            <button class="text-white px-4 py-2 rounded text-[10px] font-bold hover:bg-white/5 transition-colors">Planes <i data-lucide="chevron-right" class="w-3 h-3 inline"></i></button>
                        </div>
                    </div>
                </div>
            </div>
            """
        ]
    },
    "paquete-tienda.html": {
        "id": "shop",
        "slides": [
            # Slide 1: Moda E-commerce
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-zinc-100">
                <img src="https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-[60%] object-cover" alt="Fondo Ropa">
                <div class="relative z-10 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full p-4">
                        <i data-lucide="menu" class="w-5 h-5 text-black"></i>
                        <span class="text-black font-serif font-bold text-lg tracking-widest uppercase">VOGUE</span>
                        <div class="relative">
                            <i data-lucide="shopping-bag" class="w-5 h-5 text-black"></i>
                            <div class="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full text-white text-[7px] flex items-center justify-center font-bold">2</div>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-t-3xl p-5 mt-auto shadow-[0_-10px_40px_rgba(0,0,0,0.1)]">
                        <div class="flex justify-between items-end mb-3">
                            <div>
                                <span class="text-zinc-400 text-[9px] uppercase tracking-widest block mb-1">Nueva Colección</span>
                                <h3 class="text-black font-serif text-xl">Abrigo de Lana Premium</h3>
                            </div>
                            <span class="text-black font-bold">$2,499</span>
                        </div>
                        <div class="flex gap-2 mb-4">
                            <div class="w-6 h-6 rounded-full bg-zinc-900 border-2 border-white ring-1 ring-zinc-300"></div>
                            <div class="w-6 h-6 rounded-full bg-[#D4C3B3] border-2 border-white ring-1 ring-transparent"></div>
                        </div>
                        <button class="w-full bg-black text-white py-3 rounded-full text-[10px] font-bold uppercase tracking-widest hover:bg-zinc-800 transition-colors">
                            Añadir al Carrito
                        </button>
                    </div>
                </div>
            </div>
            """,
            # Slide 2: Tienda de Gadgets / Tech
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-black">
                <img src="https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-full object-cover opacity-50 mix-blend-luminosity" alt="Fondo PS5">
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full bg-zinc-900/80 backdrop-blur-md p-3 rounded-2xl border border-white/10">
                        <span class="text-white font-black italic text-sm">TECH<span class="text-blue-500">ZONE</span></span>
                        <div class="bg-blue-600 rounded-lg p-1.5 relative"><i data-lucide="shopping-cart" class="w-4 h-4 text-white"></i></div>
                    </div>
                    
                    <div class="mt-auto">
                        <div class="inline-block bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[9px] font-bold px-2 py-1 rounded mb-2">Envío Gratis MTY</div>
                        <h3 class="text-white font-bold text-2xl leading-tight mb-1">PlayStation 5 Pro</h3>
                        <p class="text-zinc-400 text-[10px] mb-4">Experimenta la nueva generación de gaming con ray-tracing a 4K.</p>
                        
                        <div class="flex items-center gap-3">
                            <span class="text-white font-black text-xl">$11,999</span>
                            <button class="flex-1 bg-blue-600 text-white py-2 rounded-xl text-xs font-bold hover:bg-blue-500 transition-colors shadow-[0_0_20px_rgba(37,99,235,0.4)]">
                                Comprar Ahora
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            """,
            # Slide 3: Tienda Productos Naturales / Skin care
            """
            <div class="snap-center shrink-0 w-full h-full relative bg-[#F7F9F5]">
                <img src="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=800&q=80" class="absolute inset-0 w-full h-[50%] object-cover rounded-b-[40px] shadow-sm" alt="Fondo Skincare">
                <div class="relative z-10 p-5 h-full flex flex-col">
                    <div class="flex justify-between items-center w-full">
                        <div class="bg-white/80 backdrop-blur-sm p-2 rounded-full"><i data-lucide="search" class="w-4 h-4 text-green-800"></i></div>
                        <span class="text-green-900 font-serif font-bold text-sm tracking-widest">BOTANICA</span>
                        <div class="bg-white/80 backdrop-blur-sm p-2 rounded-full relative"><i data-lucide="shopping-bag" class="w-4 h-4 text-green-800"></i></div>
                    </div>
                    
                    <div class="mt-auto pt-10">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <h3 class="text-green-950 font-serif text-xl leading-tight">Serum Hidratante<br>Ácido Hialurónico</h3>
                            </div>
                            <span class="text-green-800 font-bold">$450</span>
                        </div>
                        <p class="text-green-800/60 text-[10px] mb-4">100% Orgánico • Cruelty Free</p>
                        
                        <div class="flex gap-2">
                            <div class="flex items-center gap-3 bg-white border border-green-100 px-3 py-2 rounded-xl">
                                <span class="text-green-800 font-bold">-</span>
                                <span class="text-green-950 font-bold text-xs">1</span>
                                <span class="text-green-800 font-bold">+</span>
                            </div>
                            <button class="flex-1 bg-green-800 text-white py-2 rounded-xl text-[10px] uppercase tracking-widest font-bold hover:bg-green-900 transition-colors">
                                Agregar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            """
        ]
    }
}

# Now we need to update the HTML files. We will locate the inner carousel div `<div id="carousel-XXX"...>` and replace its contents.
# Wait, currently the contents are just `<img src="..." ...>`
# The regex will target the inside of `<div id="carousel-XXX" ...>` and `</div>`

for filename, data in packages_data.items():
    if not os.path.exists(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # We want to replace the contents inside the div with id carousel-XXX
    # The regex matches from `<div id="carousel-XXX" ...>` until the next `</div>`
    pattern = re.compile(rf'(<div id="carousel-{data["id"]}"[^>]*>)(.*?)(</div>\s*<!-- Glass Navigation Arrows -->)', re.DOTALL)
    
    slides_html = "\n".join(data["slides"])
    
    # Ensure all aspect-ratio properties on the container so they look identical to the old images
    # We will add min-w-full to the slide containers above to ensure snap scrolling works
    # Wait, the slides in python string above use `snap-center shrink-0 w-full h-full relative`.
    # Let's wrap them all in the replacement string.
    
    def replacer(match):
        return match.group(1) + "\n" + slides_html + "\n" + match.group(3)

    if pattern.search(html):
        html = pattern.sub(replacer, html)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {filename} with rich HTML mockups.")
    else:
        print(f"Could not find carousel div in {filename}.")
