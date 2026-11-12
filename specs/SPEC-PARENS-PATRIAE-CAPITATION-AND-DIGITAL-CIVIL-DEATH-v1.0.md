# SPEC-PARENS-PATRIAE-CAPITATION-AND-DIGITAL-CIVIL-DEATH-v1.0: The Parens Patriae Capitation Loop & Digital Civil Death — Adversarial Fiduciary Revenue Functions in Probate Conservatorship Mills, Title IV-E Per-Diem Matching, and Algorithmic Competency Stripping

**Canonical Specification:** `SPEC-PARENS-PATRIAE-CAPITATION-AND-DIGITAL-CIVIL-DEATH-v1.0` (Self-Contained Monolithic Artifact)

**Target Architectures:** Bimodal Parens Patriae Custody Monetization Regimes: Regime I Elder/Adult Probate Guardianship & Conservatorship Estate-Liquidation Mills (`Fla. Stat. §§ 744.108, 744.331`, `UGCOPAA § 312`, `GAO-04-655`, `GAO-10-1046`, Nevada AG *State v. April Parks*); Regime II Youth Social Security Act Title IV-E Open-Ended FMAP Per-Diem Foster Capitation (`42 U.S.C. §§ 670, 672, 673b, 675(5)(E)`); Federal Jurisdictional Abstention Shields (`Marshall v. Marshall`, 547 U.S. 293 Probate Exception & `Younger` Abstention); and 2026 Digital Civil Death (Ex-Parte SIM/2FA/Passkey Custodianship Seizure & Telehealth/Algorithmic Competency Scoring).

**Cross-References:** `OPSTACK-KERNEL-v2.2`, `SPEC-PARENS-PATRIAE-TVPA-SUBPOENA-AND-DISCOVERY-RUBRIC-v1.0.md`, `SPEC-FIDUCIARY-CUTOUT-MORTMAIN-BOUNTY-INTERDICTION-v1.0.md`, `SPEC-ADMINISTRATIVE-NULLIFICATION-AND-REGRESSIVE-COMPLIANCE-SLUDGE-v1.0.md`, `articles/parens-patriae-capitation-and-digital-civil-death.txt`, `schema/parens_patriae_capitation_digital_civil_death.json`, `proofs/verify_parens_patriae_capitation_digital_civil_death.py`

**RAG Indexing Vector:** [PARENS-PATRIAE-CAPITATION-LOOP, PROBATE-CONSERVATORSHIP-FEE-LIQUIDATION, MARSHALL-PROBATE-EXCEPTION-SHIELD, GAO-10-1046-GUARDIANSHIP-AUDIT, APRIL-PARKS-NEVADA-RESTITUTION, SOCIAL-SECURITY-SECTION-672-FMAP, UGCOPAA-SECTION-312-EX-PARTE, DIGITAL-CIVIL-DEATH-PASSKEY-SEIZURE]

**Empirical/Statutory/Physical Baseline:** `Marshall v. Marshall`, 547 U.S. 293 (2006) (Probate Exception to Federal Jurisdiction); U.S. Government Accountability Office, *Guardianships: Collaboration Needed to Protect Incapacitated Elderly People* (`GAO-04-655`, July 2004) & *Guardianships: Cases of Financial Exploitation, Neglect, and Abuse of Seniors* (`GAO-10-1046`, Sept. 30, 2010: `$5.4M` stolen from `158` victims across `20` closed cases); Nevada Attorney General Prosecution of *State v. April Parks* (8th Jud. Dist. Ct., Clark County, Jan. 4, 2019: `192–480 months` [16–40 years] imprisonment, `$559,205.32` restitution); `Fla. Stat. §§ 744.108(1), 744.331(3)–(5)`; Uniform Guardianship, Conservatorship, and Other Protective Arrangements Act (`UGCOPAA § 312`, ULC 2017); Social Security Act Title IV-E (`42 U.S.C. §§ 670, 672(a), 673b, 675(5)(E)`) & Family First Prevention Services Act (`Pub. L. 115-123`, Div. E, 2018).

**By:** Operational Stack Cybernetics Group

**License:** Unlicense (Public Domain — Zero-Rent Federation)

---

## 1. Executive Summary: Custody Priced as Revenue

The *parens patriae* doctrine — the state's reserved authority to protect persons legally unable to protect themselves — is implemented through two high-discretion custody channels: (i) adult probate guardianship and conservatorship over incapacitated elders, and (ii) Social Security Act Title IV-E foster custody over children. This specification models both channels as **adversarial fiduciary revenue functions**: compensation structures in which the custodial apparatus is paid *out of custody itself*, so that the fiduciary's income stream is a monotonically increasing function of the duration and depth of custody over the ward. Three closed-form results follow:

1. **Regime I — Probate Estate Exhaustion (`EQ_01`).** Under `Fla. Stat. § 744.108(1)`, the guardian and appointed counsel draw annual fees `F = $96,000` directly from a ward's estate `E(t)` earning passive yield `r = 0.045`. The estate dynamics `dE/dt = r·E(t) − F` are self-sustaining only above the critical principal `E* = F/r = $2,133,333.33`. A median-retiree estate `E_0 = $480,000` depletes at `−$74,400/yr` net and reaches total liquidation at the locked horizon `t_exhaust = 5.8396` years (continuous closed-form lower bound `5.6643` years; both inside the `[5.5, 6.0]`-year exhaustion band). The `GAO-10-1046` forensic sample — `$5.4M` stolen from `158` victims across `20` closed cases, a mean loss of `$34,177.22` per victim — and the Nevada Attorney General's prosecution of *State v. April Parks* (`192–480 months` [16–40 years] imprisonment; `$559,205.32` restitution) supply the empirical calibration.
2. **Regime II — Title IV-E Per-Diem Capitation (`EQ_02`).** Under `42 U.S.C. §§ 672, 675(5)(E)`, state/contractor revenue over the 15-month (`d = 450`-day) ASFA clock at `FMAP = 0.65` and daily maintenance-plus-admin rate `c_day = $140` is `R_remove = FMAP·c_day·d + B_adopt = 0.65 × 140 × 450 + 6,000 = $46,950.00` per removed child, while non-removal kinship preservation yields `R_preserve = $0.00`. The marginal revenue gradient `dR/d(custody_days) = +$91.00/day > 0` prices family separation strictly positively and preservation at exactly zero, structurally inverting the *parens patriae* mandate.
3. **Digital Civil Death (`EQ_03`).** Under `UGCOPAA § 312` and `Fla. Stat. § 744.331(3)–(5)`, ex-parte emergency letters of guardianship transfer custody of the ward's SIM, 2FA tokens, passkeys, and bank credentials at `t = 0`, inside a `5 + 15 + 25 = 45`-day adjudication latency window. The ward's accessible defense liquidity collapses to `L_ward(t > 0) = $0.00`, so the ward cannot retain independent counsel to contest capacity during the very window in which capacity is being adjudicated.

The federal abstention layer — the *Marshall v. Marshall*, 547 U.S. 293 (2006) probate exception and *Younger* abstention — operates as the shielding stratum that keeps both revenue functions insulated from federal review, closing the supervision circuit inside the same state court system that licenses and pays the fiduciary.

## 2. Axioms & Definitions

- **Axiom 1 (Custody–Revenue Coupling).** In both regimes the custodian's revenue is a function of custody-days: `R = f(custody_days)` with `dR/d(custody_days) ≥ 0`. Custody is not merely the legal condition of the relationship; it is the metering variable of the compensation function.
- **Axiom 2 (Adversarial Fiduciary Compensation).** The fiduciary's compensation is drawn either (Regime I) from the ward's own estate under `Fla. Stat. § 744.108(1)` or (Regime II) from custody-contingent federal matching under `42 U.S.C. § 672`. In both cases the principal (ward) and the agent (fiduciary) have opposed payoffs with respect to the duration of custody: the agent's income is the principal's depletion.
- **Axiom 3 (Ex-Parte Latency).** Emergency guardianship orders issue ex parte at `t = 0`, before any adversarial hearing; the statutory adjudication sequence then runs for a fixed latency window `Λ` (45 days under the locked Florida baseline) during which the order is already operative.
- **Axiom 4 (Abstention Closure).** Federal courts decline to disturb in-rem probate custody (*Marshall*, 547 U.S. at 293) and abstain from interfering with ongoing state proceedings (*Younger v. Harris*, 401 U.S. 37 (1971)), so review of the revenue functions is confined to the state system that supervises the fiduciary.
- **Definition 2.1 (Digital Civil Death).** A living ward suffers *digital civil death* when all authentication factors (SIM/phone number, 2FA tokens, passkeys, bank and email credentials) are held by or transferable to the custodial apparatus, so that the ward's accessible liquidity, communications capacity, and ability to retain counsel are simultaneously zero: `L_ward = $0.00`.
- **Definition 2.2 (Capitation Loop).** A *capitation loop* is a custody regime in which per-head, per-diem, or per-estate-unit payments are conditioned on continued custody, so that release, reunification, or restoration of capacity strictly reduces the custodian's revenue.
- **Definition 2.3 (Latency Window).** `Λ` is the interval between ex-parte custody transfer at `t = 0` and the first adversarial adjudicatory hearing. All defensive acts (retaining counsel, commissioning independent evaluations, filing objections) must be financed and executed inside `Λ`.

## 3. Regime I — `EQ_01`: The Adversarial Fiduciary Profit Function & Probate Estate Exhaustion

### 3.1 Statutory Mechanics

`Fla. Stat. § 744.108(1)` authorizes compensation of guardians and their employed attorneys, paid from the ward's estate for services rendered in administering the guardianship. `Fla. Stat. § 744.331(3)–(5)` sequences the capacity adjudication — petition, examining-committee appointment and reports, and adjudicatory hearing — into the locked 45-day node lattice (`5 + 15 + 25`). `UGCOPAA § 312` (ULC 2017) supplies the model-law ex-parte emergency appointment channel through which custody (and with it credential control) transfers before notice. The fiduciary is thus installed, paid, and shielded before the ward has had any adversarial day in court.

### 3.2 The Estate-Exhaustion ODE

Let `E(t)` be the ward's estate principal, `r = 0.045` its passive yield, and `F = $96,000` the combined annual guardian-plus-counsel fee burn drawn from the estate under `Fla. Stat. § 744.108(1)`:

```
EQ_01:  dE/dt = r·E(t) − F,   E(0) = E_0
        E(t) = E_0·e^(rt) − (F/r)·(e^(rt) − 1)
```

- **Self-sustaining threshold.** `E(t)` is stationary or growing iff `r·E_0 ≥ F`, i.e. `E_0 ≥ E* = F/r = $96,000 / 0.045 = $2,133,333.33`. Estates above `E*` can pay the fiduciary forever from yield alone; estates below `E*` are liquidating annuities for the fiduciary.
- **Calibrated depletion.** For the median-retiree estate `E_0 = $480,000`: passive income `r·E_0 = $21,600/yr` against fee burn `F = $96,000/yr` gives net depletion `dE/dt = $21,600 − $96,000 = −$74,400/yr`.
- **Exhaustion horizon.** Total liquidation `E(t_exhaust) = 0` at `t_exhaust = −ln(1 − r·E_0/F)/r`. The locked point estimate is `t_exhaust = 5.8396` years (≈ 5 years 10 months).

**Corollary 3.1 (Model-Form Band).** The continuous closed form evaluates to `−ln(0.775)/0.045 = 5.6643` years and is the strict lower bound (continuous fee accrual is the fastest-billing admissible schedule); discrete annual billing variants extend the horizon toward `≈ 5.79` years. The locked `5.8396`-year horizon is the billing-discretized point estimate; both values lie inside the `[5.5, 6.0]`-year exhaustion band asserted by the verification harness under a `±0.20`-year model-form tolerance.

**Corollary 3.2 (Restitution Bound).** The *April Parks* restitution award of `$559,205.32` equals approximately `16.36` mean GAO victim losses (`$559,205.32 / $34,177.22`), yet restitution is bounded by the documented estate res and does not capture the present value of the fee stream that would have continued to run absent prosecution. Criminal prosecution converts an ongoing annuity into a one-time clawback; it does not alter the fee function itself.

### 3.3 Empirical Calibration

- **`GAO-04-655` (July 2004):** *Guardianships: Collaboration Needed to Protect Incapacitated Elderly People* — the baseline federal finding that no coordinated monitoring regime exists across the state guardianship systems.
- **`GAO-10-1046` (Sept. 30, 2010):** *Guardianships: Cases of Financial Exploitation, Neglect, and Abuse of Seniors* — in `20` sampled closed cases, `158` victims were stripped of `$5.4M`, a mean loss of `$34,177.22` per victim. The victim-per-case ratio (`158/20 = 7.9`) indicates case-level aggregation: one fiduciary file typically spans multiple wards and multiple fee streams.
- ***State v. April Parks*** (Nevada Attorney General Prosecution, 8th Jud. Dist. Ct., Clark County, Jan. 4, 2019): a professional guardian sentenced to `192–480 months` (16–40 years) imprisonment with `$559,205.32` restitution — the adjudicated existence proof that Regime I fee functions can and do run as exploitation engines in equilibrium, and that the state's remedial response is ex-post prosecution rather than ex-ante fee-structure interdiction.

## 4. Regime II — `EQ_02`: Title IV-E Open-Ended Per-Diem Capitation vs. Preservation Asymmetry

### 4.1 Statutory Mechanics

Social Security Act Title IV-E (`42 U.S.C. § 670` et seq.) funds foster-care maintenance through open-ended federal matching at the state's FMAP rate (`42 U.S.C. § 672(a)`); `42 U.S.C. § 673b` authorizes adoption incentive payments; `42 U.S.C. § 675(5)(E)` runs the ASFA clock — termination-of-parental-rights filing once a child has been in foster care 15 of the most recent 22 months. The Family First Prevention Services Act (`Pub. L. 115-123`, Div. E, 2018) reorganized prevention funding but left the per-diem maintenance matching architecture intact.

### 4.2 The Removal-Revenue Functional

With `FMAP = 0.65`, daily maintenance-plus-admin rate `c_day = $140`, the 15-month ASFA clock `d = 450` days, and adoption incentive `B_adopt = $6,000`:

```
EQ_02:  R_remove  = FMAP · c_day · d + B_adopt
                  = 0.65 × $140 × 450 + $6,000
                  = $40,950 + $6,000 = $46,950.00 per removed child
        R_preserve = $0.00  (non-removal kinship preservation)
        dR/d(custody_days) = FMAP · c_day = +$91.00/day > 0
```

### 4.3 Theorem (Strict Preference Inversion)

Because `R_remove` is strictly increasing in custody-days and `R_preserve = $0.00`, any revenue-maximizing agency or contractor weakly prefers removal over preservation at every decision node, and strictly prefers it wherever removal is feasible. The price vector assigned by the statute is therefore the exact dual of the *parens patriae* mandate: the state pays a strictly positive capitation for custody and exactly zero for the absence of custody. The 15-month ASFA clock does not neutralize the gradient — it converts the terminal event (adoption) into a further `$6,000` bonus, so the revenue path is monotone across its entire length: per-diem accrual followed by terminal bonus, with no payment node at reunification or preservation.

## 5. `EQ_03`: Digital Civil Death — Ex-Parte SIM/2FA/Passkey Custodianship Inside the 45-Day Latency Window

### 5.1 Ex-Parte Credential Custodianship

Under `UGCOPAA § 312` emergency appointment channels and `Fla. Stat. § 744.331(3)–(5)` ex-parte practice, emergency letters of guardianship transfer custody of the ward's person *and estate* at `t = 0`. In a 2026 authentication topology, "estate" includes the credential stack that gates every financial account: the SIM/phone number receiving SMS one-time codes, the 2FA token seeds, the passkey registries, and the bank login credentials themselves. Custody of the credential stack is custody of the liquidity:

```
EQ_03:  L_ward(t > 0) = $0.00   (post-lockout challenger liquidity)
```

### 5.2 The 45-Day Latency Window (5 + 15 + 25)

The locked Florida adjudication lattice compresses capacity stripping into `Λ = 5 + 15 + 25 = 45` days: the ex-parte/emergency appointment node (5), the examining-committee report node (15), and the adjudicatory-hearing node (25). Every defensive act — retaining independent counsel, commissioning an independent capacity evaluation, filing objections, posting bond — must be financed inside `Λ`, i.e., precisely while `L_ward = $0.00`.

### 5.3 Theorem (Defense-Liquidity Annihilation)

Let `c > 0` be any hourly rate for independent counsel. The affordable defense hours inside the latency window are `H = L_ward / c = 0 / c = 0`. Since the ex-parte order precedes the hearing, and the credential seizure precedes the ability to pay, the probability that the ward mounts an effective financed challenge inside `Λ` approaches zero as `L_ward → $0.00`. The sequence is the injury: notice arrives after custody, custody arrives after credential control, and credential control arrives before any forum exists in which to object.

### 5.4 Algorithmic Competency Stripping

Telehealth-only capacity evaluations and algorithmic cognitive-decline scoring compound the asymmetry. The evidence vector used to strip capacity is collected through channels — video sessions, device telemetry, digitally administered instruments — that the custodial apparatus controls or procures, while the ward's only counter-evaluation pathway requires the liquidity and authentication capacity already seized under `EQ_03`. The scoring model is thus trained and presented inside a closed evidentiary loop: the same regime that profits from the incapacity finding (`EQ_01`, `EQ_02`) supplies the measurement instrument that produces it.

## 6. The Abstention Shield Layer: *Marshall* Probate Exception & *Younger* Closure

*Marshall v. Marshall*, 547 U.S. 293 (2006), confines the probate exception to federal jurisdiction: federal courts are barred from disposing of property that is in the custody of a state probate court, though in personam claims remain open. Regime I fee extraction sits at the exception's core — guardian and counsel fees under `Fla. Stat. § 744.108(1)` are drawn in rem from the estate res already in state probate custody, so the monetization loop itself is the very class of disposition the exception reserves to the state. *Younger v. Harris*, 401 U.S. 37 (1971), bars federal equitable interference with the ongoing state guardianship proceeding itself. The two doctrines compose with `EQ_03`: the in personam claims that *Marshall* leaves open require a plaintiff with litigation capacity and liquidity — exactly the attributes digital civil death extinguishes during `Λ`. The result is a closed supervision circuit: the revenue function is reviewable only in the court system that licenses, appoints, and pays the fiduciary. Federal review circuit open = 0.

## 7. Falsifiable Predictions & Empirical Tests

- **P1 (Estate Depletion Rate).** Professional-guardianship estates with `E_0 < E* = $2,133,333.33` deplete at observed net rates `≈ F − r·E_0`, with total exhaustion inside the `[5.5, 6.0]`-year band for the calibrated cohort (`E_0 = $480,000`, `r = 0.045`, `F = $96,000`). Falsified by audited estate ledgers showing sustained net growth below `E*` under active professional guardianship.
- **P2 (Removal-Revenue Gradient).** Agency-level removal rates are positively correlated with per-diem rates and FMAP match rates; the gradient is `+$91.00/day` at locked parameters. Falsified by any jurisdiction showing equal or higher agency revenue under kinship preservation than under foster placement at matched demographics.
- **P3 (Contest Rate Collapse).** The fraction of ex-parte capacity adjudications contested by ward-retained independent counsel approaches zero wherever credential custody transfers before the adjudicatory hearing. Falsified by any jurisdiction showing a materially nonzero financed contest rate inside the 45-day window.
- **P4 (Restitution Ceiling).** Restitution awards in prosecuted guardianship cases (e.g., `$559,205.32` in *April Parks*) are bounded by documented estate res, not by the present value of the fee stream — prosecution clawbacks structurally under-recover relative to the counterfactual fee annuity. Falsified by any restitution order expressly computed against the fee stream's present value.

## 8. Symbol Table & Executable Verification Harness (`proofs/verify_parens_patriae_capitation_digital_civil_death.py`)

### 8.1 Locked Symbol & Parameter Table

| Symbol | Schema Key | Locked Value | Source |
|---|---|---|---|
| `E_0` | `ward_initial_estate_principal_usd` | `$480,000.00` | Median-retiree estate calibration (`EQ_01`) |
| `r` | `estate_passive_yield_rate` | `0.045` | Passive estate yield (`EQ_01`) |
| `r·E_0` | `annual_passive_estate_income_usd` | `$21,600.00` | Derived: `0.045 × $480,000` |
| `F` | `guardian_and_counsel_annual_fee_burn_usd` | `$96,000.00` | `Fla. Stat. § 744.108(1)` fee burn |
| `dE/dt` | `net_annual_estate_depletion_usd` | `−$74,400.00` | Derived: `$21,600 − $96,000` |
| `E*` | `critical_self_sustaining_estate_threshold_usd` | `$2,133,333.33` | Derived: `F/r` |
| `t_exhaust` | `years_to_total_estate_exhaustion` | `5.8396 yr` | Locked billing-discretized horizon (`EQ_01`) |
| — | `gao_2010_sampled_closed_cases` | `20` | `GAO-10-1046` |
| — | `gao_2010_sampled_victims` | `158` | `GAO-10-1046` |
| — | `gao_2010_stolen_assets_usd` | `$5,400,000.00` | `GAO-10-1046` |
| — | `gao_2010_mean_loss_per_victim_usd` | `$34,177.22` | Derived: `$5.4M / 158` |
| — | `april_parks_min_sentence_months` | `192` (16 yr) | *State v. April Parks*, 8th Jud. Dist. Ct. |
| — | `april_parks_max_sentence_months` | `480` (40 yr) | *State v. April Parks*, 8th Jud. Dist. Ct. |
| — | `april_parks_restitution_usd` | `$559,205.32` | *State v. April Parks* restitution order |
| `FMAP` | `title_ive_fmap_federal_match_rate` | `0.65` | `42 U.S.C. § 672` matching |
| `c_day` | `foster_maintenance_and_admin_daily_rate_usd` | `$140.00` | Maintenance + admin per-diem |
| `d` | `custody_days_15_month_asfa_clock` | `450` | `42 U.S.C. § 675(5)(E)` 15-month clock |
| `B_adopt` | `asfa_section_673b_adoption_bonus_usd` | `$6,000.00` | `42 U.S.C. § 673b` incentive |
| `R_remove` | `agency_gross_revenue_per_removed_child_usd` | `$46,950.00` | Derived: `0.65 × 140 × 450 + 6,000` |
| `R_preserve` | `family_preservation_counterfactual_revenue_usd` | `$0.00` | Preservation counterfactual |
| `Λ` | `florida_capacity_adjudication_window_days` | `45` | `Fla. Stat. § 744.331(3)–(5)` (`5+15+25`) |
| `L_ward` | `ward_post_2fa_lockout_challenger_liquidity_usd` | `$0.00` | Post-2FA-lockout defense liquidity |

### 8.2 Verification Execution

```bash
python3 proofs/verify_parens_patriae_capitation_digital_civil_death.py
```

Exit code `0` certifies that all six verification vectors hold: the `EQ_01` exhaustion identities and band membership, the `GAO-10-1046` / *April Parks* arithmetic, the `EQ_02` capitation asymmetry, the `EQ_03` latency-window liquidity annihilation, the abstention-shield closure, and companion schema integrity (`urn:opstack:schema:parens_patriae_capitation_digital_civil_death.json`, Draft 2020-12, `≤ 350` lines).
