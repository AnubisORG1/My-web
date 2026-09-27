# Task Assignment: Iteration 2 Remediation Implementation

**Assigned Agent**: worker_2
**Working Directory**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\worker_2
**Parent**: orchestrator_1 (conversation ID: fc91f4b5-8d5b-44fe-a4a1-87721cca66da)
**Project Root**: c:\Users\joshu\OneDrive\Desktop\My web
**Specification**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\ORIGINAL_REQUEST.md
**Project Plan**: c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\orchestrator_1\PROJECT.md

## Reference Reports (MUST READ)
1. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_it2_1\handoff.md` (Modal backdrop click delegation & pointer-events)
2. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_it2_2\handoff.md` (Modal timer race condition & tag balance)
3. `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\explorer_it2_3\handoff.md` (Test harness mock fixes in test_e2e.js and test_e2e.py)

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## CRITICAL Constraint: R4 Edición Quirúrgica
- Todas las modificaciones al HTML y tests deben hacerse mediante reemplazos exactos (`replace_file_content` o `str.replace` con count=1).
- Está ESTRICTAMENTE PROHIBIDO usar expresiones regulares amplias (`re.sub` con `re.DOTALL`).

## Action Items
1. **In `c:\Users\joshu\OneDrive\Desktop\My web\index.html`**:
   - Apply modal backdrop click listener to `#modal-backdrop` and adjust `pointer-events-none` on `#modal-privacidad` and `#modal-terminos` per `explorer_it2_1/handoff.md`.
   - Apply `modalCloseTimer` in `openModal` and `closeModal` to eliminate rapid reopen timer collapse per `explorer_it2_2/handoff.md`.
   - Apply surgical tag balance cleanups in `#vista-previa` preview cards per `explorer_it2_2/handoff.md`.
2. **In `c:\Users\joshu\OneDrive\Desktop\My web\tests\test_e2e.js`**:
   - Add `tailwind: { config: {} }` to VM sandbox context (Line 483).
   - Add `body: new MockElement('body')` to `mockDocument` (Line 261).
   - Increase T1.3 slice length from 3000 to 8000 (Line 357).
   - Synchronize `MockElement` `selectedIndex` setter, `value` getter/setter, and `innerHTML` option reset per `explorer_it2_3/handoff.md`.
3. **In `c:\Users\joshu\OneDrive\Desktop\My web\tests\test_e2e.py`**:
   - Add `sys.stdout.reconfigure(encoding='utf-8')` and `sys.stderr.reconfigure(encoding='utf-8')` for Windows consoles.
4. **Verification**:
   - Run `node tests/test_e2e.js` and verify 100% pass (22/22).
   - Run `python tests/test_e2e.py` and verify 100% pass (35/35).
   - Run `node tests/test_adversarial_validation.js` and verify 100% pass (12/12).

Write your completion handoff report to `c:\Users\joshu\OneDrive\Desktop\My web\.agents\teamwork\worker_2\handoff.md`.
Notify parent via `send_message` when done.
