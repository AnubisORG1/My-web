# Handoff Report — Survey: Pricing, Maintenance & SLA Mapping (R2)

**Author Agent**: explorer_survey_2  
**Parent Agent**: orchestrator_1 (`fc91f4b5-8d5b-44fe-a4a1-87721cca66da`)  
**Scope**: Landing page investigation in `c:\Users\joshu\OneDrive\Desktop\My web\index.html` regarding pricing cards, maintenance limits ($250-$800/mes, 5 vs 10 changes), and SLA notice (24-48 hrs hábiles) according to `ORIGINAL_REQUEST.md` (R2, R4).

---

## 1. Observation

Direct inspection of `c:\Users\joshu\OneDrive\Desktop\My web\index.html` revealed the exact structural locations, line numbers, HTML elements, and CSS classes:

### 1.1 Pricing Section Container (`#paquetes`)
- **Location**: Lines 502–719.
- **Section Tag & Classes**:
  ```html
  <section id="paquetes" class="py-24 bg-zinc-50 border-y border-zinc-100 overflow-hidden relative">
      <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-16">
              <h2 id="paquetes-title" class="text-3xl md:text-4xl font-bold text-black mb-4">Soluciones claras, sin letras chiquitas</h2>
              <p id="paquetes-desc" class="text-zinc-600 max-w-2xl mx-auto">Selecciona el paquete que mejor se adapte a tu etapa actual.</p>
          </div>
          <div class="flex overflow-x-auto hide-scrollbar gap-6 pb-8 snap-x snap-mandatory lg:grid lg:grid-cols-5 lg:overflow-visible lg:snap-none">
  ```
- **Grid Layout**: Mobile displays a horizontally scrollable container with snap points (`snap-x snap-mandatory`), while desktop displays a 5-column grid (`lg:grid lg:grid-cols-5`). All cards use `flex flex-col` and have their action button pinned to the bottom via `mt-auto`.

---

### 1.2 Pricing Cards: Básica vs Profesional

#### Card 1: Web Básica (Lines 513–551)
- **Card Container**: Line 514
  `<div class="package-card min-w-[280px] lg:min-w-0 bg-white rounded-3xl p-6 border border-zinc-200 flex flex-col snap-center relative overflow-hidden">`
- **Price**: Lines 522–525: `$1,500 MXN`.
- **Existing Features List (`<ul>`, Lines 527–537)**:
  ```html
  <ul class="space-y-3 mb-8 text-sm flex-1">
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>1 Página (Landing page)
      </li>
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Alojamiento rápido
      </li>
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Links a redes (TikTok, IG, WA)
      </li>
  </ul>
  ```
  *Current status*: Does not mention the development scope constraint: `"Modificaciones básicas (solo fotos, textos y colores)"`.
- **Existing Subscription Box (Lines 538–547)**:
  ```html
  <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
      <div>
          <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
          <p class="text-xs text-zinc-800">$250/mes (Modificaciones básicas).</p>
      </div>
      <div class="border-t border-zinc-200 pt-2">
          <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Google Maps</p>
          <p class="text-xs text-zinc-800">+$350 (Opcional, Perfil Básico).</p>
      </div>
  </div>
  ```
  *Current status*: Lacks the exact monthly limit: `"Plan Básico incluye 5 cambios mensuales"`.

#### Card 2: Profesional (Lines 553–591)
- **Card Container**: Line 554
  `<div class="package-card min-w-[280px] lg:min-w-0 bg-white rounded-3xl p-6 border border-zinc-200 flex flex-col snap-center relative overflow-hidden">`
- **Price**: Lines 562–565: `$3,500 MXN`.
- **Existing Features List (`<ul>`, Lines 567–577)**:
  ```html
  <ul class="space-y-3 mb-8 text-sm flex-1">
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Hasta 3 páginas
      </li>
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Dominio propio .com
      </li>
      <li class="flex items-start gap-2 text-zinc-700">
          <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Formulario de contacto
      </li>
  </ul>
  ```
  *Current status*: Does not mention the development scope capability: `"Modificaciones completas (nuevas secciones y páginas)"`.
- **Existing Subscription Box (Lines 578–587)**:
  ```html
  <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
      <div>
          <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
          <p class="text-xs text-zinc-800">$500/mes (Modificaciones completas).</p>
      </div>
      <div class="border-t border-zinc-200 pt-2">
          <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Google Maps</p>
          <p class="text-xs text-zinc-800">Básico o Avanzado (Requerido).</p>
      </div>
  </div>
  ```
  *Current status*: Lacks the exact monthly limit: `"Plan Profesional incluye 10 cambios mensuales"`.

---

### 1.3 Maintenance Description in FAQ (`#dudas`, Lines 732–740)
- **Accordion `<details>` block**:
  ```html
  <details class="bg-zinc-50 border border-zinc-200 rounded-2xl group overflow-hidden" open>
      <summary class="flex justify-between items-center font-bold cursor-pointer list-none p-6 text-black text-lg">
          <span>¿Qué incluye la Suscripción y por qué es importante?</span>
          <span class="transition group-open:rotate-180 text-zinc-400">▼</span>
      </summary>
      <div class="p-6 pt-0 text-zinc-600 leading-relaxed border-t border-zinc-200/50 mt-2 pt-4">
          Como soy el único que mantiene tu página, la suscripción mensual ($250 a $800 según el paquete) garantiza que <strong>yo me encargaré personalmente de hacer todas las actualizaciones que necesites</strong> (cambios de texto, subir fotos nuevas, actualizar horarios o precios). Además, cubre el alojamiento rápido, la seguridad de la página para que nunca se caiga y el soporte directo conmigo por WhatsApp. Sin la suscripción, corres el riesgo de que la página quede desactualizada o vulnerable a fallos técnicos.
      </div>
  </details>
  ```
- *Operational Risk Observed*: Line 738 promises *"yo me encargaré personalmente de hacer todas las actualizaciones que necesites"*, creating open-ended liability. It lacks both the 5 vs 10 change limits and the SLA response time window.

---

### 1.4 Current Presence of SLA Notice
- Search for terms: `SLA`, `Acuerdo de Nivel de Servicio`, `Tiempo de respuesta`, `24 a 48`, `días hábiles`.
- **Result**: Exactly **0 occurrences** found across all files. SLA is currently completely omitted from the site.

---

### 1.5 Interactive Form (`#cotizacion`) & JS Sync Points
- **HTML Form field (`f_maint`, Lines 827–833)**:
  ```html
  <div>
      <label for="f_maint" class="block text-sm font-semibold text-zinc-800 mb-2">Suscripción por modificaciones futuras</label>
      <select id="f_maint" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors">
          <option value="Sí ($500/mes)">Sí, me interesa</option>
          <option value="No por ahora">No, yo la administraré</option>
      </select>
      <p class="text-[11px] text-zinc-500 mt-2">* Remodelación completa de página: Costo extra de $250.</p>
  </div>
  ```
- **Inline JavaScript (`updateFormOptions()`, Lines 921–928)**:
  ```javascript
  // Actualizar Mantenimiento
  if (isBasic) {
      f_maint.options[0].text = "Sí, $250/mes (Modificaciones básicas)";
      f_maint.options[0].value = "Sí ($250/mes)";
  } else {
      f_maint.options[0].text = "Sí, $500/mes (Modificaciones completas)";
      f_maint.options[0].value = "Sí ($500/mes)";
  }
  ```

---

## 2. Logic Chain

1. **Pricing Card Differentiation (Initial Development Scope)**:
   - *Observation*: Cards 1 and 2 list feature bullets (`1 Página`, `Hasta 3 páginas`, etc.) but do not clearly explain the scope of future modifications or development boundaries.
   - *Requirement R2*: Básica: *"Modificaciones básicas (solo fotos, textos y colores)"*; Profesional: *"Modificaciones completas (nuevas secciones y páginas)"*.
   - *Inference*: Adding these exact phrases as a 4th `<li>` in each card's `<ul>` establishes immediate visual parity between the two core packages without disrupting grid alignment.

2. **Maintenance Subscription Limits (5 vs 10 monthly changes)**:
   - *Observation*: The subscription boxes in Cards 1 and 2 (lines 541 and 581) list `$250/mes (Modificaciones básicas)` and `$500/mes (Modificaciones completas)` without setting hard volume caps.
   - *Requirement R2 & Acceptance Criteria*: Specify: *"Plan Básico incluye 5 cambios mensuales. Plan Profesional incluye 10 cambios mensuales"*.
   - *Inference*: Updating the text inside the subscription sub-boxes in Card 1 and Card 2 directly ties the monthly fee to the change quota right where users evaluate price.

3. **Eliminating Operational Vulnerability in FAQ**:
   - *Observation*: Line 738 promises unlimited updates (*"todas las actualizaciones que necesites"*).
   - *Inference*: Replacing this clause with the explicit limits (*"Plan Básico incluye 5 cambios mensuales. Plan Profesional incluye 10 cambios mensuales"*) and introducing the SLA (*"Tiempo de respuesta de 24 a 48 horas en días hábiles"*) directly eliminates the audit-flagged operational risk while reinforcing customer confidence.

4. **SLA Visibility in the Pricing Section**:
   - *Observation*: The pricing section ends abruptly at line 717 after the 5 cards. No SLA notice exists anywhere in `#paquetes`.
   - *Requirement R2 & Acceptance Criteria*: SLA (*"Tiempo de respuesta de 24 a 48 horas en días hábiles"*) must be clearly visible in its respective section.
   - *Inference*: Inserting an SLA & Maintenance Policy banner between lines 717 and 718 (below the card grid, still inside the container) creates a clean, dedicated anchor that highlights both the 24–48 hr SLA and the 5 vs 10 monthly limits using existing Tailwind card styling (`bg-white rounded-3xl border border-zinc-200 p-6 md:p-8`).

5. **Synchronization with Form and JavaScript**:
   - *Observation*: In lines 921–928, JavaScript rewrites `f_maint.options[0].text` on package change. If JS is left untouched, selecting Web Básica in the form will display the old copy without change limits.
   - *Inference*: Updating `updateFormOptions()` and the helper paragraph below `f_maint` maintains total consistency between static marketing copy and interactive quotation.

---

## 3. Caveats

1. **Pre-existing JS Syntax Bug in `index.html` Line 1039**:
   - Line 1039 contains: `message += ?? *Inversión Inicial Estimada:* {initialTotal.toLocaleString()} MXN\\n\\n;`.
   - While unrelated to R2, this syntax error breaks form submission when clicked. The implementer should be aware of this when touching or testing the script block.
2. **Missing `calculateTotal()` Function**:
   - `calculateTotal()` is invoked at lines 947, 958, and 961, but has no implementation in `index.html` (it was likely removed during an aggressive promo cleanup commit). The implementer should ensure no unhandled exceptions halt execution.
3. **Card Height Symmetry**:
   - When adding the 4th `<li>` to Web Básica and Profesional, both cards gain an identical number of lines, maintaining visual height symmetry in the desktop 5-card row. Empresarial, Tienda Web, and A Medida also have 3 or more `<li>` items.
4. **Mobile Layout**:
   - In mobile viewports (`< lg`), the card row uses horizontal scroll snapping (`overflow-x-auto hide-scrollbar snap-x`). Adding the SLA banner below the scrollable container ensures mobile users see the SLA notice regardless of how far they scroll horizontally.

---

## 4. Conclusion & Actionable Recommendations

All proposed modifications are surgical drop-in replacements conforming strictly to **R4 (Edición Quirúrgica)** without regular expressions.

### Proposed Edit 1: Card 1 (Web Básica) — Feature List & Subscription Box
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Target Lines**: ~527–543  
**Existing Content**:
```html
                        <ul class="space-y-3 mb-8 text-sm flex-1">
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>1 Página (Landing page)
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Alojamiento rápido
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Links a redes (TikTok, IG, WA)
                            </li>
                        </ul>
                        <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
                            <div>
                                <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
                                <p class="text-xs text-zinc-800">$250/mes (Modificaciones básicas).</p>
                            </div>
```
**Replacement Content**:
```html
                        <ul class="space-y-3 mb-8 text-sm flex-1">
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>1 Página (Landing page)
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Alojamiento rápido
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Links a redes (TikTok, IG, WA)
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Modificaciones básicas (solo fotos, textos y colores)
                            </li>
                        </ul>
                        <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
                            <div>
                                <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
                                <p class="text-xs text-zinc-800 font-semibold">$250/mes</p>
                                <p class="text-[11px] text-zinc-600 mt-0.5">Plan Básico incluye 5 cambios mensuales.</p>
                            </div>
```

---

### Proposed Edit 2: Card 2 (Profesional) — Feature List & Subscription Box
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Target Lines**: ~567–583  
**Existing Content**:
```html
                        <ul class="space-y-3 mb-8 text-sm flex-1">
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Hasta 3 páginas
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Dominio propio .com
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Formulario de contacto
                            </li>
                        </ul>
                        <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
                            <div>
                                <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
                                <p class="text-xs text-zinc-800">$500/mes (Modificaciones completas).</p>
                            </div>
```
**Replacement Content**:
```html
                        <ul class="space-y-3 mb-8 text-sm flex-1">
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Hasta 3 páginas
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Dominio propio .com
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Formulario de contacto
                            </li>
                            <li class="flex items-start gap-2 text-zinc-700">
                                <i data-lucide="check" class="w-4 h-4 text-black shrink-0 mt-0.5"></i>Modificaciones completas (nuevas secciones y páginas)
                            </li>
                        </ul>
                        <div class="bg-zinc-50 p-3 rounded-lg border border-zinc-100 mb-6 space-y-2">
                            <div>
                                <p class="text-[11px] text-zinc-500 font-medium uppercase tracking-wider">Suscripción</p>
                                <p class="text-xs text-zinc-800 font-semibold">$500/mes</p>
                                <p class="text-[11px] text-zinc-600 mt-0.5">Plan Profesional incluye 10 cambios mensuales.</p>
                            </div>
```

---

### Proposed Edit 3: Dedicated SLA & Maintenance Banner in Section `#paquetes`
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Target Lines**: ~716–719  
**Existing Content**:
```html
                    </div>

                </div>
            </div>
        </section>
```
**Replacement Content**:
```html
                    </div>

                </div>

                <!-- SLA y Límites de Mantenimiento Banner -->
                <div class="mt-12 bg-white border border-zinc-200 rounded-3xl p-6 md:p-8 shadow-sm">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                        <div class="flex items-start gap-4">
                            <div class="w-12 h-12 rounded-2xl bg-zinc-100 flex items-center justify-center shrink-0 text-black">
                                <i data-lucide="clock" class="w-6 h-6"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-base text-black">Acuerdo de Nivel de Servicio (SLA)</h4>
                                <p class="text-sm text-zinc-600 mt-1">Tiempo de respuesta de 24 a 48 horas en días hábiles.</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4 border-t md:border-t-0 md:border-l border-zinc-200 pt-6 md:pt-0 md:pl-8">
                            <div class="w-12 h-12 rounded-2xl bg-zinc-100 flex items-center justify-center shrink-0 text-black">
                                <i data-lucide="shield-check" class="w-6 h-6"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-base text-black">Límites de Mantenimiento Mensual ($250 - $800/mes)</h4>
                                <p class="text-sm text-zinc-600 mt-1">Plan Básico incluye 5 cambios mensuales. Plan Profesional incluye 10 cambios mensuales.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </section>
```

---

### Proposed Edit 4: FAQ Subsection Clarification (`#dudas`)
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Target Line**: ~738  
**Existing Content**:
```html
                            Como soy el único que mantiene tu página, la suscripción mensual ($250 a $800 según el paquete) garantiza que <strong>yo me encargaré personalmente de hacer todas las actualizaciones que necesites</strong> (cambios de texto, subir fotos nuevas, actualizar horarios o precios). Además, cubre el alojamiento rápido, la seguridad de la página para que nunca se caiga y el soporte directo conmigo por WhatsApp. Sin la suscripción, corres el riesgo de que la página quede desactualizada o vulnerable a fallos técnicos.
```
**Replacement Content**:
```html
                            Como soy el único que mantiene tu página, la suscripción mensual ($250 a $800 según el paquete) garantiza que <strong>yo me encargaré personalmente de tus actualizaciones con reglas y tiempos claros</strong>: Plan Básico incluye 5 cambios mensuales y Plan Profesional incluye 10 cambios mensuales (cambios de texto, subir fotos nuevas, actualizar horarios o precios). Además, todas las solicitudes tienen un SLA garantizado con <strong>Tiempo de respuesta de 24 a 48 horas en días hábiles</strong>. Cubre también el alojamiento rápido, la seguridad de la página para que nunca se caiga y el soporte directo conmigo por WhatsApp. Sin la suscripción, corres el riesgo de que la página quede desactualizada o vulnerable a fallos técnicos.
```

---

### Proposed Edit 5: Interactive Form Helper & JS Options
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Target Lines**: ~831–833  
**Existing Content**:
```html
                                </select>
                                <p class="text-[11px] text-zinc-500 mt-2">* Remodelación completa de página: Costo extra de $250.</p>
                            </div>
```
**Replacement Content**:
```html
                                </select>
                                <p class="text-[11px] text-zinc-500 mt-2">* Plan Básico: 5 cambios/mes. Plan Profesional: 10 cambios/mes. SLA: Tiempo de respuesta de 24 a 48 horas en días hábiles.</p>
                            </div>
```

**Target Lines**: ~921–928  
**Existing Content**:
```javascript
            // Actualizar Mantenimiento
            if (isBasic) {
                f_maint.options[0].text = "Sí, $250/mes (Modificaciones básicas)";
                f_maint.options[0].value = "Sí ($250/mes)";
            } else {
                f_maint.options[0].text = "Sí, $500/mes (Modificaciones completas)";
                f_maint.options[0].value = "Sí ($500/mes)";
            }
```
**Replacement Content**:
```javascript
            // Actualizar Mantenimiento
            if (isBasic) {
                f_maint.options[0].text = "Sí, $250/mes (Plan Básico: 5 cambios mensuales)";
                f_maint.options[0].value = "Sí ($250/mes - 5 cambios)";
            } else {
                f_maint.options[0].text = "Sí, $500/mes (Plan Profesional: 10 cambios mensuales)";
                f_maint.options[0].value = "Sí ($500/mes - 10 cambios)";
            }
```

---

## 5. Verification Method

To independently verify the survey and proposed changes:

1. **Exact Substring Verification**:
   Inspect `c:\Users\joshu\OneDrive\Desktop\My web\index.html` using `view_file` or Python file search to confirm lines 514–591, lines 715–740, and lines 920–930 match verbatim the target substrings quoted in this report.
2. **Text Search for Acceptance Criteria**:
   Verify that after application, searching for:
   - `"Modificaciones básicas (solo fotos, textos y colores)"`
   - `"Modificaciones completas (nuevas secciones y páginas)"`
   - `"Plan Básico incluye 5 cambios mensuales"`
   - `"Plan Profesional incluye 10 cambios mensuales"`
   - `"Tiempo de respuesta de 24 a 48 horas en días hábiles"`
   all yield exact matches in `index.html`.
3. **Visual Inspection**:
   Open `index.html` in a web browser:
   - Navigate to `#paquetes`: Verify that Card 1 and Card 2 feature lists are aligned, the subscription boxes clearly show the limits, and the SLA banner displays gracefully below the cards.
   - Resize to mobile breakpoint: Verify that the horizontal card scroll operates smoothly and the SLA banner stacks responsively (`flex-col md:flex-row`).
   - Navigate to `#dudas`: Open the first FAQ item to confirm the subscription explanation includes the SLA and limits.
4. **Invalidation Conditions**:
   - Any broken HTML tag or mismatched closing `</div>` that collapses the 5-column grid into 1 column on desktop.
   - Discrepancy between the static card text and the dynamic dropdown text in `f_maint`.
