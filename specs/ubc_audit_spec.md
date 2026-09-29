# AUDIT SPECIFICATION: UNIVERSAL BASIC COMPUTE (UBC) PROTOCOL & ESSAY AUDIT

**Reference:** `UBC-AUDIT-v1.0`  
**License:** Unlicense (Public Domain — Zero-Rent Federation)  

---

### I. THERMODYNAMIC YIELD INVARIANTS (`proofs/ubc_engine.py`)

1. **Bare-Metal Power Accounting:**
   - Operational cost (OpEx) must be computed in real-time based on local silicon power draw ($P_{\text{watts}}$) and local electricity rates ($R_{\text{kWh}}$).
   - $\text{Cost}_{\text{power}} = \left(\frac{P_{\text{watts}}}{1000}\right) \times \text{Duration}_{\text{hours}} \times R_{\text{kWh}}$.

2. **Zero-Rent Execution Gate:**
   - A node MUST NOT accept or execute any task where $\text{Net Yield} = \text{Gross Reward} - \text{Cost}_{\text{power}} \le 0$.
   - Middleman platform fee deductions or centralized tollbooth commissions are strictly non-compliant (Zero-Rent Invariant).

3. **Deterministic Settlement Verification:**
   - Task completion settlement requires a matching SHA-256 state payload hash (`expected_hash`).
   - Mismatched execution hashes immediately reject settlement and prevent ledger commit.

---

### II. ARTICLE AUDIT CRITERIA (`articles/universal-basic-compute.txt`)

1. **Thermodynamic Alignment:**
   - Article content must maintain 1:1 conceptual fidelity with `proofs/ubc_engine.py` (shifting from legacy paper welfare to self-sovereign edge yield).

2. **Serialization Rules (`KERNEL.md` Rule 8):**
   - Single-line continuous paragraphs (no mid-sentence hard breaks).
   - No ASCII line dividers.
   - Metadata included: Title, Byline, Unlicense declaration, and `##` Markdown subheadings.
