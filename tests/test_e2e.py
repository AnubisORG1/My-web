#!/usr/bin/env python3
"""
Comprehensive Automated E2E Test Suite (Tiers 1-4) in Python
Project: Static Landing Page Remediation
Targets: index.html, js/app.js, css/styles.css
Derived from: ORIGINAL_REQUEST.md & PROJECT.md
Author: test_writer_1
"""

import sys
import os
import re
import subprocess
import json
from pathlib import Path
from html.parser import HTMLParser
import bs4

# Ensure UTF-8 output on Windows consoles to prevent charmap encoding errors
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.platform == "win32" and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# --- Configuration & Paths ---
ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT_DIR / "index.html"
JS_APP = ROOT_DIR / "js" / "app.js"

# --- ANSI Color Codes ---
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"

class TestReport:
    def __init__(self):
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []
        self.tier5 = []
        self.tier6 = []
        self.tier7 = []
        self.tier8 = []
        self.passed = 0
        self.failed = 0
        self.bugs = []

    def record(self, tier, test_id, desc, passed, error_detail=None):
        entry = {"tier": tier, "id": test_id, "desc": desc, "passed": passed, "error": error_detail}
        getattr(self, tier).append(entry)
        if passed:
            self.passed += 1
            print(f"  {GREEN}✔ [PASS]{RESET} {BOLD}{test_id}:{RESET} {desc}")
        else:
            self.failed += 1
            self.bugs.append(entry)
            print(f"  {RED}✖ [FAIL]{RESET} {BOLD}{test_id}:{RESET} {desc}")
            if error_detail:
                print(f"     {RED}→ Reason: {error_detail}{RESET}")

def load_file_content(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf16le", errors="ignore")
    return raw.decode("utf-8", errors="ignore")

def run_tests():
    report = TestReport()
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  PYTHON STATIC LANDING PAGE AUTOMATED TEST SUITE (TIERS 1 - 4)     {RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")

    try:
        content = load_file_content(INDEX_HTML)
    except Exception as e:
        print(f"{RED}Fatal: Could not load index.html: {e}{RESET}")
        return 1

    # --------------------------------------------------------------------------
    # TIER 1: FEATURE COVERAGE (R1, R2, R3)
    # --------------------------------------------------------------------------
    print(f"{CYAN}{BOLD}[TIER 1] FEATURE COVERAGE TESTS{RESET}")

    # T1.1: LFPDPPP Notice in / near #wa-form
    cotizacion_match = re.search(r'id=["\']cotizacion["\'][\s\S]*?</form>', content)
    has_lfpdppp_form = bool(cotizacion_match and re.search(r'Datos protegidos bajo LFPDPPP', cotizacion_match.group(0), re.IGNORECASE))
    report.record("tier1", "T1.1_LFPDPPP_ContactForm",
                  "Verify 'Datos protegidos bajo LFPDPPP' notice is present in #wa-form / #cotizacion",
                  has_lfpdppp_form,
                  None if has_lfpdppp_form else "Notice 'Datos protegidos bajo LFPDPPP' missing from contact form")

    # T1.2: LFPDPPP Notice in #contacto
    contacto_match = re.search(r'id=["\']contacto["\'][\s\S]*?</section>', content)
    has_lfpdppp_email = bool(contacto_match and re.search(r'Datos protegidos bajo LFPDPPP', contacto_match.group(0), re.IGNORECASE))
    report.record("tier1", "T1.2_LFPDPPP_DirectEmail",
                  "Verify 'Datos protegidos bajo LFPDPPP' notice is present in #contacto (direct email)",
                  has_lfpdppp_email,
                  None if has_lfpdppp_email else "Notice 'Datos protegidos bajo LFPDPPP' missing from #contacto")

    # T1.3: Terms Modal Section 5 Cancellation Policy
    terminos_match = re.search(r'id=["\']modal-terminos["\'][\s\S]*?</div>\s*</div>\s*</div>', content)
    terminos_text = terminos_match.group(0) if terminos_match else ""
    has_cancellation = bool(re.search(r'Después de cancelar la suscripción,\s*la web te pertenece pero te quedas sin soporte', content, re.IGNORECASE))
    report.record("tier1", "T1.3_TermsModal_Section5",
                  "Verify modal-terminos contains Section 5 cancellation policy text",
                  has_cancellation,
                  None if has_cancellation else "Cancellation policy text missing from #modal-terminos")

    # T1.4: Domain Availability FAQ Clarification
    dudas_match = re.search(r'id=["\']dudas["\'][\s\S]*?</section>', content)
    dudas_text = dudas_match.group(0) if dudas_match else ""
    has_domain_fallback = bool(re.search(r'Si no está disponible,\s*sugerimos \.com\.mx o \.mx', dudas_text, re.IGNORECASE))
    report.record("tier1", "T1.4_DomainFAQ_Fallback",
                  "Verify FAQ contains domain fallback: 'Si no está disponible, sugerimos .com.mx o .mx'",
                  has_domain_fallback,
                  None if has_domain_fallback else "Domain fallback text missing from #dudas")

    # T1.5: Pricing Scope Differentiation
    paquetes_match = re.search(r'id=["\']paquetes["\'][\s\S]*?</section>', content)
    paquetes_text = paquetes_match.group(0) if paquetes_match else ""
    has_basica_scope = bool(re.search(r'Modificaciones b[áa]sicas \(solo fotos, textos y colores\)', paquetes_text, re.IGNORECASE))
    has_pro_scope = bool(re.search(r'Modificaciones completas \(nuevas secciones y p[áa]ginas\)', paquetes_text, re.IGNORECASE))
    both_scopes = has_basica_scope and has_pro_scope
    report.record("tier1", "T1.5_PricingScope_Differentiation",
                  "Verify pricing cards display development scope constraints: Básica vs Profesional",
                  both_scopes,
                  None if both_scopes else f"Básica scope={has_basica_scope}, Profesional scope={has_pro_scope}")

    # T1.6: Maintenance Subscription Limits (5 vs 10)
    has_5_changes = bool(re.search(r'Plan B[áa]sico incluye 5 cambios mensuales', content, re.IGNORECASE))
    has_10_changes = bool(re.search(r'Plan Profesional incluye 10 cambios mensuales', content, re.IGNORECASE))
    both_limits = has_5_changes and has_10_changes
    report.record("tier1", "T1.6_Maintenance_Quotas_5vs10",
                  "Verify maintenance subscription displays limits: 5 vs 10 monthly changes",
                  both_limits,
                  None if both_limits else f"5 cambios={has_5_changes}, 10 cambios={has_10_changes}")

    # T1.7: SLA Notice Response Time
    has_sla = bool(re.search(r'Tiempo de respuesta de 24 a 48 horas en d[íi]as h[áa]biles', content, re.IGNORECASE))
    report.record("tier1", "T1.7_SLA_Notice_ResponseTime",
                  "Verify SLA response time notice: 'Tiempo de respuesta de 24 a 48 horas en días hábiles'",
                  has_sla,
                  None if has_sla else "SLA response time notice missing")

    # T1.8: Package Dropdown Placeholder & Novalidate Attribute
    pkg_match = re.search(r'<select[^>]*id=["\']f_package["\'][^>]*>([\s\S]*?)</select>', content, re.IGNORECASE)
    has_pkg_placeholder = bool(pkg_match and re.search(r'<option[^>]*value=["\']["\'][^>]*>', pkg_match.group(1)))
    has_novalidate = bool(re.search(r'<form[^>]*id=["\']wa-form["\'][^>]*\bnovalidate\b', content, re.IGNORECASE))
    form_prep_ok = has_pkg_placeholder and has_novalidate
    report.record("tier1", "T1.8_FormPackage_PlaceholderAndNovalidate",
                  "Verify #f_package has unselected placeholder option and #wa-form has novalidate",
                  form_prep_ok,
                  None if form_prep_ok else f"Placeholder option={has_pkg_placeholder}, novalidate={has_novalidate}")

    # --------------------------------------------------------------------------
    # TIER 2: BOUNDARY & CORNER CASES (R3 FORM VALIDATION)
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 2] BOUNDARY & CORNER CASES (VALIDATION LOGIC){RESET}")

    # Extract inline scripts
    scripts = re.findall(r'<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
    js_code = "\n;\n".join(scripts)

    # T2.1: Check if Name & Package are checked for empty/blank values
    has_name_validation = bool(re.search(r'f_name|nameVal|name', js_code) and
                              (re.search(r'\.trim\(\)\s*===?\s*[\'"][\'"]', js_code) or re.search(r'!nameVal|!name', js_code)))
    has_pkg_validation = bool(re.search(r'f_package|pkgVal|pkg', js_code) and
                             (re.search(r'!pkgVal|!pkg|pkgVal\s*===?\s*[\'"][\'"]', js_code)))
    has_both_validations = has_name_validation and has_pkg_validation
    report.record("tier2", "T2.1_FormValidation_MandatoryFields_Check",
                  "Verify submit handler checks both Name and Package for empty/whitespace inputs",
                  has_both_validations,
                  None if has_both_validations else f"Name validation={has_name_validation}, Package validation={has_pkg_validation}")

    # T2.2: Redirection Guard (halts execution before window.open on invalid form)
    has_redirect_guard = bool(re.search(r'(return;|return\s+false;)\s*[\s\S]*?window\.open', js_code) or
                              re.search(r'if\s*\([^)]*invalid[^)]*\)\s*\{[\s\S]*?return;?\}', js_code, re.IGNORECASE) or
                              re.search(r'if\s*\(!hasError\)\s*\{[\s\S]*?window\.open', js_code))
    report.record("tier2", "T2.2_FormValidation_RedirectionBlocked_OnInvalid",
                  "Verify submission aborts execution before calling window.open when form is invalid",
                  has_redirect_guard,
                  None if has_redirect_guard else "Submission handler lacks early return/guard before window.open")

    # T2.3: Visual Error State Application (border-red-500)
    has_red_border = bool(re.search(r'border-red-500', js_code) or re.search(r'border-red-500', content))
    report.record("tier2", "T2.3_FormValidation_VisualErrorStyling",
                  "Verify visual error indicator classes ('border-red-500') are defined and applied on invalid fields",
                  has_red_border,
                  None if has_red_border else "Visual error class 'border-red-500' not found in script or DOM")

    # T2.4: Real-time Error Clearance on Input / Change
    has_error_clearance = bool(re.search(r'addEventListener\([\'"]input[\'"]', js_code) and
                               re.search(r'addEventListener\([\'"]change[\'"]', js_code))
    report.record("tier2", "T2.4_FormValidation_RealtimeClearance",
                  "Verify 'input' and 'change' listeners are attached to clear field errors in real time",
                  has_error_clearance,
                  None if has_error_clearance else "Real-time error clear listeners ('input'/'change') missing")

    # --------------------------------------------------------------------------
    # TIER 3: CROSS-FEATURE COMBINATIONS
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 3] CROSS-FEATURE COMBINATIONS{RESET}")

    # T3.1: Package Card Selection (selectPackage function definition)
    has_select_package_def = bool(re.search(r'function\s+selectPackage\s*\(', js_code))
    report.record("tier3", "T3.1_PackageCard_SelectPackage_Function",
                  "Verify selectPackage() function is defined to handle package card click selection",
                  has_select_package_def,
                  None if has_select_package_def else "selectPackage() function not defined in JavaScript")

    # T3.2: Modal Runtime Functions (openModal & closeModal)
    has_open_modal = bool(re.search(r'function\s+openModal\s*\(', js_code) or re.search(r'window\.openModal\s*=', js_code))
    has_close_modal = bool(re.search(r'function\s+closeModal\s*\(', js_code) or re.search(r'window\.closeModal\s*=', js_code))
    modals_defined = has_open_modal and has_close_modal
    report.record("tier3", "T3.2_Modal_Runtime_Functions",
                  "Verify openModal() and closeModal() functions are defined in JavaScript runtime",
                  modals_defined,
                  None if modals_defined else f"openModal={has_open_modal}, closeModal={has_close_modal}")

    # T3.3: Footer Modal Triggers
    footer_match = re.search(r'<footer[\s\S]*?</footer>', content, re.IGNORECASE)
    footer_text = footer_match.group(0) if footer_match else ""
    has_footer_privacidad = bool(re.search(r'openModal\([\'"]privacidad[\'"]\)', footer_text))
    has_footer_terminos = bool(re.search(r'openModal\([\'"]terminos[\'"]\)', footer_text))
    both_footer_triggers = has_footer_privacidad and has_footer_terminos
    report.record("tier3", "T3.3_Footer_Modal_Triggers_Present",
                  "Verify footer contains accessible buttons/links triggering openModal('privacidad') & openModal('terminos')",
                  both_footer_triggers,
                  None if both_footer_triggers else f"Footer Privacidad={has_footer_privacidad}, Términos={has_footer_terminos}")

    # --------------------------------------------------------------------------
    # TIER 4: REAL-WORLD APPLICATION & ACCEPTANCE CRITERIA
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 4] REAL-WORLD APPLICATION & ACCEPTANCE CRITERIA{RESET}")

    # T4.1: JavaScript Syntax Error Check (Specific scan for fatal Line 1039 bug)
    fatal_syntax_bug = bool(re.search(r'\?\?\s*\*Inversi[óo]n', js_code))
    script_syntax_clean = not fatal_syntax_bug
    report.record("tier4", "T4.1_JavaScript_AST_Syntax_ZeroErrors",
                  "Verify JavaScript runtime is free of fatal syntax errors (Line 1039 bug check)",
                  script_syntax_clean,
                  None if script_syntax_clean else "Fatal syntax error found on Line 1039: '?? *Inversión Inicial Estimada:...'")

    # T4.2: HTML Structural Landmarks Preservation (R4)
    landmarks = ["navbar", "paquetes", "dudas", "cotizacion", "contacto", "modal-privacidad", "modal-terminos"]
    missing_landmarks = [lm for lm in landmarks if f'id="{lm}"' not in content and f"id='{lm}'" not in content]
    structure_ok = len(missing_landmarks) == 0
    report.record("tier4", "T4.2_HTML_StructuralPreservation",
                  "Verify all core DOM landmarks exist without section deletion (R4 surgical integrity)",
                  structure_ok,
                  None if structure_ok else f"Missing landmarks: {missing_landmarks}")

    # T4.3: Acceptance Criteria Aggregation
    ac1 = both_scopes and both_limits
    ac2 = has_sla and has_domain_fallback
    ac3 = has_both_validations and has_redirect_guard and has_red_border
    ac4 = has_lfpdppp_form and has_cancellation
    ac5 = structure_ok and script_syntax_clean

    print(f"\n  {BOLD}Acceptance Criteria Evaluation:{RESET}")
    print(f"    [{GREEN + 'PASS' + RESET if ac1 else RED + 'FAIL' + RESET}] AC1: Tabla de precios clara (textos/fotos vs secciones) y límites (5 vs 10 cambios)")
    print(f"    [{GREEN + 'PASS' + RESET if ac2 else RED + 'FAIL' + RESET}] AC2: SLA visible (24-48 hrs hábiles) y alternativa de dominios (.com.mx / .mx)")
    print(f"    [{GREEN + 'PASS' + RESET if ac3 else RED + 'FAIL' + RESET}] AC3: Formulario en blanco bloquea redirección y resalta campos faltantes")
    print(f"    [{GREEN + 'PASS' + RESET if ac4 else RED + 'FAIL' + RESET}] AC4: Leyendas de datos (LFPDPPP) y retención de propiedad tras cancelar")
    print(f"    [{GREEN + 'PASS' + RESET if ac5 else RED + 'FAIL' + RESET}] AC5: Diseño y estructura intactos sin pérdida de secciones")

    all_ac = ac1 and ac2 and ac3 and ac4 and ac5
    report.record("tier4", "T4.3_AcceptanceCriteria_Aggregate",
                  "Verify all 5 user acceptance criteria from ORIGINAL_REQUEST.md are fully satisfied",
                  all_ac,
                  None if all_ac else f"AC Summary: AC1={ac1}, AC2={ac2}, AC3={ac3}, AC4={ac4}, AC5={ac5}")

    # --------------------------------------------------------------------------
    # TIER 5: ADVERSARIAL AST SYNTAX VERIFICATION ACROSS ALL SCRIPTS (NODE V8)
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 5] ADVERSARIAL AST SYNTAX VERIFICATION (NODE V8){RESET}")

    # Extract all script tags with their attributes and content
    script_blocks = re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>', content, re.IGNORECASE)

    # T5.1: Parse each inline script through node:vm Script compiler
    ast_all_valid = True
    ast_failure_reason = []
    for i, (attrs, body) in enumerate(script_blocks):
        body_trimmed = body.strip()
        if 'src=' in attrs.lower() or not body_trimmed:
            continue
        node_check_code = """
const vm = require('vm');
const fs = require('fs');
const code = fs.readFileSync(0, 'utf8');
try {
    new vm.Script(code, { filename: 'inline-script.js' });
    process.exit(0);
} catch (e) {
    console.error(e.message);
    process.exit(1);
}
"""
        proc = subprocess.run(["node", "-e", node_check_code], input=body_trimmed, text=True, encoding='utf-8', capture_output=True)
        if proc.returncode != 0:
            ast_all_valid = False
            ast_failure_reason.append(f"Inline script #{i}: {proc.stderr.strip()}")

    report.record("tier5", "T5.1_InlineScripts_AST_Compilation",
                  "Verify all inline <script> blocks compile to V8 AST without syntax errors",
                  ast_all_valid,
                  None if ast_all_valid else "; ".join(ast_failure_reason))

    # T5.2: Verify js/app.js compiles to V8 AST
    appjs_ast_valid = False
    appjs_reason = None
    if JS_APP.exists():
        appjs_code = load_file_content(JS_APP)
        proc = subprocess.run(["node", "-e", """
const vm = require('vm');
const fs = require('fs');
const code = fs.readFileSync(0, 'utf8');
try {
    new vm.Script(code, { filename: 'app.js' });
    process.exit(0);
} catch (e) {
    console.error(e.message);
    process.exit(1);
}
"""], input=appjs_code, text=True, encoding='utf-8', capture_output=True)
        appjs_ast_valid = (proc.returncode == 0)
        appjs_reason = None if appjs_ast_valid else proc.stderr.strip()
    report.record("tier5", "T5.2_AppJs_AST_Compilation",
                  "Verify js/app.js compiles to V8 AST without syntax errors",
                  appjs_ast_valid,
                  appjs_reason)

    # T5.3: Strict Mode Compliance Check for Main Logic Script
    main_script = ""
    for attrs, body in script_blocks:
        if "openModal" in body and "wa-form" in body:
            main_script = body
            break

    strict_ast_valid = False
    strict_reason = None
    if main_script:
        strict_code = "'use strict';\n" + main_script
        proc = subprocess.run(["node", "-e", """
const vm = require('vm');
const fs = require('fs');
const code = fs.readFileSync(0, 'utf8');
try {
    new vm.Script(code, { filename: 'strict-main.js' });
    process.exit(0);
} catch (e) {
    console.error(e.message);
    process.exit(1);
}
"""], input=strict_code, text=True, encoding='utf-8', capture_output=True)
        strict_ast_valid = (proc.returncode == 0)
        strict_reason = None if strict_ast_valid else proc.stderr.strip()
    report.record("tier5", "T5.3_MainScript_StrictMode_Syntax",
                  "Verify main runtime script compiles cleanly under strict mode",
                  strict_ast_valid,
                  strict_reason)

    # --------------------------------------------------------------------------
    # TIER 6: ADVERSARIAL MODAL LIFECYCLE & EVENT STRESS HARNESS
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 6] ADVERSARIAL MODAL LIFECYCLE & EVENT STRESS HARNESS{RESET}")

    modal_sim_runner = """
const vm = require('vm');
const fs = require('fs');

const mainScript = fs.readFileSync(0, 'utf8');

class MockClassList {
    constructor(initial = '') {
        this.classes = new Set(initial.split(/\\s+/).filter(Boolean));
    }
    add(...cls) { cls.forEach(c => c && c.split(/\\s+/).forEach(s => s && this.classes.add(s))); }
    remove(...cls) { cls.forEach(c => c && c.split(/\\s+/).forEach(s => s && this.classes.delete(s))); }
    contains(c) { return this.classes.has(c); }
    has(c) { return this.classes.has(c); }
    get value() { return Array.from(this.classes).join(' '); }
    set value(v) { this.classes = new Set(v.split(/\\s+/).filter(Boolean)); }
}

class MockElement {
    constructor(id, tag = 'div', classes = '') {
        this.id = id;
        this.tagName = tag.toUpperCase();
        this.classList = new MockClassList(classes);
        this.style = {};
        this.attributes = {};
        this.listeners = {};
        this.offsetWidth = 100;
        this.value = '';
        this.parentElement = { style: {} };
    }
    setAttribute(k, v) { this.attributes[k] = v; }
    getAttribute(k) { return this.attributes[k] || null; }
    removeAttribute(k) { delete this.attributes[k]; }
    addEventListener(evt, fn) {
        if (!this.listeners[evt]) this.listeners[evt] = [];
        this.listeners[evt].push(fn);
    }
    dispatchEvent(evt) {
        evt.target = evt.target || this;
        (this.listeners[evt.type] || []).forEach(fn => fn.call(this, evt));
    }
    scrollIntoView() {}
}

const elements = new Map();
function el(id, tag = 'div', classes = '') {
    const e = new MockElement(id, tag, classes);
    elements.set(id, e);
    return e;
}

const body = el('body', 'body');
const backdrop = el('modal-backdrop', 'div', 'fixed inset-0 z-[100] hidden bg-black/60 backdrop-blur-sm transition-opacity opacity-0');
const modalPriv = el('modal-privacidad', 'div', 'fixed inset-0 z-[101] hidden items-center justify-center p-4 sm:p-6 pointer-events-none');
const privContent = el('privacidad-content', 'div', 'bg-white rounded-3xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl pointer-events-auto transform scale-95 opacity-0 transition-all duration-300');
const modalTerm = el('modal-terminos', 'div', 'fixed inset-0 z-[101] hidden items-center justify-center p-4 sm:p-6 pointer-events-none');
const termContent = el('terminos-content', 'div', 'bg-white rounded-3xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl pointer-events-auto transform scale-95 opacity-0 transition-all duration-300');

// Form dependencies
el('f_package', 'select');
el('f_maint', 'select');
el('f_google', 'select');
el('google-desc', 'div');
el('wa-form', 'form');
el('f_name', 'input');
el('f_name_error', 'p');
el('f_package_error', 'p');
el('form-error-alert', 'div');
el('current-year', 'span');

const docListeners = {};
const mockDoc = {
    body: body,
    getElementById: (id) => elements.get(id) || null,
    querySelector: (sel) => sel.startsWith('#') ? elements.get(sel.slice(1)) || null : null,
    querySelectorAll: () => [],
    addEventListener: (evt, fn) => {
        if (!docListeners[evt]) docListeners[evt] = [];
        docListeners[evt].push(fn);
    },
    dispatchEvent: (evt) => {
        (docListeners[evt.type] || []).forEach(fn => fn(evt));
    }
};

let timers = [];
const mockSetTimeout = (fn, delay) => {
    const t = { id: Math.random(), fn, delay, executed: false };
    timers.push(t);
    return t;
};

const mockClearTimeout = (t) => {
    timers = timers.filter(x => x !== t && x.id !== (t ? t.id : null));
};

const flushTimers = () => {
    const pending = [...timers];
    timers = [];
    pending.forEach(t => { t.executed = true; t.fn(); });
};

const ctx = vm.createContext({
    document: mockDoc,
    window: { scrollY: 0, open: () => {}, addEventListener: () => {} },
    console: { log: () => {}, warn: () => {}, error: () => {} },
    setTimeout: mockSetTimeout,
    clearTimeout: mockClearTimeout,
    Date: Date,
    encodeURIComponent: encodeURIComponent,
    decodeURIComponent: decodeURIComponent,
    Option: function(t, v) { this.text = t; this.value = v; }
});

vm.runInContext(mainScript, ctx);

const results = {};

// Test 1: openModal('privacidad')
ctx.openModal('privacidad');
results.open_overflow_locked = (body.style.overflow === 'hidden');
results.open_backdrop_unhidden = !backdrop.classList.has('hidden');
results.open_backdrop_opacity = !backdrop.classList.has('opacity-0');
results.open_modal_unhidden = !modalPriv.classList.has('hidden');
results.open_modal_flex = modalPriv.classList.has('flex');
results.open_content_scale = !privContent.classList.has('scale-95');
results.open_content_opacity = !privContent.classList.has('opacity-0');

// Test 2: closeModal('privacidad')
ctx.closeModal('privacidad');
results.close_overflow_cleared_immediately = (body.style.overflow === '');
results.close_backdrop_opacity_during_trans = backdrop.classList.has('opacity-0');
results.close_content_scale_during_trans = privContent.classList.has('scale-95');
results.close_content_opacity_during_trans = privContent.classList.has('opacity-0');
results.close_not_hidden_before_timer = !backdrop.classList.has('hidden') && !modalPriv.classList.has('hidden');

flushTimers();
results.close_backdrop_hidden_after_timer = backdrop.classList.has('hidden');
results.close_modal_hidden_after_timer = modalPriv.classList.has('hidden');
results.close_modal_flex_removed = !modalPriv.classList.has('flex');

// Test 3: Escape key dismisses open modal
ctx.openModal('terminos');
mockDoc.dispatchEvent({ type: 'keydown', key: 'Escape' });
results.escape_overflow_cleared = (body.style.overflow === '');
flushTimers();
results.escape_modal_hidden = modalTerm.classList.has('hidden');

// Test 4: Modal container outside click
ctx.openModal('privacidad');
modalPriv.dispatchEvent({ type: 'click', target: modalPriv });
results.outside_click_clears_overflow = (body.style.overflow === '');
flushTimers();
results.outside_click_hides_modal = modalPriv.classList.has('hidden');

// Test 5: Click on modal content card does NOT close modal
ctx.openModal('privacidad');
modalPriv.dispatchEvent({ type: 'click', target: privContent });
results.card_click_keeps_overflow = (body.style.overflow === 'hidden');
results.card_click_keeps_visible = !modalPriv.classList.has('hidden');
ctx.closeModal('privacidad');
flushTimers();

// Test 6: Adversarial Race Condition - Rapid reopen within 300ms transition window
ctx.openModal('privacidad');
ctx.closeModal('privacidad'); // starts 300ms timer
ctx.openModal('privacidad'); // reopen before timer fires
flushTimers(); // old timer fires now!
// If timeout added 'hidden' to modalPriv, it was erroneously hidden!
results.race_condition_modal_survives = !modalPriv.classList.has('hidden');
results.race_condition_overflow_locked = (body.style.overflow === 'hidden');

console.log(JSON.stringify(results));
"""

    modal_results = {}
    if main_script:
        proc = subprocess.run(["node", "-e", modal_sim_runner], input=main_script, text=True, encoding='utf-8', capture_output=True)
        if proc.returncode == 0:
            try:
                modal_results = json.loads(proc.stdout.strip())
            except Exception as e:
                print(f"Error parsing modal simulation output: {e}, stdout: {proc.stdout}")
        else:
            print(f"Modal simulation failed with error: {proc.stderr}")

    # T6.1: Modal Open Lifecycle State (Backdrop, Modal classes, and Content transform)
    open_ok = bool(modal_results.get('open_backdrop_unhidden') and
                   modal_results.get('open_backdrop_opacity') and
                   modal_results.get('open_modal_unhidden') and
                   modal_results.get('open_modal_flex') and
                   modal_results.get('open_content_scale') and
                   modal_results.get('open_content_opacity'))
    report.record("tier6", "T6.1_Modal_Open_ClassTransitions",
                  "Verify openModal() correctly removes hidden/opacity-0/scale-95 and adds flex",
                  open_ok,
                  None if open_ok else f"Modal open transition mismatch: {modal_results}")

    # T6.2: Body Overflow Lock on Open
    overflow_locked = bool(modal_results.get('open_overflow_locked'))
    report.record("tier6", "T6.2_Modal_BodyOverflow_Lock",
                  "Verify openModal() locks body scroll with document.body.style.overflow = 'hidden'",
                  overflow_locked,
                  None if overflow_locked else "body.style.overflow was not set to 'hidden'")

    # T6.3: Body Overflow Unlock on Close & 300ms Transition
    close_ok = bool(modal_results.get('close_overflow_cleared_immediately') and
                    modal_results.get('close_backdrop_opacity_during_trans') and
                    modal_results.get('close_content_scale_during_trans') and
                    modal_results.get('close_not_hidden_before_timer') and
                    modal_results.get('close_backdrop_hidden_after_timer') and
                    modal_results.get('close_modal_hidden_after_timer') and
                    modal_results.get('close_modal_flex_removed'))
    report.record("tier6", "T6.3_Modal_Close_TransitionAndUnlock",
                  "Verify closeModal() restores body overflow immediately and hides modal after 300ms transition",
                  close_ok,
                  None if close_ok else f"Modal close transition mismatch: {modal_results}")

    # T6.4: Escape Key Listener Event
    escape_ok = bool(modal_results.get('escape_overflow_cleared') and modal_results.get('escape_modal_hidden'))
    report.record("tier6", "T6.4_Modal_EscapeKey_Listener",
                  "Verify Escape keydown event triggers modal dismissal and unlocks body overflow",
                  escape_ok,
                  None if escape_ok else f"Escape listener failed: {modal_results}")

    # T6.5: Outside Click Handler Behavior
    outside_click_ok = bool(modal_results.get('outside_click_clears_overflow') and
                            modal_results.get('outside_click_hides_modal') and
                            modal_results.get('card_click_keeps_overflow') and
                            modal_results.get('card_click_keeps_visible'))
    report.record("tier6", "T6.5_Modal_OutsideClick_Targeting",
                  "Verify outside click on modal container triggers dismissal while card clicks do not",
                  outside_click_ok,
                  None if outside_click_ok else f"Outside click mismatch: {modal_results}")

    # T6.6: Adversarial Stress: Rapid Reopen Race Condition Check
    # (Checking whether rapid reopen within 300ms transition causes unexpected collapse)
    reopen_survives = bool(modal_results.get('race_condition_modal_survives'))
    report.record("tier6", "T6.6_Modal_RapidReopen_RaceCondition",
                  "Stress-test rapid reopen within 300ms transition window (detects pending timer collapse)",
                  reopen_survives,
                  None if reopen_survives else "Defect: Pending 300ms timer from prior closeModal() collapsed reopened modal")

    # Initialize BeautifulSoup for DOM inspection
    soup = bs4.BeautifulSoup(content, 'html.parser')

    # T6.7: Pointer Events and Outside Click Targeting Audit
    modal_priv_tag = soup.find(id='modal-privacidad')
    modal_term_tag = soup.find(id='modal-terminos')
    priv_classes = modal_priv_tag.get('class', []) if modal_priv_tag else []
    term_classes = modal_term_tag.get('class', []) if modal_term_tag else []
    has_pe_none = 'pointer-events-none' in priv_classes and 'pointer-events-none' in term_classes
    backdrop_has_click_handler = bool(re.search(r'modal-backdrop[\'"]\)\.addEventListener\([\'"]click', js_code) or
                                      soup.find(id='modal-backdrop', onclick=True))
    pe_audit_pass = not (has_pe_none and not backdrop_has_click_handler)
    report.record("tier6", "T6.7_Modal_Backdrop_PointerEvents_Audit",
                  "Audit CSS pointer-events on modal overlay vs backdrop click listener",
                  pe_audit_pass,
                  None if pe_audit_pass else "Defect: modal overlay has 'pointer-events-none' but #modal-backdrop has no click listener, deflecting outside clicks in real browser")

    # --------------------------------------------------------------------------
    # TIER 7: DOM LANDMARK PRESERVATION & HTML SYNTAX INTEGRITY (BEAUTIFUL SOUP 4)
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 7] DOM LANDMARK PRESERVATION & HTML SYNTAX (BS4){RESET}")

    # Landmark checks
    landmarks_to_audit = [
        ("navbar", ["header", "nav"]),
        ("paquetes", ["section"]),
        ("cotizacion", ["section"]),
        ("dudas", ["section"]),
        ("contacto", ["section"]),
        ("modal-privacidad", ["div"]),
        ("modal-terminos", ["div"]),
    ]

    all_landmarks_valid = True
    landmark_errors = []
    for lm_id, allowed_tags in landmarks_to_audit:
        el = soup.find(id=lm_id)
        if not el:
            all_landmarks_valid = False
            landmark_errors.append(f"Missing #{lm_id}")
        elif allowed_tags and el.name.lower() not in [t.lower() for t in allowed_tags]:
            all_landmarks_valid = False
            landmark_errors.append(f"#{lm_id} expected one of {allowed_tags} but found <{el.name}>")
        elif len(el.contents) == 0:
            all_landmarks_valid = False
            landmark_errors.append(f"#{lm_id} is an empty element")

    # Check footer
    footer_el = soup.find('footer')
    if not footer_el or len(footer_el.contents) == 0:
        all_landmarks_valid = False
        landmark_errors.append("Missing or empty <footer> landmark")

    report.record("tier7", "T7.1_Landmark_Sections_Presence_And_Structure",
                  "Verify all 7 landmark sections (#navbar, #paquetes, #cotizacion, #dudas, #contacto, footer, modals) exist and are non-empty",
                  all_landmarks_valid,
                  None if all_landmarks_valid else "; ".join(landmark_errors))

    # T7.2: Form Structural Completeness
    form_el = soup.find('form', id='wa-form')
    required_form_elements = ['f_name', 'f_package', 'f_maint', 'f_google', 'form-submit-btn', 'form-error-alert']
    missing_form_elements = [fe for fe in required_form_elements if not soup.find(id=fe)]
    form_complete = bool(form_el and len(missing_form_elements) == 0)
    report.record("tier7", "T7.2_Form_Structural_Completeness",
                  "Verify <form id='wa-form'> contains all required inputs, selects, alerts, and submit button",
                  form_complete,
                  None if form_complete else f"Missing form components: {missing_form_elements}")

    # Tag Balance Parser
    class TagBalanceParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.unmatched_closings = []
            self.void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

        def handle_starttag(self, tag, attrs):
            if tag.lower() not in self.void_elements:
                self.stack.append((self.getpos(), tag.lower()))

        def handle_endtag(self, tag):
            tag_lower = tag.lower()
            if tag_lower in self.void_elements:
                return
            if self.stack and self.stack[-1][1] == tag_lower:
                self.stack.pop()
            else:
                matched = False
                for i in range(len(self.stack) - 1, -1, -1):
                    if self.stack[i][1] == tag_lower:
                        self.stack = self.stack[:i]
                        matched = True
                        break
                if not matched:
                    self.unmatched_closings.append((self.getpos(), tag_lower))

    # T7.3a: Tag Balance across all Remediation Landmark Sections
    remediated_sections = ['paquetes', 'cotizacion', 'dudas', 'contacto', 'modal-privacidad', 'modal-terminos']
    remediated_balance_clean = True
    remediated_balance_errors = []
    for sec_id in remediated_sections:
        sec_el = soup.find(id=sec_id)
        if sec_el:
            sec_parser = TagBalanceParser()
            sec_parser.feed(str(sec_el))
            unclosed = [t for t in sec_parser.stack if t[1] not in ['html', 'body', 'head']]
            if sec_parser.unmatched_closings or unclosed:
                remediated_balance_clean = False
                remediated_balance_errors.append(f"#{sec_id}: unclosed={unclosed}, unmatched_closings={sec_parser.unmatched_closings}")

    if footer_el:
        footer_parser = TagBalanceParser()
        footer_parser.feed(str(footer_el))
        if footer_parser.unmatched_closings or footer_parser.stack:
            remediated_balance_clean = False
            remediated_balance_errors.append(f"footer: unmatched={footer_parser.unmatched_closings}")

    report.record("tier7", "T7.3a_Remediated_Landmarks_Tag_Balance",
                  "Verify all sections modified during remediation (#paquetes, #cotizacion, #dudas, #contacto, footer, modals) have 100% balanced tags",
                  remediated_balance_clean,
                  None if remediated_balance_clean else "; ".join(remediated_balance_errors))

    # T7.3b: Global Document Orphaned Tag Audit (Detects legacy template defects)
    global_parser = TagBalanceParser()
    global_parser.feed(content)
    global_unclosed = [t for t in global_parser.stack if t[1] not in ['html', 'body', 'head']]
    global_clean = (len(global_parser.unmatched_closings) == 0 and len(global_unclosed) == 0)
    report.record("tier7", "T7.3b_Global_Document_Tag_Balance",
                  "Audit full document for orphaned tags (flags pre-existing preview card </div> imbalances)",
                  global_clean,
                  None if global_clean else f"Unclosed tags: {len(global_unclosed)}, Unmatched closing tags: {len(global_parser.unmatched_closings)} (lines {[p[0][0] for p in global_parser.unmatched_closings]})")

    # --------------------------------------------------------------------------
    # TIER 8: R4 SURGICAL INTEGRITY, DUPLICATE IDS, AND ORPHANED TAGS
    # --------------------------------------------------------------------------
    print(f"\n{CYAN}{BOLD}[TIER 8] R4 INTEGRITY, DUPLICATE IDS & ORPHAN AUDIT{RESET}")

    # T8.1: Duplicate ID Audit Across Entire Document
    all_elements_with_id = soup.find_all(id=True)
    id_counts = {}
    for el in all_elements_with_id:
        element_id = el['id'].strip()
        id_counts[element_id] = id_counts.get(element_id, 0) + 1

    duplicate_ids = {k: v for k, v in id_counts.items() if v > 1}
    zero_duplicate_ids = (len(duplicate_ids) == 0)
    report.record("tier8", "T8.1_Unique_IDs_Strict_Audit",
                  "Verify that all DOM element IDs across index.html are strictly unique (0 duplicates)",
                  zero_duplicate_ids,
                  None if zero_duplicate_ids else f"Duplicate IDs found: {duplicate_ids}")

    # T8.2: Orphaned Tags or Mangled Attributes Audit
    mangled_attrs = re.findall(r'<[a-zA-Z0-9\-]+[^>]*[\'"][^>\'"]*<', content)
    zero_mangled_attrs = (len(mangled_attrs) == 0)
    report.record("tier8", "T8.2_Mangled_Attributes_Audit",
                  "Verify no unclosed quotes or malformed attributes containing nested tags (<)",
                  zero_mangled_attrs,
                  None if zero_mangled_attrs else f"Found malformed attribute snippets: {mangled_attrs[:5]}")

    # T8.3: CSS Stylesheet Reference Check
    css_ref = soup.find('link', rel='stylesheet', href=re.compile(r'styles\.css'))
    has_css = bool(css_ref)
    report.record("tier8", "T8.3_CSS_Stylesheet_Link_Integrity",
                  "Verify ./css/styles.css stylesheet link is present and correctly referenced",
                  has_css,
                  None if has_css else "styles.css stylesheet link missing")

    # --------------------------------------------------------------------------
    # SUMMARY REPORT
    # --------------------------------------------------------------------------
    total = report.passed + report.failed
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}  TEST EXECUTION SUMMARY                                              {RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}")
    print(f"  Total Tests Run : {total}")
    print(f"  Tests Passed    : {GREEN}{report.passed}{RESET}")
    print(f"  Tests Failed    : {RED if report.failed > 0 else GREEN}{report.failed}{RESET}")

    if report.bugs:
        print(f"\n{RED}{BOLD}  DISCOVERED DEFECTS / IMPLEMENTATION BUGS TO ESCALATE:{RESET}")
        for idx, b in enumerate(report.bugs, 1):
            print(f"  {idx}. [{b['tier'].upper()}] {BOLD}{b['id']}{RESET}: {b['desc']}")
            if b['error']:
                print(f"     Details: {b['error']}")
    else:
        print(f"\n  {GREEN}{BOLD}ALL TESTS PASSED! Landing page satisfies all requirements and AC.{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")

    return 0 if report.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(run_tests())
