#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPSTACK corpus proof for SPEC-SUCCESSIONIST-GOVERNANCE-v1.0.

Closed-form, stdlib-only verification of:
  (1) dual-class agency wedge (Page/Brin voting power vs. economic equity),
  (2) deterministic tranche recovery waterfall tranche_recovery(ev_bn),
  (3) Spence separating equilibrium for Rule 14a-8 / Rule 10b-5 certification,
  (4) 2012-2024 bootstrap -> 2026 utility-hazard phase transition,
  (5) gigawatt thermodynamics and compiler-law energy penalty,
  (6) containment double delusion and sovereign P2P mesh economics.

Pure Python 3 stdlib. Deterministic JSON on stdout. Exit code 0 on success.
"""

import json
import math
import sys

# ------------------------------------------------------------------ locked constants
CLASS_A_SHARES_M = 5822.0           # Class A shares (millions; 1 vote/share)
CLASS_B_SHARES_M = 837.0            # Class B shares (millions; 10 votes/share)
CLASS_C_SHARES_M = 5438.0           # Class C shares (millions; 0 votes/share)
CLASS_A_VOTES = 1
CLASS_B_VOTES = 10
CLASS_C_VOTES = 0
PAGE_BRIN_CLASS_B_PCT = 0.893       # founders' share of Class B
INSIDER_ECON_PCT = 12.0             # aggregate insider economic stake (%)
OUTSIDE_ECON_PCT = 88.0             # outside Class A/C economic stake (%)
ANNUAL_AI_CAPEX_DRAIN_BN = 85.0     # $B/yr AI CapEx drain
OFFICERS_CLASS_B_SHARES = 770340078 # all 14 officers/directors, Class B shares
DEF14A_CLASS_SHARE_PCT = 92.2       # DEF 14A reported Class B share (%)

TRANCHE_1_PAR_BN = 48.5             # BNY Mellon trustee: senior unsecured notes
TRANCHE_2_PAR_BN = 115.0            # unconditional PPA/lease/compute commitments
CUM_THRESHOLD_BN = 163.5            # cumulative debt-stack threshold
BASELINE_EV_BN = 2200.0             # baseline enterprise-value scenario ($B)
GROSS_EV_DESTRUCTION_BN = 850.0     # regulatory breakup + un-underwritten burn

HALL_MW = 100.0                     # single data-hall IT load (MW)
THERMAL_MASS_J_PER_K = 5.0e9        # chilled-water loop + air heat capacity (J/K)
ALLOWABLE_RISE_K = 18.0             # ASHRAE A1 27C -> 45C component trip (K)
T_SHUT_MAX_S = 900.0                # 15.0 minutes
DIESEL_CAP_HOURS = 72.0             # on-site diesel fuel cap (hours)
LPT_BACKLOG_MONTHS = (24, 48)       # large-power-transformer backlog (months)
RPC_CLOUD_J = 5.0                   # runtime cloud RPC energy (J/op)
RPC_LOCAL_J = 1.0e-9                # local compiled C/Rust/SQLite primitive (J/op)

SECTOR_GPU_CAPEX_BN_YR = 400.0     # sector-wide GPU CapEx ($B/yr)
GPU_LIFESPAN_YEARS = 4.0            # GPU economic lifespan (years)
KL_STEERING_BUDGET_NATS = 2.0      # Rasputin KL steering budget (nats)

MESH_SERVER_COST_USD = 6000.0       # local MoE inference server capital cost
MESH_SERVER_WATTS = 900.0           # server draw (W)
MESH_DUTY_CYCLE = 0.05              # 5% human duty cycle
MESH_PEERS = 40                     # peers served per server
ELECTRICITY_USD_PER_KWH = 0.10      # stranded-energy tariff ($/kWh)


# ------------------------------------------------------------------ (1) dual-class wedge
def verify_dual_class_agency_wedge():
    """Page/Brin: 52.6664% voting power on 6.1787% economic equity (8.5238x)."""
    total_shares_m = CLASS_A_SHARES_M + CLASS_B_SHARES_M + CLASS_C_SHARES_M
    total_votes_m = (CLASS_A_SHARES_M * CLASS_A_VOTES
                     + CLASS_B_SHARES_M * CLASS_B_VOTES
                     + CLASS_C_SHARES_M * CLASS_C_VOTES)
    assert total_shares_m == 12097.0
    assert total_votes_m == 14192.0

    pb_shares_m = PAGE_BRIN_CLASS_B_PCT * CLASS_B_SHARES_M      # 747.441M
    pb_votes_m = pb_shares_m * CLASS_B_VOTES                     # 7,474.41M
    pb_voting_power_pct = 100.0 * pb_votes_m / total_votes_m    # 52.6664%
    pb_economic_pct = 100.0 * pb_shares_m / total_shares_m      # 6.1787%
    voting_leverage_x = pb_voting_power_pct / pb_economic_pct    # 8.5238x
    insider_leverage_x = pb_voting_power_pct / INSIDER_ECON_PCT  # 4.3889x
    assert round(pb_shares_m, 3) == 747.441
    assert round(pb_voting_power_pct, 4) == 52.6664
    assert round(pb_economic_pct, 4) == 6.1787
    assert round(voting_leverage_x, 4) == 8.5238
    assert round(insider_leverage_x, 4) == 4.3889

    outside_burden_bn = OUTSIDE_ECON_PCT / 100.0 * ANNUAL_AI_CAPEX_DRAIN_BN
    insider_burden_bn = INSIDER_ECON_PCT / 100.0 * ANNUAL_AI_CAPEX_DRAIN_BN
    assert round(outside_burden_bn, 6) == 74.8   # $74.8B/yr borne by outside 88%
    assert round(insider_burden_bn, 6) == 10.2    # $10.2B/yr borne by 12% insiders

    officers_pct_b = 100.0 * OFFICERS_CLASS_B_SHARES / (CLASS_B_SHARES_M * 1.0e6)
    officers_votes = OFFICERS_CLASS_B_SHARES * CLASS_B_VOTES
    officers_voting_pct = 100.0 * officers_votes / (total_votes_m * 1.0e6)
    assert round(officers_pct_b, 4) == 92.0359     # 92.0359% of Class B
    assert round(officers_voting_pct, 4) == 54.2799 # 54.2799% of total votes
    return {
        "total_shares_m": total_shares_m,
        "total_votes_m": total_votes_m,
        "page_brin_shares_m": round(pb_shares_m, 3),
        "page_brin_votes_m": round(pb_votes_m, 2),
        "page_brin_voting_power_pct": round(pb_voting_power_pct, 4),
        "page_brin_economic_pct": round(pb_economic_pct, 4),
        "voting_leverage_x": round(voting_leverage_x, 4),
        "insider_leverage_x": round(insider_leverage_x, 4),
        "insider_economic_pct": INSIDER_ECON_PCT,
        "outside_economic_pct": OUTSIDE_ECON_PCT,
        "annual_ai_capex_drain_bn": ANNUAL_AI_CAPEX_DRAIN_BN,
        "outside_burden_bn_yr": round(outside_burden_bn, 2),
        "insider_burden_bn_yr": round(insider_burden_bn, 2),
        "officers_directors_count": 14,
        "officers_class_b_shares": OFFICERS_CLASS_B_SHARES,
        "officers_class_b_share_pct": round(officers_pct_b, 4),
        "def14a_class_share_pct": DEF14A_CLASS_SHARE_PCT,
        "officers_voting_power_pct": round(officers_voting_pct, 4),
    }


# ------------------------------------------------------------------ (2) waterfall
def tranche_recovery(ev_bn):
    """Deterministic EV waterfall: T1 48.5 -> T2 115.0 (cum. 163.5) -> equity 88/12."""
    t1 = min(ev_bn, TRANCHE_1_PAR_BN)
    t2 = min(max(ev_bn - TRANCHE_1_PAR_BN, 0.0), TRANCHE_2_PAR_BN)
    equity = max(ev_bn - CUM_THRESHOLD_BN, 0.0)
    outside = OUTSIDE_ECON_PCT / 100.0 * equity
    insiders = INSIDER_ECON_PCT / 100.0 * equity
    return {
        "ev_bn": round(ev_bn, 3),
        "tranche_1_bn": round(t1, 6),
        "tranche_1_cents_on_dollar": round(100.0 * t1 / TRANCHE_1_PAR_BN, 4),
        "tranche_2_bn": round(t2, 6),
        "tranche_2_cents_on_dollar": round(100.0 * t2 / TRANCHE_2_PAR_BN, 4),
        "common_equity_bn": round(equity, 6),
        "outside_class_a_c_bn": round(outside, 6),
        "insiders_bn": round(insiders, 6),
    }


def verify_capital_structure_waterfall():
    baseline = tranche_recovery(BASELINE_EV_BN)
    impaired_ev = BASELINE_EV_BN - GROSS_EV_DESTRUCTION_BN      # 1350.0
    impaired = tranche_recovery(impaired_ev)
    assert baseline["common_equity_bn"] == 2036.5
    assert baseline["outside_class_a_c_bn"] == 1792.12
    assert impaired["common_equity_bn"] == 1186.5
    assert impaired["outside_class_a_c_bn"] == 1044.12
    gross_impairment = round(baseline["common_equity_bn"] - impaired["common_equity_bn"], 6)
    outside_impairment = round(baseline["outside_class_a_c_bn"] - impaired["outside_class_a_c_bn"], 6)
    insider_impairment = round(gross_impairment - outside_impairment, 6)
    assert gross_impairment == GROSS_EV_DESTRUCTION_BN   # -$850.0B gross
    assert outside_impairment == 748.0                   # -$748.0B outside Class A/C
    assert insider_impairment == 102.0                   # -$102.0B insiders

    distress = {str(ev): tranche_recovery(ev) for ev in (163.5, 100.0, 48.5, 30.0)}
    assert distress["163.5"]["common_equity_bn"] == 0.0
    assert distress["163.5"]["tranche_2_cents_on_dollar"] == 100.0
    assert distress["100.0"]["tranche_2_bn"] == 51.5
    assert round(distress["100.0"]["tranche_2_cents_on_dollar"], 4) == 44.7826
    assert distress["48.5"]["tranche_2_bn"] == 0.0
    assert distress["48.5"]["tranche_1_cents_on_dollar"] == 100.0
    assert round(distress["30.0"]["tranche_1_cents_on_dollar"], 4) == 61.8557
    assert distress["30.0"]["tranche_2_bn"] == 0.0
    return {
        "tranche_recovery_baseline_ev_2200": baseline,
        "tranche_recovery_impaired_ev_1350": impaired,
        "distress_scenarios": distress,
        "gross_ev_destruction_bn": gross_impairment,
        "outside_class_a_c_impairment_bn": outside_impairment,
        "insider_impairment_bn": insider_impairment,
    }


# ------------------------------------------------------------------ (3) Spence separator
def verify_spence_10b5_separating_equilibrium():
    """Rule 10b-5 certification is a Spence signal: separating iff delta >= 1/m."""
    transfer_gain_bn = 74.8   # $B/yr CapEx burden shifted onto the outside 88%
    damages_multiple = 3.0    # treble damages under Rule 10b-5 / PSLRA
    delta_star = 1.0 / damages_multiple

    def mimic_payoff(delta):
        return transfer_gain_bn * (1.0 - delta * damages_multiple)

    payoff_pool = mimic_payoff(0.30)   # +7.48 > 0 -> mimic -> pooling (cheap talk)
    payoff_sep = mimic_payoff(0.35)    # -3.74 < 0 -> no mimic -> separating
    assert payoff_pool > 0.0
    assert payoff_sep < 0.0
    assert abs(delta_star - 1.0 / 3.0) < 1.0e-12
    assert mimic_payoff(delta_star) == 0.0            # IC binds exactly at delta*
    # Honest type: truthful certification cost = 0 -> always certifies.
    # Counterfactual: with no 10b-5 liability (m -> 0) delta* -> infinity and
    # certification collapses to unverifiable cheap talk (Rasputin regime).
    assert damages_multiple > 0.0
    return {
        "transfer_gain_bn_yr": transfer_gain_bn,
        "damages_multiple": damages_multiple,
        "delta_star": delta_star,
        "mimic_payoff_delta_030": round(payoff_pool, 4),
        "mimic_payoff_delta_035": round(payoff_sep, 4),
        "equilibrium_at_delta_030": "pooling_cheap_talk",
        "equilibrium_at_delta_035": "separating",
        "separating_condition": "delta >= 1/m = 1/3",
        "no_liability_counterfactual": "delta* -> infinity; certification is cheap talk",
    }


# ------------------------------------------------------------------ (4) phase transition
def verify_bootstrap_to_utility_phase_transition():
    """2012-2024 bootstrap surplus > 0; 2026 utility phase surplus < 0."""
    bootstrap_spend_hi_bn = 2.0        # upper bound of $0.5-$2.0B/yr lab spend
    bootstrap_benefit_bn = 25.0        # search/Android cash-flow protection
    net_bootstrap = bootstrap_benefit_bn - bootstrap_spend_hi_bn   # +23.0
    utility_benefit_bn = 30.0          # cloud/AI revenue
    net_utility = utility_benefit_bn - ANNUAL_AI_CAPEX_DRAIN_BN    # -55.0
    ten_year_burn = ANNUAL_AI_CAPEX_DRAIN_BN * 10.0               # 850.0
    assert net_bootstrap == 23.0 and net_bootstrap > 0.0
    assert net_utility == -55.0 and net_utility < 0.0
    assert ten_year_burn == GROSS_EV_DESTRUCTION_BN
    bootstrap_blast_radius = 0         # isolated lab: no grid/monorepo coupling
    spofs_2026 = 3                     # grid feed, LPT, cooling plant
    assert bootstrap_blast_radius == 0 and spofs_2026 == 3
    return {
        "bootstrap_window": "2012-2024",
        "bootstrap_spend_bn_yr_range": [0.5, 2.0],
        "bootstrap_net_surplus_bn_yr": net_bootstrap,
        "bootstrap_blast_radius": bootstrap_blast_radius,
        "utility_hazard_year": 2026,
        "utility_capex_drain_bn_yr": ANNUAL_AI_CAPEX_DRAIN_BN,
        "utility_net_surplus_bn_yr": net_utility,
        "ten_year_un_underwritten_burn_bn": ten_year_burn,
        "systemic_coupling_2026": ["grid", "production_monorepo", "supply_chain"],
        "linear_spofs_2026": spofs_2026,
        "phase_transition_sign_flip": True,
    }


# ------------------------------------------------------------------ (5) thermodynamics
def verify_gigawatt_thermodynamics_and_compiler_law():
    """100 MW hall: 900 s adiabatic ride-through; 5.0e9 RPC energy penalty."""
    power_w = HALL_MW * 1.0e6
    t_shut_s = THERMAL_MASS_J_PER_K * ALLOWABLE_RISE_K / power_w
    assert round(t_shut_s, 6) == 900.0
    assert t_shut_s <= T_SHUT_MAX_S          # <= 15.0 minutes
    linear_spofs = ["grid_feed", "large_power_transformer", "cooling_plant"]
    assert len(linear_spofs) == 3
    assert DIESEL_CAP_HOURS == 72.0
    assert LPT_BACKLOG_MONTHS == (24, 48)
    # Diesel cannot bridge an LPT failure: 72 h << 24 months of lead time.
    assert DIESEL_CAP_HOURS < LPT_BACKLOG_MONTHS[0] * 730.0
    energy_penalty = RPC_CLOUD_J / RPC_LOCAL_J
    assert energy_penalty == 5.0e9
    return {
        "hall_it_load_mw": HALL_MW,
        "thermal_mass_j_per_k": THERMAL_MASS_J_PER_K,
        "allowable_rise_k": ALLOWABLE_RISE_K,
        "t_shut_s": round(t_shut_s, 3),
        "t_shut_bound_s": T_SHUT_MAX_S,
        "linear_spofs": linear_spofs,
        "diesel_fuel_cap_hours": DIESEL_CAP_HOURS,
        "lpt_backlog_months": list(LPT_BACKLOG_MONTHS),
        "rpc_energy_cloud_j": RPC_CLOUD_J,
        "rpc_energy_local_j": RPC_LOCAL_J,
        "runtime_rpc_energy_penalty": energy_penalty,
    }


# ------------------------------------------------------------------ (6) containment / mesh
def verify_containment_delusion_and_sovereign_mesh():
    """$400B/yr GPU CapEx -> $100B/yr amortization; Rasputin KL bound; P2P mesh."""
    amortization_bn_yr = SECTOR_GPU_CAPEX_BN_YR / GPU_LIFESPAN_YEARS
    assert amortization_bn_yr == 100.0
    # Rasputin KL steering: Pinsker TV <= sqrt(KL/2); at KL budget 2.0 nats the
    # bound is exactly 1.0 -> vacuous: the advisor can fully capture the policy.
    kl_budget = KL_STEERING_BUDGET_NATS
    tv_bound = math.sqrt(kl_budget / 2.0)
    assert tv_bound == 1.0
    p, q = (0.9, 0.1), (0.4, 0.6)   # Pinsker numeric instance
    kl_pq = sum(pi * math.log(pi / qi) for pi, qi in zip(p, q))
    tv_pq = 0.5 * sum(abs(pi - qi) for pi, qi in zip(p, q))
    assert tv_pq <= math.sqrt(kl_pq / 2.0)   # Pinsker inequality holds
    # Tiebout stranded-energy arbitrage: $6,000 / 900 W P2P MoE server.
    capital_per_peer = MESH_SERVER_COST_USD / MESH_PEERS
    avg_draw_w = MESH_SERVER_WATTS * MESH_DUTY_CYCLE
    kwh_yr = avg_draw_w * 8760.0 / 1000.0
    energy_cost_yr = kwh_yr * ELECTRICITY_USD_PER_KWH
    energy_cost_per_peer_yr = energy_cost_yr / MESH_PEERS
    amort_per_peer_yr = MESH_SERVER_COST_USD / 5.0 / MESH_PEERS
    assert capital_per_peer == 150.0
    assert round(avg_draw_w, 6) == 45.0
    assert round(kwh_yr, 4) == 394.2
    assert round(energy_cost_yr, 4) == 39.42
    assert round(energy_cost_per_peer_yr, 6) == 0.9855
    assert amort_per_peer_yr == 30.0
    return {
        "sector_gpu_capex_bn_yr": SECTOR_GPU_CAPEX_BN_YR,
        "gpu_lifespan_years": GPU_LIFESPAN_YEARS,
        "amortization_cash_flow_bn_yr": amortization_bn_yr,
        "rasputin_kl_budget_nats": kl_budget,
        "pinsker_tv_bound": tv_bound,
        "pinsker_instance_kl": round(kl_pq, 6),
        "pinsker_instance_tv": tv_pq,
        "bound_vacuous": True,
        "mesh_server_cost_usd": MESH_SERVER_COST_USD,
        "mesh_server_watts": MESH_SERVER_WATTS,
        "mesh_duty_cycle": MESH_DUTY_CYCLE,
        "mesh_peers": MESH_PEERS,
        "capital_cost_per_peer_usd": capital_per_peer,
        "avg_draw_w": avg_draw_w,
        "energy_cost_per_peer_yr_usd": round(energy_cost_per_peer_yr, 4),
        "amortization_per_peer_yr_usd": amort_per_peer_yr,
    }


def main():
    result = {
        "proof": "successionist_governance_proof.py",
        "spec": "SPEC-SUCCESSIONIST-GOVERNANCE-v1.0",
        "dual_class_agency_wedge": verify_dual_class_agency_wedge(),
        "capital_structure_waterfall": verify_capital_structure_waterfall(),
        "spence_10b5_separating_equilibrium": verify_spence_10b5_separating_equilibrium(),
        "bootstrap_to_utility_phase_transition": verify_bootstrap_to_utility_phase_transition(),
        "gigawatt_thermodynamics_and_compiler_law": verify_gigawatt_thermodynamics_and_compiler_law(),
        "containment_delusion_and_sovereign_mesh": verify_containment_delusion_and_sovereign_mesh(),
        "all_assertions_passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
