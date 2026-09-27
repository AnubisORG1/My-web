# Project: Static Landing Page Remediation

## Architecture
- **Tech Stack**: Static HTML5, Tailwind CSS (via CDN), Vanilla JavaScript, Lucide Icons.
- **Target Files**:
  - `c:\Users\joshu\OneDrive\Desktop\My web\index.html`: Primary landing page containing markup, modals, pricing cards, FAQ, contact form, and inline script.
  - `c:\Users\joshu\OneDrive\Desktop\My web\js\app.js`: Supporting scripts (Lucide icons initialization, navigation).
  - `c:\Users\joshu\OneDrive\Desktop\My web\css\styles.css`: Custom supplementary styles.
- **Data Flow**:
  - User interacts with UI / pricing cards -> `selectPackage()` updates `#f_package`, `#f_google`, `#f_maint`, and calls `calculateTotal()`.
  - Form submission on `#wa-form` -> client-side validation checks `#f_name` and `#f_package`.
  - If invalid: highlights with red border (`border-red-500`), displays error text/alert, moves focus, blocks redirection.
  - If valid: generates formatted quotation text and opens `https://wa.me/525645890610?text=...`.
  - Legal modals (`#modal-terminos`, `#modal-privacidad`): toggled via `openModal()` and `closeModal()` updating backdrop and scale/opacity classes.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | LFPDPPP Notice Placement | Add "Datos protegidos bajo LFPDPPP" near contact buttons/forms (`#wa-form` and direct email) | M1 | Survey (explorer 1) / R1 |
| F2 | Terms Modal Cancellation Policy | Expand `modal-terminos` with Section 5: "Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte" | M1 | Survey (explorer 1) / R1 |
| F3 | Domain Availability Clarification | Add "Si no está disponible, sugerimos .com.mx o .mx" to FAQ item where ".com sujeto a disponibilidad" is stated | M1 | Survey (explorer 1) / R1 |
| F4 | Modal Triggers & Handlers | Restore `openModal()` and `closeModal()` in JavaScript runtime, add accessible triggers in footer | M1 | Survey (explorer 1) / R1 |
| F5 | Pricing Scope Differentiation | In `#paquetes`, add "Modificaciones básicas (solo fotos, textos y colores)" to Básica card, and "Modificaciones completas (nuevas secciones y páginas)" to Profesional card | M1 | Survey (explorer 2) / R2 |
| F6 | Maintenance Subscription Limits | In `#paquetes` subscription boxes, specify "Plan Básico incluye 5 cambios mensuales" and "Plan Profesional incluye 10 cambios mensuales" | M1 | Survey (explorer 2) / R2 |
| F7 | SLA Notice & Visibility | Add dedicated SLA & Maintenance Policy banner in `#paquetes` and clarify FAQ item with "Tiempo de respuesta de 24 a 48 horas en días hábiles" | M1 | Survey (explorer 2) / R2 |
| F8 | Form Helper & Dropdown Synchronization | Synchronize `f_maint` dropdown options and helper text with 5 vs 10 monthly limits and 24-48h SLA | M1 | Survey (explorer 2) / R2 |
| F9 | Form Package Placeholder & Novalidate | Add `<option value="" disabled selected>-- Selecciona un paquete --</option>` to `#f_package` and `novalidate` to `#wa-form` | M1 | Survey (explorer 3) / R3 |
| F10 | Form Mandatory Validation & Redirection Block | In `wa-form` submit handler, validate Name and Package; if empty/invalid, apply red borders, display helper errors, focus first invalid field, and block `window.open` | M1 | Survey (explorer 3) / R3 |
| F11 | Real-time Error Clearance | Add `input` and `change` event listeners to clear error states dynamically upon user interaction | M1 | Survey (explorer 3) / R3 |
| F12 | JS Syntax & Runtime Restoration | Fix fatal syntax error on Line 1039 (`message += ?? ...`) and restore `calculateTotal()` function | M1 | Survey (explorer 3) / R3 |
| F13 | Acceptance Criteria & Integrity Verification | Dual track E2E verification, verifying R4 surgical replacement rules (no broad regexes, structure preserved), and Forensic Auditor verification | M2 | Survey / All AC |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Core Landing Page Remediation (R1, R2, R3, R4) | F1–F12 | none | IN_PROGRESS |
| 2 | E2E Verification, Acceptance Testing & Forensic Audit | F13 | M1 | PLANNED |

## Interface Contracts
### Modal Runtime ↔ DOM Triggers
- `openModal(modalId: 'privacidad' | 'terminos'): void`
  - Targets: `#modal-backdrop`, `#modal-${modalId}`, `#${modalId}-content`
  - Classes manipulated: remove `hidden`, add `flex`, remove `opacity-0`, remove `scale-95`
- `closeModal(modalId: 'privacidad' | 'terminos'): void`
  - Reverses animation, hides backdrop and modal after 300ms transition.

### Form Validation ↔ Submission Workflow
- `setFieldError(inputEl: HTMLElement, errorEl: HTMLElement, hasError: boolean): void`
  - `hasError === true`: adds `border-red-500 ring-2 ring-red-500/20 bg-red-50/20`, removes `border-zinc-200`, sets `aria-invalid="true"`, unhides `errorEl`.
  - `hasError === false`: removes error classes, restores `border-zinc-200`, removes `aria-invalid`, hides `errorEl`.
- Submit Handler Validation Gate:
  - If `!nameVal || !pkgVal`: displays `#form-error-alert`, focuses `firstInvalid`, executes `return;` (HALTS execution before `window.open`).

## Code Layout
- `index.html`: Main landing page (Lines 514-591 for pricing, Lines 717-740 for SLA/FAQ, Lines 748 for domain, Lines 775-874 for form, Lines 889-896 for footer, Lines 898-1054 for scripts, Lines 1060-1107 for modals).
- **Exclusive Write Ownership**: Workers operate sequentially on `index.html` per milestone to avoid write conflicts.
- **R4 Surgical Protocol**: All edits MUST use exact string matching (`replace_file_content` or `str.replace` with count=1). Never use `re.sub` with `re.DOTALL`.
