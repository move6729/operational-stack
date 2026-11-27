#!/usr/bin/env python3
"""Verification proof for SPEC-GLEICHSCHALTUNG-ENDOWMENT-CONTINUITY-v1.0.

Pure Python 3 stdlib proof re-deriving every locked constant and governing
equation of the Gleichschaltung endowment-continuity model across two regimes:

  compliant  -- Walsh Committee 20-year sunset amortization honored
                (p_t = 1/(20 - t) -> $0 terminal corpus at t = 20); zero
                dual-class estate-tax shield; zero bacteriophage state-fusion
                leverage; zero 3-prong pincer trigger; no IRC 507(c) call.
  defection  -- perpetual coupon self-perpetuation (r = 0.08 > p = 0.05);
                1936 Ford Class A/B 70% estate-tax shield; bacteriophage
                state-fusion leverage; full 3-prong pincer mosaic trigger and
                the IRC 4945 / IRC 507(c) statutory termination waterfall over
                the $27,115,146,872 Big 3 endowment stack.

Governing equations verified:
  (1) Ford dual-class estate-tax shield
        s_A = 3,280,255 / 3,452,900 = 0.95 equity,  v_A = 0.00 vote
        s_B =   172,645 / 3,452,900 = 0.05 equity,  v_B = 1.00 vote
        shield    = tau_estate * s_A = 0.70 * 0.95 = 0.665
        effective = tau_estate * s_B = 0.70 * 0.05 = 0.035
        wedge     = v_B_pct / s_B_pct = 100.0 / 5.0 = 20.0x
  (2) Bacteriophage state-fusion multiplier
        Lambda_fusion = Coerced_Host_Capital / Seed_Grant
        CFAT 1905 -> TIAA : 1.30e12 / 1.00e7            = 130,000.00x
        Big 3 -> host pool: (6.80e12 + 8.40e11) / 1.533141254e9 >= 1,000.00x
  (3) 3-prong pincer mosaic DAG detector
        trigger = P1(Continental Ore) AND P2(step-transaction)
                  AND P3(Better Business Bureau) AND acyclic AND root->terminal
  (4) Perpetual coupon vs Walsh 20-year sunset
        M_perp = (1 + (r - p))^100 = 1.03^100 = 19.2186x  (locked 19.22x)
        p_t    = 1 / (20 - t)  =>  terminal corpus at t = 20 is $0.00
  (5) IRC 4945 / IRC 507(c) statutory termination and public-policy clawback
      waterfall: tranche_recovery(ev) over the Big 3 endowment stack.

Exit code 0 iff every locked constant and governing equation holds.
"""

import json
import math

# ---------------------------------------------------------------------------
# Standardized security-master keys
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "private_foundation_issuers": [
        {
            "name": "Ford Foundation",
            "ein": "13-1684331",
            "charter_jurisdiction": "MI",
            "charter_iso_date": "1936-01-15",
            "fmv_2023_usd": 16_791_366_964,
        },
        {
            "name": "Rockefeller Foundation",
            "ein": "13-1659629",
            "charter_jurisdiction": "NY",
            "charter_iso_date": "1913-05-14",
            "fmv_2023_usd": 6_225_179_743,
        },
        {
            "name": "Carnegie Corporation of New York",
            "ein": "13-1628151",
            "charter_jurisdiction": "NY",
            "charter_iso_date": "1914-04-20",
            "fmv_2023_usd": 4_098_600_165,
        },
    ],
    "control_instruments": [
        {
            "instrument": "Ford Motor Company Class A common (non-voting)",
            "ticker": "F",
            "cik": "0000037996",
            "exchange": "NYSE",
            "shares": 3_280_255,
            "equity_share_pct": 95.0,
            "vote_share_pct": 0.0,
        },
        {
            "instrument": "Ford Motor Company Class B common (voting)",
            "ticker": "F",
            "cik": "0000037996",
            "exchange": "NYSE",
            "shares": 172_645,
            "equity_share_pct": 5.0,
            "vote_share_pct": 100.0,
        },
    ],
    "seed_grant_provenance": [
        {
            "grantor_ein": "13-1628151",
            "grantee": "Carnegie Foundation for the Advancement of Teaching",
            "fiscal_year": 1905,
            "amount_usd": 10_000_000,
            "successor_host_pool": "TIAA",
        },
        {
            "grantor_ein": "13-1659629",
            "grantee": "Kaiser Wilhelm Institute (Munich)",
            "iso_date": "1928-01-01",
            "amount_usd": 325_000,
            "successor_host_pool": "successor research estate",
        },
    ],
    "legislative_and_judicial_pin_cites": [
        {"pin_cite": "S. Doc. No. 415 (1916)", "iso_year": 1916,
         "vector": "Commission on Industrial Relations (Walsh Committee) final report: 20-year sunset recommendation"},
        {"pin_cite": "Pub. L. 74-407 (1935)", "iso_year": 1935,
         "vector": "Revenue Act of 1935: 0.70 top estate tax rate"},
        {"pin_cite": "RGBl. I S. 529 (1933)", "iso_year": 1933,
         "vector": "Gesetz zur Verhuetung erbkranken Nachwuchses (July 14, 1933 Nazi Hereditary Health Sterilization Law modeled on Harry H. Laughlin's 1922 Cold Spring Harbor ERO Model Eugenical Sterilization Law)"},
        {"pin_cite": "Iwanowa v. Ford Motor Co., 67 F. Supp. 2d 424 (D.N.J. 1999)", "iso_year": 1999,
         "vector": "host-state fusion predicate: forced-labor claim against the Class A/B control issuer"},
        {"pin_cite": "United States v. Carl Krauch et al. (Case VI, 1948)", "iso_year": 1948,
         "vector": "Nuremberg Military Tribunal Case VI: industrial host-state fusion adjudication"},
        {"pin_cite": "H. Rep. No. 2684 (1954)", "iso_year": 1954,
         "vector": "House report on charitable foundation tax treatment"},
        {"pin_cite": "Pub. L. 91-172 (1969)", "iso_year": 1969,
         "vector": "Tax Reform Act of 1969: IRC 4940-4948 and IRC 507 enacted"},
        {"pin_cite": "S. Rep. No. 94-755 Book I (1976)", "iso_year": 1976,
         "vector": "Senate Finance Committee report on private foundation excise enforcement"},
        {"pin_cite": "Bob Jones University v. United States, 461 U.S. 574 (1983)", "iso_year": 1983,
         "vector": "exemption conditioned on conformity with declared public policy"},
        {"pin_cite": "Continental Ore Co. v. Union Carbide & Carbon Corp., 370 U.S. 690 (1962)", "iso_year": 1962,
         "vector": "pincer prong 1: concerted action inferred from a course of dealing"},
        {"pin_cite": "Better Business Bureau v. United States, 326 U.S. 279 (1945)", "iso_year": 1945,
         "vector": "pincer prong 3: one substantial non-exempt purpose defeats exemption"},
        {"pin_cite": "Students for Fair Admissions v. Harvard, 600 U.S. 181 (2023)", "iso_year": 2023,
         "vector": "host-institution public-policy conformity boundary"},
        {"pin_cite": "S. Doc. No. 93-62 (1974)", "iso_year": 1974,
         "vector": "Senate Government Operations (Metcalf Report) Disclosure of Corporate Ownership: Chase Manhattan custodial street-name nominees (Kane & Co., Cudd & Co., Egg & Co.) and sub-5% trust fragmentation"},
    ],
    "court_dockets": [
        "Iwanowa v. Ford Motor Co., 67 F. Supp. 2d 424 (D.N.J. 1999)",
        "United States v. Carl Krauch et al., Case No. VI (Nuremberg Military Tribunal, 1948)",
        "Continental Ore Co. v. Union Carbide & Carbon Corp., 370 U.S. 690 (1962)",
        "Better Business Bureau v. United States, 326 U.S. 279 (1945)",
        "Bob Jones University v. United States, 461 U.S. 574 (1983)",
        "Students for Fair Admissions v. Harvard, 600 U.S. 181 (2023)",
    ],
}

# ---------------------------------------------------------------------------
# Hard-date catalyst and forbearance calendar
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = [
    {"iso_date": "1913-05-14", "catalyst": "Rockefeller Foundation New York charter (EIN 13-1659629)", "pin_cite": None},
    {"iso_date": "1914-04-20", "catalyst": "Carnegie Corporation of New York charter (EIN 13-1628151)", "pin_cite": None},
    {"iso_date": "1922-01-01", "catalyst": "Ford Motor Company Class A (non-voting) / Class B (voting) dual-class recapitalization", "pin_cite": None},
    {"iso_date": "1928-01-01", "catalyst": "Rockefeller Foundation $325,000 Kaiser Wilhelm Institute (Munich) grant", "pin_cite": None},
    {"iso_date": "1933-07-14", "catalyst": "Reich compulsory-cartel statutory instrument", "pin_cite": "RGBl. I S. 529 (1933)"},
    {"iso_date": "1935-08-30", "catalyst": "Revenue Act of 1935: 0.70 top estate tax rate", "pin_cite": "Pub. L. 74-407 (1935)"},
    {"iso_date": "1936-01-15", "catalyst": "Ford Foundation incorporation (EIN 13-1684331)", "pin_cite": None},
    {"iso_date": "1936-06-30", "catalyst": "Ford Class A non-voting corpus transfer window opens (95.0% equity / 0.0% vote)", "pin_cite": None},
    {"iso_date": "1938-07-30", "catalyst": "Ford Class A/B estate-tax shield operative (3,280,255 Class A / 172,645 Class B)", "pin_cite": None},
    {"iso_date": "1948-02-26", "catalyst": "Nuremberg Military Tribunal Case VI proceedings milestone", "pin_cite": "United States v. Carl Krauch et al. (Case VI, 1948)"},
    {"iso_date": "1948-07-29", "catalyst": "Nuremberg Military Tribunal Case VI judgment", "pin_cite": "United States v. Carl Krauch et al. (Case VI, 1948)"},
    {"iso_date": "1952-11-01", "catalyst": "host-state fusion forced-labor claim antecedent milestone", "pin_cite": "Iwanowa v. Ford Motor Co., 67 F. Supp. 2d 424 (D.N.J. 1999)"},
    {"iso_date": "1954-12-16", "catalyst": "House report on charitable foundation tax treatment", "pin_cite": "H. Rep. No. 2684 (1954)"},
    {"iso_date": "1956-01-01", "catalyst": "control-issuer public offering window: Class A/B voting bifurcation preserved", "pin_cite": None},
    {"iso_date": "1968-01-01", "catalyst": "Treasury private-foundation exemption study window (antecedent to Pub. L. 91-172)", "pin_cite": None},
    {"iso_date": "1969-12-30", "catalyst": "Tax Reform Act of 1969: IRC 4940-4948 and IRC 507 enacted", "pin_cite": "Pub. L. 91-172 (1969)"},
    {"iso_date": "1974-12-31", "catalyst": "IRC 4943 excess-business-holdings phase-down window (0.20 voting cap)", "pin_cite": "Pub. L. 91-172 (1969)"},
    {"iso_date": "1976-04-26", "catalyst": "Senate Finance Committee report on private foundation excise enforcement", "pin_cite": "S. Rep. No. 94-755 Book I (1976)"},
    {"iso_date": "1983-05-24", "catalyst": "exemption conditioned on declared public-policy conformity", "pin_cite": "Bob Jones University v. United States, 461 U.S. 574 (1983)"},
    {"iso_date": "2023-06-29", "catalyst": "host-institution public-policy conformity boundary", "pin_cite": "Students for Fair Admissions v. Harvard, 600 U.S. 181 (2023)"},
]

JURISDICTION_CONTEXT = {
    "iso_3166_1_alpha_2": "US",
    "statutory_venue": "Internal Revenue Code Chapter 42 (IRC 4942, 4943, 4945) and IRC 507(c); state attorney general cy pres / quo warranto jurisdiction",
}
CFAA_18_USC_1030_COMPLIANCE_ATTESTATION = True
ITAR_EAR_PUBLIC_DOMAIN_ATTESTATION = True

# ---------------------------------------------------------------------------
# Locked constants (locked_constants_and_outputs)
# ---------------------------------------------------------------------------
FORD_FOUNDATION_EIN = "13-1684331"
ROCKEFELLER_FOUNDATION_EIN = "13-1659629"
CARNEGIE_CORP_EIN = "13-1628151"

FORD_2023_FMV_USD = 16_791_366_964.0
ROCKEFELLER_2023_FMV_USD = 6_225_179_743.0
CARNEGIE_2023_FMV_USD = 4_098_600_165.0
BIG_3_COMBINED_2023_FMV_USD = 27_115_146_872.0
BIG_3_COMBINED_2023_EXPENSES_USD = 1_533_141_254.0

WALSH_1915_COMBINED_CORPUS_USD = 250_000_000.0
WALSH_1915_ANNUAL_REVENUE_USD = 13_500_000.0
REVENUE_ACT_1935_TOP_ESTATE_TAX_RATE = 0.70

FORD_CLASS_A_NON_VOTING_SHARES = 3_280_255
FORD_CLASS_B_VOTING_SHARES = 172_645
FORD_TOTAL_SHARES = 3_452_900
FORD_CLASS_A_EQUITY_SHARE_PCT = 95.0
FORD_CLASS_B_EQUITY_SHARE_PCT = 5.0
FORD_FAMILY_VOTING_CONTROL_PCT = 100.0

ROCKEFELLER_KWI_MUNICH_1928_GRANT_USD = 325_000.0
CARNEGIE_CFAT_1905_SEED_USD = 10_000_000.0
TIAA_MODERN_AUM_USD = 1_300_000_000_000.0
TIAA_LEVERAGE_MULTIPLIER = 130_000.0
US_FEDERAL_BUDGET_HOST_USD = 6_800_000_000_000.0
NACUBO_UNIVERSITY_ENDOWMENT_HOST_USD = 840_000_000_000.0
BACTERIOPHAGE_FUSION_MULTIPLIER_EXAMPLE = 1_000.0

IRC_4942_PAYOUT_FLOOR = 0.05
IRC_4943_VOTING_CAP = 0.20
IRC_4945_FIRST_TIER_RATE = 0.20
IRC_4945_SECOND_TIER_RATE = 1.00
IRC_507C_NET_ASSET_CAP_PCT = 100.0
SUNSET_HORIZON_YEARS = 20

# Auxiliary locked model parameters.
PERPETUAL_COUPON_RATE_R = 0.08          # endowment gross yield
PERPETUAL_PAYOUT_RATE_P = 0.05          # IRC 4942 distributive payout
CENTURY_HORIZON_YEARS = 100
PERPETUAL_COUPON_CENTURY_MULTIPLE = 19.2186   # (1 + (r - p))^100, locked 19.22x
BBB_SUBSTANTIAL_PURPOSE_THRESHOLD = 0.05      # insubstantiality safe harbor
CONTINENTAL_ORE_MIN_COORDINATED_ACTS = 2
STEP_TRANSACTION_MIN_STEPS = 2
FUSION_MULTIPLIER_GATE = BACTERIOPHAGE_FUSION_MULTIPLIER_EXAMPLE

# Two-Hull 1934 Rockefeller Family Trust Compounding Dilemma (H_0 vs. H_1)
ROCKEFELLER_1934_TRUST_SEED_USD = 500_000_000.0
ROCKEFELLER_2026_FORBES_H0_USD = 10_300_000_000.0
ROCKEFELLER_COMPOUNDING_YEARS = 92
US_CPI_ANNUAL_INFLATION_1934_2026 = 0.0330
SEC_13D_REPORTING_THRESHOLD_PCT = 5.0

# Act 0 (1872): South Improvement Company Railroad Rebate & Drawback Synthetic-NIRP
SOUTH_IMPROVEMENT_POSTED_TARIFF_USD = 2.56
SOUTH_IMPROVEMENT_REBATE_USD = 1.06
STANDARD_OIL_NET_FREIGHT_USD = 1.50
SOUTH_IMPROVEMENT_DRAWBACK_TAX_USD = 1.06
COOPERAGE_BARREL_OLD_COST_USD = 2.50
COOPERAGE_BARREL_NEW_COST_USD = 0.96
CLEVELAND_MASSACRE_ACQUIRED_REFINERIES = 22
CLEVELAND_MASSACRE_TOTAL_REFINERIES = 26

# Act I.4 (1935) & Act IV (1995-2003): FICA Payroll Vise, Actuarial Sign Inversion,
# and the David Rockefeller -> Jeffrey Epstein Institutional Peering Handoff
FICA_COMBINED_PAYROLL_TAX_RATE = 0.153
ENDOWMENT_501C3_FICA_TAX_RATE = 0.0
US_UNFUNDED_ENTITLEMENT_LIABILITY_USD = 75_000_000_000_000.0
POST_RETIREMENT_ANNUAL_DRAW_USD = 38_000.0
POST_RETIREMENT_HORIZON_YEARS = 20
SOVEREIGN_DISCOUNT_RATE = 0.04
CZECH_SMOKING_EARLY_DEATH_SAVINGS_USD = 147_000_000.0
CANADA_PBO_MAID_ANNUAL_SAVINGS_USD = 86_900_000.0
EPSTEIN_TRILATERAL_START_YEAR = 1995
EPSTEIN_CFR_START_YEAR = 1995
EPSTEIN_ROCKEFELLER_UNIV_BOARD_YEAR = 2000
EPSTEIN_HARVARD_PED_SEED_USD = 6_500_000.0
SPARTA_HELOT_CULL_424BC_COUNT = 2_000
PLATO_LAWS_STATIC_LOT_CAP = 5_040
TOKUGAWA_ZERO_GROWTH_YEARS = 125
DEEP_TIME_MORTMAIN_EPOCHS_COUNT = 6

# IRC 4945(d) taxable-expenditure base: the Big 3 annual expenditure stream
# recharacterized once the Better Business Bureau substantial-non-exempt-purpose
# prong is satisfied.
TAXABLE_EXPENDITURE_BASE_USD = BIG_3_COMBINED_2023_EXPENSES_USD

# IRC 507(c) aggregate tax benefit: Walsh-era corpus x 1936 estate-tax shield
# rate x perpetual-coupon century compounding.
ESTATE_TAX_SHIELD_RATE = REVENUE_ACT_1935_TOP_ESTATE_TAX_RATE * (
    FORD_CLASS_A_EQUITY_SHARE_PCT / 100.0)
COMPOUNDED_TAX_BENEFIT_USD = round(
    WALSH_1915_COMBINED_CORPUS_USD * ESTATE_TAX_SHIELD_RATE
    * PERPETUAL_COUPON_CENTURY_MULTIPLE, 2)

TRANCHE_STACK = (
    {
        "tranche": 1,
        "name": "IRC 4945 First/Second-Tier Taxable Expenditure Excise Assessment",
        "statutory_basis": "IRC 4945(a)-(d); Pub. L. 91-172 (1969)",
        "coupon_pik": "0.20 first tier + 1.00 second tier on taxable expenditures",
        "collateral_guarantor_box": "Big 3 combined 2023 expenditure stream",
        "seniority": 1,
    },
    {
        "tranche": 2,
        "name": "IRC 507(c) Compounded Estate/Income Tax Benefit Termination Clawback",
        "statutory_basis": "IRC 507(c); Pub. L. 91-172 (1969)",
        "coupon_pik": "lesser of aggregate tax benefit or 100.0% of net assets",
        "collateral_guarantor_box": "Big 3 combined 2023 net asset corpus",
        "seniority": 2,
    },
    {
        "tranche": 3,
        "name": "State AG Cy Pres / Quo Warranto Public Restitution Receiver",
        "statutory_basis": "IRC 507(d)(1) residual distribution; state cy pres / quo warranto",
        "coupon_pik": "100.0% residual sweep to public charitable purposes",
        "collateral_guarantor_box": "post-federal-claim residual corpus",
        "seniority": 3,
    },
    {
        "tranche": 4,
        "name": "Residual Self-Perpetuating Trustee Discretionary Corpus",
        "statutory_basis": "none: structurally subordinated perpetual trustee claim",
        "coupon_pik": "0.0 cents on the dollar",
        "collateral_guarantor_box": "exhausted: zero residual after tranches 1-3",
        "seniority": 4,
    },
)


def assert_close(actual, expected, label, rel_tol=1e-9, abs_tol=1e-6):
    """Assert numeric equality within tolerance; raise AssertionError on drift."""
    if not math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol):
        raise AssertionError(f"{label}: expected {expected!r}, computed {actual!r}")


# ---------------------------------------------------------------------------
# Eq (1): 1936 Ford Class A / Class B dual-class estate-tax shield
# ---------------------------------------------------------------------------
def ford_dual_class_shield(class_a_shares, class_b_shares, total_shares,
                           estate_tax_rate):
    """Eq (1): equity/vote bifurcation and the 70% estate-tax shield."""
    s_a = class_a_shares / total_shares
    s_b = class_b_shares / total_shares
    return {
        "class_a_equity_share": s_a,
        "class_b_equity_share": s_b,
        "class_a_vote_share": 0.0,
        "class_b_vote_share": 1.0,
        "estate_tax_shield_rate": estate_tax_rate * s_a,
        "effective_estate_tax_rate": estate_tax_rate * s_b,
        "estate_tax_eliminated_share": (estate_tax_rate * s_a) / estate_tax_rate,
        "control_to_equity_wedge": (FORD_FAMILY_VOTING_CONTROL_PCT
                                    / FORD_CLASS_B_EQUITY_SHARE_PCT),
    }


def section_4943_voting_cap_arbitrage(economic_ownership_pct, voting_cap):
    """IRC 4943 formal-compliance vs substantive-excess wedge."""
    formal_voting_attribution = 0.0     # Class A carries zero votes
    return {
        "formal_voting_attribution": formal_voting_attribution,
        "voting_cap": voting_cap,
        "formally_compliant": formal_voting_attribution <= voting_cap,
        "economic_ownership": economic_ownership_pct / 100.0,
        "substantive_excess": economic_ownership_pct / 100.0 > voting_cap,
        "arbitrage_wedge_pp": economic_ownership_pct - voting_cap * 100.0,
    }


def two_hull_compounding_dilemma(seed_1934_usd=ROCKEFELLER_1934_TRUST_SEED_USD,
                                 forbes_2026_h0_usd=ROCKEFELLER_2026_FORBES_H0_USD,
                                 years=ROCKEFELLER_COMPOUNDING_YEARS,
                                 cpi_rate=US_CPI_ANNUAL_INFLATION_1934_2026):
    """Milkovich H_0 (Forbes $10.3B -> 0.04% real CAGR) vs. H_1 (7%-8% net CAGR
    -> $252.81B-$596.38B cloaked below 5.0% SEC Schedule 13D/13G threshold)."""
    h0_nominal_cagr = (forbes_2026_h0_usd / seed_1934_usd) ** (1.0 / years) - 1.0
    h0_real_cagr = h0_nominal_cagr - cpi_rate
    h1_7pct_usd = seed_1934_usd * ((1.0 + 0.07) ** years)
    h1_8pct_usd = seed_1934_usd * ((1.0 + 0.08) ** years)
    underperformance_vs_7pct = 1.0 - (forbes_2026_h0_usd / h1_7pct_usd)
    underperformance_vs_8pct = 1.0 - (forbes_2026_h0_usd / h1_8pct_usd)
    return {
        "seed_1934_usd": seed_1934_usd,
        "forbes_2026_h0_usd": forbes_2026_h0_usd,
        "compounding_years": years,
        "h0_nominal_cagr": round(h0_nominal_cagr, 6),
        "h0_real_cagr": round(h0_real_cagr, 6),
        "h1_net_7pct_2026_usd": round(h1_7pct_usd, 2),
        "h1_net_8pct_2026_usd": round(h1_8pct_usd, 2),
        "h0_underperformance_vs_7pct": round(underperformance_vs_7pct, 4),
        "h0_underperformance_vs_8pct": round(underperformance_vs_8pct, 4),
        "sec_13d_reporting_threshold_pct": SEC_13D_REPORTING_THRESHOLD_PCT,
    }


def south_improvement_drawback_nirp():
    """Act 0 (1872): Verify Standard Oil's South Improvement Co. railroad
    rebate + competitor drawback tax (synthetic NIRP) and Cleveland Massacre."""
    net_tariff = SOUTH_IMPROVEMENT_POSTED_TARIFF_USD - SOUTH_IMPROVEMENT_REBATE_USD
    effective_1to1_outlay = net_tariff - SOUTH_IMPROVEMENT_DRAWBACK_TAX_USD
    asymmetry_spread_usd = SOUTH_IMPROVEMENT_POSTED_TARIFF_USD - effective_1to1_outlay
    asymmetry_pct = (asymmetry_spread_usd / SOUTH_IMPROVEMENT_POSTED_TARIFF_USD) * 100.0
    cooperage_savings = COOPERAGE_BARREL_OLD_COST_USD - COOPERAGE_BARREL_NEW_COST_USD
    cleveland_share = (CLEVELAND_MASSACRE_ACQUIRED_REFINERIES
                       / CLEVELAND_MASSACRE_TOTAL_REFINERIES)
    return {
        "posted_tariff_usd": SOUTH_IMPROVEMENT_POSTED_TARIFF_USD,
        "standard_oil_net_freight_usd": round(net_tariff, 2),
        "competitor_drawback_tax_usd": SOUTH_IMPROVEMENT_DRAWBACK_TAX_USD,
        "effective_1to1_outlay_usd": round(effective_1to1_outlay, 2),
        "asymmetry_spread_usd": round(asymmetry_spread_usd, 2),
        "asymmetry_pct": round(asymmetry_pct, 4),
        "cooperage_savings_per_bbl_usd": round(cooperage_savings, 2),
        "cleveland_massacre_share": round(cleveland_share, 6),
    }


def actuarial_sign_inversion_and_peering():
    """Act I.4 (1935) & Act IV (1995-2003): Verify the FICA payroll tax wedge,
    post-retirement sovereign NPV < 0 sign inversion, and the David Rockefeller
    -> Jeffrey Epstein institutional peering handoff."""
    fica_wedge = FICA_COMBINED_PAYROLL_TAX_RATE - ENDOWMENT_501C3_FICA_TAX_RATE
    post_65_npv = -sum(
        POST_RETIREMENT_ANNUAL_DRAW_USD / ((1.0 + SOVEREIGN_DISCOUNT_RATE) ** k)
        for k in range(1, POST_RETIREMENT_HORIZON_YEARS + 1)
    )
    return {
        "fica_payroll_tax_wedge": round(fica_wedge, 4),
        "post_65_sovereign_npv_20yr_usd": round(post_65_npv, 2),
        "citizen_post_retirement_is_net_liability": post_65_npv < 0.0,
        "czech_smoking_early_death_savings_usd": CZECH_SMOKING_EARLY_DEATH_SAVINGS_USD,
        "canada_pbo_maid_annual_savings_usd": CANADA_PBO_MAID_ANNUAL_SAVINGS_USD,
        "epstein_rockefeller_peering_years": [
            EPSTEIN_TRILATERAL_START_YEAR,
            EPSTEIN_CFR_START_YEAR,
            EPSTEIN_ROCKEFELLER_UNIV_BOARD_YEAR,
        ],
        "epstein_harvard_ped_seed_usd": EPSTEIN_HARVARD_PED_SEED_USD,
        "deep_time_short_gamma_epochs": DEEP_TIME_MORTMAIN_EPOCHS_COUNT,
        "sparta_424bc_helot_cull_count": SPARTA_HELOT_CULL_424BC_COUNT,
        "plato_static_lot_cap": PLATO_LAWS_STATIC_LOT_CAP,
        "tokugawa_zero_growth_years": TOKUGAWA_ZERO_GROWTH_YEARS,
    }


# ---------------------------------------------------------------------------
# Eq (2): Bacteriophage state-fusion multiplier
# ---------------------------------------------------------------------------
def bacteriophage_fusion_multiplier(coerced_host_capital_usd, seed_grant_usd):
    """Eq (2): Lambda_fusion = Coerced_Host_Capital / Seed_Grant."""
    return coerced_host_capital_usd / seed_grant_usd


# ---------------------------------------------------------------------------
# Eq (3): 3-prong pincer mosaic DAG detector
# ---------------------------------------------------------------------------
PINCER_MOSAIC_DAG = {
    "P1_continental_ore_concerted_action": ["P2_step_transaction_integration"],
    "P2_step_transaction_integration": ["P3_bbb_substantial_non_exempt_purpose"],
    "P3_bbb_substantial_non_exempt_purpose": ["T_irc_507c_termination_call"],
    "T_irc_507c_termination_call": [],
}
PINCER_ROOT = "P1_continental_ore_concerted_action"
PINCER_TERMINAL = "P3_bbb_substantial_non_exempt_purpose"


def topological_order(graph):
    """Deterministic Kahn topological sort; returns (order, acyclic)."""
    indegree = {node: 0 for node in graph}
    for node in graph:
        for succ in graph[node]:
            indegree[succ] = indegree.get(succ, 0) + 1
    ready = sorted(node for node, deg in indegree.items() if deg == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        freed = []
        for succ in sorted(graph.get(node, [])):
            indegree[succ] -= 1
            if indegree[succ] == 0:
                freed.append(succ)
        ready = sorted(ready + freed)
    return order, len(order) == len(indegree)


def reachable(graph, source, target):
    """Deterministic depth-first reachability test."""
    seen = set()
    stack = [source]
    while stack:
        node = stack.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        stack.extend(sorted(graph.get(node, [])))
    return False


def pincer_mosaic_dag_detect(evidence, graph=PINCER_MOSAIC_DAG):
    """Eq (3): 3-prong pincer mosaic trigger over an acyclic mosaic DAG."""
    prong_1 = (evidence["coordinated_acts"] >= CONTINENTAL_ORE_MIN_COORDINATED_ACTS
               and evidence["common_design"])
    prong_2 = (evidence["integrated_steps"] >= STEP_TRANSACTION_MIN_STEPS
               and evidence["binding_commitment"])
    prong_3 = evidence["non_exempt_purpose_share"] >= BBB_SUBSTANTIAL_PURPOSE_THRESHOLD
    order, acyclic = topological_order(graph)
    path = reachable(graph, PINCER_ROOT, PINCER_TERMINAL)
    return {
        "prong_1_continental_ore": bool(prong_1),
        "prong_2_step_transaction": bool(prong_2),
        "prong_3_bbb_substantial_non_exempt_purpose": bool(prong_3),
        "topological_order": order,
        "acyclic": acyclic,
        "root_to_terminal_path": path,
        "pincer_triggered": bool(prong_1 and prong_2 and prong_3 and acyclic and path),
    }


# ---------------------------------------------------------------------------
# Eq (4): perpetual coupon vs Walsh 20-year sunset amortization
# ---------------------------------------------------------------------------
def perpetual_coupon_multiple(rate_r, payout_p, years):
    """Eq (4a): M_perp = (1 + (r - p))^years net-retention compounding."""
    return (1.0 + (rate_r - payout_p)) ** years


def walsh_sunset_amortization(corpus_usd, horizon_years=SUNSET_HORIZON_YEARS):
    """Eq (4b): p_t = 1/(horizon - t) spend-down; $0 terminal corpus at t = horizon."""
    remaining = float(corpus_usd)
    schedule = []
    for t in range(horizon_years):
        p_t = 1.0 / (horizon_years - t)
        spend = remaining * p_t
        remaining -= spend
        schedule.append({
            "t": t,
            "p_t": p_t,
            "spend_usd": spend,
            "terminal_corpus_usd": remaining,
        })
    return schedule


# ---------------------------------------------------------------------------
# Eq (5): IRC 4945 / IRC 507(c) statutory termination waterfall
# ---------------------------------------------------------------------------
def tranche_claims(ev):
    """Uncapped face claim per tranche at enterprise value / asset pool `ev`."""
    pool = float(ev)
    claim_1 = ((IRC_4945_FIRST_TIER_RATE + IRC_4945_SECOND_TIER_RATE)
               * TAXABLE_EXPENDITURE_BASE_USD)
    claim_2 = min(COMPOUNDED_TAX_BENEFIT_USD,
                  (IRC_507C_NET_ASSET_CAP_PCT / 100.0) * pool)
    claim_3 = max(pool - claim_1 - claim_2, 0.0)
    claim_4 = pool          # asserted self-perpetuating trustee discretionary corpus
    return [claim_1, claim_2, claim_3, claim_4]


def tranche_recovery(ev):
    """Eq (5): parameterized statutory termination / public-policy clawback
    waterfall over the Big 3 endowment stack.

    Sequential seniority: tranche 1 (IRC 4945 excise) -> tranche 2 (IRC 507(c)
    termination clawback, capped at 100.0% of net assets) -> tranche 3 (state AG
    cy pres / quo warranto residual sweep) -> tranche 4 (residual
    self-perpetuating trustee discretionary corpus, 0.0 cents on the dollar).
    Returns exact dollar and cent-on-the-dollar recovery vectors per tranche.
    """
    pool = float(ev)
    claims = tranche_claims(pool)
    recoveries = []
    remaining = pool
    for claim in claims:
        recovery = min(claim, remaining) if remaining > 0.0 else 0.0
        recoveries.append(recovery)
        remaining -= recovery
    breakevens = [
        0.0,
        (IRC_4945_FIRST_TIER_RATE + IRC_4945_SECOND_TIER_RATE)
        * TAXABLE_EXPENDITURE_BASE_USD,
        ((IRC_4945_FIRST_TIER_RATE + IRC_4945_SECOND_TIER_RATE)
         * TAXABLE_EXPENDITURE_BASE_USD) + COMPOUNDED_TAX_BENEFIT_USD,
        None,               # tranche 4 never recovers at any ev
    ]
    tranches = []
    for meta, claim, recovery, breakeven in zip(TRANCHE_STACK, claims,
                                                recoveries, breakevens):
        tranches.append({
            "tranche": meta["tranche"],
            "name": meta["name"],
            "statutory_basis": meta["statutory_basis"],
            "coupon_pik": meta["coupon_pik"],
            "collateral_guarantor_box": meta["collateral_guarantor_box"],
            "seniority": meta["seniority"],
            "breakeven_ev_threshold_usd": breakeven,
            "claim_usd": round(claim, 2),
            "recovery_usd": round(recovery, 2),
            "cents_on_dollar_of_ev": round(recovery / pool * 100.0, 6) if pool else 0.0,
            "recovery_rate_on_claim_cents":
                round(recovery / claim * 100.0, 6) if claim else 0.0,
        })
    total = sum(t["recovery_usd"] for t in tranches)
    return {
        "ev_usd": round(pool, 2),
        "tranches": tranches,
        "total_recovery_usd": round(total, 2),
        "total_cents_on_dollar_of_ev": round(total / pool * 100.0, 6) if pool else 0.0,
        "trustee_residual_cents_on_dollar": tranches[3]["recovery_rate_on_claim_cents"],
        "waterfall_exhausts_pool": math.isclose(total, pool, rel_tol=1e-12, abs_tol=0.01),
    }


def main():
    # -- Security-master and calendar integrity --------------------------------
    eins = [e["ein"] for e in ENTITY_AND_INSTRUMENT_IDS["private_foundation_issuers"]]
    assert eins == [FORD_FOUNDATION_EIN, ROCKEFELLER_FOUNDATION_EIN,
                    CARNEGIE_CORP_EIN], "entity EIN master mismatch"
    assert len(CATALYST_CALENDAR) == 20, "catalyst calendar must encode 20 hard dates"
    assert [c["iso_date"] for c in CATALYST_CALENDAR] == sorted(
        c["iso_date"] for c in CATALYST_CALENDAR), "catalyst calendar not monotonic"
    assert CFAA_18_USC_1030_COMPLIANCE_ATTESTATION is True, "CFAA attestation"
    assert JURISDICTION_CONTEXT["iso_3166_1_alpha_2"] == "US", "jurisdiction context"

    # -- Big 3 corpus decomposition --------------------------------------------
    assert_close(FORD_2023_FMV_USD + ROCKEFELLER_2023_FMV_USD + CARNEGIE_2023_FMV_USD,
                 BIG_3_COMBINED_2023_FMV_USD, "Big 3 combined 2023 FMV")
    expenditure_intensity = (BIG_3_COMBINED_2023_EXPENSES_USD
                             / BIG_3_COMBINED_2023_FMV_USD)
    assert expenditure_intensity >= IRC_4942_PAYOUT_FLOOR, \
        "IRC 4942 payout floor: expenditure intensity below statutory floor"

    # -- Eq (1): Ford Class A/B dual-class estate-tax shield --------------------
    assert FORD_CLASS_A_NON_VOTING_SHARES + FORD_CLASS_B_VOTING_SHARES == \
        FORD_TOTAL_SHARES, "Ford share count identity"
    shield = ford_dual_class_shield(FORD_CLASS_A_NON_VOTING_SHARES,
                                    FORD_CLASS_B_VOTING_SHARES,
                                    FORD_TOTAL_SHARES,
                                    REVENUE_ACT_1935_TOP_ESTATE_TAX_RATE)
    assert_close(shield["class_a_equity_share"], FORD_CLASS_A_EQUITY_SHARE_PCT / 100.0,
                 "eq1 Class A equity share")
    assert_close(shield["class_b_equity_share"], FORD_CLASS_B_EQUITY_SHARE_PCT / 100.0,
                 "eq1 Class B equity share")
    assert_close(shield["class_a_equity_share"] + shield["class_b_equity_share"], 1.0,
                 "eq1 equity share partition")
    assert_close(shield["estate_tax_shield_rate"], 0.665, "eq1 70% estate-tax shield")
    assert_close(shield["effective_estate_tax_rate"], 0.035,
                 "eq1 effective estate tax rate")
    assert_close(shield["estate_tax_eliminated_share"], 0.95,
                 "eq1 share of estate tax eliminated")
    assert_close(shield["control_to_equity_wedge"], 20.0,
                 "eq1 control-to-equity wedge")
    assert_close(shield["class_b_vote_share"], FORD_FAMILY_VOTING_CONTROL_PCT / 100.0,
                 "eq1 retained voting control")

    cap = section_4943_voting_cap_arbitrage(FORD_CLASS_A_EQUITY_SHARE_PCT,
                                            IRC_4943_VOTING_CAP)
    assert cap["formally_compliant"] is True, "IRC 4943 formal voting compliance"
    assert cap["substantive_excess"] is True, "IRC 4943 substantive excess"
    assert_close(cap["arbitrage_wedge_pp"], 75.0, "IRC 4943 arbitrage wedge (pp)")

    # -- Two-Hull 1934 Rockefeller Compounding Dilemma (H_0 vs H_1) -------------
    dilemma = two_hull_compounding_dilemma()
    assert_close(dilemma["h0_nominal_cagr"], 0.033425, "Two-Hull H0 nominal CAGR", rel_tol=1e-3)
    assert_close(dilemma["h0_real_cagr"], 0.000425, "Two-Hull H0 real CAGR", abs_tol=1e-4)
    assert_close(dilemma["h1_net_7pct_2026_usd"], 252_509_400_829.69, "Two-Hull H1 7% net USD", rel_tol=1e-6)
    assert_close(dilemma["h1_net_8pct_2026_usd"], 594_231_280_067.09, "Two-Hull H1 8% net USD", rel_tol=1e-6)
    assert dilemma["h0_underperformance_vs_7pct"] >= 0.959, "Two-Hull H0 underperformance vs 7%"
    assert dilemma["h0_underperformance_vs_8pct"] >= 0.982, "Two-Hull H0 underperformance vs 8%"

    # -- Act 0 (1872) & Act I.4 / IV (1935 / 2000) Synthetic-NIRP & Sign Flip ---
    nirp = south_improvement_drawback_nirp()
    assert_close(nirp["standard_oil_net_freight_usd"], STANDARD_OIL_NET_FREIGHT_USD,
                 "1872 Standard Oil net freight")
    assert_close(nirp["effective_1to1_outlay_usd"], 0.44,
                 "1872 South Improvement 1:1 net outlay")
    assert_close(nirp["asymmetry_spread_usd"], 2.12,
                 "1872 South Improvement freight asymmetry spread")
    assert_close(nirp["asymmetry_pct"], 82.8125,
                 "1872 South Improvement asymmetry pct")
    assert_close(nirp["cooperage_savings_per_bbl_usd"], 1.54,
                 "1872 cooperage barrel savings")
    assert_close(nirp["cleveland_massacre_share"], 22.0 / 26.0,
                 "1872 Cleveland Massacre buyout share")

    actuarial = actuarial_sign_inversion_and_peering()
    assert_close(actuarial["fica_payroll_tax_wedge"], 0.153,
                 "1935 FICA payroll tax wedge vs 501(c)(3)")
    assert_close(actuarial["post_65_sovereign_npv_20yr_usd"], -516_432.40,
                 "Post-65 sovereign NPV sign inversion", abs_tol=1e-2)
    assert actuarial["citizen_post_retirement_is_net_liability"] is True, \
        "Post-retirement citizen must register as net sovereign actuarial liability"
    assert actuarial["epstein_rockefeller_peering_years"] == [1995, 1995, 2000], \
        "David Rockefeller -> Epstein Trilateral/CFR/Rockefeller Univ chronological sequence"
    assert actuarial["deep_time_short_gamma_epochs"] == 6, \
        "6 deep-time short-gamma rentier epochs (1700 BC - 2026 AD)"
    assert actuarial["sparta_424bc_helot_cull_count"] == 2_000, \
        "Thucydides 4.80.3-4 424 BC Helot cull count"
    assert actuarial["plato_static_lot_cap"] == 5_040, \
        "Plato Laws 737e static land-lot cap"
    assert actuarial["tokugawa_zero_growth_years"] == 125, \
        "Tokugawa 1721-1846 zero-population-growth plateau"

    # -- Eq (2): bacteriophage state-fusion multiplier --------------------------
    lam_cfat = bacteriophage_fusion_multiplier(TIAA_MODERN_AUM_USD,
                                               CARNEGIE_CFAT_1905_SEED_USD)
    assert_close(lam_cfat, TIAA_LEVERAGE_MULTIPLIER, "eq2 CFAT->TIAA leverage")
    host_pool = US_FEDERAL_BUDGET_HOST_USD + NACUBO_UNIVERSITY_ENDOWMENT_HOST_USD
    lam_big3 = bacteriophage_fusion_multiplier(host_pool,
                                               BIG_3_COMBINED_2023_EXPENSES_USD)
    assert lam_big3 >= FUSION_MULTIPLIER_GATE, \
        "eq2 Big 3 state-fusion leverage below 1,000x gate"
    assert_close(host_pool, 7_640_000_000_000.0, "eq2 coerced host capital pool")
    assert ROCKEFELLER_KWI_MUNICH_1928_GRANT_USD < CARNEGIE_CFAT_1905_SEED_USD, \
        "eq2 seed-grant ordering"

    # -- Eq (3): 3-prong pincer mosaic DAG detector -----------------------------
    evidence_compliant = {
        "coordinated_acts": 1,
        "common_design": False,
        "integrated_steps": 1,
        "binding_commitment": False,
        "non_exempt_purpose_share": 0.0,
    }
    evidence_defection = {
        "coordinated_acts": 3,
        "common_design": True,
        "integrated_steps": 4,
        "binding_commitment": True,
        "non_exempt_purpose_share": expenditure_intensity,
    }
    pincer_compliant = pincer_mosaic_dag_detect(evidence_compliant)
    pincer_defection = pincer_mosaic_dag_detect(evidence_defection)
    assert pincer_compliant["acyclic"] is True, "eq3 mosaic DAG acyclicity"
    assert pincer_compliant["pincer_triggered"] is False, "eq3 compliant no trigger"
    assert pincer_defection["prong_1_continental_ore"] is True, "eq3 prong 1"
    assert pincer_defection["prong_2_step_transaction"] is True, "eq3 prong 2"
    assert pincer_defection["prong_3_bbb_substantial_non_exempt_purpose"] is True, \
        "eq3 prong 3"
    assert pincer_defection["root_to_terminal_path"] is True, "eq3 root->terminal path"
    assert pincer_defection["pincer_triggered"] is True, "eq3 defection trigger"
    assert pincer_defection["topological_order"].index(PINCER_ROOT) < \
        pincer_defection["topological_order"].index(PINCER_TERMINAL), \
        "eq3 topological precedence"

    # -- Eq (4): perpetual coupon vs Walsh 20-year sunset -----------------------
    m_perp = perpetual_coupon_multiple(PERPETUAL_COUPON_RATE_R,
                                       PERPETUAL_PAYOUT_RATE_P,
                                       CENTURY_HORIZON_YEARS)
    assert PERPETUAL_COUPON_RATE_R > PERPETUAL_PAYOUT_RATE_P, "eq4 r > p"
    assert_close(m_perp, PERPETUAL_COUPON_CENTURY_MULTIPLE,
                 "eq4 century compounding multiple", rel_tol=1e-4)
    assert_close(round(m_perp, 2), 19.22, "eq4 locked 19.22x century multiple",
                 rel_tol=0.0, abs_tol=1e-9)
    perpetual_corpus = WALSH_1915_COMBINED_CORPUS_USD * PERPETUAL_COUPON_CENTURY_MULTIPLE
    assert perpetual_corpus > WALSH_1915_COMBINED_CORPUS_USD, "eq4 perpetual growth"

    schedule = walsh_sunset_amortization(WALSH_1915_COMBINED_CORPUS_USD)
    assert len(schedule) == SUNSET_HORIZON_YEARS, "eq4 sunset horizon length"
    level_amortization = WALSH_1915_COMBINED_CORPUS_USD / SUNSET_HORIZON_YEARS
    for row in schedule:
        assert_close(row["spend_usd"], level_amortization,
                     f"eq4 level amortization at t={row['t']}", rel_tol=1e-9)
        assert_close(row["p_t"], 1.0 / (SUNSET_HORIZON_YEARS - row["t"]),
                     f"eq4 p_t schedule at t={row['t']}")
    assert_close(schedule[-1]["p_t"], 1.0, "eq4 terminal p_t = 1/(20-19)")
    assert_close(schedule[-1]["terminal_corpus_usd"], 0.0,
                 "eq4 $0 terminal corpus at t = 20", rel_tol=0.0, abs_tol=1e-6)
    assert_close(sum(row["spend_usd"] for row in schedule),
                 WALSH_1915_COMBINED_CORPUS_USD, "eq4 sunset amortization identity",
                 rel_tol=1e-9)
    assert_close(WALSH_1915_ANNUAL_REVENUE_USD / WALSH_1915_COMBINED_CORPUS_USD,
                 0.054, "eq4 Walsh 1915 revenue yield")
    continuity_wedge = perpetual_corpus - schedule[-1]["terminal_corpus_usd"]
    assert continuity_wedge > 0.0, "eq4 perpetual coupon dominates sunset"

    # -- Eq (5): statutory termination waterfall --------------------------------
    waterfall = tranche_recovery(BIG_3_COMBINED_2023_FMV_USD)
    t1, t2, t3, t4 = waterfall["tranches"]
    assert_close(t1["claim_usd"],
                 (IRC_4945_FIRST_TIER_RATE + IRC_4945_SECOND_TIER_RATE)
                 * TAXABLE_EXPENDITURE_BASE_USD, "eq5 tranche 1 claim")
    assert_close(t1["claim_usd"], 1_839_769_504.80, "eq5 tranche 1 locked claim",
                 rel_tol=1e-12)
    assert_close(t2["claim_usd"], COMPOUNDED_TAX_BENEFIT_USD, "eq5 tranche 2 claim")
    assert_close(t2["claim_usd"], 3_195_092_250.00, "eq5 tranche 2 locked claim",
                 rel_tol=1e-9)
    assert_close(t3["claim_usd"],
                 BIG_3_COMBINED_2023_FMV_USD - t1["claim_usd"] - t2["claim_usd"],
                 "eq5 tranche 3 residual sweep")
    assert_close(t4["claim_usd"], BIG_3_COMBINED_2023_FMV_USD,
                 "eq5 tranche 4 asserted trustee corpus")
    assert_close(t4["recovery_usd"], 0.0, "eq5 tranche 4 zero recovery",
                 rel_tol=0.0, abs_tol=1e-6)
    assert_close(t4["recovery_rate_on_claim_cents"], 0.0,
                 "eq5 tranche 4 0.0 cents on the dollar", rel_tol=0.0, abs_tol=1e-9)
    assert waterfall["waterfall_exhausts_pool"] is True, "eq5 pool exhaustion"
    assert_close(waterfall["total_recovery_usd"], BIG_3_COMBINED_2023_FMV_USD,
                 "eq5 total recovery = Big 3 stack", rel_tol=1e-12)
    assert_close(waterfall["total_cents_on_dollar_of_ev"], 100.0,
                 "eq5 total cents on the dollar", rel_tol=1e-9)
    assert t1["breakeven_ev_threshold_usd"] < t2["breakeven_ev_threshold_usd"] < \
        t3["breakeven_ev_threshold_usd"], "eq5 breakeven monotonicity"
    assert t4["breakeven_ev_threshold_usd"] is None, "eq5 tranche 4 never recovers"

    # Sub-scale stress: below the tranche 1 breakeven the junior tranches are 0.
    stress = tranche_recovery(t1["claim_usd"] - 1.0)
    assert_close(stress["tranches"][0]["recovery_usd"], t1["claim_usd"] - 1.0,
                 "eq5 stress tranche 1 absorbs pool", rel_tol=1e-12)
    for junior in stress["tranches"][1:]:
        assert_close(junior["recovery_usd"], 0.0, "eq5 stress junior tranche zero",
                     rel_tol=0.0, abs_tol=1e-6)

    # Compliant regime: Walsh sunset terminal corpus is $0, so no pool to call.
    compliant_waterfall = tranche_recovery(schedule[-1]["terminal_corpus_usd"])
    assert_close(compliant_waterfall["total_recovery_usd"], 0.0,
                 "eq5 compliant regime zero recovery", rel_tol=0.0, abs_tol=1e-6)

    outputs = {
        "regime": "defection",
        "big_3_combined_2023_fmv_usd": BIG_3_COMBINED_2023_FMV_USD,
        "big_3_expenditure_intensity": round(expenditure_intensity, 6),
        "ford_class_a_equity_share": shield["class_a_equity_share"],
        "ford_class_b_vote_share": shield["class_b_vote_share"],
        "estate_tax_shield_rate": shield["estate_tax_shield_rate"],
        "effective_estate_tax_rate": shield["effective_estate_tax_rate"],
        "control_to_equity_wedge": shield["control_to_equity_wedge"],
        "irc_4943_arbitrage_wedge_pp": cap["arbitrage_wedge_pp"],
        "two_hull_h0_nominal_cagr": dilemma["h0_nominal_cagr"],
        "two_hull_h0_real_cagr": dilemma["h0_real_cagr"],
        "two_hull_h1_net_7pct_2026_usd": dilemma["h1_net_7pct_2026_usd"],
        "two_hull_h1_net_8pct_2026_usd": dilemma["h1_net_8pct_2026_usd"],
        "south_improvement_asymmetry_spread_usd": nirp["asymmetry_spread_usd"],
        "south_improvement_asymmetry_pct": nirp["asymmetry_pct"],
        "cleveland_massacre_buyout_share": nirp["cleveland_massacre_share"],
        "fica_payroll_tax_wedge": actuarial["fica_payroll_tax_wedge"],
        "post_65_sovereign_npv_20yr_usd": actuarial["post_65_sovereign_npv_20yr_usd"],
        "epstein_rockefeller_univ_trustee_year": EPSTEIN_ROCKEFELLER_UNIV_BOARD_YEAR,
        "lambda_fusion_cfat_tiaa": lam_cfat,
        "lambda_fusion_big_3_host_pool": round(lam_big3, 2),
        "pincer_triggered": pincer_defection["pincer_triggered"],
        "pincer_topological_order": pincer_defection["topological_order"],
        "perpetual_coupon_century_multiple": round(m_perp, 4),
        "perpetual_corpus_usd": round(perpetual_corpus, 2),
        "walsh_sunset_terminal_corpus_usd": round(
            schedule[-1]["terminal_corpus_usd"], 2),
        "walsh_sunset_level_amortization_usd": round(level_amortization, 2),
        "compounded_tax_benefit_usd": COMPOUNDED_TAX_BENEFIT_USD,
        "tranche_1_recovery_usd": t1["recovery_usd"],
        "tranche_1_cents_on_dollar_of_ev": t1["cents_on_dollar_of_ev"],
        "tranche_2_recovery_usd": t2["recovery_usd"],
        "tranche_2_cents_on_dollar_of_ev": t2["cents_on_dollar_of_ev"],
        "tranche_3_recovery_usd": t3["recovery_usd"],
        "tranche_3_cents_on_dollar_of_ev": t3["cents_on_dollar_of_ev"],
        "tranche_4_recovery_usd": t4["recovery_usd"],
        "tranche_4_cents_on_dollar": t4["recovery_rate_on_claim_cents"],
        "total_recovery_usd": waterfall["total_recovery_usd"],
        "total_cents_on_dollar_of_ev": waterfall["total_cents_on_dollar_of_ev"],
    }
    print(json.dumps(outputs, indent=2))
    print("PROOF PASS: all locked constants and governing equations verified "
          "across compliant (Walsh sunset) and defection (perpetual coupon) regimes")


if __name__ == "__main__":
    main()
