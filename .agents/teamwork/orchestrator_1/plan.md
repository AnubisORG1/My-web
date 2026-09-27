# Execution Plan — Static Landing Page Remediation

## Objective
Remediate operational, legal, and financial vulnerabilities in the static landing page (`index.html` / JS / Tailwind) per `ORIGINAL_REQUEST.md`, maintaining high visual and architectural integrity with surgical edits.

## Constraints & Requirements
- **R1. Claridad Legal y Dominio**:
  - Add: "Datos protegidos bajo LFPDPPP" near contact buttons/forms.
  - Terms & Conditions modal update: cancellation policy ("Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte").
  - Domain availability note: add "Si no está disponible, sugerimos .com.mx o .mx".
- **R2. Límites Financieros y SLA**:
  - SLA: "Tiempo de respuesta de 24 a 48 horas en días hábiles".
  - Maintenance limits: "Plan Básico incluye 5 cambios mensuales. Plan Profesional incluye 10 cambios mensuales".
  - Pricing table development differentiation:
    - Básica: "Modificaciones básicas (solo fotos, textos y colores)".
    - Profesional: "Modificaciones completas (nuevas secciones y páginas)".
- **R3. Validación de Formulario (JavaScript)**:
  - Mandatory validation on contact form fields (Name and Package).
  - Visual alerts/error messages (e.g. red borders, error text), blocking WhatsApp redirect if empty/invalid.
- **R4. Edición Quirúrgica (CRITICAL)**:
  - Exact string replacement or safe BeautifulSoup/DOM manipulation only. Broad regexes strictly prohibited.

## Phase Breakdown

### Phase 0: Survey & Architecture Discovery
- Dispatch 3 Explorers (`teamwork_preview_explorer`) to inspect:
  - Explorer 1: Document structure, contact form markup, buttons, and legal modals.
  - Explorer 2: Pricing tables, maintenance sections, domain sections, and SLA locations.
  - Explorer 3: JavaScript form submission scripts, WhatsApp redirect logic, existing validation, and event listeners.
- Consolidate explorer findings into `PROJECT.md` (Feature Inventory, Architecture, Milestones, Interface Contracts).

### Phase 1: Implementation & Verification Loop
For each milestone:
1. Dispatch Worker with Explorer findings, R4 surgical requirements, and mandatory integrity warning.
2. Dispatch 2 Reviewers independently.
3. Dispatch 2 Challengers for empirical testing.
4. Dispatch 1 Forensic Auditor (`teamwork_preview_auditor`).
5. Evaluate Gate in `GATE_STATUS.md`. All criteria must pass before milestone sign-off.

### Phase 2: Comprehensive E2E Testing & Final Gate
- Verify all Acceptance Criteria:
  - Pricing table change limits & subscription caps.
  - SLA & domain fallback clarity.
  - Form validation blocks empty submission & highlights fields.
  - Data protection & cancellation policies in UI/modals.
  - Visual layout & HTML structure preserved without regression.

### Phase 3: Final Synthesis & Reporting
- Synthesize all results.
- Report back to caller agent and human user.
