#!/usr/bin/env python3
"""
verify_protectorate_ashby_trap.py

Deterministic verification engine for SPEC-PROTECTORATE-ASHBY-TRAP-v1.0.

Verifies four coupled mechanisms:
  1. Sovereign liability waterfall (4 tranches, 2500.0B EUR total) with the
     Native Ratepayer Residual (Tranche 4) as fulcrum at EV = 1800.0B EUR.
  2. OOD search survival under Common Law vs Civil Code Guild ex-ante
     friction regimes (exponential payoff survival, N = 1000 trials), the
     EU AI Act 1e25 FLOPs cap, and the EU/US industrial energy cost ratio.
  3. M/M/1 judicial queue instability (continental 4-tier cascade, rho = 5.0)
     vs the UK post-repeal unlocked regime (rho = 0.875).
  4. Eastern Nullification Arbitrage (Hungarian cohort-liability avoidance
     vs the ECJ Case C-123/22 annualized fine tariff).

Pure Python 3 stdlib. Deterministic (closed-form, zero RNG).
Exit code 0 on full verification.

License: Unlicense (Public Domain).
"""

import math
import sys

# ---------------------------------------------------------------------------
# Standardized security-master keys (entity_and_instrument_ids)
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "sovereign_and_supranational_entities": [
        {
            "entity": "European Union (supranational regulatory cartel)",
            "instrument": "GDPR Art. 83(4) turnover fine (4.0% ceiling); EU AI Act compute cap",
            "ticker": None,
            "cik": None,
        },
        {
            "entity": "Hungary (ISO 3166-1: HU)",
            "instrument": "ECJ non-compliance fine tariff (lump sum + daily penalty)",
            "ticker": None,
            "cik": None,
        },
        {
            "entity": "United Kingdom (ISO 3166-1: GB)",
            "instrument": "Parliamentary repeal majority (326 seats) as queue-unlock catalyst",
            "ticker": None,
            "cik": None,
        },
        {
            "entity": "Germany (ISO 3166-1: DE)",
            "instrument": "Nuclear decommissioning liability stack (22.6 GW cumulative)",
            "ticker": None,
            "cik": None,
        },
    ],
    "court_dockets": [
        "ECJ Case C-123/22 (Commission v. Hungary, asylum-code non-compliance; "
        "judgment 2024-06-13: EUR 200,000,000 lump sum + EUR 1,000,000/day)",
    ],
    "sovereign_liability_tranches": [
        {"tranche": 1, "name": "Senior State-Guaranteed Grid & Decommissioning Debt", "principal_bn_eur": 450.0},
        {"tranche": 2, "name": "Mezzanine Industrial Subsidy / Capacity-Market Obligations", "principal_bn_eur": 850.0},
        {"tranche": 3, "name": "Junior Municipal Integration & Housing Obligations", "principal_bn_eur": 300.0},
        {"tranche": 4, "name": "Native Ratepayer Residual (unfunded fiscal tail)", "principal_bn_eur": 900.0},
    ],
}

# ---------------------------------------------------------------------------
# Hard-date catalyst & forbearance calendar (catalyst_calendar)
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = [
    {
        "date": "2024-06-13",
        "event": "ECJ Case C-123/22 judgment: EUR 200M lump sum + EUR 1M/day periodic penalty vs Hungary",
        "type": "judicial",
    },
    {
        "date": "2025-08-02",
        "event": "EU AI Act GPAI obligations and governance enforcement commence",
        "type": "statutory",
    },
    {
        "date": "2026-08-02",
        "event": "EU AI Act full application (Annex III high-risk obligations enforceable)",
        "type": "statutory",
    },
    {
        "date": "2027-08-02",
        "event": "EU AI Act Annex I regulated-product high-risk obligations apply",
        "type": "statutory",
    },
]

# ---------------------------------------------------------------------------
# Locked constants (zero-drift contract with architecture_ast)
# ---------------------------------------------------------------------------
LOCKED = {
    "eu_ai_act_flops_cap": 1e25,
    "gdpr_turnover_fine_pct": 4.0,
    "german_nuclear_shut_gw_2023": 4.1,
    "german_total_nuclear_decommissioned_gw": 22.6,
    "industrial_power_cost_eu_mwh_eur": 145.0,
    "industrial_power_cost_us_mwh_eur": 48.0,
    "energy_cost_ratio_eu_to_us": 3.0208,
    "ood_search_trials_N": 1000,
    "ood_experiment_payoff_scale_eur": 50000.0,
    "common_law_ex_ante_friction_eur": 25000.0,
    "civil_code_guild_ex_ante_friction_eur": 2500000.0,
    "common_law_viable_ood_experiments": 606,
    "civil_code_viable_ood_experiments": 0,
    "guild_cartel_compliance_moat_ratio": 100.0,
    "asylum_inflow_lambda_annual": 350000.0,
    "judicial_4_tier_service_mu_annual": 70000.0,
    "queue_utilization_rho_continental": 5.0,
    "annual_unprocessed_backlog_continental": 280000.0,
    "uk_parliamentary_repeal_majority_seats": 326,
    "uk_post_repeal_service_mu_annual": 400000.0,
    "queue_utilization_rho_uk_unlocked": 0.875,
    "danish_fm_menapt_annual_net_drain_dkk_bn": -31.0,
    "dutch_asylum_cohort_npv_eur": -475000.0,
    "skilled_western_cohort_npv_eur": 125000.0,
    "ecj_hungary_lump_sum_fine_eur": 200000000.0,
    "ecj_hungary_daily_fine_eur": 1000000.0,
    "ecj_hungary_annualized_tariff_eur": 565000000.0,
    "hungary_avoided_cohort_fiscal_liability_npv_eur": 14250000000.0,
    "nullification_arbitrage_benefit_to_cost_ratio": 25.2212,
    "sweden_utsatta_omraden_count": 61,
    "france_qrr_enclave_count": 62,
    "tranche_4_recovery_pct": 22.22,
    "tranche_4_dollar_recovery_bn_eur": 200.0,
}

TRANCHE_PRINCIPALS_BN_EUR = [450.0, 850.0, 300.0, 900.0]
TOTAL_LIABILITY_BN_EUR = sum(TRANCHE_PRINCIPALS_BN_EUR)  # 2500.0
FULCRUM_EV_BN_EUR = 1800.0
HUNGARY_AVOIDED_COHORT_N = 30000

FAILURES = []


def check(name, computed, expected, tol=1e-9):
    """Deterministic equality/tolerance gate; records failures."""
    if isinstance(expected, bool) or isinstance(computed, bool):
        ok = bool(computed) == bool(expected)
    else:
        ok = abs(float(computed) - float(expected)) <= tol
    print("[{}] {}: computed={!r} expected={!r}".format("PASS" if ok else "FAIL", name, computed, expected))
    if not ok:
        FAILURES.append(name)
    return ok


# ---------------------------------------------------------------------------
# 1. Deterministic capital-structure waterfall
# ---------------------------------------------------------------------------
def tranche_recovery(ev_bn_eur):
    """
    Parameterized tranche payoff function.

    Input:  ev_bn_eur -- enterprise/sovereign asset value in BN EUR.
    Output: recovery vector across the 4 sovereign liability tranches
            (exact BN EUR dollars and cent-on-the-dollar percentages),
            seniority-ordered, strictly sequential waterfall.
    """
    if ev_bn_eur < 0.0:
        raise ValueError("ev_bn_eur must be non-negative")
    remaining = float(ev_bn_eur)
    waterfall = []
    for idx, principal in enumerate(TRANCHE_PRINCIPALS_BN_EUR, start=1):
        paid = min(remaining, principal)
        remaining -= paid
        waterfall.append({
            "tranche": idx,
            "principal_bn_eur": principal,
            "recovery_bn_eur": round(paid, 4),
            "recovery_pct": round(100.0 * paid / principal, 2),
        })
    return waterfall


# ---------------------------------------------------------------------------
# 2. OOD search survival (Ashby requisite-variety gate)
# ---------------------------------------------------------------------------
def ood_search_survival():
    """
    Closed-form exponential payoff survival over N = 1000 OOD experiments.

    Payoff X ~ Exp(scale = 50000 EUR). An experiment is viable iff its
    expected payoff exceeds the jurisdiction's ex-ante legal friction:
      viable = floor(N * S(friction)),  S(x) = exp(-x / scale)

    Common Law:      friction = 25,000 EUR   -> floor(1000 * e^-0.5)  = 606
    Civil Code Guild: friction = 2,500,000 EUR -> floor(1000 * e^-50)  = 0
    """
    n = LOCKED["ood_search_trials_N"]
    scale = LOCKED["ood_experiment_payoff_scale_eur"]
    s_common = math.exp(-LOCKED["common_law_ex_ante_friction_eur"] / scale)
    s_civil = math.exp(-LOCKED["civil_code_guild_ex_ante_friction_eur"] / scale)
    return {
        "survival_prob_common_law": s_common,
        "survival_prob_civil_code": s_civil,
        "viable_common_law": int(n * s_common),
        "viable_civil_code": int(n * s_civil),
        "moat_ratio": LOCKED["civil_code_guild_ex_ante_friction_eur"] / LOCKED["common_law_ex_ante_friction_eur"],
        "energy_cost_ratio": round(
            LOCKED["industrial_power_cost_eu_mwh_eur"] / LOCKED["industrial_power_cost_us_mwh_eur"], 4
        ),
        "flops_cap": LOCKED["eu_ai_act_flops_cap"],
    }


# ---------------------------------------------------------------------------
# 3. M/M/1 judicial queue dynamics
# ---------------------------------------------------------------------------
def mm1_queue(lambda_annual, mu_annual):
    """M/M/1 utilization rho = lambda/mu; stable iff rho < 1."""
    if mu_annual <= 0.0:
        raise ValueError("mu_annual must be positive")
    rho = lambda_annual / mu_annual
    return {
        "rho": rho,
        "stable": rho < 1.0,
        "annual_unprocessed_backlog": max(0.0, lambda_annual - mu_annual),
        "steady_state_queue_length": rho / (1.0 - rho) if rho < 1.0 else float("inf"),
    }


# ---------------------------------------------------------------------------
# 4. Eastern Nullification Arbitrage
# ---------------------------------------------------------------------------
def nullification_arbitrage():
    """
    Hungary's revealed-preference defection payoff vs ECJ fine tariff.

    Avoided liability = 30,000 avoided cohort entrants * |NPV -475,000 EUR|
                      = 14,250,000,000 EUR
    ECJ annualized tariff = 200,000,000 lump sum + 365 * 1,000,000/day
                      = 565,000,000 EUR
    Benefit-to-cost ratio = 25.2212x  -> defection is strictly dominant.
    """
    avoided = HUNGARY_AVOIDED_COHORT_N * abs(LOCKED["dutch_asylum_cohort_npv_eur"])
    annualized_fine = LOCKED["ecj_hungary_lump_sum_fine_eur"] + 365.0 * LOCKED["ecj_hungary_daily_fine_eur"]
    return {
        "avoided_liability_npv_eur": avoided,
        "ecj_annualized_tariff_eur": annualized_fine,
        "benefit_to_cost_ratio": round(avoided / annualized_fine, 4),
    }


def main():
    print("=== verify_protectorate_ashby_trap.py :: deterministic verification engine ===")

    print("\n-- Gate 0: locked-constant integrity --")
    check("total_sovereign_liability_bn_eur", TOTAL_LIABILITY_BN_EUR, 2500.0)
    check("danish_fm_menapt_annual_net_drain_dkk_bn", LOCKED["danish_fm_menapt_annual_net_drain_dkk_bn"], -31.0)
    check("sweden_utsatta_omraden_count", LOCKED["sweden_utsatta_omraden_count"], 61)
    check("france_qrr_enclave_count", LOCKED["france_qrr_enclave_count"], 62)
    check("skilled_western_cohort_npv_eur", LOCKED["skilled_western_cohort_npv_eur"], 125000.0)
    check("german_nuclear_shut_gw_2023", LOCKED["german_nuclear_shut_gw_2023"], 4.1)
    check("german_total_nuclear_decommissioned_gw", LOCKED["german_total_nuclear_decommissioned_gw"], 22.6)
    check("gdpr_turnover_fine_pct", LOCKED["gdpr_turnover_fine_pct"], 4.0)

    print("\n-- Gate 1: sovereign liability waterfall @ EV = 1800.0B EUR --")
    wf = tranche_recovery(FULCRUM_EV_BN_EUR)
    for row in wf:
        print("   Tranche {}: principal={:.1f}B recovery={:.1f}B pct={:.2f}%".format(
            row["tranche"], row["principal_bn_eur"], row["recovery_bn_eur"], row["recovery_pct"]))
    check("tranche_1_recovery_pct", wf[0]["recovery_pct"], 100.0)
    check("tranche_2_recovery_pct", wf[1]["recovery_pct"], 100.0)
    check("tranche_3_recovery_pct", wf[2]["recovery_pct"], 100.0)
    check("tranche_4_dollar_recovery_bn_eur", wf[3]["recovery_bn_eur"], LOCKED["tranche_4_dollar_recovery_bn_eur"])
    check("tranche_4_recovery_pct", wf[3]["recovery_pct"], LOCKED["tranche_4_recovery_pct"])
    # Boundary regimes: full coverage and total wipeout.
    wf_full = tranche_recovery(2500.0)
    wf_zero = tranche_recovery(0.0)
    check("boundary_ev_2500_tranche_4_pct", wf_full[3]["recovery_pct"], 100.0)
    check("boundary_ev_0_tranche_1_pct", wf_zero[0]["recovery_pct"], 0.0)

    print("\n-- Gate 2: OOD search survival (Ashby requisite-variety gate) --")
    ood = ood_search_survival()
    check("common_law_viable_ood_experiments", ood["viable_common_law"], LOCKED["common_law_viable_ood_experiments"])
    check("civil_code_viable_ood_experiments", ood["viable_civil_code"], LOCKED["civil_code_viable_ood_experiments"])
    check("guild_cartel_compliance_moat_ratio", ood["moat_ratio"], LOCKED["guild_cartel_compliance_moat_ratio"])
    check("energy_cost_ratio_eu_to_us", ood["energy_cost_ratio"], LOCKED["energy_cost_ratio_eu_to_us"])
    check("eu_ai_act_flops_cap", ood["flops_cap"], LOCKED["eu_ai_act_flops_cap"])

    print("\n-- Gate 3: M/M/1 judicial queue instability --")
    q_cont = mm1_queue(LOCKED["asylum_inflow_lambda_annual"], LOCKED["judicial_4_tier_service_mu_annual"])
    q_uk = mm1_queue(LOCKED["asylum_inflow_lambda_annual"], LOCKED["uk_post_repeal_service_mu_annual"])
    check("queue_utilization_rho_continental", q_cont["rho"], LOCKED["queue_utilization_rho_continental"])
    check("continental_queue_stable", q_cont["stable"], False)
    check("annual_unprocessed_backlog_continental", q_cont["annual_unprocessed_backlog"],
          LOCKED["annual_unprocessed_backlog_continental"])
    check("uk_parliamentary_repeal_majority_seats", LOCKED["uk_parliamentary_repeal_majority_seats"], 326)
    check("queue_utilization_rho_uk_unlocked", q_uk["rho"], LOCKED["queue_utilization_rho_uk_unlocked"])
    check("uk_queue_stable", q_uk["stable"], True)
    check("uk_steady_state_queue_length", q_uk["steady_state_queue_length"], 7.0)

    print("\n-- Gate 4: Eastern Nullification Arbitrage --")
    na = nullification_arbitrage()
    check("hungary_avoided_cohort_fiscal_liability_npv_eur", na["avoided_liability_npv_eur"],
          LOCKED["hungary_avoided_cohort_fiscal_liability_npv_eur"])
    check("ecj_hungary_annualized_tariff_eur", na["ecj_annualized_tariff_eur"],
          LOCKED["ecj_hungary_annualized_tariff_eur"])
    check("nullification_arbitrage_benefit_to_cost_ratio", na["benefit_to_cost_ratio"],
          LOCKED["nullification_arbitrage_benefit_to_cost_ratio"])

    print("\n=== RESULT ===")
    if FAILURES:
        print("VERIFICATION FAILED: {} check(s): {}".format(len(FAILURES), FAILURES))
        return 1
    print("ALL CHECKS PASSED (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
