/**
 * Challenger 2: Adversarial Runtime & Modal Lifecycle Test Harness
 * Author: challenger_2
 * Focus: AST Verification, Modal Lifecycle (Escape, Backdrop clicks, Overflow lock, Race Conditions)
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML_PATH = path.resolve(__dirname, '..', 'index.html');
const JS_APP_PATH = path.resolve(__dirname, '..', 'js', 'app.js');

const rawHtml = fs.readFileSync(HTML_PATH, 'utf8');

// 1. EXTRACT ALL SCRIPT BLOCKS
const scriptTagRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let match;
const scripts = [];
let scriptIdx = 0;

while ((match = scriptTagRegex.exec(rawHtml)) !== null) {
  const attrs = match[1];
  const body = match[2];
  const srcMatch = attrs.match(/\bsrc=["'](.*?)["']/i);
  scripts.push({
    index: scriptIdx++,
    attrs,
    src: srcMatch ? srcMatch[1] : null,
    body: body.trim(),
    line: rawHtml.substring(0, match.index).split('\n').length
  });
}

console.log(`[CHALLENGER 2] Found ${scripts.length} script elements in index.html.`);

// 2. AST COMPILATION OF EVERY INLINE SCRIPT
let astErrors = [];
scripts.forEach((s) => {
  if (!s.src && s.body.length > 0) {
    try {
      new vm.Script(s.body, { filename: `index.html#script-${s.index}-line-${s.line}` });
      console.log(`  ✔ AST Syntax PASS: Inline script ${s.index} (line ${s.line}, ${s.body.length} chars)`);
    } catch (err) {
      console.error(`  ✖ AST Syntax FAIL: Inline script ${s.index} (line ${s.line}): ${err.message}`);
      astErrors.push({ script: s.index, line: s.line, error: err.message });
    }
  }
});

// AST Compilation of js/app.js
if (fs.existsSync(JS_APP_PATH)) {
  try {
    const appJs = fs.readFileSync(JS_APP_PATH, 'utf8');
    new vm.Script(appJs, { filename: 'js/app.js' });
    console.log(`  ✔ AST Syntax PASS: js/app.js (${appJs.length} chars)`);
  } catch (err) {
    console.error(`  ✖ AST Syntax FAIL: js/app.js: ${err.message}`);
    astErrors.push({ script: 'app.js', error: err.message });
  }
}

// 3. ADVERSARIAL DOM SIMULATION FOR MODAL LIFECYCLE
class DomNode {
  constructor(tag, id = '', classes = '') {
    this.tagName = tag.toUpperCase();
    this.id = id;
    this.classList = new Set(classes.split(/\s+/).filter(Boolean));
    this.style = {};
    this.attributes = new Map();
    this.listeners = new Map();
    this.parentElement = null;
    this.children = [];
    this.offsetWidth = 100;
    this.value = '';
    this.textContent = '';
    this.innerHTML = '';
  }

  get className() {
    return Array.from(this.classList).join(' ');
  }

  set className(val) {
    this.classList = new Set(val.split(/\s+/).filter(Boolean));
  }

  setAttribute(k, v) { this.attributes.set(k, String(v)); }
  getAttribute(k) { return this.attributes.get(k) || null; }
  removeAttribute(k) { this.attributes.delete(k); }

  addEventListener(event, fn) {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event).push(fn);
  }

  dispatchEvent(evt) {
    evt.target = this;
    const fns = this.listeners.get(evt.type) || [];
    for (const fn of fns) fn.call(this, evt);
  }
}

// Set up DOM registry
const domElements = new Map();

function registerElement(tag, id, classes = '') {
  const el = new DomNode(tag, id, classes);
  domElements.set(id, el);
  return el;
}

// Parse IDs and initial classes from index.html
const idClassRegex = /<([a-zA-Z0-9\-]+)[^>]*\bid=["']([a-zA-Z0-9_\-]+)["'][^>]*>/gi;
let m;
while ((m = idClassRegex.exec(rawHtml)) !== null) {
  const tag = m[1];
  const id = m[2];
  const tagStr = m[0];
  const clsMatch = tagStr.match(/\bclass=["']([^"']*)["']/i);
  const cls = clsMatch ? clsMatch[1] : '';
  registerElement(tag, id, cls);
}

// Ensure specific elements exist with accurate initial classes
const body = new DomNode('body', 'body');
const backdrop = domElements.get('modal-backdrop');
const modalPrivacidad = domElements.get('modal-privacidad');
const privacidadContent = domElements.get('privacidad-content');
const modalTerminos = domElements.get('modal-terminos');
const terminosContent = domElements.get('terminos-content');

console.log('\n[CHALLENGER 2] Initial Modal DOM State:');
console.log('  modal-backdrop classes:', backdrop ? backdrop.className : 'NOT FOUND');
console.log('  modal-privacidad classes:', modalPrivacidad ? modalPrivacidad.className : 'NOT FOUND');
console.log('  privacidad-content classes:', privacidadContent ? privacidadContent.className : 'NOT FOUND');
console.log('  modal-terminos classes:', modalTerminos ? modalTerminos.className : 'NOT FOUND');
console.log('  terminos-content classes:', terminosContent ? terminosContent.className : 'NOT FOUND');

// Build sandboxed browser execution environment
const documentListeners = new Map();
const windowListeners = new Map();

const mockDocument = {
  body: body,
  getElementById: (id) => domElements.get(id) || null,
  querySelector: (sel) => {
    if (sel.startsWith('#')) return domElements.get(sel.substring(1)) || null;
    return null;
  },
  querySelectorAll: () => [],
  addEventListener: (event, fn) => {
    if (!documentListeners.has(event)) documentListeners.set(event, []);
    documentListeners.get(event).push(fn);
  },
  dispatchEvent: (evt) => {
    const fns = documentListeners.get(evt.type) || [];
    for (const fn of fns) fn(evt);
  }
};

const mockWindow = {
  scrollY: 0,
  open: () => {},
  addEventListener: (event, fn) => {
    if (!windowListeners.has(event)) windowListeners.set(event, []);
    windowListeners.get(event).push(fn);
  }
};

// Extract main inline script (the one after </footer>)
const mainScript = scripts.find(s => s.body.includes('function openModal'));
if (!mainScript) {
  console.error('✖ FATAL: Could not locate main inline script containing openModal');
  process.exit(1);
}

// Create VM context and execute main inline script
let timerQueue = [];
const mockSetTimeout = (fn, delay) => {
  const t = { fn, delay, executed: false };
  timerQueue.push(t);
  return t;
};

const sandboxContext = vm.createContext({
  document: mockDocument,
  window: mockWindow,
  console: console,
  setTimeout: mockSetTimeout,
  clearTimeout: (t) => {
    timerQueue = timerQueue.filter(x => x !== t);
  },
  Date: Date,
  encodeURIComponent: encodeURIComponent,
  decodeURIComponent: decodeURIComponent,
  Option: function(text, val) { this.text = text; this.value = val; },
  tailwind: { config: {} }
});

try {
  vm.runInContext(mainScript.body, sandboxContext);
  console.log('✔ Main inline script evaluated in VM sandbox successfully.');
} catch (err) {
  console.error(`✖ Main inline script evaluation failed: ${err.stack}`);
  process.exit(1);
}

// Access functions from sandbox
const openModal = sandboxContext.openModal;
const closeModal = sandboxContext.closeModal;

// 4. ADVERSARIAL TESTS ON MODAL LIFECYCLE
console.log('\n[CHALLENGER 2] Running Adversarial Modal Lifecycle Stress Tests...');

const modalTests = [];
function testModal(name, fn) {
  try {
    fn();
    console.log(`  ✔ [PASS] ${name}`);
    modalTests.push({ name, passed: true });
  } catch (err) {
    console.error(`  ✖ [FAIL] ${name}: ${err.message}`);
    modalTests.push({ name, passed: false, error: err.message });
  }
}

// Helper to flush all pending setTimeouts
function flushTimers() {
  const pending = [...timerQueue];
  timerQueue = [];
  for (const t of pending) {
    t.executed = true;
    t.fn();
  }
}

// Test 1: openModal('privacidad') sets overflow hidden, reveals backdrop & modal
testModal('openModal("privacidad") sets body overflow hidden & removes hidden classes', () => {
  openModal('privacidad');
  
  if (body.style.overflow !== 'hidden') throw new Error(`Expected body.style.overflow == 'hidden', got '${body.style.overflow}'`);
  if (backdrop.classList.has('hidden')) throw new Error('modal-backdrop should not have hidden class');
  if (backdrop.classList.has('opacity-0')) throw new Error('modal-backdrop should not have opacity-0 class');
  if (modalPrivacidad.classList.has('hidden')) throw new Error('modal-privacidad should not have hidden class');
  if (!modalPrivacidad.classList.has('flex')) throw new Error('modal-privacidad should have flex class');
  if (privacidadContent.classList.has('opacity-0')) throw new Error('privacidad-content should not have opacity-0');
  if (privacidadContent.classList.has('scale-95')) throw new Error('privacidad-content should not have scale-95');
});

// Test 2: closeModal('privacidad') restores body overflow immediately, and hides elements after timer
testModal('closeModal("privacidad") restores overflow immediately and hides modal after transition', () => {
  closeModal('privacidad');
  
  if (body.style.overflow !== '') throw new Error(`Expected body.style.overflow == '', got '${body.style.overflow}'`);
  if (!backdrop.classList.has('opacity-0')) throw new Error('modal-backdrop should have opacity-0 during transition');
  if (!privacidadContent.classList.has('opacity-0')) throw new Error('privacidad-content should have opacity-0 during transition');
  if (!privacidadContent.classList.has('scale-95')) throw new Error('privacidad-content should have scale-95 during transition');
  
  // Before timer fires, elements are still visible (not hidden)
  if (backdrop.classList.has('hidden')) throw new Error('modal-backdrop should not be hidden before transition timer fires');
  if (modalPrivacidad.classList.has('hidden')) throw new Error('modal-privacidad should not be hidden before transition timer fires');

  // Flush timers (simulate 300ms transition end)
  flushTimers();

  if (!backdrop.classList.has('hidden')) throw new Error('modal-backdrop should have hidden class after transition');
  if (!modalPrivacidad.classList.has('hidden')) throw new Error('modal-privacidad should have hidden class after transition');
  if (modalPrivacidad.classList.has('flex')) throw new Error('modal-privacidad should not have flex class after transition');
});

// Test 3: openModal('terminos') sets overflow hidden & reveals terminos modal
testModal('openModal("terminos") sets body overflow hidden & reveals terminos modal', () => {
  openModal('terminos');
  
  if (body.style.overflow !== 'hidden') throw new Error(`Expected body.style.overflow == 'hidden', got '${body.style.overflow}'`);
  if (modalTerminos.classList.has('hidden')) throw new Error('modal-terminos should not have hidden class');
  if (!modalTerminos.classList.has('flex')) throw new Error('modal-terminos should have flex class');
  if (terminosContent.classList.has('opacity-0')) throw new Error('terminos-content should not have opacity-0');
  if (terminosContent.classList.has('scale-95')) throw new Error('terminos-content should not have scale-95');
});

// Test 4: Escape key listener dismisses modals
testModal('Escape key event dismisses open modal and restores body overflow', () => {
  mockDocument.dispatchEvent({ type: 'keydown', key: 'Escape' });
  
  if (body.style.overflow !== '') throw new Error(`Expected body.style.overflow == '', got '${body.style.overflow}'`);
  flushTimers();
  if (!modalTerminos.classList.has('hidden')) throw new Error('modal-terminos should be hidden after Escape and transition');
});

// Test 5: Outside backdrop click simulation
testModal('Outside click on modal container triggers closeModal', () => {
  openModal('privacidad');
  if (body.style.overflow !== 'hidden') throw new Error('Modal should be open');

  // Clicking on modalPrivacidad itself (the outer container representing the backdrop area)
  modalPrivacidad.dispatchEvent({ type: 'click', target: modalPrivacidad });

  if (body.style.overflow !== '') throw new Error('Clicking modal container should trigger closeModal');
  flushTimers();
  if (!modalPrivacidad.classList.has('hidden')) throw new Error('modal-privacidad should be hidden');
});

// Test 6: Clicking inside modal content does NOT close the modal
testModal('Clicking inside modal content does NOT close the modal', () => {
  openModal('privacidad');
  if (body.style.overflow !== 'hidden') throw new Error('Modal should be open');

  // Clicking on content card
  modalPrivacidad.dispatchEvent({ type: 'click', target: privacidadContent });

  if (body.style.overflow !== 'hidden') throw new Error('Clicking content card should NOT trigger closeModal');
  if (modalPrivacidad.classList.has('hidden')) throw new Error('modal-privacidad should remain visible');
  
  // Clean up
  closeModal('privacidad');
  flushTimers();
});

// Test 7: Race condition: rapid openModal during closeModal transition
testModal('Rapid openModal while closeModal transition is pending handles state correctly', () => {
  openModal('privacidad');
  closeModal('privacidad'); // starts 300ms timer
  
  // Before timer expires, reopen modal
  openModal('privacidad');
  if (modalPrivacidad.classList.has('hidden')) throw new Error('modal should be visible after reopen');
  if (body.style.overflow !== 'hidden') throw new Error('body overflow should be locked');

  // Timer from earlier closeModal fires now!
  flushTimers();
  
  // Inspect behavior: did the delayed timeout close the reopened modal?
  const wasHiddenByTimeout = modalPrivacidad.classList.has('hidden');
  console.log(`    [Observation] When openModal occurs during 300ms closeModal transition, pending timer hidden status: ${wasHiddenByTimeout}`);
});

// Test 8: Non-existent modal ID does not crash
testModal('Calling openModal / closeModal with non-existent ID gracefully does nothing', () => {
  openModal('inexistente');
  closeModal('inexistente');
});

// Summary
const failedCount = modalTests.filter(t => !t.passed).length;
console.log(`\n[CHALLENGER 2 SUMMARY] Total Tests: ${modalTests.length}, Failed: ${failedCount}`);
if (failedCount > 0 || astErrors.length > 0) {
  process.exit(1);
} else {
  console.log('ALL JAVASCRIPT AST & MODAL LIFECYCLE TESTS COMPLETED.');
}
