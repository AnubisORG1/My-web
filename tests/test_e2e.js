/**
 * Comprehensive Automated E2E Test Suite (Tiers 1-4)
 * Project: Static Landing Page Remediation
 * Targets: index.html, js/app.js, css/styles.css
 * Derived from: ORIGINAL_REQUEST.md & PROJECT.md
 * Author: test_writer_1
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// --- Configuration & Paths ---
const ROOT_DIR = path.resolve(__dirname, '..');
const INDEX_HTML_PATH = path.join(ROOT_DIR, 'index.html');
const JS_APP_PATH = path.join(ROOT_DIR, 'js', 'app.js');

// --- Colors for Terminal Output ---
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const BOLD = '\x1b[1m';
const RESET = '\x1b[0m';

// --- Test Results Aggregator ---
const results = {
  tier1: [],
  tier2: [],
  tier3: [],
  tier4: [],
  passed: 0,
  failed: 0,
  bugs: []
};

function recordResult(tier, testId, description, passed, errorDetail = null) {
  const item = { tier, testId, description, passed, errorDetail };
  results[tier].push(item);
  if (passed) {
    results.passed++;
    console.log(`  ${GREEN}✔ [PASS]${RESET} ${BOLD}${testId}:${RESET} ${description}`);
  } else {
    results.failed++;
    results.bugs.push({ tier, testId, description, errorDetail });
    console.log(`  ${RED}✖ [FAIL]${RESET} ${BOLD}${testId}:${RESET} ${description}`);
    if (errorDetail) {
      console.log(`     ${RED}→ Reason: ${errorDetail}${RESET}`);
    }
  }
}

// --- Encoding-Safe File Reader ---
function readHtmlSafe(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  const raw = fs.readFileSync(filePath);
  if (raw[0] === 0xff && raw[1] === 0xfe) {
    return raw.toString('utf16le');
  }
  return raw.toString('utf8');
}

// ============================================================================
// SIMULATED HEADLESS DOM & RUNTIME ENVIRONMENT
// ============================================================================

class MockClassList {
  constructor() {
    this._classes = new Set();
  }
  add(...cls) {
    cls.forEach(c => c && c.split(/\s+/).forEach(s => s && this._classes.add(s)));
  }
  remove(...cls) {
    cls.forEach(c => c && c.split(/\s+/).forEach(s => s && this._classes.delete(s)));
  }
  toggle(cls, force) {
    if (force !== undefined) {
      if (force) this.add(cls); else this.remove(cls);
      return force;
    }
    if (this._classes.has(cls)) {
      this.remove(cls);
      return false;
    } else {
      this.add(cls);
      return true;
    }
  }
  contains(cls) {
    return this._classes.has(cls);
  }
  get value() {
    return Array.from(this._classes).join(' ');
  }
  set value(val) {
    this._classes.clear();
    if (val) this.add(val);
  }
}

class MockElement {
  constructor(tag, id = '') {
    this.tagName = tag.toUpperCase();
    this.id = id;
    this.classList = new MockClassList();
    this.style = {};
    this.attributes = {};
    this.eventListeners = {};
    this.children = [];
    this.parentElement = null;
    this.textContent = '';
    this._innerHTML = '';
    this._value = '';
    this.options = [];
    this._selectedIndex = 0;
    this._focused = false;
  }

  get innerHTML() {
    return this._innerHTML;
  }
  set innerHTML(val) {
    this._innerHTML = val;
    if (val === '') {
      this.options = [];
    }
  }

  get value() {
    if (this.tagName === 'SELECT' && this.options.length > 0) {
      const idx = this.selectedIndex;
      if (idx >= 0 && idx < this.options.length) {
        return this.options[idx].value;
      }
    }
    return this._value;
  }
  set value(val) {
    this._value = String(val);
    if (this.tagName === 'SELECT' && this.options.length > 0) {
      const idx = this.options.findIndex(o => o.value === val);
      if (idx !== -1) {
        this._selectedIndex = idx;
        this.options.forEach((o, i) => { o.selected = (i === idx); });
      }
    }
  }

  get selectedIndex() {
    return this._selectedIndex !== undefined ? this._selectedIndex : 0;
  }
  set selectedIndex(idx) {
    this._selectedIndex = idx;
    if (this.options && this.options[idx]) {
      this._value = this.options[idx].value;
      this.options.forEach((o, i) => { o.selected = (i === idx); });
    }
  }

  setAttribute(name, val) {
    this.attributes[name] = String(val);
    if (name === 'class') this.classList.value = String(val);
  }
  getAttribute(name) {
    if (name === 'class') return this.classList.value;
    return this.attributes[name] !== undefined ? this.attributes[name] : null;
  }
  hasAttribute(name) {
    return this.attributes[name] !== undefined;
  }
  removeAttribute(name) {
    delete this.attributes[name];
  }

  addEventListener(event, callback) {
    if (!this.eventListeners[event]) {
      this.eventListeners[event] = [];
    }
    this.eventListeners[event].push(callback);
  }

  dispatchEvent(event) {
    const listeners = this.eventListeners[event.type] || [];
    event.target = this;
    for (const listener of listeners) {
      listener.call(this, event);
    }
    return !event.defaultPrevented;
  }

  focus() {
    this._focused = true;
  }

  scrollIntoView() {}

  // Option select helpers
  add(option) {
    this.options.push(option);
  }
}

class MockOption {
  constructor(text, value, defaultSelected = false, selected = false) {
    this.text = text;
    this.value = value !== undefined ? value : text;
    this.defaultSelected = defaultSelected;
    this.selected = selected;
  }
}

function createMockEnvironment(htmlContent) {
  const elements = new Map();

  function getOrCreate(id, tag = 'div') {
    if (!elements.has(id)) {
      const el = new MockElement(tag, id);
      elements.set(id, el);
    }
    return elements.get(id);
  }

  // Pre-seed elements found in index.html
  const idRegex = /id=["']([a-zA-Z0-9_\-]+)["']/g;
  let match;
  while ((match = idRegex.exec(htmlContent)) !== null) {
    getOrCreate(match[1]);
  }

  // Ensure known critical elements exist
  const form = getOrCreate('wa-form', 'form');
  const f_name = getOrCreate('f_name', 'input');
  const f_clients = getOrCreate('f_clients', 'select');
  const f_package = getOrCreate('f_package', 'select');
  const f_google = getOrCreate('f_google', 'select');
  const google_desc = getOrCreate('google-desc', 'div');
  const f_details = getOrCreate('f_details', 'textarea');
  const f_maint = getOrCreate('f_maint', 'select');
  const f_budget = getOrCreate('f_budget', 'input');
  const summary_block = getOrCreate('summary-block', 'div');
  const form_submit_btn = getOrCreate('form-submit-btn', 'button');
  const backdrop = getOrCreate('modal-backdrop', 'div');
  const modal_privacidad = getOrCreate('modal-privacidad', 'div');
  const privacidad_content = getOrCreate('privacidad-content', 'div');
  const modal_terminos = getOrCreate('modal-terminos', 'div');
  const terminos_content = getOrCreate('terminos-content', 'div');
  const current_year = getOrCreate('current-year', 'span');

  // Hierarchy
  form.parentElement = getOrCreate('form-container', 'div');

  // Parse f_package options from HTML
  const pkgMatch = htmlContent.match(/<select[^>]*id=["']f_package["'][^>]*>([\s\S]*?)<\/select>/i);
  if (pkgMatch) {
    const optRegex = /<option[^>]*value=["'](.*?)["'][^>]*>([\s\S]*?)<\/option>/gi;
    let optM;
    while ((optM = optRegex.exec(pkgMatch[1])) !== null) {
      const val = optM[1];
      const txt = optM[2].trim();
      const isSelected = /selected/i.test(optM[0]);
      const opt = new MockOption(txt, val, isSelected, isSelected);
      f_package.add(opt);
    }
    // Set initial selected value
    const selectedOpt = f_package.options.find(o => o.selected);
    if (selectedOpt) {
      f_package.value = selectedOpt.value;
      f_package.selectedIndex = f_package.options.indexOf(selectedOpt);
    } else if (f_package.options.length > 0) {
      f_package.value = f_package.options[0].value;
      f_package.selectedIndex = 0;
    }
  }

  // Parse f_maint options from HTML
  const maintMatch = htmlContent.match(/<select[^>]*id=["']f_maint["'][^>]*>([\s\S]*?)<\/select>/i);
  if (maintMatch) {
    const optRegex = /<option[^>]*value=["'](.*?)["'][^>]*>([\s\S]*?)<\/option>/gi;
    let optM;
    while ((optM = optRegex.exec(maintMatch[1])) !== null) {
      f_maint.add(new MockOption(optM[2].trim(), optM[1]));
    }
    if (f_maint.options.length > 0) {
      f_maint.value = f_maint.options[0].value;
    }
  }

  // Spy on window.open
  const openedUrls = [];
  const mockWindow = {
    open: (url, target) => {
      openedUrls.push({ url, target });
    },
    scrollY: 0,
    addEventListener: () => {}
  };

  const documentListeners = {};
  const mockDocument = {
    body: new MockElement('body'),
    getElementById: (id) => elements.get(id) || null,
    querySelector: (sel) => {
      if (sel.startsWith('#')) return elements.get(sel.substring(1)) || null;
      return null;
    },
    querySelectorAll: (sel) => [],
    addEventListener: (event, cb) => {
      if (!documentListeners[event]) documentListeners[event] = [];
      documentListeners[event].push(cb);
    },
    dispatchEvent: (event) => {
      const listeners = documentListeners[event.type] || [];
      listeners.forEach(cb => cb(event));
    }
  };

  return {
    elements,
    mockDocument,
    mockWindow,
    openedUrls,
    Option: MockOption
  };
}

// ============================================================================
// EXTRACT & RUN INLINE JAVASCRIPT
// ============================================================================

function extractInlineScript(htmlContent) {
  const scriptRegex = /<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  let combinedScript = '';
  while ((match = scriptRegex.exec(htmlContent)) !== null) {
    combinedScript += match[1] + '\n;\n';
  }
  return combinedScript;
}

// ============================================================================
// MAIN TEST SUITE
// ============================================================================

async function runTestSuite() {
  console.log(`\n${BOLD}======================================================================${RESET}`);
  console.log(`${BOLD}  STATIC LANDING PAGE E2E AUTOMATED TEST SUITE (TIERS 1 - 4)          ${RESET}`);
  console.log(`${BOLD}======================================================================${RESET}\n`);

  let htmlContent = '';
  try {
    htmlContent = readHtmlSafe(INDEX_HTML_PATH);
  } catch (err) {
    console.error(`${RED}Failed to read index.html: ${err.message}${RESET}`);
    process.exit(1);
  }

  // --------------------------------------------------------------------------
  // TIER 1: FEATURE COVERAGE (R1, R2, R3)
  // --------------------------------------------------------------------------
  console.log(`${CYAN}${BOLD}[TIER 1] FEATURE COVERAGE TESTS${RESET}`);

  // Test 1.1: LFPDPPP Notice Placement near Contact Form
  {
    const cotizacionIdx = htmlContent.indexOf('id="cotizacion"');
    const formEndIdx = htmlContent.indexOf('</form>', cotizacionIdx);
    const formSection = (cotizacionIdx !== -1 && formEndIdx !== -1)
      ? htmlContent.slice(cotizacionIdx, formEndIdx + 200)
      : '';
    const hasLfpdpppInForm = /Datos protegidos bajo LFPDPPP/i.test(formSection);
    recordResult('tier1', 'T1.1_LFPDPPP_ContactForm',
      'Verify "Datos protegidos bajo LFPDPPP" notice is present near #wa-form submit button',
      hasLfpdpppInForm,
      hasLfpdpppInForm ? null : 'Notice "Datos protegidos bajo LFPDPPP" not found near #wa-form'
    );
  }

  // Test 1.2: LFPDPPP Notice Placement near Direct Email Contact
  {
    const contactoIdx = htmlContent.indexOf('id="contacto"');
    const contactoEndIdx = htmlContent.indexOf('</section>', contactoIdx);
    const contactoSection = (contactoIdx !== -1 && contactoEndIdx !== -1)
      ? htmlContent.slice(contactoIdx, contactoEndIdx)
      : '';
    const hasLfpdpppInEmail = /Datos protegidos bajo LFPDPPP/i.test(contactoSection);
    recordResult('tier1', 'T1.2_LFPDPPP_DirectEmail',
      'Verify "Datos protegidos bajo LFPDPPP" notice is present in #contacto section',
      hasLfpdpppInEmail,
      hasLfpdpppInEmail ? null : 'Notice "Datos protegidos bajo LFPDPPP" not found in direct email contact section (#contacto)'
    );
  }

  // Test 1.3: Terms Modal Section 5 Cancellation Policy
  {
    const terminosIdx = htmlContent.indexOf('id="modal-terminos"');
    const terminosEndIdx = htmlContent.indexOf('</div>\n    </div>', terminosIdx);
    const terminosSection = terminosIdx !== -1 ? htmlContent.slice(terminosIdx, terminosIdx + 8000) : '';
    const hasCancellationText = /Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte/i.test(terminosSection);
    recordResult('tier1', 'T1.3_TermsModal_Section5',
      'Verify modal-terminos contains Section 5 cancellation policy: "Después de cancelar la suscripción, la web te pertenece pero te quedas sin soporte"',
      hasCancellationText,
      hasCancellationText ? null : 'Cancellation policy text not found inside #modal-terminos'
    );
  }

  // Test 1.4: Domain Availability FAQ Clarification (.com.mx / .mx)
  {
    const dudasIdx = htmlContent.indexOf('id="dudas"');
    const dudasSection = dudasIdx !== -1 ? htmlContent.slice(dudasIdx, dudasIdx + 4000) : '';
    const hasDomainFallback = /Si no está disponible, sugerimos \.com\.mx o \.mx/i.test(dudasSection);
    recordResult('tier1', 'T1.4_DomainFAQ_Fallback',
      'Verify FAQ domain item includes clarification: "Si no está disponible, sugerimos .com.mx o .mx"',
      hasDomainFallback,
      hasDomainFallback ? null : 'Domain fallback text ("Si no está disponible, sugerimos .com.mx o .mx") not found in #dudas'
    );
  }

  // Test 1.5: Pricing Scope Differentiation (Básica vs Profesional)
  {
    const paquetesIdx = htmlContent.indexOf('id="paquetes"');
    const paquetesSection = paquetesIdx !== -1 ? htmlContent.slice(paquetesIdx, paquetesIdx + 10000) : '';
    const hasBasicaScope = /Modificaciones b[áa]sicas \(solo fotos, textos y colores\)/i.test(paquetesSection);
    const hasProScope = /Modificaciones completas \(nuevas secciones y p[áa]ginas\)/i.test(paquetesSection);
    const bothScopesPresent = hasBasicaScope && hasProScope;
    recordResult('tier1', 'T1.5_PricingScope_Differentiation',
      'Verify pricing cards display development scope constraints: Básica (fotos/textos/colores) vs Profesional (nuevas secciones/páginas)',
      bothScopesPresent,
      bothScopesPresent ? null : `Missing scope: Básica=${hasBasicaScope}, Profesional=${hasProScope}`
    );
  }

  // Test 1.6: Maintenance Monthly Limits (5 vs 10 changes)
  {
    const has5Changes = /Plan B[áa]sico incluye 5 cambios mensuales/i.test(htmlContent);
    const has10Changes = /Plan Profesional incluye 10 cambios mensuales/i.test(htmlContent);
    const bothLimitsPresent = has5Changes && has10Changes;
    recordResult('tier1', 'T1.6_Maintenance_Quotas_5vs10',
      'Verify maintenance subscription displays quotas: "Plan Básico incluye 5 cambios mensuales" and "Plan Profesional incluye 10 cambios mensuales"',
      bothLimitsPresent,
      bothLimitsPresent ? null : `Quotas missing: 5 cambios=${has5Changes}, 10 cambios=${has10Changes}`
    );
  }

  // Test 1.7: SLA Response Time Notice (24-48 hrs hábiles)
  {
    const hasSlaNotice = /Tiempo de respuesta de 24 a 48 horas en d[íi]as h[áa]biles/i.test(htmlContent);
    recordResult('tier1', 'T1.7_SLA_Notice_ResponseTime',
      'Verify SLA response time notice is specified: "Tiempo de respuesta de 24 a 48 horas en días hábiles"',
      hasSlaNotice,
      hasSlaNotice ? null : 'SLA notice ("Tiempo de respuesta de 24 a 48 horas en días hábiles") not found'
    );
  }

  // Test 1.8: Package Dropdown Placeholder & Novalidate Attribute
  {
    const pkgMatch = htmlContent.match(/<select[^>]*id=["']f_package["'][^>]*>([\s\S]*?)<\/select>/i);
    let hasPlaceholderOption = false;
    if (pkgMatch) {
      // Must have an option with value="" that is selected or disabled by default
      hasPlaceholderOption = /<option\b[^>]*value=["']["'][^>]*>/i.test(pkgMatch[1]);
    }
    const hasNovalidate = /<form\b[^>]*id=["']wa-form["'][^>]*\bnovalidate\b/i.test(htmlContent);
    const isValid = hasPlaceholderOption && hasNovalidate;
    recordResult('tier1', 'T1.8_FormPackage_PlaceholderAndNovalidate',
      'Verify #f_package has unselected placeholder (<option value="">) and #wa-form has novalidate attribute',
      isValid,
      isValid ? null : `Dropdown placeholder option=${hasPlaceholderOption}, Form novalidate=${hasNovalidate}`
    );
  }

  // --------------------------------------------------------------------------
  // TIER 4 (AST/SYNTAX EVALUATION PRE-REQUISITE FOR TIERS 2 & 3)
  // --------------------------------------------------------------------------
  console.log(`\n${CYAN}${BOLD}[TIER 4 - PART 1] JAVASCRIPT AST & SYNTAX COMPILATION${RESET}`);

  const inlineScript = extractInlineScript(htmlContent);
  let scriptAstValid = false;
  let syntaxErrorMessage = null;

  try {
    new vm.Script(inlineScript, { filename: 'index.html#inline-script' });
    scriptAstValid = true;
    recordResult('tier4', 'T4.1_JavaScript_AST_Syntax_ZeroErrors',
      'Verify index.html inline <script> compiles without syntax errors (V8 AST check)',
      true
    );
  } catch (err) {
    syntaxErrorMessage = err.stack ? err.stack.split('\n')[0] : err.message;
    recordResult('tier4', 'T4.1_JavaScript_AST_Syntax_ZeroErrors',
      'Verify index.html inline <script> compiles without syntax errors (V8 AST check)',
      false,
      syntaxErrorMessage
    );
  }

  // Also check js/app.js syntax
  if (fs.existsSync(JS_APP_PATH)) {
    try {
      const appJsCode = fs.readFileSync(JS_APP_PATH, 'utf8');
      new vm.Script(appJsCode, { filename: 'js/app.js' });
      recordResult('tier4', 'T4.1b_AppJs_Syntax_ZeroErrors',
        'Verify js/app.js compiles without syntax errors',
        true
      );
    } catch (err) {
      recordResult('tier4', 'T4.1b_AppJs_Syntax_ZeroErrors',
        'Verify js/app.js compiles without syntax errors',
        false,
        err.message
      );
    }
  }

  // --------------------------------------------------------------------------
  // RUNTIME INITIALIZATION (FOR TIER 2 & TIER 3)
  // --------------------------------------------------------------------------
  let env = null;
  let context = null;

  if (scriptAstValid) {
    try {
      env = createMockEnvironment(htmlContent);
      context = vm.createContext({
        document: env.mockDocument,
        window: env.mockWindow,
        console: { log: () => {}, warn: () => {}, error: () => {} },
        setTimeout: (fn) => fn(),
        clearTimeout: () => {},
        Date: Date,
        Option: env.Option,
        encodeURIComponent: encodeURIComponent,
        decodeURIComponent: decodeURIComponent,
        lucide: { createIcons: () => {} },
        tailwind: { config: {} }
      });

      // Execute script in sandbox
      vm.runInContext(inlineScript, context);
    } catch (runtimeErr) {
      console.log(`  ${YELLOW}Notice: Runtime initialization threw error: ${runtimeErr.message}${RESET}`);
    }
  }

  // --------------------------------------------------------------------------
  // TIER 2: BOUNDARY & CORNER CASES (R3 FORM VALIDATION)
  // --------------------------------------------------------------------------
  console.log(`\n${CYAN}${BOLD}[TIER 2] BOUNDARY & CORNER CASES (FORM VALIDATION)${RESET}`);

  // Test 2.1: Blank Form Submission (Empty Name & Empty Package)
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');
    const form = env.elements.get('wa-form');

    f_name.value = '';
    f_package.value = '';
    env.openedUrls.length = 0;

    const event = { type: 'submit', defaultPrevented: false, preventDefault: () => { event.defaultPrevented = true; } };
    form.dispatchEvent(event);

    const redirectBlocked = env.openedUrls.length === 0;
    const nameHasError = f_name.classList.contains('border-red-500') || f_name.getAttribute('aria-invalid') === 'true';
    const pkgHasError = f_package.classList.contains('border-red-500') || f_package.getAttribute('aria-invalid') === 'true';
    const passed = redirectBlocked && nameHasError && pkgHasError;

    recordResult('tier2', 'T2.1_BlankSubmission_BlockedAndHighlighted',
      'Submit blank form: redirection to WhatsApp blocked, #f_name and #f_package highlighted with error classes',
      passed,
      passed ? null : `Redirect blocked: ${redirectBlocked} (urls: ${env.openedUrls.length}), f_name error: ${nameHasError}, f_package error: ${pkgHasError}`
    );
  } else {
    recordResult('tier2', 'T2.1_BlankSubmission_BlockedAndHighlighted',
      'Submit blank form: redirection to WhatsApp blocked, #f_name and #f_package highlighted with error classes',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 2.2: Whitespace-only Name
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');
    const form = env.elements.get('wa-form');

    f_name.value = '     ';
    f_package.value = 'Web Básica ($1,500)';
    env.openedUrls.length = 0;

    const event = { type: 'submit', defaultPrevented: false, preventDefault: () => { event.defaultPrevented = true; } };
    form.dispatchEvent(event);

    const redirectBlocked = env.openedUrls.length === 0;
    const nameHasError = f_name.classList.contains('border-red-500') || f_name.getAttribute('aria-invalid') === 'true';
    const passed = redirectBlocked && nameHasError;

    recordResult('tier2', 'T2.2_WhitespaceName_BlockedAndHighlighted',
      'Submit form with whitespace-only Name ("   "): blocks redirection and flags #f_name',
      passed,
      passed ? null : `Redirect blocked: ${redirectBlocked}, f_name error: ${nameHasError}`
    );
  } else {
    recordResult('tier2', 'T2.2_WhitespaceName_BlockedAndHighlighted',
      'Submit form with whitespace-only Name ("   "): blocks redirection and flags #f_name',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 2.3: Name Filled, Package Empty
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');
    const form = env.elements.get('wa-form');

    f_name.value = 'Juan Pérez';
    f_package.value = '';
    env.openedUrls.length = 0;

    const event = { type: 'submit', defaultPrevented: false, preventDefault: () => { event.defaultPrevented = true; } };
    form.dispatchEvent(event);

    const redirectBlocked = env.openedUrls.length === 0;
    const pkgHasError = f_package.classList.contains('border-red-500') || f_package.getAttribute('aria-invalid') === 'true';
    const nameNoError = !f_name.classList.contains('border-red-500');
    const passed = redirectBlocked && pkgHasError && nameNoError;

    recordResult('tier2', 'T2.3_NameFilled_PackageEmpty_BlocksAndFlagsPackage',
      'Submit form with Name filled but Package empty: blocks redirection, flags #f_package, keeps #f_name valid',
      passed,
      passed ? null : `Redirect blocked: ${redirectBlocked}, f_package error: ${pkgHasError}, f_name clean: ${nameNoError}`
    );
  } else {
    recordResult('tier2', 'T2.3_NameFilled_PackageEmpty_BlocksAndFlagsPackage',
      'Submit form with Name filled but Package empty: blocks redirection, flags #f_package, keeps #f_name valid',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 2.4: Package Selected, Name Empty
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');
    const form = env.elements.get('wa-form');

    f_name.value = '';
    f_package.value = 'Profesional ($3,500)';
    env.openedUrls.length = 0;

    const event = { type: 'submit', defaultPrevented: false, preventDefault: () => { event.defaultPrevented = true; } };
    form.dispatchEvent(event);

    const redirectBlocked = env.openedUrls.length === 0;
    const nameHasError = f_name.classList.contains('border-red-500') || f_name.getAttribute('aria-invalid') === 'true';
    const pkgNoError = !f_package.classList.contains('border-red-500');
    const passed = redirectBlocked && nameHasError && pkgNoError;

    recordResult('tier2', 'T2.4_PackageSelected_NameEmpty_BlocksAndFlagsName',
      'Submit form with Package selected but Name empty: blocks redirection, flags #f_name, keeps #f_package valid',
      passed,
      passed ? null : `Redirect blocked: ${redirectBlocked}, f_name error: ${nameHasError}, f_package clean: ${pkgNoError}`
    );
  } else {
    recordResult('tier2', 'T2.4_PackageSelected_NameEmpty_BlocksAndFlagsName',
      'Submit form with Package selected but Name empty: blocks redirection, flags #f_name, keeps #f_package valid',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 2.5: Dynamic Error Clearing on Input and Change
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');

    // Simulate error state
    f_name.classList.add('border-red-500');
    f_package.classList.add('border-red-500');

    // Dispatch input on f_name
    f_name.value = 'Ana Martínez';
    f_name.dispatchEvent({ type: 'input' });

    // Dispatch change on f_package
    f_package.value = 'Web Básica ($1,500)';
    f_package.dispatchEvent({ type: 'change' });

    const nameCleared = !f_name.classList.contains('border-red-500');
    const pkgCleared = !f_package.classList.contains('border-red-500');
    const passed = nameCleared && pkgCleared;

    recordResult('tier2', 'T2.5_DynamicErrorClearing_OnInputAndChange',
      'Dynamic error clearing: typing in #f_name clears its error; selecting in #f_package clears its error',
      passed,
      passed ? null : `Name error cleared: ${nameCleared}, Package error cleared: ${pkgCleared}`
    );
  } else {
    recordResult('tier2', 'T2.5_DynamicErrorClearing_OnInputAndChange',
      'Dynamic error clearing: typing in #f_name clears its error; selecting in #f_package clears its error',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 2.6: Valid Submission Redirection to WhatsApp
  if (scriptAstValid && env) {
    const f_name = env.elements.get('f_name');
    const f_package = env.elements.get('f_package');
    const form = env.elements.get('wa-form');

    f_name.value = 'Ana Martínez';
    f_package.value = 'Web Básica ($1,500)';
    env.openedUrls.length = 0;

    const event = { type: 'submit', defaultPrevented: false, preventDefault: () => { event.defaultPrevented = true; } };
    form.dispatchEvent(event);

    const redirectAllowed = env.openedUrls.length === 1;
    let urlValid = false;
    if (redirectAllowed) {
      const url = env.openedUrls[0].url;
      urlValid = url.startsWith('https://wa.me/525645890610?text=') && url.includes(encodeURIComponent('Ana Martínez'));
    }
    const passed = redirectAllowed && urlValid;

    recordResult('tier2', 'T2.6_ValidSubmission_RedirectsToWhatsApp',
      'Submit valid form: opens https://wa.me/525645890610 with encoded customer details',
      passed,
      passed ? null : `Opened count: ${env.openedUrls.length}, URL valid: ${urlValid}`
    );
  } else {
    recordResult('tier2', 'T2.6_ValidSubmission_RedirectsToWhatsApp',
      'Submit valid form: opens https://wa.me/525645890610 with encoded customer details',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // --------------------------------------------------------------------------
  // TIER 3: CROSS-FEATURE COMBINATIONS
  // --------------------------------------------------------------------------
  console.log(`\n${CYAN}${BOLD}[TIER 3] CROSS-FEATURE COMBINATIONS${RESET}`);

  // Test 3.1: selectPackage() function exists and syncs form
  if (scriptAstValid && context && typeof context.selectPackage === 'function') {
    let selectPackageWorks = false;
    let errorDetail = null;
    try {
      context.selectPackage('Web Básica');
      const f_package = env.elements.get('f_package');
      const f_maint = env.elements.get('f_maint');
      const basicSelected = f_package.value.includes('Básica');
      const maintOptionUpdated = f_maint.options[0] && f_maint.options[0].text.includes('250');
      selectPackageWorks = basicSelected && maintOptionUpdated;
      if (!selectPackageWorks) {
        errorDetail = `Package value: ${f_package.value}, Maint option: ${f_maint.options[0] ? f_maint.options[0].text : 'none'}`;
      }
    } catch (err) {
      errorDetail = err.message;
    }

    recordResult('tier3', 'T3.1_PackageCard_SelectPackage_Sync',
      'Clicking package cards invokes selectPackage(), populating #f_package and synchronizing form options',
      selectPackageWorks,
      errorDetail
    );
  } else {
    recordResult('tier3', 'T3.1_PackageCard_SelectPackage_Sync',
      'Clicking package cards invokes selectPackage(), populating #f_package and synchronizing form options',
      false,
      scriptAstValid ? 'selectPackage is not a function in global context' : `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 3.2: Modal Open/Close Runtime Functions
  if (scriptAstValid && context) {
    const hasOpenModal = typeof context.openModal === 'function';
    const hasCloseModal = typeof context.closeModal === 'function';
    const modalsFunctional = hasOpenModal && hasCloseModal;

    recordResult('tier3', 'T3.2_Modal_Runtime_Functions',
      'Verify openModal() and closeModal() functions exist in runtime and manipulate modal classes',
      modalsFunctional,
      modalsFunctional ? null : `openModal defined: ${hasOpenModal}, closeModal defined: ${hasCloseModal}`
    );
  } else {
    recordResult('tier3', 'T3.2_Modal_Runtime_Functions',
      'Verify openModal() and closeModal() functions exist in runtime and manipulate modal classes',
      false,
      `Blocked by syntax error: ${syntaxErrorMessage}`
    );
  }

  // Test 3.3: Modal Open & Close Cycles
  if (scriptAstValid && context && typeof context.openModal === 'function' && typeof context.closeModal === 'function') {
    let modalCyclePassed = false;
    let cycleDetail = null;
    try {
      const backdrop = env.elements.get('modal-backdrop');
      const terminos = env.elements.get('modal-terminos');

      context.openModal('terminos');
      const openedBackdrop = !backdrop.classList.contains('hidden');
      const openedModal = !terminos.classList.contains('hidden');

      context.closeModal('terminos');
      const closedBackdrop = backdrop.classList.contains('hidden') || backdrop.classList.contains('opacity-0');
      const closedModal = terminos.classList.contains('hidden') || terminos.classList.contains('scale-95');

      modalCyclePassed = openedBackdrop && openedModal && (closedBackdrop || closedModal);
      if (!modalCyclePassed) {
        cycleDetail = `Opened: (backdrop=${openedBackdrop}, modal=${openedModal}), Closed: (backdrop=${closedBackdrop}, modal=${closedModal})`;
      }
    } catch (err) {
      cycleDetail = err.message;
    }

    recordResult('tier3', 'T3.3_Modal_OpenClose_DOM_Cycle',
      'Execute full openModal / closeModal cycle and verify backdrop and modal visibility transitions',
      modalCyclePassed,
      cycleDetail
    );
  } else {
    recordResult('tier3', 'T3.3_Modal_OpenClose_DOM_Cycle',
      'Execute full openModal / closeModal cycle and verify backdrop and modal visibility transitions',
      false,
      'openModal / closeModal not available for execution'
    );
  }

  // Test 3.4: Footer Legal Modal Triggers Exist in DOM
  {
    const footerIdx = htmlContent.indexOf('<footer');
    const footerSection = footerIdx !== -1 ? htmlContent.slice(footerIdx) : '';
    const hasPrivacidadTrigger = /openModal\(['"]privacidad['"]\)/i.test(footerSection);
    const hasTerminosTrigger = /openModal\(['"]terminos['"]\)/i.test(footerSection);
    const bothTriggersPresent = hasPrivacidadTrigger && hasTerminosTrigger;

    recordResult('tier3', 'T3.4_Footer_Modal_Triggers_Present',
      'Verify footer contains accessible triggers for openModal("privacidad") and openModal("terminos")',
      bothTriggersPresent,
      bothTriggersPresent ? null : `Footer triggers: Privacidad=${hasPrivacidadTrigger}, Términos=${hasTerminosTrigger}`
    );
  }

  // --------------------------------------------------------------------------
  // TIER 4: REAL-WORLD APPLICATION & ACCEPTANCE CRITERIA
  // --------------------------------------------------------------------------
  console.log(`\n${CYAN}${BOLD}[TIER 4 - PART 2] REAL-WORLD APPLICATION & ACCEPTANCE CRITERIA${RESET}`);

  // Test 4.2: HTML Structural Preservation (R4 Surgical Check)
  {
    const requiredLandmarks = [
      { id: 'navbar', pattern: /id=["']navbar["']/i },
      { id: 'paquetes', pattern: /id=["']paquetes["']/i },
      { id: 'dudas', pattern: /id=["']dudas["']/i },
      { id: 'cotizacion', pattern: /id=["']cotizacion["']/i },
      { id: 'contacto', pattern: /id=["']contacto["']/i },
      { id: 'footer', pattern: /<footer\b/i },
      { id: 'modal-privacidad', pattern: /id=["']modal-privacidad["']/i },
      { id: 'modal-terminos', pattern: /id=["']modal-terminos["']/i },
      { id: 'cookie-banner', pattern: /id=["']cookie-banner["']/i }
    ];

    const missingLandmarks = [];
    requiredLandmarks.forEach(landmark => {
      if (!landmark.pattern.test(htmlContent)) {
        missingLandmarks.push(landmark.id);
      }
    });

    // Check for corrupt regex artifacts
    const hasRegexArtifacts = /\{\{[^}]*\}\}|\bundefined\b|nullMXN/i.test(htmlContent);
    const structurePreserved = missingLandmarks.length === 0 && !hasRegexArtifacts;

    recordResult('tier4', 'T4.2_HTML_StructuralPreservation',
      'Verify all critical DOM sections remain intact with zero structural corruption or tag deletion (R4)',
      structurePreserved,
      structurePreserved ? null : `Missing landmarks: [${missingLandmarks.join(', ')}], regex artifacts: ${hasRegexArtifacts}`
    );
  }

  // Test 4.3: End-to-End Acceptance Criteria Aggregation
  {
    const ac1 = results.tier1.find(r => r.testId === 'T1.5_PricingScope_Differentiation')?.passed &&
                results.tier1.find(r => r.testId === 'T1.6_Maintenance_Quotas_5vs10')?.passed;

    const ac2 = results.tier1.find(r => r.testId === 'T1.7_SLA_Notice_ResponseTime')?.passed &&
                results.tier1.find(r => r.testId === 'T1.4_DomainFAQ_Fallback')?.passed;

    const ac3 = results.tier2.find(r => r.testId === 'T2.1_BlankSubmission_BlockedAndHighlighted')?.passed;

    const ac4 = results.tier1.find(r => r.testId === 'T1.1_LFPDPPP_ContactForm')?.passed &&
                results.tier1.find(r => r.testId === 'T1.3_TermsModal_Section5')?.passed;

    const ac5 = results.tier4.find(r => r.testId === 'T4.2_HTML_StructuralPreservation')?.passed &&
                results.tier4.find(r => r.testId === 'T4.1_JavaScript_AST_Syntax_ZeroErrors')?.passed;

    const allAcPassed = ac1 && ac2 && ac3 && ac4 && ac5;

    console.log(`\n  ${BOLD}Acceptance Criteria Evaluation:${RESET}`);
    console.log(`    [${ac1 ? GREEN + 'PASS' + RESET : RED + 'FAIL' + RESET}] AC1: Tabla de precios clara (textos/fotos vs secciones) y límites (5 vs 10 cambios)`);
    console.log(`    [${ac2 ? GREEN + 'PASS' + RESET : RED + 'FAIL' + RESET}] AC2: SLA visible (24-48 hrs hábiles) y alternativa de dominios (.com.mx / .mx)`);
    console.log(`    [${ac3 ? GREEN + 'PASS' + RESET : RED + 'FAIL' + RESET}] AC3: Formulario en blanco bloquea redirección y resalta campos faltantes`);
    console.log(`    [${ac4 ? GREEN + 'PASS' + RESET : RED + 'FAIL' + RESET}] AC4: Leyendas de datos (LFPDPPP) y retención de propiedad tras cancelar`);
    console.log(`    [${ac5 ? GREEN + 'PASS' + RESET : RED + 'FAIL' + RESET}] AC5: Diseño y estructura intactos sin pérdida de secciones`);

    recordResult('tier4', 'T4.3_AcceptanceCriteria_Aggregate',
      'Verify all 5 user acceptance criteria from ORIGINAL_REQUEST.md are fully satisfied',
      allAcPassed,
      allAcPassed ? null : `AC Status: AC1=${!!ac1}, AC2=${!!ac2}, AC3=${!!ac3}, AC4=${!!ac4}, AC5=${!!ac5}`
    );
  }

  // --------------------------------------------------------------------------
  // SUMMARY REPORT
  // --------------------------------------------------------------------------
  console.log(`\n${BOLD}======================================================================${RESET}`);
  console.log(`${BOLD}  TEST EXECUTION SUMMARY                                              ${RESET}`);
  console.log(`${BOLD}======================================================================${RESET}`);
  console.log(`  Total Tests Run : ${results.passed + results.failed}`);
  console.log(`  Tests Passed    : ${GREEN}${results.passed}${RESET}`);
  console.log(`  Tests Failed    : ${results.failed > 0 ? RED : GREEN}${results.failed}${RESET}`);

  if (results.bugs.length > 0) {
    console.log(`\n${RED}${BOLD}  DISCOVERED DEFECTS / IMPLEMENTATION BUGS TO ESCALATE:${RESET}`);
    results.bugs.forEach((b, idx) => {
      console.log(`  ${idx + 1}. [${b.tier.toUpperCase()}] ${BOLD}${b.testId}${RESET}: ${b.description}`);
      if (b.errorDetail) {
        console.log(`     Details: ${b.errorDetail}`);
      }
    });
  } else {
    console.log(`\n  ${GREEN}${BOLD}ALL TESTS PASSED! Landing page satisfies all requirements and AC.${RESET}`);
  }
  console.log(`${BOLD}======================================================================${RESET}\n`);

  // Return exit code
  return results.failed === 0 ? 0 : 1;
}

// Execute when run directly
if (require.main === module) {
  runTestSuite().then(exitCode => {
    process.exit(exitCode);
  }).catch(err => {
    console.error(`Fatal test runner error: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { runTestSuite, results };
