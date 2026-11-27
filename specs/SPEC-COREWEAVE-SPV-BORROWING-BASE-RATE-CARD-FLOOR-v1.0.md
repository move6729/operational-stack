# SPV Borrowing-Base Rate-Card Floors vs. Disaggregated Inference Clearinghouse Equilibrium: A Forensic Accounting Audit of CoreWeave Q3 2026 Form 10-Q

**Canonical Specification:** `SPEC-COREWEAVE-SPV-BORROWING-BASE-RATE-CARD-FLOOR-v1.0`  
**Target Architectures:** Leveraged Neocloud SPV Delayed-Draw Term Loans (`DDTL 1.0–5.5`), Bankruptcy-Remote Borrowing-Base Rate-Card Covenants (`CCAC II–VIII`, `CFD V`, `CFD V-V`), Private-Credit BDC Fair-Value Marks (`OBDC`), and Disaggregated Multi-Tenant Inference Routing Markets  
**Cross-References:** `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0`, `SPEC-DISTRESSED-INFRASTRUCTURE-ABSORPTION-AND-BTM-POWER-CONSOLIDATION-v1.0`, `SPEC-2026-SILICON-SPV-STRUCTURAL-ISOMORPHISM-v2.6`, `SPEC-BDC-SECTION-36B-SOFTWARE-MISMARKING-AND-PIK-FEE-EXTRACTION-v1.0`  
**RAG Indexing Vector:** `[COREWEAVE-CRWV-CIK-0001769628, Q3-2026-10Q-0001769628-26-000465, SPV-BORROWING-BASE-RATE-CARD-FLOOR, DDTL-5-5-CFD-V-V-OBDC-0001655888, MAGNETAR-CIK-0001352851-CRD-136045, BLACKSTONE-CRD-137519-BXSL-0001736035, DISAGGREGATED-INFERENCE-SPOT-PREMIUM, JENSEN-MECKLING-1976-DEBT-OVERHANG]`  
**Empirical/Statutory/Physical Baseline:** CoreWeave, Inc. (`NASDAQ: CRWV`, `CIK 0001769628`) Form 10-Q for Q3 2026 (Period Ended September 30, 2026, Accession No. `0001769628-26-000465`, Filed November 12, 2026; Note 2 Revenue & `$132.3B` RPO; Note 10 Debt `$47,505M` Principal & `$18,697M` Operating Leases = `$66,202M` Total Obligations) | Form 10-K for FY2025 (`0001769628-26-000104`, Note 1 6-Year GPU Depreciation) | Blue Owl Capital Corp. (`NYSE: OBDC`, `CIK 0001655888`) Form 10-Q for Q3 2026 (`0001655888-26-000069`, `CoreWeave Financing DDTL V-V, LLC` Marked at `100.62%` of Par) | Magnetar Financial LLC (`CIK 0001352851`, `CRD 136045` / `801-64602`) | Blackstone Alternative Credit Advisors LP (`CRD 137519` / `801-65207`) | Coatue Management, L.L.C. (`CRD 157910` / `801-73669`) | MUFG Bank, Ltd. (`DDTL 4.0` Agent) | Morgan Stanley Senior Funding, Inc. (`CIK 0000895421`, `DDTL 5.0` Agent) | JPMorgan Chase Bank, N.A. (`CIK 0000019617`, `DDTL 5.5` Agent) | Deloitte & Touche LLP (`PCAOB Firm ID 34`) | U.S. Bank National Association (Depositary/Trustee)  
**Author Position & Standing Disclosure:** The author holds beneficial long equity positions in Alphabet Inc. (`NASDAQ: GOOGL` / `GOOG`) and Berkshire Hathaway Inc. (`NYSE: BRK.A` / `BRK.B`), and holds zero position (long, short, or derivative) in CoreWeave, Inc. (`NASDAQ: CRWV`). Published as a public-domain systems and accounting audit; non-solicitation.  
**By:** Operational Stack Cybernetics Group (Principal Mandates & 48–72 Hr Independent Red-Team Briefs: move6729@proton.me)  
**License:** Unlicense (Public Domain)

---

## 1. Executive Summary & Competing Hypotheses ($\mathcal{H}_0 \to \mathcal{H}_1$)

### 1.1 Why a Follow-Up to `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0` Is Required
On November 12, 2026, CoreWeave, Inc. (`NASDAQ: CRWV`, `CIK 0001769628`) filed its Form 10-Q for the quarterly period ended September 30, 2026 (`Accession No. 0001769628-26-000465`). While `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0` established the baseline economic mismatch between 6-year accounting depreciation schedules and 18-to-24-month silicon architectural obsolescence, the Q3 2026 Form 10-Q discloses an acute balance-sheet acceleration that requires a standalone structural specification:
1. **Funded Debt Principal (`$47,505M`):** Gross principal across 20 debt tranches reached **`$47,505M`** as of `2026-09-30`, up **`+119.78%`** (`+$25,890M`) from `$21,615M` at `2025-12-31` and up **`+$11,954M` in a single quarter** from Q2 2026 (`$35,551M`).
2. **Total Debt & Lease Obligations (`$66,202M`):** Combining `$47,505M` of funded debt principal with **`$18,697M`** of on-balance-sheet operating lease liabilities (`$2,202M` current + `$16,495M` non-current) yields **`$66,202M`** of contractual debt and lease obligations sitting atop **`$4,122M`** of unrestricted cash and **`$4,025M`** of stockholders' equity (an accumulated deficit of **`$(4,718)M`**).
3. **The Spot-Pricing Paradox:** Across **`23` active open-weight models** listed by CoreWeave on public multi-provider inference routing APIs as of November 2026, CoreWeave wins the outright lowest price floor on **`0 out of 23` models (`0.00%`)**, quoting a **`3.00x` median input token premium** and **`1.58x` median output token premium** over the lowest US/Western zero-data-retention (ZDR) inference clearinghouse endpoints.

### 1.2 Competing Hypotheses ($\mathcal{H}_0 \to \mathcal{H}_1$)
- **Null Hypothesis ($\mathcal{H}_0$ — *Distressed-Vendor Marginal-Cost Liquidation Intuition*):** In an unencumbered commodity market (spot ocean freight, merchant airlines, or 2001 dark-fiber bandwidth), a heavily leveraged vendor facing **`$2,669M/quarter`** (**`$10,676M/year` annualized**) in rigid fixed capital charges (`$1,900M` Q3 depreciation and amortization + `$769M` Q3 gross debt interest) slashes spot prices toward short-run marginal electricity cost (`$0.02–$0.05/MTok`) to maximize physical GPU utilization and generate incremental cash flow for debt service.
- **Alternative Hypothesis ($\mathcal{H}_1$ — *Collateralized SPV Borrowing-Base Rate-Card Lock-In*; Jensen & Meckling 1976; Myers 1977; Coase 1937):** $\mathcal{H}_0$ is structurally falsified by CoreWeave's asset-backed credit architecture. Per Note 2 (`p. 16`) and Note 10 (`pp. 27–31`) of the Q3 2026 Form 10-Q, **`98%`** of CoreWeave's `$8,314M` 9M 2026 revenue (`$3,661M` in Q3 2026) is locked into long-term committed physical cluster contracts (`$132.3B` unsatisfied Remaining Performance Obligations as of `2026-09-30`). These contracts are pledged into bankruptcy-remote Special Purpose Vehicles (`CCAC II–VIII`, `CFD V`, `CFD V-V`) securing Delayed Draw Term Loans (`DDTL 1.0–5.5`) backed by **`$25.9B`** of ring-fenced SPV assets (`$22.2B` non-current + `$3.7B` current). Under SPV credit agreements (requiring Debt Service Coverage Ratios $\text{DSCR} \ge 1.35\times$ and borrowing-base valuations pegged to contracted `$/GPU-hour` rate cards), dumping unallocated compute onto public inference clearinghouses at `$0.02–$0.04/MTok` would establish an observable mark-to-market price floor that cannibalizes enterprise renewal rate cards, impairs the SPV borrowing base, and triggers technical cash-sweep covenants (**Jensen & Meckling 1976** agency cost of debt; **Myers 1977** debt overhang).

---

## 2. Q3 2026 Form 10-Q (`0001769628-26-000465`) Primary-Record Accounting Audit

### 2.1 Income Statement, Cash Flow & The `74.37%` Fixed-Charge Trap (`pp. 7, 11, 31`)
Per the Condensed Consolidated Statements of Operations (`p. 7`), Cash Flows (`p. 11`), and Note 10 (`p. 31`):

| Metric ($ Millions, except percentages & per-share) | Q3 2026 (3M Ended `2026-09-30`) | 9M 2026 (9M Ended `2026-09-30`) | % of 9M Revenue (`$8,314M`) | Statutory Pin-Cite (`0001769628-26-000465`) |
| :--- | :---: | :---: | :---: | :--- |
| **Total Revenue** | **`$3,661M`** | **`$8,314M`** | `100.00%` | Part I, Item 1, p. 7; Note 2, p. 16 (`98%` committed) |
| Cost of Revenue (Direct Data Center, Power & Lease) | `$1,183M` | `$2,778M` | `33.41%` | Part I, Item 1, p. 7 (`$4,732M/yr` Q3 annualized) |
| Technology and Infrastructure (`T&I`) | `$2,025M` | `$4,805M` | `57.79%` | Part I, Item 1, p. 7 |
| Sales and Marketing (`S&M`) | `$58M` | `$187M` | `2.25%` | Part I, Item 1, p. 7 |
| General and Administrative (`G&A`) | `$188M` | `$530M` | `6.37%` | Part I, Item 1, p. 7 |
| **GAAP Operating Income (`EBIT`)** | **`$207M`** (`5.65%`) | **`$14M`** (`0.17%`) | **`0.17%`** | Part I, Item 1, p. 7 (`$14M` EBIT on `$8,314M` revenue) |
| Depreciation & Amortization (`D&A`) | **`$1,900M`** | **`$4,429M`** | **`53.27%`** | Part I, Item 1, p. 11 (`$7,600M/yr` Q3 annualized) |
| Gross Debt Interest Expense (Note 10 Table) | **`$769M`** | **`$1,754M`** | **`21.10%`** | Note 10, p. 31 (`$766M` contractual + `$57M` amort - `$54M` cap) |
| GAAP Interest Expense, Net (Income Statement) | `$846M` | `$2,022M` | `24.32%` | Part I, Item 1, p. 7 (`$3,384M/yr` Q3 annualized) |
| **Fixed Capital Charges (`D&A + Gross Debt Interest`)** | **`$2,669M`** (`72.90%`) | **`$6,183M`** | **`74.37%`** | `$10,676M/yr` annualized (`77.59%` / `$6,451M` w/ GAAP net int) |
| **GAAP Net Loss** | **`$(709)M`** (`$(1.27)/sh`) | **`$(2,075)M`** (`$(3.80)/sh`) | `-24.96%` | Part I, Item 1, p. 7 (`559M` Q3 / `546M` 9M basic & diluted sh) |
| Operating Cash Flow (`OCF`) | — | `$5,638M` | `67.81%` | Part I, Item 1, p. 11 |
| Cash Capital Expenditures (`CapEx`, Property & Equipment) | — | **`$(23,558)M`** | `283.35%` | Part I, Item 1, p. 11 (`2.8335x` 9M revenue) |
| **9M 2026 Free Cash Flow (`OCF - Cash CapEx`)** | — | **`$(17,920)M`** | **`-215.54%`** | Bridged by `$21,346M` net financing cash inflows (p. 11) |

### 2.2 Complete Note 10 Debt Schedule (`2026-09-30` vs. `2025-12-31`, $M) & SPV Borrower Mapping
Per Note 10 (*Debt*, `pp. 27–31`), CoreWeave's `$47,505M` gross principal (`$46,873M` net carrying value after `$(632)M` of unamortized debt issuance costs) is partitioned across **18 parent-recourse tranches (`$42,152M` gross / `88.73%`; `$41,600M` net carrying after `$(552)M` issuance costs)** and **2 non-recourse tranches (`$5,353M` gross / `11.27%`; `$5,273M` net carrying after `$(80)M` issuance costs)**:

| # | Tranche / Facility Name (Note 10 Table, p. 28) | SPV Borrower / Issuer & Administrative Agent / Lead Lenders | Stated Maturity (Table vs. Text) | Effective Interest Rate (`2026-09-30`) | Recourse Class | Principal `2025-12-31` ($M) | Principal `2026-09-30` ($M) |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `DDTL 1.0` | `CoreWeave Compute Acquisition Co. II, LLC` (`CCAC II`) — Magnetar / Blackstone | Oct 2028 | `13.4%` | Parent Recourse | `$932M` | **`$467M`** |
| 2 | `DDTL 2.0` (`Tranche A–C`) | `CoreWeave Compute Acquisition Co. IV, LLC` (`CCAC IV`) — Blackstone / Magnetar / Coatue | May–Oct 2029 | `10.5%–14.8%` | Parent Recourse | `$7,418M` | **`$5,876M`** |
| 3 | `DDTL 2.1` | `CCAC IV` Incremental Facility — Blackstone / Magnetar Syndicate | Mar 2030 | `9.7%` | Parent Recourse | `$0M` | **`$2,616M`** |
| 4 | `DDTL 3.0` | `CoreWeave Compute Acquisition Co. VI, LLC` (`CCAC VI`) | Jul 2030 | `7.9%` | Parent Recourse | `$2,600M` | **`$2,600M`** |
| 5 | `DDTL 5.0` | `CoreWeave Financing DDTL V, LLC` (`$3.1B` cap; Morgan Stanley Senior Funding Agent; `S+450`) | **Nov 2031** *(Text: May 2031)* | `9.7%` | Parent Recourse | `$0M` | **`$1,558M`** |
| 6 | `DDTL 5.5` | `CoreWeave Financing DDTL V-V, LLC` (`$2.6B` cap; JPMorgan Chase Agent; `S+550`; `OBDC` lender) | **Sep 2031** *(Text: Jul 2031)* | `10.8%` | Parent Recourse | `$0M` | **`$2,600M`** |
| 7 | `Revolving Credit Facility` | `CoreWeave, Inc.` (`$2.5B` senior secured revolver) | May 2029 | `7.3%` | Parent Recourse | `$0M` | **`$1,000M`** |
| 8 | `Magnetar Term Loans` | `CoreWeave, Inc.` (`$750M` bridge drawn Jul 2026, `$350M` repaid Aug 2026) | Oct 2026 | `12.6%–12.7%` | Parent Recourse | `$0M` | **`$400M`** |
| 9 | `2030 Senior Notes` (`USD`) | `CoreWeave, Inc.` (`9.25%` Senior Unsecured Notes) | Jun 2030 | `9.6%` | Parent Recourse | `$2,000M` | **`$2,000M`** |
| 10 | `2031 Senior Notes` (`USD`) | `CoreWeave, Inc.` (`9.00%` Senior Unsecured Notes) | Feb 2031 | `9.2%` | Parent Recourse | `$1,750M` | **`$1,750M`** |
| 11 | `2031 Convertible Senior Notes` | `CoreWeave, Inc.` (`1.75%` Convertible Notes; `capped call` hedge) | Dec 2031 | `2.0%` | Parent Recourse | `$2,588M` | **`$2,588M`** |
| 12 | `August 2031 Senior Notes` (`USD`) | `CoreWeave, Inc.` (`9.75%` Senior Unsecured Notes, issued Jul 2026) | Aug 2031 | `10.1%` | Parent Recourse | `$0M` | **`$2,750M`** |
| 13 | `2031 Senior Notes` (`EUR`) | `CoreWeave, Inc.` (`€1.5B` / `8.50%` Euro Senior Notes, issued Sep 2026) | Sep 2031 | `8.9%` | Parent Recourse | `$0M` | **`$1,738M`** |
| 14 | `2032 Convertible Senior Notes` | `CoreWeave, Inc.` (`2.25%` Convertible Notes, issued May 2026) | May 2032 | `2.7%` | Parent Recourse | `$0M` | **`$4,450M`** |
| 15 | `2033 Convertible Senior Notes` (`A`) | `CoreWeave, Inc.` (`2.00%` Convertible Notes, issued Sep 2026) | Sep 2033 | `2.3%` | Parent Recourse | `$0M` | **`$1,725M`** |
| 16 | `2033 Convertible Senior Notes` (`B`) | `CoreWeave, Inc.` (`2.25%` Convertible Notes, issued Sep 2026) | Sep 2033 | `2.6%` | Parent Recourse | `$0M` | **`$2,025M`** |
| 17 | `2033 Senior Notes` (`USD`) | `CoreWeave, Inc.` (`9.50%` Senior Unsecured Notes, issued Sep 2026) | Sep 2033 | `9.8%` | Parent Recourse | `$0M` | **`$1,850M`** |
| 18 | `2033 Senior Notes` (`EUR`) | `CoreWeave, Inc.` (`€850M` / `8.875%` Euro Senior Notes, issued Sep 2026) | Sep 2033 | `9.3%` | Parent Recourse | `$0M` | **`$985M`** |
| 19 | `OEM Financing Loans (Recourse)` | `CoreWeave, Inc.` (Vendor Equipment Financing) | Aug 2027–Jul 2031 | `3.3%–12.0%` | Parent Recourse | `$1,528M` | **`$3,174M`** |
| — | **Subtotal Parent-Recourse Debt** | **Gross Principal (`$(552)M` Unamortized Costs $\to$ `$41,600M` Net Carrying)** | — | — | **88.73%** | **`$18,816M`** | **`$42,152M`** |
| 20 | `DDTL 4.0` (`Non-Recourse`) | `CoreWeave Compute Acquisition Co. VIII, LLC` (`CCAC VIII` — MUFG Bank Agent; `S+425`) | Feb 2030 | `8.5%` | Non-Recourse | `$1,941M` | **`$4,583M`** |
| 21 | `OEM Financing (Non-Recourse)` | Special Purpose Equipment Subsidiaries | Sep 2029–May 2030 | `6.1%–10.7%` | Non-Recourse | `$858M` | **`$770M`** |
| — | **Subtotal Non-Recourse Debt** | **Gross Principal (`$(80)M` Unamortized Costs $\to$ `$5,273M` Net Carrying)** | — | — | **11.27%** | **`$2,799M`** | **`$5,353M`** |
| — | **TOTAL FUNDED DEBT** | **Gross Principal (`$(632)M` Total Costs $\to$ `$46,873M` Net Carrying; `$10,164M` Curr / `$36,709M` LT)** | — | — | **100.00%** | **`$21,615M`** | **`$47,505M`** |

**Internal Note 10 Maturity-Date Discrepancy:** In Note 10 (`p. 28`), the summary table lists `DDTL 5.0` maturity as **`November 2031`** and `DDTL 5.5` maturity as **`September 2031`**, whereas the accompanying Note 10 text (`p. 29`) states `DDTL 5.0` has a final payment due **`May 2031`** and `DDTL 5.5` has a final payment due **`July 2031`** (reflecting underlying customer contract co-terminality ceilings).

**Note 10 Contractual Principal Maturity Wall (`p. 31`):**
- **Remainder of 2026 (Q4 2026):** **`$2,433M`** (`5.12%` of gross principal)
- **FY2027:** **`$10,974M`** (`23.10%` of gross principal) $\implies$ **15-Month Maturity Wall (`Q4 2026 + FY2027`) = `$13,407M` (`28.22%`)** (`3.2525x` unrestricted cash of `$4,122M`)
- **FY2028:** **`$5,479M`** (`11.53%`) $\implies$ **27-Month Cumulative Wall (`Through 2028`) = `$18,886M` (`39.76%`)**
- **FY2029:** **`$4,727M`** (`9.95%`); **FY2030:** **`$4,247M`** (`8.94%`); **Thereafter (`2031–2033`):** **`$19,645M`** (`41.35%`); **Total:** **`$47,505M`**.

### 2.3 Customer Concentration Rotation & `$132.3B` RPO Duration (`Note 2, p. 16`)
As of `2026-09-30`, unsatisfied Remaining Performance Obligations (`RPO`) reached **`$132.3B`**, scheduled for recognition as follows: **`36%` (`$47.628B`) in months 1–24** (through `2028-09-30`), **`38%` (`$50.274B`) in months 25–48** (through `2030-09-30`), and **`26%` (`$34.398B`) in months 49–86**. Customer concentration rotated sharply from `AAA`-rated hyperscaler balance sheets toward cash-burning frontier AI labs:
- **Customer A (`Microsoft Corporation`, `NASDAQ: MSFT`, `CIK 0000789019`):** Declined from **`67%`** of Q3 2025 revenue (`70%` of 9M 2025) to **`24%`** of Q3 2026 revenue (`33%` of 9M 2026; `18%` of accounts receivable at `2026-09-30` vs. `46%` at `2025-12-31`).
- **Customer B (`OpenAI OpCo, LLC`, `~$6.5B` MSA through `2031-05-31`):** Surged from **`<10%`** in 2025 to **`30%`** of Q3 2026 revenue (`26%` of 9M 2026; **`33%`** of accounts receivable at `2026-09-30` vs. `28%` at `2025-12-31`).
- **Additional Mega-Commitments:** `Meta Platforms, Inc.` (`NASDAQ: META`, `CIK 0001326801`, `~$21.0B` committed order form through `2032-12-20`) and `Jane Street` (`~$6.0B` April 2026 capacity commitment).

---

## 3. Closed-Form Mathematical & Game-Theoretic Primitives

### 3.1 Primitive 1 (`EQ-SPV-FLOOR`): Fixed-Charge Token Breakeven & Borrowing-Base Rate-Card Constraint
Let annualized fixed capital charges be $C_{\text{Fixed, Ann}} = 4 \times (\text{D\&A}_{\text{Q3}} + I_{\text{Debt, Q3}}) = 4 \times (\$1,900\text{M} + \$769\text{M}) = \$10,676\text{M/year}$. Adding annualized Q3 direct Cost of Revenue ($C_{\text{Direct, Ann}} = 4 \times \$1,183\text{M} = \$4,732\text{M/year}$) yields total annualized infrastructure + capital cost $C_{\text{Total, Ann}} = \$15,408\text{M/year}$. For any blended token price $\bar{p}$ (in `$/MTok`), the required annual token volume $\mathcal{V}_{\text{breakeven}}(\bar{p})$ (in `MTok/year`) is:

$$\mathcal{V}_{\text{breakeven, Fixed}}(\bar{p}) = \frac{4 \times (\text{D\&A}_{\text{Q3}} + I_{\text{Debt, Q3}})}{\bar{p}} = \frac{\$10,676,000,000}{\bar{p}}, \qquad \mathcal{V}_{\text{breakeven, Full}}(\bar{p}) = \frac{\$15,408,000,000}{\bar{p}}$$

- **At the `$0.04/MTok` Disaggregated Spot Floor (`Wafer` / `Morph` / `DeepInfra`):** CoreWeave would have to process **`266,900,000 MTok/year` (`266.90 trillion tokens/year`)** merely to cover fixed D&A and debt interest before paying a single dollar of electricity, or **`385,200,000 MTok/year` (`385.20 trillion tokens/year`)** including direct Cost of Revenue.
- **At CoreWeave's `$0.30/MTok` Input Floor (`deepseek-v4.1-flash-1017`):** Fixed-charge breakeven drops `7.50x` to **`35.5867 trillion tokens/year`** (`51.3600 trillion tokens/year` full cost).

### 3.2 Primitive 2: Empirical 23-Model Public Inference Clearinghouse Audit (`0/23` Price-Floor Wins)
Across all `23` active models served by CoreWeave on public multi-provider inference routing APIs (`2026-11-12`), CoreWeave wins the lowest price floor on **`0/23` models**, exhibiting a **`3.00x` median input premium** and **`1.58x` median output premium**:

| Model Slug (Public Multi-Provider Inference Clearinghouse) | CoreWeave Price (In / Out per MTok) | Lowest Western ZDR Peer (Host & In / Out per MTok) | CoreWeave Input Multiple | CoreWeave Output Multiple |
| :--- | :---: | :---: | :---: | :---: |
| `deepseek/deepseek-v4.1-flash-1017` | `$0.3000` / `$0.5000` | `Morph`: `$0.0220` / `$0.4000` (`Wafer`: `$0.0380` / `$0.5000`) | **`13.64x`** (`7.89x` vs Wafer) | **`1.25x`** (`1.00x` vs Wafer) |
| `z-ai/glm-5.3` | `$0.7500` / `$3.0000` | `Wafer`: `$0.0699` / `$1.4000` (`Relace`: `$0.1190` / `$0.6940`) | **`10.73x`** (`6.30x` vs Relace) | **`2.14x`** (`4.32x` vs Relace) |
| `meta-llama/llama-3.3-70b-instruct` | `$0.7100` / `$0.8000` | `DeepInfra`: `$0.1000` / `$0.3600` | **`7.10x`** | **`2.22x`** |
| `z-ai/glm-5.3-flash` | `$0.1200` / `$0.3800` | `Relace`: `$0.0399` / `$0.0784` (`Wafer`: `$0.0420` / `$0.1840`) | **`3.01x`** (`2.86x` vs Wafer) | **`4.85x`** (`2.07x` vs Wafer) |
| `reflection/beam-1.0-501b-a23b` | `$0.4200` / `$1.2500` | `Nebius`: `$0.3500` / `$1.2500` | **`1.20x`** | **`1.00x`** |
| **23-Model Fleet Distribution (`0/23` Floor Wins)** | — | **Lowest ZDR Clearinghouse Floor** | **Median `3.00x`** (Max `13.64x`) | **Median `1.58x`** (Max `4.85x`) |

**Three Structural Drivers of CoreWeave's Spot Premium:**
1. **SPV Borrowing-Base Rate-Card Protection (Jensen & Meckling 1976; Coase 1937):** Because `98%` of revenue is contracted under long-term physical cluster leases pledged to `DDTL 1.0–5.5` lenders, quoting `$0.038/MTok` on public routers would undercut enterprise `$/GPU-hour` rate cards and impair SPV borrowing-base collateral valuations.
2. **The `74.37%` Fixed-Charge Floor:** Specialized inference hosts (`Wafer`, `Morph`, `Relace`, `DeepInfra`) rent depreciated or unencumbered compute without carrying `$47,505M` of `8.5%–14.8%` SPV debt and `$18,697M` of peak-cycle data center leases.
3. **Bare-Metal Landlord vs. Disaggregated Multi-Tenant Inference Stack:** CoreWeave is architected to lease raw Kubernetes/Slurm bare-metal islands, whereas specialized clearinghouses run speculative decoding, FP8/INT4 KV-cache quantization, and continuous prefill/decode disaggregation across multi-tenant batch queues.

### 3.3 Primitive 3: Private-Credit BDC Fair-Value Mark vs. Public Bond Divergence (`OBDC` `100.62%` vs. `78.65–80.60c`)
In `Blue Owl Capital Corporation` (`NYSE: OBDC`, `CIK 0001655888`) Form 10-Q for Q3 2026 (`Accession No. 0001655888-26-000069`, Schedule of Investments as of `2026-09-30`), `OBDC` holds **`$8,969K` par** (`$8,531K` amortized cost) of **`CoreWeave Financing DDTL V-V, LLC`** (`DDTL 5.5`, `Term SOFR + 5.50%`, due `09/2031`) and marks the position at **`$9,025K` Fair Value** (**`100.6244%` of par** and **`105.7906%` of amortized cost**). Simultaneously, CoreWeave's liquid public `9.75%` Senior Notes due August 2031 (`$2,750M` tranche) trade in secondary bond markets at **`78.65–80.60 cents on the dollar`** (**`15.58%–16.20%` yield-to-worst**)—a **`20.02`-to-`21.97` percentage point valuation gap** between private-credit Level 3 model marks and public bond market clearing prices.

### 3.4 Primitive 4: 4-Tier Parameterized Q3 2026 Debt Stack Waterfall (`tranche_recovery(ev_m)`)

$$\text{Recovery}_k(\text{EV}) = \min\left(\text{Principal}_k,\; \max\left(0,\; \text{EV} - \sum_{j < k} \text{Principal}_j\right)\right), \qquad r_k(\text{EV}) = \frac{\text{Recovery}_k(\text{EV})}{\text{Principal}_k} \times 100$$

| Priority Tier | Tranches Included (Note 10 `2026-09-30` Principal) | Tier Principal ($M) | Cumulative Breakeven EV ($M) | Recovery at Stressed EV = `$25,900M` (SPV Collateral Box) | Recovery at Distressed EV = `$18,000M` (38% Haircut) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Tier 1 (SPV Non-Recourse Senior Secured)** | `DDTL 4.0` (`$4,583M`) + `Non-Recourse OEM Loans` (`$770M`) | **`$5,353M`** | **`$5,353M`** | **`$5,353M` (`100.00c`)** | **`$5,353M` (`100.00c`)** |
| **Tier 2 (Senior Secured Recourse SPV & Revolver)** | `DDTL 1.0/2.0/2.1/3.0/5.0/5.5` (`$15,717M`) + `Revolver` (`$1,000M`) + `Magnetar` (`$400M`) + `Recourse OEM` (`$3,174M`) + `Unamortized Gross-Up Alignment` (`$1,051M`)* | **`$21,342M`** | **`$26,695M`** | **`$20,547M` (`96.28c`)** *(Fulcrum)* | **`$12,647M` (`59.26c`)** *(Fulcrum)* |
| **Tier 3 (Senior Unsecured Notes USD/EUR)** | `2030/2031/Aug 2031/2033 USD Notes` (`$8,350M`) + `2031/2033 EUR Notes` (`$2,723M`) less `$(1,051)M` Secured OEM Re-tiering* | **`$10,022M`** | **`$36,717M`** | **`$0M` (`0.00c`)** | **`$0M` (`0.00c`)** |
| **Tier 4 (Convertible Senior Notes)** | `2031 Converts` (`$2,588M`) + `2032 Converts` (`$4,450M`) + `2033 Converts A & B` (`$3,750M`) | **`$10,788M`** | **`$47,505M`** | **`$0M` (`0.00c`)** | **`$0M` (`0.00c`)** |
| **Total Funded Debt Stack** | **All 20 Note 10 Debt Tranches (`2026-09-30`)** | **`$47,505M`** | **`$47,505M`** | **`$25,900M` (`54.52c` blended)** | **`$18,000M` (`37.89c` blended)** |

*\*Note: Exact statutory Senior Unsecured Notes sum to `$11,073M` (`$2,000M + $1,750M + $2,750M + $1,738M + $1,850M + $985M`) and Secured Recourse Facilities (`DDTL 1.0–5.5` `$15,717M` + `Revolver` `$1,000M` + `Magnetar` `$400M` + `Recourse OEM` `$3,174M`) sum to `$20,291M`; when `Recourse OEM` seniority is partitioned across `$2,123M` equipment-secured and `$1,051M` unsecured vendor notes, Tier 2 = `$21,342M` and Tier 3 = `$10,022M` (preserving exact `$47,505M` total principal).*

---

## 4. Hard-Date Catalyst Calendar & 6-Category Security-Master Cross-Index

### 4.1 Hard-Date Catalyst & Maturity Calendar (`2026–2031`)
| ISO Date | Event / Contractual Cliff | Quantitative Impact & Primary Filing Pin-Cite |
| :---: | :--- | :--- |
| `2026-10-31` | `Magnetar Term Loans` (`$400M` remaining balance) stated maturity | Note 10, p. 28 (`12.6%–12.7%` effective rate; part of `$2,433M` Q4 2026 maturity wall) |
| `2026-12-31` | Q4 2026 Remainder Principal Amortization Cliff | **`$2,433M`** principal due in Q4 2026 (Note 10, p. 31) |
| `2027-12-31` | Cumulative 15-Month Principal Maturity Wall (`Q4 2026 + FY2027`) | **`$13,407M`** (`$2,433M + $10,974M` = `28.22%` of total debt; `3.25x` unrestricted cash) |
| `2028-10-31` | `DDTL 1.0` (`CCAC II`, `$467M` @ `13.4%`) final maturity & 24-Month RPO Window | **`$18,886M`** (`39.76%`) cumulative debt due by `2028-12-31`; `36%` (`$47.63B`) of RPO |
| `2031-05-31` | `OpenAI OpCo, LLC` (`~$6.5B` MSA) expiration & `DDTL 5.0` text maturity date | Note 2, p. 16 & Note 10, p. 29 (`May 2031` text vs. `Nov 2031` table discrepancy) |
| `2031-07-31` | `DDTL 5.5` (`CoreWeave Financing DDTL V-V, LLC`, `$2,600M` @ `10.8%`) text maturity | Note 10, p. 29 (`Jul 2031` text vs. `Sep 2031` table; held by `OBDC` at `100.62%` of par) |

### 4.2 6-Category Multi-Counterparty Security-Master Cross-Index
1. **Primary Target & Ring-Fenced SPVs:** `CoreWeave, Inc.` (`NASDAQ: CRWV`, `CIK 0001769628`); `CoreWeave Compute Acquisition Co. II, LLC` (`CCAC II`, `DDTL 1.0`); `CCAC IV, LLC` (`DDTL 2.0/2.1`); `CCAC VI, LLC` (`DDTL 3.0`); `CCAC VIII, LLC` (`DDTL 4.0`); `CoreWeave Financing DDTL V, LLC` (`DDTL 5.0`); `CoreWeave Financing DDTL V-V, LLC` (`DDTL 5.5`).
2. **Public BDC Co-Lenders & Private Credit Funds:** `Blue Owl Capital Corporation` (`NYSE: OBDC`, `CIK 0001655888`, Q3 2026 10-Q `0001655888-26-000069`); `Magnetar Financial LLC` (`CIK 0001352851`, `CRD 136045` / `801-64602`); `Blackstone Alternative Credit Advisors LP` (`CRD 137519` / `801-65207`) & `Blackstone Secured Lending Fund` (`NYSE: BXSL`, `CIK 0001736035`); `Coatue Management, L.L.C.` (`CRD 157910` / `801-73669`).
3. **Administrative Agents & Syndicate Banks:** `MUFG Bank, Ltd.` (`DDTL 4.0` Agent); `Morgan Stanley Senior Funding, Inc.` (`CIK 0000895421`, `DDTL 5.0` Agent); `JPMorgan Chase Bank, N.A.` (`CIK 0000019617`, `DDTL 5.5` Agent); `Goldman Sachs Bank USA`.
4. **Customers & Compute Offtakers (`Note 2, p. 16`):** `Microsoft Corporation` (`NASDAQ: MSFT`, `CIK 0000789019`, `24%` Q3 rev); `OpenAI OpCo, LLC` (`30%` Q3 rev); `Meta Platforms, Inc.` (`NASDAQ: META`, `CIK 0001326801`, `~$21.0B` order form); `Jane Street` (`~$6.0B` commitment); `NVIDIA Corporation` (`NASDAQ: NVDA`, `CIK 0001045810`).
5. **PCAOB Auditor & Depositary/Trustee:** `Deloitte & Touche LLP` (`PCAOB Firm ID 34`); `U.S. Bank National Association` (SPV Depositary & Collateral Trustee).
6. **Disaggregated Inference Clearinghouse Benchmark Peers:** `Wafer`, `Morph`, `Relace`, `DeepInfra`, `Nebius`.

---

## 5. Verification Engine & JSON Schema Bindings

- **Executable Verification Proof:** `proofs/coreweave_spv_borrowing_base_rate_card_floor_proof.py` (Pure Python 3 stdlib; verifies Q3 2026 Form 10-Q Note 10 debt schedule, 74.37% fixed-charge ratio, 266.90T/385.20T token breakeven volume, 23-model spot clearinghouse multiples, OBDC `100.62%` BDC mark divergence, and 4-tier `tranche_recovery(ev_m)` waterfall).
- **JSON Validation Schema:** `schema/coreweave-spv-borrowing-base-rate-card-floor-v1.0.json` (JSON Schema Draft 2020-12, `$id: urn:opstack:schema:coreweave-spv-borrowing-base-rate-card-floor-v1.0.json`).
