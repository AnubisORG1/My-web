# Handoff Report — Survey: JavaScript & Form Validation Mapping (R3, R4)

**Author Agent**: `explorer_survey_3`  
**Parent Agent**: `orchestrator_1` (`fc91f4b5-8d5b-44fe-a4a1-87721cca66da`)  
**Scope**: Complete investigation of landing page contact form (`#wa-form`, `#cotizacion`), JavaScript submission handling, WhatsApp redirection, mandatory field validation (Name & Package), visual error indicators (red borders/alerts), and R4 surgical editing rules.  
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Related Files**: `js/app.js`, `css/styles.css`  
**Date**: 2026-09-27  

---

## 1. Observation

Direct inspection of `index.html`, `js/app.js`, and `css/styles.css` using file inspection tools, node syntax parsers, and git commit history revealed the following concrete architectural facts, line numbers, and defects:

### 1.1 Form DOM Elements & Attributes (`index.html`)

- **Contact Form Section Container**: Lines 765–874
  - Section wrapper: `<section id="cotizacion" class="py-24 bg-white border-t border-zinc-100">` (Line 765)
  - Card container: `<div class="bg-white rounded-3xl p-8 border border-zinc-200 shadow-xl shadow-zinc-100/50 relative overflow-hidden">` (Line 772)
  - Form element: `<form id="wa-form" class="space-y-6 relative z-10">` (Line 775)
  - The form currently lacks custom error containers and uses standard browser submit behavior (`type="submit"`).

- **Name Input Field (`#f_name`)**: Lines 778–781
  ```html
  778: <div>
  779:     <label for="f_name" class="block text-sm font-semibold text-zinc-800 mb-2">Tu Nombre</label>
  780:     <input type="text" id="f_name" required class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors" placeholder="¿Cómo te llamas?">
  781: </div>
  ```
  - **Defect**: Has HTML5 `required`, but zero inline error messaging element (`<p id="f_name_error">`), no `aria-describedby`, and no JavaScript validation checking for whitespace-only strings (`.trim() === ''`).

- **Package Select Field (`#f_package`)**: Lines 792–804
  ```html
  792: <div>
  793:     <label for="f_package" class="block text-sm font-semibold text-zinc-800 mb-2">Paquete que te interesa</label>
  794:     <select id="f_package" required class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors font-medium">
  795:         
  796:         <option value="Web Básica ($1,500)">Web Básica ($1,500 MXN)</option>
  797:         <option value="Profesional ($3,500)">Profesional ($3,500 MXN)</option>
  798:         <option value="Empresarial ($6,000)" selected>Empresarial ($6,000 MXN) - Recomendado</option>
  799:         <option value="Tienda Web ($9,000)">Tienda Web ($9,000 MXN)</option>
  800:         <option value="Sistema A Medida">Sistema a Medida (Cotizar)</option>
  801:         <option value="No estoy seguro">Aún no estoy seguro</option>
  802: 
  803:     </select>
  804: </div>
  ```
  - **Defect**: Option 3 (`Empresarial ($6,000)`) is hardcoded with `selected`. There is **no empty/placeholder option** (e.g. `<option value="" disabled selected>-- Selecciona un paquete --</option>`). If a user opens the page and attempts to submit a blank form, `f_package.value` is already pre-filled with `"Empresarial ($6,000)"`. This prevents true blank-form validation from failing on package selection.

- **Submit Button**: Lines 867–870
  ```html
  867: <button type="submit" id="form-submit-btn" class="w-full py-4 mt-6 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2 shadow-lg shadow-red-600/20">
  868:     <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">...</svg>
  869:     Enviar cotización a WhatsApp
  870: </button>
  ```
  - Trigger: Form `submit` event triggered on click or Enter key.

- **Other Form Fields**:
  - `#f_clients` (Lines 784–789): `<select id="f_clients" required>`
  - `#f_google` (Lines 808–814): `<select id="f_google">` (dynamic options generated via JS)
  - `#f_details` (Lines 821–823): `<textarea id="f_details" rows="3" required ...>`
  - `#f_maint` (Lines 827–832): `<select id="f_maint">`
  - `#f_budget` (Lines 835–837): `<input type="text" id="f_budget">`
  - `#summary-block` (Lines 841–865): Hidden summary card (`hidden`) updated by JS.

---

### 1.2 JavaScript Architecture, Script Blocks & Existing Validation

- **File Distribution**:
  - `js/app.js` (41 lines): Loaded at Line 1055. Contains only:
    - `lucide.createIcons()`
    - `#current-year` textContent
    - `#mobile-menu-btn` toggle
    - `#navbar` scroll shadow effect
    - **No form or WhatsApp logic exists in `js/app.js`**.
  - `index.html` inline `<script>` (Lines 898–1054): Contains all form interaction, package card synchronization (`selectPackage`), and form submission handling.

- **Form Event Listeners & Functions in `index.html`**:
  - Line 950: `f_google.addEventListener('change', ...)`
  - Line 961: `f_maint.addEventListener('change', calculateTotal);`
  - Line 962: `f_package.addEventListener('change', updateFormOptions);`
  - Lines 965–987: `function selectPackage(pkgName) { ... }` — called by package buttons across the page (Lines 200, 272, 339, 381, 483, 548, 588, 631, 671, 712).
  - Lines 989–1049: `document.getElementById('wa-form').addEventListener('submit', function(e) { ... });`

- **Verbatim WhatsApp Redirection Code (Lines 989–1049)**:
  ```javascript
  document.getElementById('wa-form').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const active = isPromoActive();
      const name = document.getElementById('f_name').value;
      const history = document.getElementById('f_clients').value;
      const pkg = document.getElementById('f_package').value;
      const details = document.getElementById('f_details').value;
      const maint = document.getElementById('f_maint').value;
      const google = document.getElementById('f_google').value;
      const budget = document.getElementById('f_budget').value || "No especificado";

      let initialTotal = 0;
      let originalTotal = 0;
      let isCustom = false;
      ...
      const phone = "525645890610";
      
      let message = "";
      ...
      message += `👤 *Mi nombre:* ${name}\n`;
      message += `🤝 *Historial:* ${history}\n`;
      message += `📦 *Paquete interesado:* ${pkg}\n`;
      ...
      message += ?? *Inversión Inicial Estimada:* {initialTotal.toLocaleString()} MXN\\n\\n;
      ...
      const encodedMessage = encodeURIComponent(message);
      window.open(`https://wa.me/${phone}?text=${encodedMessage}`, '_blank');
  });
  ```

---

### 1.3 Critical Existing Defects Uncovered

1. **Fatal Syntax Error on Line 1039**:
   - Verbatim line 1039:
     ```javascript
     message += ?? *Inversión Inicial Estimada:* {initialTotal.toLocaleString()} MXN\\n\\n;
     ```
   - Node JS parser verification command:
     ```bash
     node -e "const fs = require('fs'); const s = fs.readFileSync('index.html', 'utf8').match(/<script[\s\S]*?<\/script>/gi)[3]; new Function(s.replace(/<\/?script[^>]*>/gi, ''));"
     ```
   - Result:
     ```
     SYNTAX ERROR -> Unexpected token '??'
     ```
   - **Consequence**: Because this syntax error is in the main inline `<script>` tag, modern browsers fail to parse the script block completely. **None of the event listeners inside this script block are attached** (`submit`, `change`, `selectPackage`). Submitting the form triggers default HTML form GET submission rather than WhatsApp redirect!

2. **Missing `calculateTotal()` Function**:
   - Lines 947, 958, and 961 invoke `calculateTotal()`.
   - Inspection of git history (commit `cf5e050`: *"fix: limpieza real de JS que rompia el footer"*) shows `calculateTotal()` was accidentally deleted when an overzealous script cleanup was performed.
   - When the syntax error at line 1039 is fixed, selecting a package in `f_package` calls `updateFormOptions()`, which executes line 947: `calculateTotal()`. This will immediately throw:
     ```
     Uncaught ReferenceError: calculateTotal is not defined
     ```

3. **Complete Absence of JavaScript Form Validation**:
   - Lines 989–1049 contain zero validation code.
   - No checks for `name.trim() === ''`.
   - No checks for empty package selection.
   - No visual error classes added to inputs.
   - No error text or warning banner rendered.
   - Once the syntax error is fixed, clicking submit with empty inputs immediately opens WhatsApp with empty fields:
     `Mi nombre: `
     `Detalles y personalización: `

4. **Styles in `css/styles.css` vs DOM Structure**:
   - Lines 16–27 in `css/styles.css` attempt to style `.form-group input:invalid` and `.form-group ... ~ .error-msg`.
   - However, grep inspection across `index.html` confirmed `form-group` is never used anywhere in `index.html`.

---

## 2. Logic Chain

1. **From Acceptance Criteria to HTML Adjustments**:
   - *Requirement R3 / Acceptance Criteria*: "Intentar enviar el formulario en blanco bloquea la redirección a WhatsApp y resalta los campos faltantes (por ejemplo, con bordes rojos)."
   - *Observation*: `f_package` currently selects `"Empresarial ($6,000)"` by default on Line 798, and lacks an empty placeholder.
   - *Logic Step*: To permit testing a "formulario en blanco" where both Name and Package are missing, `f_package` must have a default disabled option:
     `<option value="" disabled selected>-- Selecciona un paquete --</option>`
     When a user clicks any package card elsewhere on the page, `selectPackage(pkgName)` automatically sets `f_package.selectedIndex = i`, pre-selecting the package. If the user enters the form directly, `f_package.value` remains `""`, correctly identifying it as unselected.

2. **From R3 Validation to Redirection Prevention**:
   - *Observation*: The `submit` event listener currently extracts values and unconditionally executes `window.open(...)` at Line 1048.
   - *Logic Step*: Client-side JavaScript validation must execute at the very start of the `submit` event listener (after `e.preventDefault()`). If either `name.trim() === ''` or `!pkg || pkg === ''`:
     - Visual error styles (e.g. `border-red-500 ring-2 ring-red-500/20 bg-red-50/20`) must be applied to the invalid field(s).
     - Dedicated helper error text (`#f_name_error`, `#f_package_error`) and an accessible alert banner (`#form-error-alert`) must be unhidden.
     - The first invalid element must receive keyboard focus (`firstInvalid.focus()`).
     - **Execution must terminate immediately (`return;`) before reaching `window.open`**.
     - This guarantees that no WhatsApp URL is opened when mandatory fields are omitted.

3. **From Modern Web Guidance to Real-Time Error Recovery**:
   - *Observation*: Modern Web Guidance (`required-field-feedback`) stresses that error states should clear immediately when the user provides input, without forcing them to re-submit to discover they fixed it.
   - *Logic Step*: Attach `input` event listener to `#f_name` and `change` event listener to `#f_package` to dynamically remove error classes and hide error messages as soon as the user enters valid text or picks a package.

4. **From Line 1039 Syntax Error to JS Restoration**:
   - *Observation*: Line 1039 currently contains `message += ?? *Inversión Inicial Estimada:* {initialTotal.toLocaleString()} MXN\\n\\n;`.
   - *Logic Step*: This must be surgically replaced with valid JavaScript template literal:
     ```javascript
     message += `💸 *Inversión Inicial Estimada:* $${initialTotal.toLocaleString()} MXN\n\n`;
     ```
   - Furthermore, `calculateTotal()` must be restored (or safely guarded) so that `updateFormOptions()` (called on Line 962 and within `selectPackage`) executes smoothly without throwing `ReferenceError`.

5. **From R4 to Surgical Implementation Strategy**:
   - *Observation*: R4 explicitly forbids broad regex replacements (`re.sub` with `re.DOTALL`). The repository history (`fixwhatsapp.py` and commit `cf5e050`) proves that broad regexes destroyed `calculateTotal()` and caused the line 1039 corruption.
   - *Logic Step*: All modifications must be executed using exact, unique string chunks via `replace_file_content` (or Python `str.replace` with count=1). Target strings must include sufficient surrounding context to guarantee uniqueness.

---

## 3. Caveats

1. **Browser Native Tooltips vs Custom JS Validation**:
   - Both `#f_name` and `#f_details` currently have the HTML5 `required` attribute.
   - If HTML5 validation is not bypassed via `novalidate` on `<form id="wa-form">`, browsers will show their native tooltip on the first invalid field and prevent the `submit` event from firing in some browsers, which may prevent custom red borders and custom alert banners from rendering.
   - *Recommendation*: Add `novalidate` to `<form id="wa-form">` so that JavaScript has full control over displaying the custom red borders and accessible error messages required by R3, while still retaining `required` in HTML for semantic and fallback support.
2. **Details Textarea (`#f_details`)**:
   - Notice `#f_details` has `required` in HTML Line 822. However, R3 specifically scopes mandatory validation to *"los campos del formulario de contacto (Nombre y paquete)"*. To avoid blocking users who only fill Name and Package, the JS validation should specifically enforce Name and Package. If `#f_details` is intended to be optional, removing `required` from Line 822 is recommended.
3. **Legal Modals (`openModal` / `closeModal`)**:
   - Discovered that `openModal` and `closeModal` were deleted in commit `cf5e050`. While `explorer_survey_1` handles legal modals, any restoration in `index.html` or `js/app.js` must ensure no conflicts occur.

---

## 4. Conclusion & Recommended Action Plan

### 4.1 Form HTML Changes (`index.html`)

#### 1. Form Element (Line 775)
- **Target**: `<form id="wa-form" class="space-y-6 relative z-10">`
- **Replacement**: `<form id="wa-form" class="space-y-6 relative z-10" novalidate>`

#### 2. Name Field with Error Helper (Lines 778–781)
- **Target**:
  ```html
  <div>
      <label for="f_name" class="block text-sm font-semibold text-zinc-800 mb-2">Tu Nombre</label>
      <input type="text" id="f_name" required class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors" placeholder="¿Cómo te llamas?">
  </div>
  ```
- **Replacement**:
  ```html
  <div>
      <label for="f_name" class="block text-sm font-semibold text-zinc-800 mb-2">Tu Nombre <span class="text-red-500">*</span></label>
      <input type="text" id="f_name" required aria-describedby="f_name_error" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors" placeholder="¿Cómo te llamas?">
      <p id="f_name_error" class="hidden text-xs text-red-600 font-medium mt-1.5 flex items-center gap-1"><span aria-hidden="true">⚠️</span> Por favor ingresa tu nombre.</p>
  </div>
  ```

#### 3. Package Field with Placeholder & Error Helper (Lines 792–804)
- **Target**:
  ```html
  <div>
      <label for="f_package" class="block text-sm font-semibold text-zinc-800 mb-2">Paquete que te interesa</label>
      <select id="f_package" required class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors font-medium">
          
          <option value="Web Básica ($1,500)">Web Básica ($1,500 MXN)</option>
          <option value="Profesional ($3,500)">Profesional ($3,500 MXN)</option>
          <option value="Empresarial ($6,000)" selected>Empresarial ($6,000 MXN) - Recomendado</option>
          <option value="Tienda Web ($9,000)">Tienda Web ($9,000 MXN)</option>
          <option value="Sistema A Medida">Sistema a Medida (Cotizar)</option>
          <option value="No estoy seguro">Aún no estoy seguro</option>

      </select>
  </div>
  ```
- **Replacement**:
  ```html
  <div>
      <label for="f_package" class="block text-sm font-semibold text-zinc-800 mb-2">Paquete que te interesa <span class="text-red-500">*</span></label>
      <select id="f_package" required aria-describedby="f_package_error" class="w-full bg-zinc-50 border border-zinc-200 rounded-xl px-4 py-3 text-black focus:outline-none focus:border-black focus:bg-white transition-colors font-medium">
          <option value="" disabled selected>-- Selecciona un paquete --</option>
          <option value="Web Básica ($1,500)">Web Básica ($1,500 MXN)</option>
          <option value="Profesional ($3,500)">Profesional ($3,500 MXN)</option>
          <option value="Empresarial ($6,000)">Empresarial ($6,000 MXN) - Recomendado</option>
          <option value="Tienda Web ($9,000)">Tienda Web ($9,000 MXN)</option>
          <option value="Sistema A Medida">Sistema a Medida (Cotizar)</option>
          <option value="No estoy seguro">Aún no estoy seguro</option>
      </select>
      <p id="f_package_error" class="hidden text-xs text-red-600 font-medium mt-1.5 flex items-center gap-1"><span aria-hidden="true">⚠️</span> Por favor selecciona un paquete.</p>
  </div>
  ```

#### 4. Form Alert Banner above Submit Button (around Line 866)
- **Insert right before `#form-submit-btn`**:
  ```html
  <div id="form-error-alert" class="hidden p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm font-semibold flex items-center gap-2 shadow-sm">
      <svg class="w-5 h-5 text-red-600 shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      <span>Por favor completa los campos obligatorios antes de continuar.</span>
  </div>
  ```

---

### 4.2 JavaScript Changes (`index.html`)

#### 1. Restore `calculateTotal()` Function
Insert before `updateFormOptions()` (around Line 918) to fix the missing function call that currently causes ReferenceErrors:
```javascript
function calculateTotal() {
    const active = isPromoActive();
    const pkgText = f_package.value;
    const googleText = f_google.value;
    const maintText = f_maint.value;
    const sumBlock = document.getElementById('summary-block');
    
    let pkgPrice = 0;
    let isCustom = false;

    if (pkgText.includes('$1,500')) pkgPrice = 1500;
    else if (pkgText.includes('$3,500')) pkgPrice = 3500;
    else if (pkgText.includes('$6,000')) pkgPrice = 6000;
    else if (pkgText.includes('$9,000')) pkgPrice = 9000;
    else isCustom = true;

    let googlePrice = 0;
    if (googleText && googleText.includes('$350')) googlePrice = 350;
    else if (googleText && googleText.includes('$750')) googlePrice = 750;

    let monthly = "$0";
    if (maintText && maintText.includes('$250')) monthly = "$250";
    else if (maintText && maintText.includes('$500')) monthly = "$500";
    
    if (isCustom || !pkgText) {
        if (sumBlock) sumBlock.classList.add('hidden');
    } else if (sumBlock) {
        sumBlock.classList.remove('hidden');
        const pkgNameEl = document.getElementById('sum-pkg-name');
        if (pkgNameEl) pkgNameEl.textContent = pkgText.split('-')[0].split('(')[0].trim();
        
        const pkgPriceEl = document.getElementById('sum-pkg-price');
        if (pkgPriceEl) {
            pkgPriceEl.textContent = `$${pkgPrice.toLocaleString()}`;
            pkgPriceEl.className = "font-bold text-white";
        }

        const gRow = document.getElementById('sum-google-row');
        if (gRow) {
            if (googlePrice > 0) {
                gRow.classList.remove('hidden');
                document.getElementById('sum-google-name').textContent = googlePrice === 750 ? "Google Maps Avanzado" : "Google Maps Básico";
                document.getElementById('sum-google-price').textContent = `+$${googlePrice.toLocaleString()}`;
            } else {
                gRow.classList.add('hidden');
            }
        }

        const initialTotal = pkgPrice + googlePrice;
        const totalEl = document.getElementById('sum-total');
        if (totalEl) totalEl.innerHTML = `$${initialTotal.toLocaleString()} <span class="text-sm font-normal text-zinc-400">MXN</span>`;
        const monthlyEl = document.getElementById('sum-monthly');
        if (monthlyEl) monthlyEl.textContent = monthly + " / mes";
    }
}
```

#### 2. Implement Validation and Redirection Logic (Replacing Lines 989–1049)
```javascript
// Validation helpers
function setFieldError(inputEl, errorEl, hasError) {
    if (hasError) {
        inputEl.classList.add('border-red-500', 'ring-2', 'ring-red-500/20', 'bg-red-50/20');
        inputEl.classList.remove('border-zinc-200');
        inputEl.setAttribute('aria-invalid', 'true');
        if (errorEl) errorEl.classList.remove('hidden');
    } else {
        inputEl.classList.remove('border-red-500', 'ring-2', 'ring-red-500/20', 'bg-red-50/20');
        inputEl.classList.add('border-zinc-200');
        inputEl.removeAttribute('aria-invalid');
        if (errorEl) errorEl.classList.add('hidden');
    }
}

// Clear error on user interaction
const nameInput = document.getElementById('f_name');
const pkgSelect = document.getElementById('f_package');
const nameError = document.getElementById('f_name_error');
const pkgError = document.getElementById('f_package_error');
const formAlert = document.getElementById('form-error-alert');

if (nameInput) {
    nameInput.addEventListener('input', () => {
        if (nameInput.value.trim() !== '') {
            setFieldError(nameInput, nameError, false);
            if (!pkgSelect || pkgSelect.value !== '') {
                if (formAlert) formAlert.classList.add('hidden');
            }
        }
    });
}

if (pkgSelect) {
    pkgSelect.addEventListener('change', () => {
        if (pkgSelect.value !== '') {
            setFieldError(pkgSelect, pkgError, false);
            if (!nameInput || nameInput.value.trim() !== '') {
                if (formAlert) formAlert.classList.add('hidden');
            }
        }
    });
}

document.getElementById('wa-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const nameVal = nameInput ? nameInput.value.trim() : '';
    const pkgVal = pkgSelect ? pkgSelect.value.trim() : '';

    let isValid = true;
    let firstInvalid = null;

    if (!nameVal) {
        setFieldError(nameInput, nameError, true);
        isValid = false;
        firstInvalid = firstInvalid || nameInput;
    } else {
        setFieldError(nameInput, nameError, false);
    }

    if (!pkgVal || pkgVal === '') {
        setFieldError(pkgSelect, pkgError, true);
        isValid = false;
        firstInvalid = firstInvalid || pkgSelect;
    } else {
        setFieldError(pkgSelect, pkgError, false);
    }

    if (!isValid) {
        if (formAlert) formAlert.classList.remove('hidden');
        if (firstInvalid) firstInvalid.focus();
        return; // PREVENT WHATSAPP REDIRECTION WHEN EMPTY
    }

    if (formAlert) formAlert.classList.add('hidden');

    // Safe retrieval of other form fields
    const active = isPromoActive();
    const history = document.getElementById('f_clients') ? document.getElementById('f_clients').value : '';
    const details = document.getElementById('f_details') ? document.getElementById('f_details').value : '';
    const maint = document.getElementById('f_maint') ? document.getElementById('f_maint').value : '';
    const google = document.getElementById('f_google') ? document.getElementById('f_google').value : '';
    const budget = (document.getElementById('f_budget') && document.getElementById('f_budget').value) ? document.getElementById('f_budget').value : "No especificado";

    let initialTotal = 0;
    let isCustom = false;

    if (pkgVal.includes('$1,500')) initialTotal += 1500;
    else if (pkgVal.includes('$3,500')) initialTotal += 3500;
    else if (pkgVal.includes('$6,000')) initialTotal += 6000;
    else if (pkgVal.includes('$9,000')) initialTotal += 9000;
    else isCustom = true;

    if (google.includes('$350')) initialTotal += 350;
    else if (google.includes('$750')) initialTotal += 750;

    const phone = "525645890610";
    let message = `*¡Hola! Me gustaría cotizar un proyecto web con AV My Web Studio*\n\n`;
    message += `👤 *Mi nombre:* ${nameVal}\n`;
    message += `🤝 *Historial:* ${history}\n`;
    message += `📦 *Paquete interesado:* ${pkgVal}\n`;
    message += `📍 *Google Maps:* ${google}\n`;
    message += `🛠️ *Mantenimiento:* ${maint}\n`;
    message += `💰 *Presupuesto max:* ${budget}\n\n`;

    if (!isCustom) {
        message += `💸 *Inversión Inicial Estimada:* $${initialTotal.toLocaleString()} MXN\n\n`;
    } else {
        message += `💸 *Inversión Inicial Estimada:* A Cotizar\n\n`;
    }

    message += `📝 *Detalles y personalización:*\n${details}\n\n`;
    message += `Quedo a la espera de tu respuesta.`;

    const encodedMessage = encodeURIComponent(message);
    window.open(`https://wa.me/${phone}?text=${encodedMessage}`, '_blank');
});
```

---

## 5. Verification Method

To independently verify all findings and confirm fixes after implementation:

### 5.1 Syntax & AST Verification Command
Run Node syntax validation across all script blocks in `index.html`:
```bash
node -e "
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scripts = html.match(/<script[\s\S]*?<\/script>/gi);
let hasError = false;
scripts.forEach((s, idx) => {
    const code = s.replace(/<\/?script[^>]*>/gi, '').trim();
    if (!code) return;
    try {
        new Function(code);
        console.log('Script ' + idx + ': OK');
    } catch(err) {
        console.error('Script ' + idx + ': ERROR -> ' + err.message);
        hasError = true;
    }
});
if (hasError) process.exit(1);
"
```
- **Pass condition**: Exits with code 0 and all scripts report `OK`.
- **Fail condition (current state)**: Exits with code 1: `Script 3: ERROR -> Unexpected token '??'`.

### 5.2 Functional Validation Test (Manual / Browser Flow)
1. **Empty Form Test**:
   - Open `index.html` in browser.
   - Navigate directly to `#cotizacion`.
   - Leave `#f_name` blank and leave `#f_package` on `-- Selecciona un paquete --`.
   - Click `#form-submit-btn` ("Enviar cotización a WhatsApp").
   - **Expected Result**:
     - No new tab or WhatsApp URL opens.
     - `#f_name` and `#f_package` receive red borders (`border-red-500`).
     - `#f_name_error` and `#f_package_error` become visible.
     - `#form-error-alert` banner is displayed.
     - Keyboard focus moves to `#f_name`.
2. **Partial Form Test**:
   - Type `"Carlos"` into `#f_name`.
   - Notice red border on `#f_name` immediately disappears.
   - Click `#form-submit-btn`.
   - WhatsApp is still blocked; `#f_package` remains red and `#f_package_error` remains visible.
3. **Valid Form Test**:
   - Select `"Profesional ($3,500 MXN)"` in `#f_package`.
   - Red border disappears.
   - Click `#form-submit-btn`.
   - WhatsApp redirect opens in a new tab with encoded text containing `"Mi nombre: Carlos"` and `"Paquete interesado: Profesional ($3,500)"`.
4. **Package Cards Integration Test**:
   - Click `"Elegir Profesional"` on Card 2 in `#paquetes`.
   - Verify page smoothly scrolls to `#wa-form`, `#f_package` selects `"Profesional ($3,500 MXN)"`, and `#summary-block` displays `$3,500 MXN`.

### 5.3 Invalidation Conditions
- If `f_package` is left hardcoded with `selected` on `Empresarial ($6,000)` without an unselected placeholder, a blank form cannot be simulated.
- If broad regex (`re.sub`) is used to modify `index.html`, surrounding handlers or modals may be corrupted.
