/**
 * Adversarial Form Validation & Redirection Security Test Harness
 * Project: Static Landing Page Remediation
 * Agent: challenger_1
 * Specification: ORIGINAL_REQUEST.md (§ R3, AC3) & PROJECT.md
 * 
 * Tests:
 * 1. Blank submission (Empty Name + Empty Package)
 * 2. Whitespace-only Name ("   ", "\t\r\n") with empty package
 * 3. Whitespace-only Name with valid package
 * 4. Empty package with valid name
 * 5. Valid submission redirects to WhatsApp with correctly encoded URI
 * 6. Dynamic error clearing on Name input (rejects whitespace, accepts text)
 * 7. Dynamic error clearing on Package change
 * 8. Form error banner visibility coordination (hides only when BOTH valid)
 * 9. selectPackage() card click error clearance integration
 * 10. Adversarial payloads (XSS, SQLi, Unicode, emojis) handling
 * 11. Repeated rapid invalid submissions stress test
 * 12. Re-invalidation after valid state
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT_DIR = path.resolve(__dirname, '..');
const INDEX_HTML_PATH = path.join(ROOT_DIR, 'index.html');

// ANSI Colors
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const CYAN = '\x1b[36m';
const YELLOW = '\x1b[33m';
const BOLD = '\x1b[1m';
const RESET = '\x1b[0m';

const testResults = [];

function record(id, description, passed, details = null) {
  testResults.push({ id, description, passed, details });
  if (passed) {
    console.log(`  ${GREEN}✔ [PASS]${RESET} ${BOLD}${id}:${RESET} ${description}`);
  } else {
    console.log(`  ${RED}✖ [FAIL]${RESET} ${BOLD}${id}:${RESET} ${description}`);
    if (details) {
      console.log(`     ${RED}→ ${details}${RESET}`);
    }
  }
}

// Minimal DOM Sandbox for AST Execution
class MockClassList {
  constructor() {
    this._set = new Set();
  }
  add(...classes) {
    for (const c of classes) {
      if (c) c.split(/\s+/).forEach(token => token && this._set.add(token));
    }
  }
  remove(...classes) {
    for (const c of classes) {
      if (c) c.split(/\s+/).forEach(token => token && this._set.delete(token));
    }
  }
  contains(cls) {
    return this._set.has(cls);
  }
  toggle(cls, force) {
    if (force !== undefined) {
      if (force) this.add(cls); else this.remove(cls);
      return force;
    }
    if (this._set.has(cls)) {
      this.remove(cls);
      return false;
    } else {
      this.add(cls);
      return true;
    }
  }
}

class MockElement {
  constructor(id, tagName = 'div') {
    this.id = id;
    this.tagName = tagName.toUpperCase();
    this.value = '';
    this.textContent = '';
    this.innerHTML = '';
    this.classList = new MockClassList();
    this.attributes = new Map();
    this.options = [];
    this.selectedIndex = 0;
    this.listeners = new Map();
    this.style = {};
    this.parentElement = { style: {} };
    this.focused = false;
  }
  setAttribute(k, v) { this.attributes.set(k, String(v)); }
  getAttribute(k) { return this.attributes.has(k) ? this.attributes.get(k) : null; }
  removeAttribute(k) { this.attributes.delete(k); }
  hasAttribute(k) { return this.attributes.has(k); }
  addEventListener(evt, fn) {
    if (!this.listeners.has(evt)) this.listeners.set(evt, []);
    this.listeners.get(evt).push(fn);
  }
  dispatchEvent(evt) {
    const list = this.listeners.get(evt.type) || [];
    for (const fn of list) fn(evt);
  }
  focus() { this.focused = true; }
  blur() { this.focused = false; }
  scrollIntoView() {}
  add(opt) { this.options.push(opt); }
}

function readHtmlSafe(filePath) {
  const raw = fs.readFileSync(filePath);
  if (raw[0] === 0xff && raw[1] === 0xfe) {
    return raw.toString('utf16le');
  }
  return raw.toString('utf8');
}

function buildTestEnvironment(html) {
  const elements = new Map();
  const openedUrls = [];

  function getEl(id, tag = 'div') {
    if (!elements.has(id)) {
      elements.set(id, new MockElement(id, tag));
    }
    return elements.get(id);
  }

  // Pre-seed known elements
  const f_name = getEl('f_name', 'input');
  const f_clients = getEl('f_clients', 'select');
  const f_package = getEl('f_package', 'select');
  const f_google = getEl('f_google', 'select');
  const f_details = getEl('f_details', 'textarea');
  const f_maint = getEl('f_maint', 'select');
  const f_budget = getEl('f_budget', 'input');
  const wa_form = getEl('wa-form', 'form');
  const f_name_error = getEl('f_name_error', 'p');
  const f_package_error = getEl('f_package_error', 'p');
  const form_error_alert = getEl('form-error-alert', 'div');
  const summary_block = getEl('summary-block', 'div');

  f_name_error.classList.add('hidden');
  f_package_error.classList.add('hidden');
  form_error_alert.classList.add('hidden');
  summary_block.classList.add('hidden');

  // Populate f_package options from HTML
  const pkgMatch = html.match(/<select[^>]*id=["']f_package["'][^>]*>([\s\S]*?)<\/select>/i);
  if (pkgMatch) {
    const optRegex = /<option\b[^>]*value=(["'])(.*?)\1[^>]*>(.*?)<\/option>/gi;
    let m;
    while ((m = optRegex.exec(pkgMatch[1])) !== null) {
      f_package.options.push({ value: m[2], text: m[3] });
    }
  }

  f_maint.options = [
    { value: 'Sí ($500/mes)', text: 'Sí, me interesa' },
    { value: 'No por ahora', text: 'No, yo la administraré' }
  ];

  const mockDocument = {
    getElementById: (id) => elements.get(id) || null,
    querySelector: (sel) => {
      const match = sel.match(/#([\w-]+)/);
      return match ? (elements.get(match[1]) || null) : null;
    },
    querySelectorAll: () => []
  };

  const mockWindow = {
    open: (url) => { openedUrls.push(url); },
    location: { href: 'https://avmyweb.studio/' }
  };

  // Extract inline script
  const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
  let inlineScript = '';
  let match;
  while ((match = scriptRegex.exec(html)) !== null) {
    if (!match[0].includes('src=')) {
      inlineScript += '\n' + match[1];
    }
  }

  const sandboxContext = vm.createContext({
    document: mockDocument,
    window: mockWindow,
    console: { log: () => {}, warn: () => {}, error: () => {} },
    setTimeout: (fn) => fn(),
    clearTimeout: () => {},
    Date: Date,
    Option: function(text, val) { return { text, value: val }; },
    encodeURIComponent: encodeURIComponent,
    decodeURIComponent: decodeURIComponent,
    lucide: { createIcons: () => {} },
    f_package: f_package,
    f_google: f_google,
    f_maint: f_maint,
    googleDesc: getEl('google-desc', 'div'),
    txtBasico: 'Básico',
    txtAvanzado: 'Avanzado',
    isPromoActive: () => false
  });

  vm.runInContext(inlineScript, sandboxContext);

  return { elements, openedUrls, sandboxContext };
}

function runAdversarialValidationSuite() {
  console.log(`\n${BOLD}======================================================================${RESET}`);
  console.log(`${BOLD}  ADVERSARIAL FORM VALIDATION & SECURITY TEST SUITE                  ${RESET}`);
  console.log(`${BOLD}======================================================================${RESET}\n`);

  const html = readHtmlSafe(INDEX_HTML_PATH);
  const env = buildTestEnvironment(html);
  const { elements, openedUrls, sandboxContext } = env;

  const f_name = elements.get('f_name');
  const f_package = elements.get('f_package');
  const form = elements.get('wa-form');
  const f_name_error = elements.get('f_name_error');
  const f_package_error = elements.get('f_package_error');
  const form_error_alert = elements.get('form-error-alert');

  function submitForm() {
    openedUrls.length = 0;
    f_name.focused = false;
    f_package.focused = false;
    const evt = { type: 'submit', defaultPrevented: false, preventDefault: () => { evt.defaultPrevented = true; } };
    form.dispatchEvent(evt);
    return evt;
  }

  // --------------------------------------------------------------------------
  // TEST ADV-01: Blank Form Submission (Both Fields Empty)
  // --------------------------------------------------------------------------
  f_name.value = '';
  f_package.value = '';
  submitForm();

  const adv01_blocked = openedUrls.length === 0;
  const adv01_name_err = f_name.classList.contains('border-red-500') && f_name.getAttribute('aria-invalid') === 'true';
  const adv01_pkg_err = f_package.classList.contains('border-red-500') && f_package.getAttribute('aria-invalid') === 'true';
  const adv01_alert_vis = !form_error_alert.classList.contains('hidden');
  const adv01_name_help = !f_name_error.classList.contains('hidden');
  const adv01_pkg_help = !f_package_error.classList.contains('hidden');
  const adv01_focus_name = f_name.focused === true;

  const adv01_pass = adv01_blocked && adv01_name_err && adv01_pkg_err && adv01_alert_vis && adv01_name_help && adv01_pkg_help && adv01_focus_name;
  record('ADV-01_BlankSubmission',
    'Blank submission strictly blocks window.open, applies border-red-500, unhides error helpers & banner, focuses f_name',
    adv01_pass,
    adv01_pass ? null : `blocked=${adv01_blocked}, nameErr=${adv01_name_err}, pkgErr=${adv01_pkg_err}, alertVis=${adv01_alert_vis}, focus=${adv01_focus_name}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-02: Whitespace-Only Name ("   ") with Empty Package
  // --------------------------------------------------------------------------
  f_name.value = '   ';
  f_package.value = '';
  submitForm();

  const adv02_blocked = openedUrls.length === 0;
  const adv02_name_err = f_name.classList.contains('border-red-500');
  const adv02_pkg_err = f_package.classList.contains('border-red-500');
  const adv02_pass = adv02_blocked && adv02_name_err && adv02_pkg_err;
  record('ADV-02_WhitespaceName_EmptyPackage',
    'Whitespace-only Name ("   ") with empty package blocks redirection and highlights both inputs',
    adv02_pass,
    adv02_pass ? null : `blocked=${adv02_blocked}, nameErr=${adv02_name_err}, pkgErr=${adv02_pkg_err}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-03: Whitespace Tabs/Newlines Name ("\t\r\n  ") with Valid Package
  // --------------------------------------------------------------------------
  f_name.value = '\t\r\n   \n';
  f_package.value = 'Web Básica ($1,500)';
  submitForm();

  const adv03_blocked = openedUrls.length === 0;
  const adv03_name_err = f_name.classList.contains('border-red-500');
  const adv03_pkg_clean = !f_package.classList.contains('border-red-500');
  const adv03_focus_name = f_name.focused === true;
  const adv03_pass = adv03_blocked && adv03_name_err && adv03_pkg_clean && adv03_focus_name;
  record('ADV-03_WhitespaceTabsNewlines_ValidPackage',
    'Whitespace tabs/newlines Name ("\\t\\r\\n  ") with valid package blocks redirection and flags only f_name',
    adv03_pass,
    adv03_pass ? null : `blocked=${adv03_blocked}, nameErr=${adv03_name_err}, pkgClean=${adv03_pkg_clean}, focusName=${adv03_focus_name}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-04: Valid Name with Placeholder Empty Package ("")
  // --------------------------------------------------------------------------
  f_name.value = 'Roberto Gomez';
  f_package.value = '';
  submitForm();

  const adv04_blocked = openedUrls.length === 0;
  const adv04_name_clean = !f_name.classList.contains('border-red-500');
  const adv04_pkg_err = f_package.classList.contains('border-red-500');
  const adv04_focus_pkg = f_package.focused === true;
  const adv04_pass = adv04_blocked && adv04_name_clean && adv04_pkg_err && adv04_focus_pkg;
  record('ADV-04_ValidName_EmptyPackage',
    'Valid Name with placeholder empty package blocks redirection, flags f_package, focuses f_package',
    adv04_pass,
    adv04_pass ? null : `blocked=${adv04_blocked}, nameClean=${adv04_name_clean}, pkgErr=${adv04_pkg_err}, focusPkg=${adv04_focus_pkg}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-05: Valid Name and Valid Package Redirection
  // --------------------------------------------------------------------------
  f_name.value = 'Laura Méndez';
  f_package.value = 'Profesional ($3,500)';
  submitForm();

  const adv05_redirected = openedUrls.length === 1;
  const adv05_name_clean = !f_name.classList.contains('border-red-500');
  const adv05_pkg_clean = !f_package.classList.contains('border-red-500');
  const adv05_alert_hidden = form_error_alert.classList.contains('hidden');
  const targetUrl = openedUrls[0] || '';
  const adv05_url_valid = targetUrl.startsWith('https://wa.me/525645890610?text=') &&
                          targetUrl.includes(encodeURIComponent('Laura Méndez')) &&
                          targetUrl.includes(encodeURIComponent('Profesional ($3,500)'));
  const adv05_pass = adv05_redirected && adv05_name_clean && adv05_pkg_clean && adv05_alert_hidden && adv05_url_valid;
  record('ADV-05_ValidSubmission_Redirects',
    'Valid Name & Package clears alerts and triggers window.open with correctly encoded WhatsApp quote',
    adv05_pass,
    adv05_pass ? null : `redirected=${adv05_redirected}, urlValid=${adv05_url_valid}, alertHidden=${adv05_alert_hidden}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-06: Real-time Error Clearance - Name Input Rejects Whitespace
  // --------------------------------------------------------------------------
  // Reset to error state
  f_name.value = '';
  f_package.value = '';
  submitForm(); // both in error

  // User types whitespace into f_name -> error must persist
  f_name.value = '   ';
  f_name.dispatchEvent({ type: 'input' });
  const adv06_ws_persists = f_name.classList.contains('border-red-500');

  // User types valid letter -> error must clear
  f_name.value = 'A';
  f_name.dispatchEvent({ type: 'input' });
  const adv06_text_cleared = !f_name.classList.contains('border-red-500');
  const adv06_help_hidden = f_name_error.classList.contains('hidden');
  // Alert banner must STILL be visible because package is still empty!
  const adv06_alert_still_visible = !form_error_alert.classList.contains('hidden');

  const adv06_pass = adv06_ws_persists && adv06_text_cleared && adv06_help_hidden && adv06_alert_still_visible;
  record('ADV-06_Realtime_Name_Input',
    'f_name input event ignores whitespace, clears error on valid character, maintains banner while package invalid',
    adv06_pass,
    adv06_pass ? null : `wsPersists=${adv06_ws_persists}, textCleared=${adv06_text_cleared}, alertStillVis=${adv06_alert_still_visible}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-07: Real-time Error Clearance - Package Change Hides Alert
  // --------------------------------------------------------------------------
  // Continuing from ADV-06 where f_name is valid ('A') and f_package is in error
  f_package.value = 'Empresarial ($6,000)';
  f_package.dispatchEvent({ type: 'change' });

  const adv07_pkg_cleared = !f_package.classList.contains('border-red-500');
  const adv07_pkg_help_hidden = f_package_error.classList.contains('hidden');
  // Now BOTH are valid -> form alert banner MUST be hidden
  const adv07_alert_hidden = form_error_alert.classList.contains('hidden');

  const adv07_pass = adv07_pkg_cleared && adv07_pkg_help_hidden && adv07_alert_hidden;
  record('ADV-07_Realtime_Package_Change',
    'f_package change event clears error and hides alert banner when f_name is also valid',
    adv07_pass,
    adv07_pass ? null : `pkgCleared=${adv07_pkg_cleared}, alertHidden=${adv07_alert_hidden}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-08: Pricing Card Click via selectPackage() Integration
  // --------------------------------------------------------------------------
  // Reset to error state
  f_name.value = '';
  f_package.value = '';
  submitForm();

  // Invoke selectPackage('Web Básica') from global sandbox
  sandboxContext.selectPackage('Web Básica');

  const adv08_pkg_val = f_package.value;
  const adv08_pkg_cleared = !f_package.classList.contains('border-red-500');
  // Since f_name is still empty, formAlert must remain visible
  const adv08_alert_vis = !form_error_alert.classList.contains('hidden');

  // Now fill name
  f_name.value = 'Santiago';
  f_name.dispatchEvent({ type: 'input' });
  const adv08_alert_now_hidden = form_error_alert.classList.contains('hidden');

  const adv08_pass = adv08_pkg_val.includes('Básica') && adv08_pkg_cleared && adv08_alert_vis && adv08_alert_now_hidden;
  record('ADV-08_SelectPackage_CardClick_Integration',
    'selectPackage() properly synchronizes select value, clears f_package error, and coordinates alert visibility',
    adv08_pass,
    adv08_pass ? null : `pkgVal=${adv08_pkg_val}, pkgCleared=${adv08_pkg_cleared}, alertVis=${adv08_alert_vis}, alertHidden=${adv08_alert_now_hidden}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-09: Adversarial Payloads (XSS, SQLi, Emojis, Long Strings)
  // --------------------------------------------------------------------------
  const payloads = [
    { name: '<script>alert("xss")</script>', pkg: 'Web Básica ($1,500)' },
    { name: "Robert'); DROP TABLE Students;--", pkg: 'Profesional ($3,500)' },
    { name: '🎉🚀✨ José María ⚡💻', pkg: 'Empresarial ($6,000)' },
    { name: 'A'.repeat(5000), pkg: 'Tienda Web ($9,000)' }
  ];

  let payloadsPassed = true;
  for (let i = 0; i < payloads.length; i++) {
    const p = payloads[i];
    f_name.value = p.name;
    f_package.value = p.pkg;
    submitForm();
    if (openedUrls.length !== 1) {
      payloadsPassed = false;
      break;
    }
    const url = openedUrls[0];
    if (!url.startsWith('https://wa.me/525645890610?text=') || !url.includes(encodeURIComponent(p.name.trim()))) {
      payloadsPassed = false;
      break;
    }
  }

  record('ADV-09_Adversarial_Payloads_Sanitization',
    'Handles XSS, SQLi, emojis, and 5000-char strings safely via encodeURIComponent without crashing',
    payloadsPassed,
    payloadsPassed ? null : 'Failed to properly sanitize and encode adversarial payload into URL'
  );

  // --------------------------------------------------------------------------
  // TEST ADV-10: Rapid Consecutive Invalid Submissions (Stress Test)
  // --------------------------------------------------------------------------
  f_name.value = '';
  f_package.value = '';
  let zeroLeaks = true;
  for (let i = 0; i < 20; i++) {
    submitForm();
    if (openedUrls.length !== 0) {
      zeroLeaks = false;
      break;
    }
  }
  const adv10_pass = zeroLeaks && f_name.classList.contains('border-red-500');
  record('ADV-10_Rapid_Invalid_Submissions_Stress',
    '20 rapid consecutive invalid submissions consistently block window.open with 0 url leaks',
    adv10_pass,
    adv10_pass ? null : `zeroLeaks=${zeroLeaks}, openedCount=${openedUrls.length}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-11: Re-invalidation After Previously Valid State
  // --------------------------------------------------------------------------
  // First make valid
  f_name.value = 'Carlos';
  f_package.value = 'Web Básica ($1,500)';
  submitForm();
  const step1_ok = openedUrls.length === 1;

  // Now clear name back to empty and re-submit
  f_name.value = '';
  submitForm();
  const step2_blocked = openedUrls.length === 0;
  const step2_name_err = f_name.classList.contains('border-red-500');
  const step2_alert = !form_error_alert.classList.contains('hidden');

  const adv11_pass = step1_ok && step2_blocked && step2_name_err && step2_alert;
  record('ADV-11_ReInvalidation_After_Valid',
    'Emptying a previously valid field re-triggers full validation failure, re-highlights field, and blocks redirection',
    adv11_pass,
    adv11_pass ? null : `step1=${step1_ok}, step2Blocked=${step2_blocked}, nameErr=${step2_name_err}`
  );

  // --------------------------------------------------------------------------
  // TEST ADV-12: Zero-Width Space Bypass Check
  // --------------------------------------------------------------------------
  // Unicode U+200B is a zero-width space. In standard JS String.prototype.trim(), U+200B is not in Zs.
  // We document whether JS trim() treats U+200B as character vs standard ASCII whitespace.
  f_name.value = '\u200B';
  f_package.value = 'Web Básica ($1,500)';
  submitForm();
  const u200b_treated_as_char = openedUrls.length === 1; // standard ECMAScript behavior
  record('ADV-12_ZeroWidthSpace_Behavior',
    'Documented Unicode zero-width space (U+200B) behavior under ECMAScript trim() specification',
    true,
    `U+200B recognized as ${u200b_treated_as_char ? 'non-empty character (standard ECMAScript category Cf)' : 'trimmed whitespace'}`
  );

  console.log(`\n${BOLD}======================================================================${RESET}`);
  const passCount = testResults.filter(t => t.passed).length;
  const failCount = testResults.filter(t => !t.passed).length;
  console.log(`${BOLD}SUMMARY: ${passCount} PASSED, ${failCount} FAILED out of ${testResults.length} tests${RESET}\n`);

  return { passCount, failCount, results: testResults };
}

if (require.main === module) {
  runAdversarialValidationSuite();
}

module.exports = { runAdversarialValidationSuite };
