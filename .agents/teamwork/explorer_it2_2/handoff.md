# Investigation Report: Modal Timer Race Condition & Tag Balance Remediation

**Agent**: `explorer_it2_2`  
**Parent**: `orchestrator_1` (`fc91f4b5-8d5b-44fe-a4a1-87721cca66da`)  
**Working Directory**: `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_it2_2`  
**Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`  
**Date**: 2026-09-27  

---

## 1. Observation

### 1.1 Modal Close Timer Race Condition (`test_e2e.py` T6.6 Failure)
- **Direct Code Observation (`index.html` lines 1243–1273)**:
  ```javascript
  // --- Modal Management ---
  function openModal(modalId) {
      const backdrop = document.getElementById('modal-backdrop');
      const modal = document.getElementById(`modal-${modalId}`);
      const content = document.getElementById(`${modalId}-content`);
      if (!modal || !backdrop || !content) return;
      
      backdrop.classList.remove('hidden');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      void modal.offsetWidth; // Force reflow for CSS transition
      backdrop.classList.remove('opacity-0');
      content.classList.remove('scale-95', 'opacity-0');
      document.body.style.overflow = 'hidden';
  }

  function closeModal(modalId) {
      const backdrop = document.getElementById('modal-backdrop');
      const modal = document.getElementById(`modal-${modalId}`);
      const content = document.getElementById(`${modalId}-content`);
      if (!modal || !backdrop || !content) return;
      
      backdrop.classList.add('opacity-0');
      content.classList.add('scale-95', 'opacity-0');
      document.body.style.overflow = '';
      setTimeout(() => {
          backdrop.classList.add('hidden');
          modal.classList.add('hidden');
          modal.classList.remove('flex');
      }, 300);
  }
  ```
- **Test Observation (`tests/test_e2e.py` lines 533–540 & 608–611)**:
  ```javascript
  // Test 6: Adversarial Race Condition - Rapid reopen within 300ms transition window
  ctx.openModal('privacidad');
  ctx.closeModal('privacidad'); // starts 300ms timer
  ctx.openModal('privacidad'); // reopen before timer fires
  flushTimers(); // old timer fires now!
  results.race_condition_modal_survives = !modalPriv.classList.has('hidden');
  ```
  **Verbatim Error**:
  `✖ [FAIL] T6.6_Modal_RapidReopen_RaceCondition: Stress-test rapid reopen within 300ms transition window (detects pending timer collapse)`
  `→ Reason: Defect: Pending 300ms timer from prior closeModal() collapsed reopened modal`
- **Root Cause**: `closeModal()` creates an anonymous `setTimeout` whose handle is never stored. When `openModal()` is invoked during the 300ms transition window, it has no reference to cancel the pending timer. When the 300ms delay elapses, the scheduled callback unconditionally executes `modal.classList.add('hidden')` and `backdrop.classList.add('hidden')`, collapsing the freshly reopened modal. Furthermore, when Escape is pressed (`closeModal('privacidad'); closeModal('terminos');`), consecutive calls without guard checks can overwrite or clear active modal timers.

---

### 1.2 Legacy Tag Balance Imbalance in `#vista-previa` (`test_e2e.py` T7.3b Failure)
- **Test Observation (`tests/test_e2e.py` lines 735–744)**:
  **Verbatim Error**:
  `✖ [FAIL] T7.3b_Global_Document_Tag_Balance: Audit full document for orphaned tags (flags pre-existing preview card </div> imbalances)`
  `→ Reason: Unclosed tags: 0, Unmatched closing tags: 10 (lines [206, 277, 343, 344, 345, 416, 417, 488, 489, 499])`
- **Direct Code Observation across `#vista-previa` (Lines 125–505)**:
  Detailed DOM traversal revealed that lines `[206, 277, 343, 344, 345, 416, 417, 488, 489, 499]` are **not** the source of the defect; they are legitimate closing tags for card containers and grid layouts that were flagged because the HTML parser stack was emptied prematurely.
  In all 5 preview cards in `#vista-previa`, an identical structural error exists: between the feature list and the "Inversión Inicial" card, two extra closing `</div>` tags were mistakenly pasted:
  1. **Preview 1 (Web Básica, lines 186–188)**:
     ```html
     184:                                 </div>
     185:                                 
     186: </div>
     187:                             </div>
     188:                             </div>
     189:                             <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
     ```
     Line 184 closes feature list (`line 179`). Line 186 closes header/feature column (`line 172`). Lines 187 and 188 prematurely close the column wrapper (`line 171`) and grid (`line 136`).
  2. **Preview 2 (Profesional - Clínica, lines 258–260)**:
     ```html
     256:                                 </div>
     257:                                 
     258: </div>
     259:                             </div>
     260:                             </div>
     261:                             <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
     ```
     Lines 259 and 260 are identical premature closing tags.
  3. **Preview 3 (Empresarial - Despacho, lines 325–327)**:
     ```html
     323:                                 </div>
     324:                                 
     325: </div>
     326:                             </div>
     327:                             </div>
     328:                             <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
     ```
     Lines 326 and 327 are identical premature closing tags.
  4. **Preview 4 (Tienda Web, lines 367–369)**:
     ```html
     365:                                 </div>
     366:                                 
     367: </div>
     368:                             </div>
     369:                             </div>
     370:                             <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
     ```
     Lines 368 and 369 are identical premature closing tags.
  5. **Preview 5 (Servicios Locales / Urgencias, lines 469–471)**:
     ```html
     467:                                 </div>
     468:                                 
     469: </div>
     470:                             </div>
     471:                             </div>
     472:                             <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
     ```
     Lines 470 and 471 are identical premature closing tags.

  **Total Premature Tags**: Exactly 2 tags × 5 cards = 10 orphaned tags.

---

## 2. Logic Chain

1. **Modal Timer Race Condition**:
   - `closeModal()` initiates a 300ms CSS transition (`opacity-0`, `scale-95`) before hiding elements via `setTimeout`.
   - Without storing `modalCloseTimer`, rapid reopen calls `openModal()`, removing `hidden` and restoring `opacity-100`.
   - When the previous `setTimeout` fires, it forcibly adds `hidden` to `#modal-backdrop` and `#modal-${modalId}`.
   - Introducing `let modalCloseTimer = null;` allows `openModal()` to clear any pending timeout before modifying classes.
   - In `closeModal()`, adding `if (modal.classList.contains('hidden')) return;` guards against the common pattern where `closeModal('privacidad')` and `closeModal('terminos')` are called sequentially (e.g. Escape key listener or backdrop click listener), preventing an inactive modal call from wiping out an active modal's transition timer.
   - Clearing `modalCloseTimer` prior to creating a new `setTimeout` ensures only one close transition can be active at a time, and resetting `modalCloseTimer = null` inside the callback restores pristine state.

2. **Legacy Tag Balance Remediation**:
   - In `#vista-previa`, each card has a column with Tailwind class `p-8 flex flex-col justify-between` (or `p-6 flex flex-col justify-between mt-auto`).
   - Flexbox `justify-between` requires two direct children:
     1. Upper child: `<div>` containing package badge, title, description, and feature list.
     2. Lower child: `<div class="bg-zinc-800/80...">` containing "Inversión Inicial" pricing and the action button.
   - The two extra closing `</div>` tags in lines [187–188, 259–260, 326–327, 368–369, 470–471] closed the column and grid prematurely, kicking the lower child out of the flex container.
   - In HTML5 parser algorithms, browsers silently compensated, but the DOM tree was malformed and `TagBalanceParser` reported 10 unmatched closing tags at the ends of the cards.
   - Removing the 2 premature `</div>` tags from each of the 5 cards restores the exact 1:1 balance between opening and closing `<div>` tags across `#vista-previa`.
   - Because the lower child is returned to its intended parent (`p-8 flex flex-col justify-between`), the layout is not disrupted; rather, the intended Tailwind CSS `justify-between` spacing is properly restored.

---

## 3. Caveats

- **Scope Boundary**: This investigation focuses specifically on the timer race condition and the tag balance in `#vista-previa`. Backdrop click event delegation and `pointer-events-none` adjustments are covered by `explorer_it2_1`.
- **Pre-existing Browser Forgiveness**: Modern browser rendering engines parse around unmatched closing tags without fatal display breaks, but strict validators, AST builders, and BS4 parsers flag them as syntax defects. Removing them achieves 100% test passing in `T7.3b`.

---

## 4. Conclusion & Surgical Remediation Plan

We provide 6 exact, non-conflicting `replace_file_content` drop-ins for the worker agent.

### 4.1 Edit 1: Modal Timer Race Condition Fix
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **Lines**: 1243–1273
- **AllowMultiple**: `false`
- **StartLine**: 1243
- **EndLine**: 1274
- **TargetContent**:
```javascript
        // --- Modal Management ---
        function openModal(modalId) {
            const backdrop = document.getElementById('modal-backdrop');
            const modal = document.getElementById(`modal-${modalId}`);
            const content = document.getElementById(`${modalId}-content`);
            if (!modal || !backdrop || !content) return;
            
            backdrop.classList.remove('hidden');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            void modal.offsetWidth; // Force reflow for CSS transition
            backdrop.classList.remove('opacity-0');
            content.classList.remove('scale-95', 'opacity-0');
            document.body.style.overflow = 'hidden';
        }

        function closeModal(modalId) {
            const backdrop = document.getElementById('modal-backdrop');
            const modal = document.getElementById(`modal-${modalId}`);
            const content = document.getElementById(`${modalId}-content`);
            if (!modal || !backdrop || !content) return;
            
            backdrop.classList.add('opacity-0');
            content.classList.add('scale-95', 'opacity-0');
            document.body.style.overflow = '';
            setTimeout(() => {
                backdrop.classList.add('hidden');
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }, 300);
        }
```
- **ReplacementContent**:
```javascript
        // --- Modal Management ---
        let modalCloseTimer = null;

        function openModal(modalId) {
            const backdrop = document.getElementById('modal-backdrop');
            const modal = document.getElementById(`modal-${modalId}`);
            const content = document.getElementById(`${modalId}-content`);
            if (!modal || !backdrop || !content) return;
            
            if (modalCloseTimer) {
                clearTimeout(modalCloseTimer);
                modalCloseTimer = null;
            }

            backdrop.classList.remove('hidden');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            void modal.offsetWidth; // Force reflow for CSS transition
            backdrop.classList.remove('opacity-0');
            content.classList.remove('scale-95', 'opacity-0');
            document.body.style.overflow = 'hidden';
        }

        function closeModal(modalId) {
            const backdrop = document.getElementById('modal-backdrop');
            const modal = document.getElementById(`modal-${modalId}`);
            const content = document.getElementById(`${modalId}-content`);
            if (!modal || !backdrop || !content) return;
            if (modal.classList.contains('hidden')) return;
            
            backdrop.classList.add('opacity-0');
            content.classList.add('scale-95', 'opacity-0');
            document.body.style.overflow = '';
            if (modalCloseTimer) {
                clearTimeout(modalCloseTimer);
                modalCloseTimer = null;
            }
            modalCloseTimer = setTimeout(() => {
                backdrop.classList.add('hidden');
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                modalCloseTimer = null;
            }, 300);
        }
```

---

### 4.2 Edits 2–6: Tag Balance Remediation in `#vista-previa`

#### Edit 2: Preview 1 (Web Básica)
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **StartLine**: 183
- **EndLine**: 190
- **AllowMultiple**: `false`
- **TargetContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Horario de atención y ubicación con mapa interactivo</div>
                                </div>
                                
</div>
                            </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```
- **ReplacementContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Horario de atención y ubicación con mapa interactivo</div>
                                </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```

#### Edit 3: Preview 2 (Profesional - Clínica)
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **StartLine**: 255
- **EndLine**: 262
- **AllowMultiple**: `false`
- **TargetContent**:
```html
                                    <div class="flex items-center gap-1.5 text-xs text-zinc-300"><span class="text-green-400">✓</span> Perfil Google Maps integrado</div>
                                </div>
                                
</div>
                            </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
```
- **ReplacementContent**:
```html
                                    <div class="flex items-center gap-1.5 text-xs text-zinc-300"><span class="text-green-400">✓</span> Perfil Google Maps integrado</div>
                                </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
```

#### Edit 4: Preview 3 (Empresarial - Despacho)
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **StartLine**: 322
- **EndLine**: 329
- **AllowMultiple**: `false`
- **TargetContent**:
```html
                                    <div class="flex items-center gap-1.5 text-xs text-zinc-300"><span class="text-green-400">✓</span> Formulario empresarial detallado</div>
                                </div>
                                
</div>
                            </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
```
- **ReplacementContent**:
```html
                                    <div class="flex items-center gap-1.5 text-xs text-zinc-300"><span class="text-green-400">✓</span> Formulario empresarial detallado</div>
                                </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-xl p-4 border border-zinc-700 flex flex-col gap-3 mt-auto">
```

#### Edit 5: Preview 4 (Tienda Web)
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **StartLine**: 364
- **EndLine**: 371
- **AllowMultiple**: `false`
- **TargetContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Configuración de costos de envío</div>
                                </div>
                                
</div>
                            </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```
- **ReplacementContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Configuración de costos de envío</div>
                                </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```

#### Edit 6: Preview 5 (Servicios Locales / Urgencias)
- **Target File**: `c:\Users\joshu\OneDrive\Desktop\My web\index.html`
- **StartLine**: 466
- **EndLine**: 473
- **AllowMultiple**: `false`
- **TargetContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Carga ultrarrápida en cualquier celular</div>
                                </div>
                                
</div>
                            </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```
- **ReplacementContent**:
```html
                                    <div class="flex items-center gap-2 text-sm text-zinc-300"><span class="text-green-400">✓</span> Carga ultrarrápida en cualquier celular</div>
                                </div>
                            </div>
                            <div class="bg-zinc-800/80 rounded-2xl p-4 border border-zinc-700 flex flex-col gap-3">
```

---

## 5. Verification Method

To independently verify after applying these edits:

1. **Automated E2E Python Test Suite**:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; python tests/test_e2e.py
   ```
   **Expected Outcome**:
   - `T6.6_Modal_RapidReopen_RaceCondition`: **PASS** (reopened modal survives with body overflow locked).
   - `T7.3b_Global_Document_Tag_Balance`: **PASS** (`Unclosed tags: 0, Unmatched closing tags: 0`).

2. **Challenger Adversarial Runtime Harness**:
   ```powershell
   node tests/challenger_2_runtime.js
   ```
   **Expected Outcome**:
   - Test 7 (`Rapid openModal while closeModal transition is pending handles state correctly`): `wasHiddenByTimeout: false`.

3. **Invalidation Condition**:
   - If `modalCloseTimer` fails to clear before new modal display, or if `TagBalanceParser` identifies any unmatched tag across `index.html`.
