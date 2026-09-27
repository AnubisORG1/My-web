# Original User Request

## 2026-09-27T00:02:06Z

# Teamwork Project Prompt — Draft

Solucionar vulnerabilidades operacionales, legales y financieras de la landing page estática (HTML/Tailwind/JS) señaladas por una auditoría externa. Se debe clarificar la oferta, agregar validaciones al formulario y expandir los modales legales existentes.

Working directory: c:\Users\joshu\OneDrive\Desktop\My web
Integrity mode: development

## Requirements

### R1. Claridad Legal y Dominio
- Añadir la frase: "Datos protegidos bajo LFPDPPP" cerca de los botones/formularios de contacto.
- Expandir el modal de Términos y Condiciones existente con la política de cancelación: "Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte".
- En la sección donde se menciona el dominio ".com sujeto a disponibilidad", añadir la aclaración: "Si no está disponible, sugerimos .com.mx o .mx".

### R2. Límites Financieros y SLA (Sección de Precios/Mantenimiento)
- Especificar el Acuerdo de Nivel de Servicio (SLA): "Tiempo de respuesta de 24 a 48 horas en días hábiles".
- Especificar en el mantenimiento mensual ($250-$800/mes) los límites: "Plan Básico incluye 5 cambios mensuales. Plan Profesional incluye 10 cambios mensuales".
- Diferenciar el desarrollo inicial en la tabla de precios:
  - Básica: "Modificaciones básicas (solo fotos, textos y colores)".
  - Profesional: "Modificaciones completas (nuevas secciones y páginas)".

### R3. Validación de Formulario (JavaScript)
- Implementar validación obligatoria en los campos del formulario de contacto (Nombre y paquete).
- Mostrar alertas visuales o mensajes de error claros si el usuario intenta enviar sin llenar los campos obligatorios, previniendo que se abra el enlace de WhatsApp con datos vacíos.

### R4. Edición Quirúrgica (CRITICAL)
- Todas las modificaciones al HTML deben hacerse mediante reemplazos exactos (`str.replace`) o parseo seguro (BeautifulSoup).
- Está ESTRICTAMENTE PROHIBIDO usar expresiones regulares amplias (`re.sub` con `re.DOTALL`) para reemplazar grandes bloques de HTML, ya que esto puede destruir la estructura de la página.

## Acceptance Criteria

### Operacional y Financiero
- [ ] La tabla de precios muestra claramente los límites de cambios (textos/fotos vs secciones) y las cantidades de la suscripción (5 vs 10 cambios mensuales).
- [ ] El SLA (24-48 hrs hábiles) y la alternativa de dominios (.com.mx / .mx) están visibles en sus respectivas secciones.

### Funcional y Legal
- [ ] Intentar enviar el formulario en blanco bloquea la redirección a WhatsApp y resalta los campos faltantes (por ejemplo, con bordes rojos).
- [ ] Las leyendas de protección de datos (LFPDPPP) y retención de propiedad tras cancelar están implementadas en la UI o modales.
- [ ] La página mantiene su diseño intacto, sin pérdida de secciones (comprobado abriendo index.html).
