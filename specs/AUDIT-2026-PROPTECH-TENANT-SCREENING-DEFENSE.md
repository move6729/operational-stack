# AUDIT-2026: PROPTECH TENANT SCREENING FCRA PRO SE DEFENSE

**Specification Target:** `OPEN-PROP-SCREEN-v1.0`  
**License:** Unlicense (Public Domain — Zero-Rent Federation)  

---

### I. MECHANISTIC MISMATCH & EXPLOITATION MECHANICS

Corporate PropTech platforms rely on automated, unverified web scraping and legacy public record aggregators to perform algorithmic tenant screening. These systems systematically introduce false positives, including expunged eviction records, incorrect criminal records due to common names, and inaccurate arrears figures.

Under the Fair Credit Reporting Act (FCRA 15 U.S.C. § 1681i), screening vendors are statutory Consumer Reporting Agencies (CRAs) required to conduct a reasonable reinvestigation within 30 days upon receiving a dispute. Failure to do so constitutes willful noncompliance under 15 U.S.C. § 1681n, triggering statutory damages of $1,000 per violation plus attorney fees.

### II. GAME-THEORETIC & ECONOMIC ASYMMETRY

PropTech screening vendors operate on thin per-query margins ($5–$15 per background check). When confronted with a schema-formatted 30-day statutory notice followed by an auto-generated pro se court complaint:

$$\text{Defense Cost}_{\text{Vendor}} \approx \$12,000 \quad \gg \quad \text{Statutory Damage Cap} = \$1,000$$

The vendor cannot scale human legal defense against automated, schema-validated pro se filings. The cost of defending a single case destroys the profit margin on over 1,000 screening reports.

### III. SCHEMA & PROOF INTEGRATION

- **Schema Target:** `schema/prop_tenant_screening.json`
- **Verification Engine:** `proofs/prop_tenant_screening_engine.py`

Enforces strict zero-egress state commitments and deterministic FCRA statutory escalation timers.
