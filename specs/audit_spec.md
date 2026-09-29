# AUDIT SPECIFICATION: OPERATIONAL-STACK COMPLIANCE & INVARIANTS

**Reference:** `OPSTACK-AUDIT-v1.0`  
**License:** Unlicense (Public Domain — Zero-Rent Federation)  

---

### I. EXECUTABLE ENGINE AUDIT SUITE

All engine modules located in `proofs/` MUST satisfy the following structural and operational invariants:

1. **Zero Third-Party Dependencies:**
   - Standard library imports only (`hashlib`, `ast`, `json`, `time`, `typing`, `socket`, `struct`).
   - Third-party packages (`requests`, `numpy`, `pytest`, etc.) are forbidden.

2. **Deterministic Cryptographic State Transitions:**
   - Every state transition must be authenticated via `SHA-256` payload verification against an explicit target hash (`expected_hash`).
   - Mismatched execution hashes must halt state commit operations immediately and return `False`.

3. **Standalone Verification Proof:**
   - Each engine file must implement an executable verification proof function (`run_*_proof() -> bool`).
   - Each engine file must expose a standard main execution block (`if __name__ == "__main__":`) that invokes the verification proof and asserts correct execution without error.

4. **AST Static Analysis & Zero-C2 Controls:**
   - Task engines and execution sandboxes must validate python code via native `ast.NodeVisitor`.
   - Dynamic execution vectors (`eval`, un-sanitized `exec`) without explicit AST sandboxing are non-compliant.

---

### II. ARTICLE & ESSAY SERIALIZATION AUDIT

All canonical articles located in `articles/` MUST adhere to the following Substack/rich-text serialization rules:

1. **Paragraph Continuity:**
   - Text paragraphs must be formatted as continuous single-line strings without mid-sentence hard carriage returns (~80-column line breaks).
   - Paragraphs must be separated strictly by double newlines (`\n\n`).

2. **Zero Plain-Text ASCII Line Dividers:**
   - Plain-text ASCII line dividers (e.g., `--------`, `========`, `***`, `---`) are strictly prohibited to prevent manual editor cleanup overhead in rich-text and Substack platforms.

3. **Zero Markdown Formatting Syntax:**
   - Markdown formatting markup such as headers (`#`, `##`, `###`), bolding (`**text**`), italics (`*text*`), or bullet syntax (`*`, `-`) MUST NOT be used in `.txt` article files. Substack's rich-text editor does not parse raw markdown correctly.
   - Headers and section titles must use plain-text capitalization (e.g., ALL CAPS titles and numbered section headings) without `#` or `**` syntax.

4. **Metadata & Header Structure:**
   - Must include Title, Byline, and Unlicense statement in plain text.

---

### III. TREE MAP & MASTER INDEX SYNCHRONIZATION AUDIT

1. **Master Index Parity:**
   - `specs/OPERATIONAL-STACK-MASTER-INDEX.md` and `README.md` must maintain a 1:1 mapped inventory of all specifications, engines, proofs, schemas, and articles (`KERNEL.md` Rule 7).
   - Any addition, deletion, or modification of files across the repository must be immediately reflected in `specs/OPERATIONAL-STACK-MASTER-INDEX.md` and `README.md`.

2. **Cognitive Containment & Escalation Hierarchy:**
   - All computation and state transitions MUST exhaust local resources ($\text{Local Silicon} \to \text{Local Operator}$) before initiating external network transport or inter-node egress.
   - Handoff to the local human operator (including encrypted WireGuard virtual perimeter tunnels) is a zero-egress state transition and MUST ALWAYS remain open to prevent agent deadlock. External egress is permitted strictly as an explicit escalation of last resort.
