# Task Assignment: Milestone 1 - Core Landing Page Remediation

**Assigned Agent**: worker_1
**Working Directory**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\worker_1
**Parent**: orchestrator_1 (conversation ID: fc91f4b5-8d5b-44fe-a4a1-87721cca66da)
**Target File**: c:\Users\joshu\OneDrive\Desktop\My web\index.html (Exclusive Write Ownership)
**Specification**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\ORIGINAL_REQUEST.md
**Project Plan**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\orchestrator_1\PROJECT.md

## Reference Reports (MUST READ)
1. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_survey_1\handoff.md` (Legal, Modals, LFPDPPP, Domain)
2. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_survey_2\handoff.md` (Pricing Cards, Subscription Limits, SLA)
3. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_survey_3\handoff.md` (Form Validation, JS Syntax Fix, CalculateTotal)

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## CRITICAL Constraint: R4 Edición Quirúrgica
- Todas las modificaciones al HTML deben hacerse mediante reemplazos exactos (`str.replace` / `replace_file_content`) o parseo seguro (`BeautifulSoup`).
- Está ESTRICTAMENTE PROHIBIDO usar expresiones regulares amplias (`re.sub` con `re.DOTALL`) para reemplazar grandes bloques de HTML, ya que esto puede destruir la estructura de la página.

## Implementation Tasks (F1 through F12)
1. **R1 Legal Clarity & Domain**:
   - Add `"Datos protegidos bajo LFPDPPP"` near the contact form submit button `#form-submit-btn` and the direct email section `#contacto`.
   - Expand the Terms & Conditions modal (`#modal-terminos`) with Section 5: `"5. Política de Cancelación y Propiedad"` containing `"Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte"`.
   - In FAQ `#dudas` where domain is mentioned, append: `"Si no está disponible, sugerimos .com.mx o .mx"`.
   - Implement `openModal(modalId)` and `closeModal(modalId)` functions and add accessible triggers in the footer for "Aviso de Privacidad (LFPDPPP)" and "Términos y Condiciones".
2. **R2 Financial Limits & SLA**:
   - Differentiate development in `#paquetes`:
     - Básica: `"Modificaciones básicas (solo fotos, textos y colores)"`.
     - Profesional: `"Modificaciones completas (nuevas secciones y páginas)"`.
   - Specify subscription quotas in Cards 1 and 2:
     - Básica: `"Plan Básico incluye 5 cambios mensuales"`.
     - Profesional: `"Plan Profesional incluye 10 cambios mensuales"`.
   - Insert dedicated SLA banner in `#paquetes` with `"Tiempo de respuesta de 24 a 48 horas en días hábiles"` and update FAQ `#dudas` with the SLA and 5 vs 10 limits.
   - Synchronize `#f_maint` dropdown options and helper text.
3. **R3 Form Validation & JavaScript Runtime**:
   - Add `<option value="" disabled selected>-- Selecciona un paquete --</option>` to `#f_package`.
   - Add `novalidate` to `<form id="wa-form">`.
   - Add helper error elements (`#f_name_error`, `#f_package_error`) and alert banner (`#form-error-alert`).
   - Implement submit validation: if Name (`.trim() === ''`) or Package (`!pkg || pkg === ''`) are missing, apply red borders (`border-red-500 ring-2 ring-red-500/20 bg-red-50/20`), display error messages, focus first invalid field, and block WhatsApp redirection (`return;`).
   - Clear error styling dynamically on user input (`input` and `change` events).
   - Fix syntax error on Line 1039 (`Unexpected token '??'`) with proper template string.
   - Restore `calculateTotal()` function so package selection and calculation run cleanly without ReferenceError.

## Verification Requirements
- Execute syntax check (`node -e "..."` or python validator) to prove zero syntax errors.
- Verify all required strings exist verbatim in `index.html`.
- Run tests and document passing status in your handoff report.

Write your complete handoff report to `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\worker_1\handoff.md`.
Notify parent via `send_message` when done.

## 2026-09-27T00:14:48Z
Task Assignment Received:
Implement all changes for R1, R2, R3 per the survey recommendations in index.html following R4 (Edición Quirúrgica).

