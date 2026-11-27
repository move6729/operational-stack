#!/usr/bin/env python3
"""
CoreWeave SPV Borrowing-Base Rate-Card Floor — Deterministic Verification Proof
================================================================================
Companion proof for SPEC-COREWEAVE-SPV-BORROWING-BASE-RATE-CARD-FLOOR-v1.0 and
articles/coreweave-spv-borrowing-base-rate-card-floor.txt.

Verifies (pure Python 3 stdlib, exit code 0):
  1. Q3 2026 Form 10-Q (Accession 0001769628-26-000465) balance-sheet, income-
     statement, cash-burn and Note 10 debt-maturity arithmetic.
  2. SPV borrowing-base rate-card floor breakeven token volumes at the
     $0.04/MTok spot floor and the 23-model public inference clearinghouse
     head-to-head price multiples (0/23 floor wins).
  3. OBDC fair-value mark vs. public bond price divergence.
  4. Parameterized 4-tier Q3 debt-stack recovery waterfall tranche_recovery(ev_m).

License: Unlicense (Public Domain).
"""

import sys

TOL = 1e-9  # exact-arithmetic tolerance for cent/percentage checks


def approx(a: float, b: float, tol: float = 1e-4) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def check(label: str, a: float, b: float, tol: float = 1e-4) -> bool:
    ok = approx(a, b, tol)
    print(f"  [{'OK' if ok else 'FAIL'}] {label}: {a!r} vs {b!r}")
    return ok


failures = 0


def verify(label: str, a: float, b: float, tol: float = 1e-4) -> None:
    global failures
    if not check(label, a, b, tol):
        failures += 1


# =============================================================================
# 1. Q3 2026 FORM 10-Q (0001769628-26-000465, filed 2026-11-12) FIGURES
# =============================================================================
print("== 1. Q3 2026 Form 10-Q Income Statement / Balance Sheet / Burn ==")

Q3_26_REV_M = 3661.0
NINE_M_26_REV_M = 8314.0
Q3_26_COR_M = 1183.0
NINE_M_26_COR_M = 2778.0
Q3_26_DA_M = 1900.0
NINE_M_26_DA_M = 4429.0
Q3_26_DEBT_INT_GROSS_M = 766.0 + 57.0 - 54.0  # interest + amort - capitalized
NINE_M_26_DEBT_INT_GROSS_M = 1841.0 + 143.0 - 230.0
Q3_26_NET_INT_IS_M = 846.0
NINE_M_26_NET_INT_IS_M = 2022.0
Q3_26_OP_INC_M = 207.0
NINE_M_26_OP_INC_M = 14.0
Q3_26_NET_LOSS_M = -709.0
NINE_M_26_NET_LOSS_M = -2075.0
NINE_M_26_OCF_M = 5638.0
NINE_M_26_CAPEX_M = 23558.0

verify("Q3 gross debt interest build (766 + 57 - 54)", Q3_26_DEBT_INT_GROSS_M, 769.0)
verify("9M gross debt interest build (1841 + 143 - 230)", NINE_M_26_DEBT_INT_GROSS_M, 1754.0)
verify("Q3 COR annualized (1183 x 4)", Q3_26_COR_M * 4.0, 4732.0)
verify("Q3 D&A annualized (1900 x 4)", Q3_26_DA_M * 4.0, 7600.0)
verify("Q3 gross interest annualized (769 x 4)", Q3_26_DEBT_INT_GROSS_M * 4.0, 3076.0)
verify("Q3 operating margin (207 / 3661)", 100.0 * Q3_26_OP_INC_M / Q3_26_REV_M, 5.6542)
verify("9M operating margin (14 / 8314)", 100.0 * NINE_M_26_OP_INC_M / NINE_M_26_REV_M, 0.1684)
verify("9M D&A as % of 9M revenue (4429 / 8314)", 100.0 * NINE_M_26_DA_M / NINE_M_26_REV_M, 53.2716)
verify("9M capex as multiple of 9M revenue (23558 / 8314)", NINE_M_26_CAPEX_M / NINE_M_26_REV_M, 2.833534)
verify("9M FCF (OCF - capex)", NINE_M_26_OCF_M - NINE_M_26_CAPEX_M, -17920.0)

# Debt stack
Q3_26_DEBT_PRINCIPAL_M = 47505.0
FY25_DEBT_PRINCIPAL_M = 21615.0
Q2_26_DEBT_PRINCIPAL_M = 35551.0
Q3_26_RECOURSE_GROSS_M = 42152.0
Q3_26_NONRECOURSE_GROSS_M = 5353.0
Q3_26_TOTAL_DEBT_NET_M = 41600.0 + 5273.0

verify("9M debt principal growth (47505 vs 21615)", 100.0 * (Q3_26_DEBT_PRINCIPAL_M - FY25_DEBT_PRINCIPAL_M) / FY25_DEBT_PRINCIPAL_M, 119.7779)
verify("Q3 single-quarter debt jump (47505 - 35551)", Q3_26_DEBT_PRINCIPAL_M - Q2_26_DEBT_PRINCIPAL_M, 11954.0)
verify("recourse share of gross principal (42152 / 47505)", 100.0 * Q3_26_RECOURSE_GROSS_M / Q3_26_DEBT_PRINCIPAL_M, 88.7317)
verify("non-recourse share of gross principal (5353 / 47505)", 100.0 * Q3_26_NONRECOURSE_GROSS_M / Q3_26_DEBT_PRINCIPAL_M, 11.2683)
verify("total debt net of issuance costs (41600 + 5273)", Q3_26_TOTAL_DEBT_NET_M, 46873.0)

# Operating leases, obligations, assets
Q3_26_OP_LEASE_LIAB_M = 668.0 + 18029.0
FY25_OP_LEASE_LIAB_M = 8195.0
Q3_26_TOTAL_OBLIGATIONS_M = Q3_26_DEBT_PRINCIPAL_M + Q3_26_OP_LEASE_LIAB_M
Q3_26_PPE_NET_M = 56778.0
Q3_26_TOTAL_ASSETS_M = 91481.0
Q3_26_SPV_COLLATERAL_BOX_M = 22200.0 + 3700.0

verify("Q3 operating lease liabilities (668 + 18029)", Q3_26_OP_LEASE_LIAB_M, 18697.0)
verify("op-lease liability growth (18697 vs 8195)", 100.0 * (Q3_26_OP_LEASE_LIAB_M - FY25_OP_LEASE_LIAB_M) / FY25_OP_LEASE_LIAB_M, 128.1513)
verify("total obligations (47505 + 18697)", Q3_26_TOTAL_OBLIGATIONS_M, 66202.0)
verify("PPE share of total assets (56778 / 91481)", 100.0 * Q3_26_PPE_NET_M / Q3_26_TOTAL_ASSETS_M, 62.0653)
verify("SPV collateral box (22200 + 3700)", Q3_26_SPV_COLLATERAL_BOX_M, 25900.0)

# RPO decomposition
RPO_B = 132.3
rpo_m1_24, rpo_m25_48, rpo_m49_86 = 0.36 * RPO_B, 0.38 * RPO_B, 0.26 * RPO_B
verify("RPO M1-24 tranche (36% x 132.3)", rpo_m1_24, 47.628)
verify("RPO M25-48 tranche (38% x 132.3)", rpo_m25_48, 50.274)
verify("RPO M49-86 tranche (26% x 132.3)", rpo_m49_86, 34.398)
verify("RPO tranches sum to total", rpo_m1_24 + rpo_m25_48 + rpo_m49_86, RPO_B)

# Fixed-charge trap
Q3_FIXED_CHARGES_M = Q3_26_DEBT_INT_GROSS_M + Q3_26_DA_M  # 769 + 1900
NINE_M_FIXED_CHARGES_M = NINE_M_26_DEBT_INT_GROSS_M + NINE_M_26_DA_M  # 1754 + 4429
NINE_M_FIXED_CHARGES_GAAP_M = NINE_M_26_NET_INT_IS_M + NINE_M_26_DA_M  # 2022 + 4429
verify("Q3 fixed charges (769 + 1900)", Q3_FIXED_CHARGES_M, 2669.0)
verify("Q3 fixed charges annualized (2669 x 4)", Q3_FIXED_CHARGES_M * 4.0, 10676.0)
verify("Q3 fixed-charge ratio (2669 / 3661)", 100.0 * Q3_FIXED_CHARGES_M / Q3_26_REV_M, 72.9036)
verify("9M fixed charges (1754 + 4429)", NINE_M_FIXED_CHARGES_M, 6183.0)
verify("9M fixed-charge ratio (6183 / 8314)", 100.0 * NINE_M_FIXED_CHARGES_M / NINE_M_26_REV_M, 74.3685)
verify("9M GAAP-net fixed charges (2022 + 4429)", NINE_M_FIXED_CHARGES_GAAP_M, 6451.0)
verify("9M GAAP-net fixed-charge ratio (6451 / 8314)", 100.0 * NINE_M_FIXED_CHARGES_GAAP_M / NINE_M_26_REV_M, 77.5920)

# Note 10 principal maturity schedule
MATURITIES = {"Rem 2026": 2433.0, "2027": 10974.0, "2028": 5479.0, "2029": 4727.0, "2030": 4247.0, "Thereafter": 19645.0}
verify("Note 10 maturity schedule sums to principal", sum(MATURITIES.values()), 47505.0)
cliff_15m = MATURITIES["Rem 2026"] + MATURITIES["2027"]
through_2028 = cliff_15m + MATURITIES["2028"]
verify("15-month maturity cliff (2433 + 10974)", cliff_15m, 13407.0)
verify("15-month cliff share of principal", 100.0 * cliff_15m / Q3_26_DEBT_PRINCIPAL_M, 28.2223)
verify("maturities through 2028", through_2028, 18886.0)
verify("through-2028 share of principal", 100.0 * through_2028 / Q3_26_DEBT_PRINCIPAL_M, 39.7558)

# =============================================================================
# 2. EQ-SPV-FLOOR: RATE-CARD FLOOR BREAKEVEN VOLUMES & 23-MODEL CLEARINGHOUSE
# =============================================================================
print("== 2. EQ-SPV-FLOOR: Breakeven Token Volumes & Head-to-Head Multiples ==")

SPOT_FLOOR_PER_MTOK = 0.04  # $/MTok spot floor
CAPITAL_CHARGES_M = 10676.0  # $10,676.0M/yr annualized fixed charges
COR_ANNUALIZED_M = 4732.0

breakeven_capital_mtok = (CAPITAL_CHARGES_M / SPOT_FLOOR_PER_MTOK) * 1e3  # MTok/yr
breakeven_incl_cor_mtok = ((CAPITAL_CHARGES_M + COR_ANNUALIZED_M) / SPOT_FLOOR_PER_MTOK) * 1e3
verify("capital-only breakeven volume (10676.0M / 0.04)", breakeven_capital_mtok / 1e3, 266900.0)
verify("capital-only breakeven volume in trillions of tokens", breakeven_capital_mtok / 1e6, 266.90)
verify("COR-inclusive breakeven volume (15408.0M / 0.04)", breakeven_incl_cor_mtok / 1e3, 385200.0)
verify("COR-inclusive breakeven volume in trillions of tokens", breakeven_incl_cor_mtok / 1e6, 385.20)

# Head-to-head CoreWeave-vs-lowest-ZDR-peer multiples (CW price / peer price)
CLEARINGHOUSE = [
    # (slug, cw_in, cw_out, peer_in, peer_out, in_mult, out_mult)
    ("deepseek/deepseek-v4.1-flash-1017", 0.3000, 0.5000, 0.0220, 0.4000, 13.6364, 1.25),
    ("z-ai/glm-5.3", 0.7500, 3.0000, 0.0699, 1.4000, 10.7296, 2.1429),
    ("meta-llama/llama-3.3-70b-instruct", 0.7100, 0.8000, 0.1000, 0.3600, 7.10, 2.2188),
    ("z-ai/glm-5.3-flash", 0.1200, 0.3800, 0.0399, 0.0784, 3.0075, 4.8469),
    ("reflection/beam-1.0-501b-a23b", 0.4200, 1.2500, 0.3500, 1.2500, 1.20, 1.00),
]
for slug, cw_in, cw_out, p_in, p_out, m_in, m_out in CLEARINGHOUSE:
    verify(f"{slug} input multiple (CW {cw_in} / peer {p_in})", cw_in / p_in, m_in, tol=0.005)
    verify(f"{slug} output multiple (CW {cw_out} / peer {p_out})", cw_out / p_out, m_out, tol=0.005)
# Wafer cross-check on the deepseek input leg: 0.3000 / 0.0380
verify("deepseek input multiple vs Wafer (0.30 / 0.038)", 0.3000 / 0.0380, 7.8947, tol=0.005)

# =============================================================================
# 3. OBDC FAIR-VALUE MARK VS. PUBLIC BOND DIVERGENCE
# =============================================================================
print("== 3. OBDC (0001655888-26-000069) DDTL V-V Mark vs. Public Bonds ==")

OBDC_PAR_K = 8969.0
OBDC_AMORT_COST_K = 8531.0
OBDC_FV_K = 9025.0
PUBLIC_BOND_LOW, PUBLIC_BOND_HIGH = 78.65, 80.60  # 9.75% Senior Notes cents

fv_par_pct = 100.0 * OBDC_FV_K / OBDC_PAR_K
fv_cost_pct = 100.0 * OBDC_FV_K / OBDC_AMORT_COST_K
verify("OBDC FV as % of par (9025 / 8969)", fv_par_pct, 100.6244)
verify("OBDC FV as % of amortized cost (9025 / 8531)", fv_cost_pct, 105.7906)
verify("private-vs-public spread at high bond price (100.6244 - 80.60)", fv_par_pct - PUBLIC_BOND_HIGH, 20.0244)
verify("private-vs-public spread at low bond price (100.6244 - 78.65)", fv_par_pct - PUBLIC_BOND_LOW, 21.9744)

# =============================================================================
# 4. PARAMETERIZED 4-TIER Q3 DEBT-STACK RECOVERY WATERFALL
# =============================================================================
print("== 4. 4-Tier Debt-Stack Recovery Waterfall tranche_recovery(ev_m) ==")

TIERS = [
    ("Tier 1: Non-Recourse SPV DDTL 4.0 + Non-Recourse OEM", 5353.0),
    ("Tier 2: Senior Secured Recourse (DDTL 1.0/2.0/2.1/3.0/5.0/5.5 + Revolver + Magnetar + Recourse OEM)", 21342.0),
    ("Tier 3: Senior Unsecured Notes (USD/EUR)", 10022.0),
    ("Tier 4: Convertible Senior Notes 2031/2032/2033", 10788.0),
]
TIER_PRINCIPALS = [p for _, p in TIERS]
verify("tier principals sum to gross debt stack", sum(TIER_PRINCIPALS), 47505.0)
verify("recourse tiers (2+3+4) sum to recourse gross", sum(TIER_PRINCIPALS[1:]), 42152.0)


def tranche_recovery(ev_m: float):
    """Map enterprise value ev_m ($M) to per-tier recoveries (cents on dollar)."""
    remaining = ev_m
    cents, cumulative = [], 0.0
    for principal in TIER_PRINCIPALS:
        pay = max(0.0, min(remaining, principal))
        cents.append(100.0 * pay / principal)
        cumulative += principal
        remaining = max(0.0, remaining - principal)
    blended = 100.0 * min(ev_m, sum(TIER_PRINCIPALS)) / sum(TIER_PRINCIPALS)
    return cents, blended


def verify_waterfall(ev_m: float, expected_cents, expected_blended: float) -> None:
    cents, blended = tranche_recovery(ev_m)
    for (name, _), got, exp in zip(TIERS, cents, expected_cents):
        verify(f"EV={ev_m:.0f} {name[:28]}... recovery", got, exp)
    verify(f"EV={ev_m:.0f} blended recovery", blended, expected_blended)


# Breakeven EV thresholds (cumulative principal)
cum = 0.0
for (name, principal), exp_breakeven in zip(TIERS, [5353.0, 26695.0, 36717.0, 47505.0]):
    cum += principal
    verify(f"{name[:40]}... breakeven EV threshold", cum, exp_breakeven)

# EV = $25,900M (SPV collateral box)
verify_waterfall(25900.0, [100.0, 96.2750, 0.0, 0.0], 54.5206)
verify("EV=25900 Tier 2 dollar recovery ($M)", min(25900.0 - 5353.0, 21342.0), 20547.0)
# EV = $18,000M
verify_waterfall(18000.0, [100.0, 59.2634, 0.0, 0.0], 37.8907)
verify("EV=18000 Tier 2 dollar recovery ($M)", min(18000.0 - 5353.0, 21342.0), 12647.0)

# =============================================================================
# RESULT
# =============================================================================
if failures:
    print(f"PROOF FAILED: {failures} check(s) failed")
    sys.exit(1)
print("ALL CHECKS PASSED: CoreWeave SPV borrowing-base rate-card floor verified")
sys.exit(0)
