import os
import re

packages_data = {
    "paquete-basico.html": {
        "id": "basico",
        "slides": [
            {"id": "s1", "name": "Café Minimalista", "img": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full">
                        <span class="text-white font-serif italic text-lg">Café Noir</span>
                        <div class="flex gap-2 text-white/80 text-[8px] uppercase tracking-widest">
                            <span>Origen</span><span>Menú</span>
                        </div>
                    </div>
                    <div class="text-center">
                        <h3 class="text-white font-serif text-2xl mb-1">El arte del café,<br>en tu taza.</h3>
                        <button class="bg-white text-black px-4 py-1.5 rounded-full text-[10px] font-bold mt-2">Menú Digital</button>
                    </div>
                    <div class="flex gap-2">
                        <div class="bg-white/10 backdrop-blur-sm border border-white/20 p-2 rounded-lg flex-1 text-center"><span class="text-white text-[8px] block">Centro Histórico</span></div>
                    </div>
                </div>
            '''},
            {"id": "s2", "name": "Taller Urbano", "img": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <div class="flex justify-between items-center w-full border-b border-white/10 pb-2">
                        <span class="text-yellow-500 font-black tracking-tighter text-lg uppercase">RACING<span class="text-white">PRO</span></span>
                    </div>
                    <div>
                        <div class="w-6 h-1 bg-yellow-500 mb-2"></div>
                        <h3 class="text-white font-black text-xl uppercase leading-none mb-2">Expertos en<br>Motores.</h3>
                        <button class="bg-yellow-500 text-black px-3 py-1.5 text-[10px] font-black uppercase">Cotizar</button>
                    </div>
                </div>
            '''},
            {"id": "s3", "name": "Spa Elegante", "img": "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between bg-gradient-to-t from-pink-900/60 to-transparent">
                    <span class="text-white font-light tracking-widest text-xs uppercase text-center w-full block">Lumière</span>
                    <div class="text-center mt-auto mb-4">
                        <h3 class="text-white font-light text-xl mb-1">Tu momento de<br>relajación.</h3>
                    </div>
                    <button class="w-full bg-pink-100 text-pink-900 py-2 rounded text-[10px] font-semibold tracking-widest uppercase">Agendar</button>
                </div>
            '''},
            {"id": "s4", "name": "Gym Neón", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <span class="text-green-400 font-black text-xl italic tracking-tighter">IRONFIT</span>
                    <div class="text-left mt-auto">
                        <h3 class="text-white font-black text-3xl uppercase leading-none mb-2">Supérate.</h3>
                        <button class="bg-green-500 text-black px-4 py-2 text-[10px] font-black uppercase">Únete hoy</button>
                    </div>
                </div>
            '''},
            {"id": "s5", "name": "Barbería Clásica", "img": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between bg-gradient-to-t from-black/80 to-transparent">
                    <span class="text-amber-500 font-serif text-lg text-center block border-b border-amber-500/30 pb-2">GENTLEMEN'S</span>
                    <div class="text-center">
                        <button class="border border-amber-500 text-amber-500 px-4 py-2 text-[10px] uppercase">Reservar Cita</button>
                    </div>
                </div>
            '''},
            {"id": "s6", "name": "Taquería Local", "img": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <span class="text-red-500 font-black text-2xl drop-shadow-md">EL REY</span>
                    <div class="mt-auto">
                        <h3 class="text-white font-black text-2xl mb-2 drop-shadow-md">El verdadero<br>sabor.</h3>
                        <button class="bg-red-600 text-white px-4 py-2 rounded-full text-[10px] font-bold">Ver Menú</button>
                    </div>
                </div>
            '''},
            {"id": "s7", "name": "Odontología", "img": "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <span class="text-blue-500 font-bold text-sm bg-white px-2 py-1 rounded w-fit">SmileClinic</span>
                    <div class="bg-white/90 p-3 rounded-lg">
                        <h3 class="text-blue-900 font-bold text-lg mb-1">Sonrisas perfectas.</h3>
                        <button class="w-full bg-blue-500 text-white py-1.5 rounded text-[10px] font-bold">Agendar Valoración</button>
                    </div>
                </div>
            '''},
            {"id": "s8", "name": "Estudio Foto", "img": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=70", "html": '''
                <div class="relative z-10 p-5 h-full flex flex-col justify-between">
                    <span class="text-white font-mono text-xs tracking-widest border border-white p-1 w-fit">FOCUS.STUDIO</span>
                    <div class="text-center mt-auto">
                        <h3 class="text-white font-light text-2xl mb-3">Capturando<br>momentos.</h3>
                        <button class="bg-white text-black px-4 py-2 text-[10px] font-bold">Portafolio</button>
                    </div>
                </div>
            '''}
        ]
    },
    "paquete-profesional.html": {
        "id": "pro",
        "slides": [
            {"id": "s1", "name": "Consultorio Clínico", "img": "https://images.unsplash.com/photo-1638202993928-7267aad84c31?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-blue-600 font-bold text-sm bg-white p-2 rounded-lg">MediCare</span><div class="bg-white/80 p-4 rounded-xl mt-4"><h3 class="text-zinc-900 font-bold text-xl mb-2">Salud y bienestar.</h3><button class="bg-blue-600 text-white px-3 py-2 rounded text-[10px] font-bold w-full">Portal Pacientes</button></div></div>'''},
            {"id": "s2", "name": "Despacho Legal", "img": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between border-4 border-white/10 m-2"><div class="text-center"><span class="text-white font-serif text-sm tracking-widest uppercase border-b border-amber-600/50 pb-1">Mendoza & Asoc.</span></div><div class="mt-auto text-center"><h3 class="text-white font-serif text-xl mb-4">Defensa y Estrategia.</h3><button class="border border-amber-600 text-amber-500 px-4 py-2 text-[10px] uppercase">Asesoría</button></div></div>'''},
            {"id": "s3", "name": "Agencia Creativa", "img": "https://images.unsplash.com/photo-1493238792000-8113da705763?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-6 h-full flex flex-col justify-between"><div class="w-6 h-6 rounded bg-white text-black flex items-center justify-center font-black text-xs">A.</div><div><h3 class="text-white font-black text-3xl tracking-tighter leading-none mb-3">Creamos<br>el futuro.</h3><button class="bg-white text-black py-2 rounded-xl text-xs font-black px-4">Ver Portafolio</button></div></div>'''},
            {"id": "s4", "name": "Firma Arquitectura", "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-white font-light text-xs tracking-[0.3em] uppercase">Vectra</span><div class="mt-auto"><h3 class="text-white font-light text-2xl mb-4">Espacios que<br>inspiran.</h3><button class="border border-white text-white px-4 py-2 text-[9px] uppercase tracking-widest">Proyectos</button></div></div>'''},
            {"id": "s5", "name": "Agencia Seguros", "img": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-emerald-500 font-bold text-lg">SafeGuard</span><div class="bg-white/95 p-4 rounded-lg mt-auto border-t-4 border-emerald-500"><h3 class="text-zinc-900 font-bold text-lg mb-2">Protege lo que más importa.</h3><button class="bg-emerald-500 text-white px-4 py-2 rounded text-[10px] font-bold w-full">Cotizar Seguro</button></div></div>'''},
            {"id": "s6", "name": "Consultoría IT", "img": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-cyan-400 font-mono text-sm border border-cyan-400 p-1 w-fit">/TECH.SYS</span><div class="mt-auto"><h3 class="text-white font-mono text-xl mb-3">Soporte y Redes.</h3><button class="bg-cyan-500 text-black font-mono px-4 py-2 text-[10px] w-full">Contactar</button></div></div>'''},
            {"id": "s7", "name": "Despacho Contable", "img": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-blue-900 font-bold text-lg bg-white/80 p-1">FinanzasPro</span><div class="bg-blue-900 p-4 mt-auto"><h3 class="text-white font-bold text-xl mb-2">Claridad en tus números.</h3><button class="bg-white text-blue-900 px-4 py-2 text-[10px] font-bold w-full">Asesoría</button></div></div>'''},
            {"id": "s8", "name": "Boutique Creativa", "img": "https://images.unsplash.com/photo-1522542550221-31fd19575a2d?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-pink-500 font-serif italic text-2xl">Maison</span><div class="mt-auto text-center"><button class="bg-white text-black rounded-full px-6 py-2 text-[10px] font-bold uppercase tracking-widest">Descubrir</button></div></div>'''}
        ]
    },
    "paquete-empresarial.html": {
        "id": "emp",
        "slides": [
            {"id": "s1", "name": "Inmobiliaria Luxury", "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><div class="bg-white/90 p-2 rounded"><span class="text-zinc-900 font-serif font-bold text-xs uppercase tracking-widest">LUXE REALTY</span></div><div class="bg-white/95 p-4 rounded-xl mt-auto"><span class="bg-zinc-900 text-white text-[8px] uppercase px-2 py-1 rounded mb-2 inline-block">Destacada</span><h3 class="text-zinc-900 font-serif text-lg mb-1">Villa Serena</h3><button class="w-full bg-zinc-900 text-white py-2 rounded text-[10px] uppercase tracking-widest font-bold">Ver Detalles</button></div></div>'''},
            {"id": "s2", "name": "Constructora", "img": "https://images.unsplash.com/photo-1541888086225-f64112e56cc1?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col"><div class="border-l-4 border-yellow-500 pl-2 mb-6"><span class="text-white font-black text-xl tracking-tighter">BUILD<span class="text-yellow-500">CORP</span></span></div><div class="mt-auto"><h3 class="text-white font-black text-2xl uppercase leading-none mb-3">Ingeniería que perdura.</h3><button class="w-full bg-yellow-500 text-black py-2 text-xs font-black uppercase">Cotizar</button></div></div>'''},
            {"id": "s3", "name": "Tech B2B", "img": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-6 h-full flex flex-col"><span class="text-blue-500 font-bold tracking-tight text-lg mb-10">NexusData</span><div class="mt-auto"><h3 class="text-white font-bold text-2xl leading-tight mb-3">Escala con IA.</h3><button class="bg-blue-600 text-white px-4 py-2 rounded text-[10px] font-bold">Solicitar Demo</button></div></div>'''},
            {"id": "s4", "name": "Logística Global", "img": "https://images.unsplash.com/photo-1586528116311-ad8ed7c1590f?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-orange-500 font-black italic text-2xl">AERO<span class="text-white">FREIGHT</span></span><div class="bg-zinc-900/90 p-4 border-t-4 border-orange-500 mt-auto"><h3 class="text-white font-bold text-lg mb-2">Entregas sin límites.</h3><button class="bg-orange-500 text-black px-4 py-2 text-[10px] font-black w-full uppercase">Rastrear Carga</button></div></div>'''},
            {"id": "s5", "name": "Hospital Privado", "img": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-cyan-600 font-bold text-xl bg-white/90 p-2 rounded shadow">Centro Médico</span><div class="bg-white/95 p-4 rounded-xl mt-auto"><h3 class="text-zinc-800 font-bold text-lg mb-2">Tecnología y cuidado humano.</h3><button class="bg-cyan-600 text-white px-4 py-2 rounded-lg text-[10px] font-bold w-full">Urgencias 24/7</button></div></div>'''},
            {"id": "s6", "name": "Financiera Corporativa", "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-white font-serif text-lg tracking-widest uppercase">Capital Bank</span><div class="mt-auto text-center"><h3 class="text-white font-serif text-2xl mb-4">Invierte en tu futuro.</h3><button class="bg-white text-black px-6 py-2 text-[10px] uppercase font-bold tracking-widest">Abrir Cuenta</button></div></div>'''},
            {"id": "s7", "name": "Firma Auditoría", "img": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-white font-bold text-sm bg-blue-900 p-2">GlobalAudit</span><div class="bg-blue-900/90 p-4 mt-auto"><h3 class="text-white font-bold text-xl mb-2">Transparencia Total.</h3><button class="border border-white text-white px-4 py-2 text-[10px] font-bold w-full">Servicios</button></div></div>'''},
            {"id": "s8", "name": "Desarrolladora Software", "img": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-green-400 font-mono text-sm border border-green-400 p-1 w-fit">{ CODE.SYS }</span><div class="mt-auto"><h3 class="text-white font-mono text-xl mb-3">Sistemas a medida.</h3><button class="bg-green-500 text-black font-mono px-4 py-2 text-[10px] w-full font-bold">Documentación</button></div></div>'''}
        ]
    },
    "paquete-tienda.html": {
        "id": "shop",
        "slides": [
            {"id": "s1", "name": "Ropa de Moda", "img": "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 h-full flex flex-col justify-between"><div class="p-4"><span class="text-white font-serif font-bold text-lg tracking-widest uppercase shadow-sm">VOGUE</span></div><div class="bg-white rounded-t-2xl p-4 mt-auto shadow-2xl"><span class="text-zinc-400 text-[9px] uppercase tracking-widest block mb-1">Nueva Colección</span><h3 class="text-black font-serif text-lg mb-2">Abrigo de Lana</h3><button class="w-full bg-black text-white py-2 rounded-full text-[10px] font-bold uppercase tracking-widest">Añadir al Carrito</button></div></div>'''},
            {"id": "s2", "name": "Tienda Tech", "img": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><div class="bg-zinc-900/80 p-2 rounded-xl"><span class="text-white font-black italic text-sm">TECH<span class="text-blue-500">ZONE</span></span></div><div class="mt-auto"><h3 class="text-white font-bold text-xl leading-tight mb-1">PlayStation 5 Pro</h3><span class="text-white font-black text-lg block mb-2">$11,999</span><button class="w-full bg-blue-600 text-white py-2 rounded-xl text-xs font-bold shadow-[0_0_15px_rgba(37,99,235,0.4)]">Comprar Ahora</button></div></div>'''},
            {"id": "s3", "name": "Skincare Natural", "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><div class="text-center"><span class="text-green-900 font-serif font-bold text-sm tracking-widest bg-white/50 px-2 py-1 rounded">BOTANICA</span></div><div class="bg-white/90 p-4 rounded-xl mt-auto"><h3 class="text-green-950 font-serif text-lg leading-tight mb-2">Serum Ácido Hialurónico</h3><button class="w-full bg-green-800 text-white py-2 rounded-xl text-[10px] uppercase tracking-widest font-bold">Agregar - $450</button></div></div>'''},
            {"id": "s4", "name": "Tienda Muebles", "img": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-amber-800 font-bold text-xl tracking-tight">KøK</span><div class="bg-[#F4F1EA] p-4 mt-auto rounded-lg"><h3 class="text-amber-900 font-bold text-lg mb-1">Silla Nórdica V2</h3><span class="text-amber-700 font-bold block mb-3">$1,200 MXN</span><button class="bg-amber-800 text-white px-4 py-2 w-full text-[10px] uppercase tracking-widest">Comprar</button></div></div>'''},
            {"id": "s5", "name": "Accesorios Deportivos", "img": "https://images.unsplash.com/photo-1518002171953-a080ee817e1f?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-white font-black text-2xl italic tracking-tighter">SPEED<span class="text-red-500">X</span></span><div class="mt-auto"><h3 class="text-white font-black text-2xl uppercase italic mb-1">Tenis Running</h3><span class="text-red-500 font-black text-xl block mb-3">$2,599</span><button class="bg-red-600 text-white px-4 py-2 font-black uppercase italic w-full">Añadir</button></div></div>'''},
            {"id": "s6", "name": "Joyería Fina", "img": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><div class="text-center"><span class="text-white font-serif tracking-[0.4em] text-xs uppercase border-b border-white pb-1">Aura</span></div><div class="text-center mt-auto bg-black/40 backdrop-blur-md p-4"><h3 class="text-white font-serif text-lg mb-2">Anillo Diamante 18k</h3><button class="border border-white text-white px-6 py-2 text-[9px] uppercase tracking-widest hover:bg-white hover:text-black transition-colors">Añadir al Carrito</button></div></div>'''},
            {"id": "s7", "name": "Productos Mascotas", "img": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-orange-500 font-bold text-2xl bg-white px-2 py-1 rounded-2xl w-fit shadow">HappyPet</span><div class="bg-orange-100 p-4 rounded-2xl mt-auto border-2 border-orange-500"><h3 class="text-orange-900 font-bold text-lg mb-1">Alimento Premium</h3><button class="bg-orange-500 text-white px-4 py-2 rounded-xl text-xs font-bold w-full shadow-md shadow-orange-500/30">Comprar - $850</button></div></div>'''},
            {"id": "s8", "name": "Postres / Repostería", "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=70", "html": '''<div class="relative z-10 p-5 h-full flex flex-col justify-between"><span class="text-pink-600 font-serif italic text-2xl bg-white/80 px-3 py-1 rounded-full w-fit">SweetBites</span><div class="bg-white/95 p-4 rounded-2xl mt-auto text-center"><h3 class="text-pink-900 font-serif text-xl mb-1">Pastel Red Velvet</h3><span class="text-pink-600 font-bold block mb-3">$450 MXN</span><button class="bg-pink-500 text-white px-6 py-2 rounded-full text-[10px] font-bold uppercase tracking-widest w-full">Pedir Ahora</button></div></div>'''}
        ]
    }
}

for filename, data in packages_data.items():
    if not os.path.exists(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # We will replace the ENTIRE lg:w-1/2 section.
    # The regex targets from `<div class="lg:w-1/2 w-full relative">` up to its closing tag (before `</div>\s*</div>\s*</div>\s*</section>`)
    # Because of nested divs, it's safer to split the file by a known marker if possible.
    # The previous structure was injected into the Hero section.
    # Let's find the Hero section:
    # `<div class="flex flex-col lg:flex-row gap-12 items-center">`
    #   `<div class="lg:w-1/2"> ... textual content ... </div>`
    #   `<div class="lg:w-1/2 w-full ..."> ... old carousel or messy stuff ... </div>`
    # `</div>`
    
    # We will slice out the second `lg:w-1/2` div completely.
    match = re.search(r'(<div class="lg:w-1/2 w-full relative">.*?</section>)', html, re.DOTALL)
    if not match:
        # Fallback if the previous script left a mess
        match = re.search(r'(<div class="lg:w-1/2 w-full.*?</section>)', html, re.DOTALL)
        if not match:
            print(f"Could not find hero image block in {filename}")
            continue
            
    # Build the new JS logic for this specific page
    slides_json = []
    for slide in data["slides"]:
        # Escape quotes for JS
        html_str = slide['html'].replace('`', '\`').replace('\n', ' ')
        slides_json.append(f"{{ id: '{slide['id']}', name: '{slide['name']}', img: '{slide['img']}', html: `{html_str}` }}")
        
    js_array = "[\n" + ",\n".join(slides_json) + "\n]"
    
    # Generate the initial HTML of the first slide
    first_slide = data["slides"][0]
    
    # Build the Control Bar Buttons
    buttons_html = ""
    for idx, slide in enumerate(data["slides"]):
        active_class = "bg-white text-black" if idx == 0 else "bg-white/10 text-white hover:bg-white/20"
        buttons_html += f'<button onclick="changeTemplate(\'{slide["id"]}\')" id="btn-{slide["id"]}" class="template-btn whitespace-nowrap px-4 py-2 rounded-full text-[10px] font-bold uppercase tracking-widest transition-colors {active_class} border border-white/20">{slide["name"]}</button>'

    new_viewer_html = f'''
                    <div class="lg:w-1/2 w-full relative">
                        <!-- Optimized glowing background (No pulse, lower blur for better performance) -->
                        <div class="absolute -inset-2 bg-gradient-to-br from-red-500/20 via-pink-500/20 to-orange-400/20 blur-xl rounded-full pointer-events-none transform-gpu"></div>
                        
                        <!-- Main Screen Viewer -->
                        <div class="relative p-2 rounded-3xl bg-zinc-900/60 backdrop-blur-md border border-white/10 shadow-2xl z-10 mb-4 transition-transform duration-300">
                            
                            <!-- Browser Chrome -->
                            <div class="flex items-center gap-2 mb-2 px-2 pt-1">
                                <div class="flex gap-1.5">
                                    <div class="w-3 h-3 rounded-full bg-red-400"></div>
                                    <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                                    <div class="w-3 h-3 rounded-full bg-green-400"></div>
                                </div>
                                <div class="flex-1 bg-black/40 border border-white/5 rounded px-3 py-1 text-[10px] text-zinc-400 flex items-center gap-2 font-mono">
                                    <i data-lucide="lock" class="w-3 h-3 text-green-500"></i> www.tu-negocio.com
                                </div>
                            </div>

                            <!-- Screen Content -->
                            <div class="relative rounded-xl overflow-hidden bg-black w-full" style="aspect-ratio: 16/10;">
                                <img id="viewer-img" src="{first_slide['img']}" class="absolute inset-0 w-full h-full object-cover transition-opacity duration-500 opacity-50">
                                <div id="viewer-content" class="absolute inset-0 w-full h-full transition-opacity duration-500">
                                    {first_slide['html']}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Interactive Liquid Glass Control Bar -->
                        <div class="relative p-2 rounded-2xl bg-black/80 backdrop-blur-xl border border-white/10 shadow-xl z-10 flex flex-col gap-2">
                            <div class="px-2 flex items-center gap-2 text-white/50 text-[10px] uppercase tracking-widest font-bold">
                                <i data-lucide="layout" class="w-3 h-3"></i> 8 Estilos y Vistas de Clientes:
                            </div>
                            <div class="flex overflow-x-auto gap-2 pb-1 scrollbar-hide snap-x" id="template-bar">
                                {buttons_html}
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </section>

        <!-- Template Viewer Script -->
        <script>
            const templates = {js_array};
            
            function changeTemplate(id) {{
                const tpl = templates.find(t => t.id === id);
                if(!tpl) return;
                
                // Update Image and Content with fade
                const imgEl = document.getElementById('viewer-img');
                const contentEl = document.getElementById('viewer-content');
                
                imgEl.style.opacity = 0;
                contentEl.style.opacity = 0;
                
                setTimeout(() => {{
                    imgEl.src = tpl.img;
                    contentEl.innerHTML = tpl.html;
                    
                    // Re-init lucide icons for newly injected HTML
                    if(window.lucide) window.lucide.createIcons();
                    
                    imgEl.style.opacity = 0.5;
                    contentEl.style.opacity = 1;
                }}, 250);
                
                // Update buttons
                document.querySelectorAll('.template-btn').forEach(btn => {{
                    btn.classList.remove('bg-white', 'text-black');
                    btn.classList.add('bg-white/10', 'text-white');
                }});
                const activeBtn = document.getElementById('btn-' + id);
                if(activeBtn) {{
                    activeBtn.classList.remove('bg-white/10', 'text-white');
                    activeBtn.classList.add('bg-white', 'text-black');
                    activeBtn.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
                }}
            }}
        </script>
'''

    # Split the HTML at `<div class="lg:w-1/2 w-full`
    # Ensure we safely replace it.
    parts = re.split(r'<div class="lg:w-1/2 w-full[^>]*>', html, maxsplit=1)
    if len(parts) == 2:
        # The second part contains everything from the hero image down.
        # We want to keep everything AFTER `</section>`
        post_section = parts[1].split('</section>', 1)
        if len(post_section) == 2:
            final_html = parts[0] + new_viewer_html + post_section[1]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"Updated {filename} successfully.")
        else:
            print(f"Failed to find </section> in {filename}")
    else:
        print(f"Failed to split {filename}")

