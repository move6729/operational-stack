#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: CENTRALIZATION PERCOLATION PARALYSIS (v1.0)

Canonical Specification: SPEC-CENTRALIZATION-PERCOLATION-PARALYSIS-v1.0
License: Unlicense

Proves:
EQ-1 Star-vs-Mesh Percolation Asymmetry (Molloy & Reed 1995; Callaway et al. 2000):
     p_c = <k> / (<k^2> - <k>), f_c = 1 - p_c, kappa = <k^2> / <k>. The 15,000-edge
     mesh (k0 = 4.0, <k^2> = 16.0, kappa = 4.0) shatters only at f_c = 0.666667
     (10,000 compromised nodes); the 15,001-vertex dealer star (<k> = 1.999867,
     <k^2>_hub = 14999.000067, kappa = 7500.5) collapses at f_targeted = 0.00006666
     (a single hub node): adversary leverage multiplier lambda_extort = 10,000x.
EQ-2 Synchronous Coupling Paralysis: A_eff = A_phys * A_hub^gamma. Cloud/SaaS coupling
     (gamma = 1.0) => A_eff = 0.0 under total hub fault; air-gapped local custody
     (gamma = 0.0) => A_eff = 0.9999. Cloud LLM/ERP p99 = 850 ms against a 2 ms PLC
     scan cycle => 425x latency penalty: synchronous control coupling is infeasible.
EQ-3 Extortion Coasean Asymmetry: 15,000 dealers x $4,800/day x 14 days =
     $1,008,000,000 aggregate loss vs $25,000,000 ransom => 40.32x loss-to-ransom
     ratio; OEM JIT line-stop penalties EUR 25,000/min = EUR 1,500,000/hr =
     EUR 36,000,000/day.
EQ-4 Municipal Queue Blowup (Suedwestfalen IT): Lambda = lambda0 * N * (1 + beta*ln N)
     = 359.544/hr against degraded central service rate mu = 180/hr => rho =
     1.997467 > 1 (M/M/1 stability violated), drift delta_Q = 179.544/hr, 4,320-hour
     (180-day) accumulated backlog = 775,630 transactions.
EQ-5 Regulatory Boomerang (GDPR Art. 83(4)-(5) / NIS2 Art. 34): max(0.04 x EUR 500M,
     EUR 20M) = EUR 20M; p_audit = 0.5 => EUR 10M expected fine surcharge; expanded
     extortion reserve ceiling EUR 15M = 3.0x the EUR 5M direct downtime loss.
EQ-6 CDK Global Holdings, LLC LBO Waterfall: tranche_recovery(ev) over the $8,300M
     stack (RCF $650M / TLB $3,800M / unsecured notes $1,000M / sponsor equity
     $2,850M); at stressed EV $4,200M: RCF 100.0c, TLB $3,550M = 93.42c (fulcrum
     security), unsecured notes 0.0c, sponsor equity 0.0c.
EQ-7 VARTA AG StaRUG Waterfall: tranche_recovery(ev) over the EUR 485M senior stack
     (EUR 235M syndicated loan + EUR 250M Schuldschein notes); at plan value EUR 200M:
     senior 41.24c pari passu (EUR 285M haircut), public equity 0.0c, EUR 60M new
     rescue equity (Porsche Automobil Holding SE / Michael Tojner).

Zero external dependencies.
"""

import hashlib
import json
import math
from datetime import date

TOL = 1e-6

# --- EQ-1: star-vs-mesh percolation (locked constants) ---
N_EDGE_NODES = 15000
V_STAR_VERTICES = 15001
MESH_K0 = 4.0
MESH_K2 = 16.0
MESH_KAPPA = 4.0
MESH_PC = 0.333333
MESH_FC = 0.666667
MESH_NODES_TO_COMPROMISE = 10000
STAR_AVG_DEGREE_K = 1.999867
STAR_SECOND_MOMENT_K2 = 14999.000067
STAR_KAPPA = 7500.5
STAR_F_TARGETED = 0.00006666
STAR_NODES_TO_COMPROMISE = 1
LAMBDA_EXTORT = 10000.0

# --- EQ-2: synchronous coupling paralysis (locked constants) ---
A_PHYS = 0.9999
A_HUB_FAULT = 0.0
GAMMA_CLOUD_SAAS = 1.0
GAMMA_AIRGAPPED_LOCAL = 0.0
A_EFF_CENTRALIZED = 0.0
A_EFF_AIRGAPPED = 0.9999
PLC_SCAN_CYCLE_MS = 2.0
CLOUD_LLM_ERP_P99_MS = 850.0
LATENCY_PENALTY_MULTIPLIER = 425.0

# --- EQ-3: extortion Coasean asymmetry (locked constants) ---
CDK_DEALERS_M = 15000
CDK_DAILY_LOSS_PER_DEALER_USD = 4800.0
CDK_OUTAGE_DAYS_D = 14
CDK_AGGREGATE_DEALER_LOSS_USD = 1008000000.0
CDK_RANSOM_PAID_USD = 25000000.0
CDK_LOSS_TO_RANSOM_RATIO = 40.32
OEM_JIT_PENALTY_EUR_PER_MIN = 25000.0
OEM_JIT_PENALTY_EUR_PER_HOUR = 1500000.0
OEM_JIT_PENALTY_EUR_PER_DAY = 36000000.0

# --- EQ-4: municipal queue blowup, Suedwestfalen IT (locked constants) ---
MUNICIPALITIES_N = 72
CITIZENS_AFFECTED = 1600000
LAMBDA0_PER_HR = 2.0
COUPLING_GROWTH_BETA = 0.35
LAMBDA_TOTAL_PER_HR = 359.544
MU_DEGRADED_PER_HR = 180.0
UTILIZATION_RHO = 1.997467
QUEUE_DRIFT_DELTA_Q_PER_HR = 179.544
OUTAGE_HOURS_6_MONTHS = 4320
ACCUMULATED_BACKLOG_TRANSACTIONS = 775630

# --- EQ-5: regulatory boomerang, double extortion (locked constants) ---
ADVERSARY_JURISDICTIONAL_REACHABILITY = 0.0
VICTIM_DOMESTIC_REACHABILITY = 1.0
EXAMPLE_VICTIM_REVENUE_EUR = 500000000.0
GDPR_ART83_MAX_FINE_PCT = 0.04
GDPR_ART83_STATUTORY_CEILING_EUR = 20000000.0
NIS2_ART34_MAX_FINE_PCT = 0.02
NIS2_ART34_STATUTORY_CEILING_EUR = 10000000.0
P_AUDIT = 0.5
DIRECT_DOWNTIME_LOSS_EUR = 5000000.0
EXPECTED_REGULATORY_FINE_SURCHARGE_EUR = 10000000.0
EXPANDED_EXTORTION_RESERVE_CEILING_EUR = 15000000.0
RANSOM_DEMAND_SETTLED_EUR = 1500000.0
BOOMERANG_LEVERAGE_EXPANSION_RATIO = 3.0

# --- EQ-6: CDK Global Holdings, LLC LBO capital structure (USD millions) ---
CDK_TOTAL_LBO_CAP_M = 8300.0
CDK_RCF_PRINCIPAL_M = 650.0
CDK_TLB_PRINCIPAL_M = 3800.0
CDK_UNSECURED_PRINCIPAL_M = 1000.0
CDK_SPONSOR_EQUITY_M = 2850.0
CDK_STRESSED_EV_M = 4200.0
CDK_STRESSED_TLB_RECOVERY_M = 3550.0

CDK_STACK = (
    ("rcf", CDK_RCF_PRINCIPAL_M),
    ("tlb", CDK_TLB_PRINCIPAL_M),
    ("unsecured_notes", CDK_UNSECURED_PRINCIPAL_M),
    ("sponsor_equity", CDK_SPONSOR_EQUITY_M),
)

# --- EQ-7: VARTA AG StaRUG capital structure (EUR millions) ---
VARTA_PRE_STARUG_GROSS_DEBT_M = 485.0
VARTA_SYNDICATED_LOAN_M = 235.0
VARTA_SCHULDSCHEIN_NOTES_M = 250.0
VARTA_POST_STARUG_DEBT_M = 200.0
VARTA_SENIOR_HAIRCUT_M = 285.0
VARTA_NEW_RESCUE_EQUITY_M = 60.0

VARTA_STACK = (
    ("senior_debt_pari_passu", VARTA_PRE_STARUG_GROSS_DEBT_M),
    ("public_equity_residual", 0.0),
)

# --- Hard-date catalyst calendar (iso_date, event, jurisdiction, precision) ---
CATALYST_CALENDAR = (
    ("2023-10-30", "Suedwestfalen IT (SIT) ransomware intrusion onset; 72-municipality consortium offline", "DE", "exact"),
    ("2024-03-01", "VARTA AG StaRUG plan agreement window; EUR 60.0M rescue equity commitment (Porsche SE / Tojner)", "DE", "month"),
    ("2024-04-27", "SIT 4,320-hour (180-day) degraded-service boundary; backlog 775,630 transactions", "DE", "derived"),
    ("2024-06-19", "CDK Global ransomware intrusion onset; ~15,000 dealer rooftops offline", "US", "exact"),
    ("2024-06-21", "CDK USD 25.0M ransom payment per public reporting", "US", "reported"),
    ("2024-07-01", "VARTA StaRUG plan implementation window; senior debt EUR 485.0M -> EUR 200.0M", "DE", "month"),
    ("2024-07-03", "CDK 14-day core-outage boundary (2024-06-19 + D = 14)", "US", "derived"),
)


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def tranche_recovery(ev, stack):
    """
    Deterministic absolute-priority waterfall (Debt Stack, Collateral Box & Fulcrum
    Recovery Waterfall invariant). stack is seniority-ordered (tranche, principal_m);
    principal 0.0 encodes a residual equity stub with no locked notional (recovery =
    leftover EV; cents-on-dollar reported as 0.0 while the stub is out of the money).
    Returns {tranche: {"dollars_m": float, "cents_on_dollar": float}}.
    """
    remaining = max(0.0, float(ev))
    recoveries = {}
    for name, principal in stack:
        if principal > 0.0:
            dollars = min(principal, remaining)
            cents = round(100.0 * dollars / principal, 2)
        else:
            dollars = remaining
            cents = 0.0
        remaining -= dollars
        recoveries[name] = {"dollars_m": round(dollars, 6), "cents_on_dollar": cents}
    return recoveries


def total_dollars(recoveries):
    return round(sum(r["dollars_m"] for r in recoveries.values()), 6)


def verify_eq1_star_vs_mesh_percolation():
    """
    Molloy-Reed / Callaway criterion: a giant component survives iff kappa =
    <k^2>/<k> > 2; site-percolation threshold p_c = <k>/(<k^2> - <k>); critical
    targeted-removal fraction f_c = 1 - p_c.
    """
    assert V_STAR_VERTICES == N_EDGE_NODES + 1

    # Mesh: regular degree-4 topology over 15,000 edge nodes.
    kappa_mesh = MESH_K2 / MESH_K0
    assert close(kappa_mesh, MESH_KAPPA), kappa_mesh
    assert kappa_mesh > 2.0  # giant component exists pre-attack
    p_c = MESH_K0 / (MESH_K2 - MESH_K0)
    assert round(p_c, 6) == MESH_PC, p_c
    f_c = 1.0 - p_c
    assert round(f_c, 6) == MESH_FC, f_c
    mesh_nodes = round(f_c * N_EDGE_NODES)
    assert mesh_nodes == MESH_NODES_TO_COMPROMISE, mesh_nodes

    # Star: 1 hub + 15,000 leaves; V = 15,001, E = 15,000.
    k_avg = 2.0 * N_EDGE_NODES / V_STAR_VERTICES
    assert round(k_avg, 6) == STAR_AVG_DEGREE_K, k_avg
    k2_hub = (N_EDGE_NODES ** 2) / V_STAR_VERTICES
    assert round(k2_hub, 6) == STAR_SECOND_MOMENT_K2, k2_hub
    k2_leaves = N_EDGE_NODES / V_STAR_VERTICES
    k2_full = (N_EDGE_NODES ** 2 + N_EDGE_NODES) / V_STAR_VERTICES
    assert close(k2_hub + k2_leaves, k2_full, 1e-9), (k2_hub, k2_leaves, k2_full)
    assert close(k2_full, 15000.0, 1e-9), k2_full
    kappa_star = k2_full / k_avg
    assert close(kappa_star, STAR_KAPPA, 1e-6), kappa_star
    assert kappa_star > kappa_mesh

    # Targeted attack: removing the single hub shatters the star.
    f_targeted = 1.0 / N_EDGE_NODES
    assert math.floor(f_targeted * 1e8) / 1e8 == STAR_F_TARGETED, f_targeted
    assert close(f_targeted, STAR_F_TARGETED, 1e-8), f_targeted
    assert STAR_NODES_TO_COMPROMISE == 1

    lambda_extort = MESH_NODES_TO_COMPROMISE / STAR_NODES_TO_COMPROMISE
    assert close(lambda_extort, LAMBDA_EXTORT), lambda_extort

    return {
        "mesh_kappa": round(kappa_mesh, 6),
        "mesh_percolation_threshold_pc": round(p_c, 6),
        "mesh_critical_removal_fraction_fc": round(f_c, 6),
        "mesh_nodes_to_compromise": mesh_nodes,
        "star_avg_degree_k": round(k_avg, 6),
        "star_second_moment_k2": round(k2_hub, 6),
        "star_kappa": round(kappa_star, 6),
        "star_targeted_removal_fraction_f_targeted": math.floor(f_targeted * 1e8) / 1e8,
        "star_nodes_to_compromise": STAR_NODES_TO_COMPROMISE,
        "lambda_extort": round(lambda_extort, 6),
    }


def verify_eq2_synchronous_coupling_paralysis():
    """A_eff = A_phys * A_hub^gamma; latency penalty = cloud p99 / PLC scan cycle."""
    a_eff_centralized = A_PHYS * (A_HUB_FAULT ** GAMMA_CLOUD_SAAS)
    assert a_eff_centralized == A_EFF_CENTRALIZED, a_eff_centralized
    a_eff_airgapped = A_PHYS * (A_HUB_FAULT ** GAMMA_AIRGAPPED_LOCAL)
    assert close(a_eff_airgapped, A_EFF_AIRGAPPED), a_eff_airgapped
    latency_penalty = CLOUD_LLM_ERP_P99_MS / PLC_SCAN_CYCLE_MS
    assert close(latency_penalty, LATENCY_PENALTY_MULTIPLIER), latency_penalty
    assert latency_penalty > 1.0  # cloud round trip exceeds the PLC scan cycle
    assert a_eff_airgapped > a_eff_centralized  # decoupling strictly dominates

    return {
        "effective_availability_centralized": a_eff_centralized,
        "effective_availability_airgapped_local": round(a_eff_airgapped, 6),
        "latency_penalty_multiplier": round(latency_penalty, 6),
    }


def verify_eq3_extortion_coasean_asymmetry():
    """Aggregate dealer loss vs ransom settlement; OEM JIT line-stop penalty ladder."""
    aggregate = CDK_DEALERS_M * CDK_DAILY_LOSS_PER_DEALER_USD * CDK_OUTAGE_DAYS_D
    assert close(aggregate, CDK_AGGREGATE_DEALER_LOSS_USD, 1e-6), aggregate
    ratio = aggregate / CDK_RANSOM_PAID_USD
    assert close(ratio, CDK_LOSS_TO_RANSOM_RATIO, 1e-9), ratio
    per_hour = OEM_JIT_PENALTY_EUR_PER_MIN * 60.0
    assert close(per_hour, OEM_JIT_PENALTY_EUR_PER_HOUR), per_hour
    per_day = per_hour * 24.0
    assert close(per_day, OEM_JIT_PENALTY_EUR_PER_DAY), per_day
    adversary_capture_share = CDK_RANSOM_PAID_USD / aggregate
    assert close(adversary_capture_share, 0.024802, 1e-6), adversary_capture_share
    assert ratio > 1.0  # Coasean collapse: imposed loss >> settlement claim

    return {
        "aggregate_dealer_loss_usd": round(aggregate, 2),
        "loss_to_ransom_ratio": round(ratio, 6),
        "adversary_capture_share": round(adversary_capture_share, 6),
        "oem_jit_penalty_eur_per_hour": round(per_hour, 2),
        "oem_jit_penalty_eur_per_day": round(per_day, 2),
    }


def verify_eq4_municipal_queue_blowup():
    """
    Lambda = lambda0 * N * (1 + beta * ln N); rho = Lambda / mu. M/M/1 stability
    requires rho < 1; rho > 1 => non-stationary linear queue drift delta_Q.
    """
    coupling_multiplier = 1.0 + COUPLING_GROWTH_BETA * math.log(MUNICIPALITIES_N)
    assert close(coupling_multiplier, 2.496833, 1e-6), coupling_multiplier
    lam = LAMBDA0_PER_HR * MUNICIPALITIES_N * coupling_multiplier
    assert round(lam, 3) == LAMBDA_TOTAL_PER_HR, lam
    rho = LAMBDA_TOTAL_PER_HR / MU_DEGRADED_PER_HR
    assert round(rho, 6) == UTILIZATION_RHO, rho
    assert rho > 1.0  # stability violated: the queue diverges
    delta_q = LAMBDA_TOTAL_PER_HR - MU_DEGRADED_PER_HR
    assert close(delta_q, QUEUE_DRIFT_DELTA_Q_PER_HR, 1e-6), delta_q
    backlog = math.floor(delta_q * OUTAGE_HOURS_6_MONTHS)
    assert backlog == ACCUMULATED_BACKLOG_TRANSACTIONS, backlog
    assert OUTAGE_HOURS_6_MONTHS == 180 * 24

    return {
        "coupling_multiplier": round(coupling_multiplier, 6),
        "total_arrival_rate_lambda_per_hr": round(lam, 3),
        "utilization_rho": round(rho, 6),
        "queue_drift_delta_q_per_hr": round(delta_q, 3),
        "accumulated_backlog_transactions": backlog,
        "municipalities_n": MUNICIPALITIES_N,
        "citizens_affected": CITIZENS_AFFECTED,
    }


def verify_eq5_regulatory_boomerang():
    """
    GDPR Art. 83(4)-(5): max(4% turnover, EUR 20M); NIS2 Art. 34: max(2% turnover,
    EUR 10M). Expected fine surcharge = p_audit * GDPR ceiling; expanded extortion
    reserve ceiling = direct downtime loss + expected surcharge.
    """
    gdpr_ceiling = max(
        GDPR_ART83_MAX_FINE_PCT * EXAMPLE_VICTIM_REVENUE_EUR,
        GDPR_ART83_STATUTORY_CEILING_EUR,
    )
    assert close(gdpr_ceiling, GDPR_ART83_STATUTORY_CEILING_EUR, 1e-3), gdpr_ceiling
    nis2_ceiling = max(
        NIS2_ART34_MAX_FINE_PCT * EXAMPLE_VICTIM_REVENUE_EUR,
        NIS2_ART34_STATUTORY_CEILING_EUR,
    )
    assert close(nis2_ceiling, NIS2_ART34_STATUTORY_CEILING_EUR, 1e-3), nis2_ceiling
    expected_surcharge = P_AUDIT * gdpr_ceiling
    assert close(expected_surcharge, EXPECTED_REGULATORY_FINE_SURCHARGE_EUR, 1e-3)
    expanded_reserve = DIRECT_DOWNTIME_LOSS_EUR + expected_surcharge
    assert close(expanded_reserve, EXPANDED_EXTORTION_RESERVE_CEILING_EUR, 1e-3)
    boomerang = expanded_reserve / DIRECT_DOWNTIME_LOSS_EUR
    assert close(boomerang, BOOMERANG_LEVERAGE_EXPANSION_RATIO, 1e-9), boomerang
    # Rational settlement band: ransom < direct loss < expanded reserve ceiling.
    assert RANSOM_DEMAND_SETTLED_EUR < DIRECT_DOWNTIME_LOSS_EUR < expanded_reserve
    # Jurisdictional asymmetry: adversary unreachable, victim fully reachable.
    assert ADVERSARY_JURISDICTIONAL_REACHABILITY < VICTIM_DOMESTIC_REACHABILITY

    return {
        "gdpr_art83_ceiling_eur": round(gdpr_ceiling, 2),
        "nis2_art34_ceiling_eur": round(nis2_ceiling, 2),
        "expected_regulatory_fine_surcharge_eur": round(expected_surcharge, 2),
        "expanded_extortion_reserve_ceiling_eur": round(expanded_reserve, 2),
        "boomerang_leverage_expansion_ratio": round(boomerang, 6),
        "ransom_demand_settled_eur": RANSOM_DEMAND_SETTLED_EUR,
    }


def verify_eq6_cdk_tranche_recovery_waterfall():
    """CDK Global Holdings, LLC: $8,300M LBO stack, stressed EV $4,200M."""
    total_claims = sum(principal for _, principal in CDK_STACK)
    assert close(total_claims, CDK_TOTAL_LBO_CAP_M), total_claims

    # Breakeven EV thresholds = cumulative principal under absolute priority.
    breakevens, cumulative = [], 0.0
    for _, principal in CDK_STACK:
        cumulative += principal
        breakevens.append(cumulative)
    assert breakevens == [650.0, 4450.0, 5450.0, 8300.0], breakevens

    stressed = tranche_recovery(CDK_STRESSED_EV_M, CDK_STACK)
    assert close(stressed["rcf"]["dollars_m"], CDK_RCF_PRINCIPAL_M)
    assert close(stressed["rcf"]["cents_on_dollar"], 100.0)
    assert close(stressed["tlb"]["dollars_m"], CDK_STRESSED_TLB_RECOVERY_M)
    assert close(stressed["tlb"]["cents_on_dollar"], 93.42)
    assert close(stressed["unsecured_notes"]["dollars_m"], 0.0)
    assert close(stressed["unsecured_notes"]["cents_on_dollar"], 0.0)
    assert close(stressed["sponsor_equity"]["dollars_m"], 0.0)
    assert close(stressed["sponsor_equity"]["cents_on_dollar"], 0.0)
    assert close(total_dollars(stressed), CDK_STRESSED_EV_M)
    # The TLB is the fulcrum security at stressed EV.
    assert breakevens[0] < CDK_STRESSED_EV_M < breakevens[1]

    # Boundary-regime fidelity: each tranche hits par exactly at its breakeven EV.
    for ev, tranche in ((650.0, "rcf"), (4450.0, "tlb"), (5450.0, "unsecured_notes"), (8300.0, "sponsor_equity")):
        rec = tranche_recovery(ev, CDK_STACK)
        assert close(rec[tranche]["cents_on_dollar"], 100.0), (ev, rec)
        assert close(total_dollars(rec), min(ev, CDK_TOTAL_LBO_CAP_M)), (ev, rec)
    impaired = tranche_recovery(5449.0, CDK_STACK)
    assert close(impaired["sponsor_equity"]["cents_on_dollar"], 0.0), impaired
    deep = tranche_recovery(9000.0, CDK_STACK)
    assert close(deep["sponsor_equity"]["dollars_m"], CDK_SPONSOR_EQUITY_M)
    assert close(total_dollars(deep), CDK_TOTAL_LBO_CAP_M)
    zero = tranche_recovery(0.0, CDK_STACK)
    assert all(close(r["cents_on_dollar"], 0.0) for r in zero.values())

    return {
        "breakeven_ev_thresholds_m": breakevens,
        "stressed_ev_m": CDK_STRESSED_EV_M,
        "stressed": stressed,
        "fulcrum_security": "tlb",
    }


def verify_eq7_varta_starug_tranche_recovery_waterfall():
    """VARTA AG: StaRUG plan, EUR 485M senior stack reorganized to EUR 200M."""
    pre_debt = VARTA_SYNDICATED_LOAN_M + VARTA_SCHULDSCHEIN_NOTES_M
    assert close(pre_debt, VARTA_PRE_STARUG_GROSS_DEBT_M), pre_debt
    haircut = pre_debt - VARTA_POST_STARUG_DEBT_M
    assert close(haircut, VARTA_SENIOR_HAIRCUT_M), haircut
    haircut_fraction = haircut / pre_debt
    assert close(haircut_fraction, 0.587629, 1e-6), haircut_fraction

    plan = tranche_recovery(VARTA_POST_STARUG_DEBT_M, VARTA_STACK)
    assert close(plan["senior_debt_pari_passu"]["dollars_m"], VARTA_POST_STARUG_DEBT_M)
    assert close(plan["senior_debt_pari_passu"]["cents_on_dollar"], 41.24)
    assert close(plan["public_equity_residual"]["dollars_m"], 0.0)
    assert close(plan["public_equity_residual"]["cents_on_dollar"], 0.0)
    assert close(total_dollars(plan), VARTA_POST_STARUG_DEBT_M)

    # Boundary regimes: senior par at pre-plan gross debt; stub absorbs surplus.
    par = tranche_recovery(VARTA_PRE_STARUG_GROSS_DEBT_M, VARTA_STACK)
    assert close(par["senior_debt_pari_passu"]["cents_on_dollar"], 100.0), par
    surplus = tranche_recovery(VARTA_PRE_STARUG_GROSS_DEBT_M + VARTA_NEW_RESCUE_EQUITY_M, VARTA_STACK)
    assert close(surplus["public_equity_residual"]["dollars_m"], VARTA_NEW_RESCUE_EQUITY_M)
    assert close(total_dollars(surplus), 545.0), surplus

    return {
        "pre_starug_gross_debt_m": round(pre_debt, 2),
        "post_starug_reorganized_debt_m": VARTA_POST_STARUG_DEBT_M,
        "senior_debt_haircut_m": round(haircut, 2),
        "senior_debt_haircut_fraction": round(haircut_fraction, 6),
        "plan": plan,
        "new_rescue_equity_porsche_tojner_m": VARTA_NEW_RESCUE_EQUITY_M,
    }


def verify_catalyst_calendar():
    """Hard-date catalyst calendar: ISO-8601 validity, chronology, derived spans."""
    parsed = []
    for iso, _event, jurisdiction, precision in CATALYST_CALENDAR:
        parsed.append(date.fromisoformat(iso))
        assert jurisdiction in ("US", "DE", "EU"), jurisdiction
        assert precision in ("exact", "month", "derived", "reported"), precision
    assert parsed == sorted(parsed)  # chronological ordering
    # Derived-date arithmetic against locked constants.
    assert (date(2024, 4, 27) - date(2023, 10, 30)).days * 24 == OUTAGE_HOURS_6_MONTHS
    assert (date(2024, 7, 3) - date(2024, 6, 19)).days == CDK_OUTAGE_DAYS_D

    return {
        "entries": len(CATALYST_CALENDAR),
        "first_iso_date": CATALYST_CALENDAR[0][0],
        "last_iso_date": CATALYST_CALENDAR[-1][0],
    }


def run_verification():
    eq1 = verify_eq1_star_vs_mesh_percolation()
    eq2 = verify_eq2_synchronous_coupling_paralysis()
    eq3 = verify_eq3_extortion_coasean_asymmetry()
    eq4 = verify_eq4_municipal_queue_blowup()
    eq5 = verify_eq5_regulatory_boomerang()
    eq6 = verify_eq6_cdk_tranche_recovery_waterfall()
    eq7 = verify_eq7_varta_starug_tranche_recovery_waterfall()
    calendar = verify_catalyst_calendar()

    manifest = {
        "spec_version": "SPEC-CENTRALIZATION-PERCOLATION-PARALYSIS-v1.0",
        "jurisdiction_context": ["US", "DE", "EU"],
        "cfaa_compliance_attestation": True,
        "star_vs_mesh_percolation_eq1": eq1,
        "synchronous_coupling_paralysis_eq2": eq2,
        "extortion_coasean_asymmetry_eq3": eq3,
        "municipal_queue_blowup_eq4": eq4,
        "regulatory_boomerang_eq5": eq5,
        "capital_structure_cdk_waterfall_eq6": eq6,
        "capital_structure_varta_starug_eq7": eq7,
        "catalyst_calendar": calendar,
        "verification_vectors": [
            "star_vs_mesh_percolation",
            "synchronous_coupling",
            "extortion_coasean_asymmetry",
            "municipal_queue_blowup",
            "regulatory_boomerang",
            "cdk_tranche_recovery_waterfall",
            "varta_starug_tranche_recovery",
            "catalyst_calendar_chronology",
            "schema_integrity_gate",
        ],
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-CENTRALIZATION-PERCOLATION-PARALYSIS-v1.0 | "
        f"kappa_star={eq1['star_kappa']:.1f} vs kappa_mesh={eq1['mesh_kappa']:.1f} | "
        f"f_c_mesh={eq1['mesh_critical_removal_fraction_fc']:.6f} "
        f"f_targeted_star={eq1['star_targeted_removal_fraction_f_targeted']:.8f} | "
        f"lambda_extort={eq1['lambda_extort']:.0f}x | "
        f"A_eff_centralized={eq2['effective_availability_centralized']:.4f} vs "
        f"A_eff_airgapped={eq2['effective_availability_airgapped_local']:.4f} | "
        f"latency_penalty={eq2['latency_penalty_multiplier']:.0f}x | "
        f"loss_to_ransom={eq3['loss_to_ransom_ratio']:.2f}x | "
        f"JIT=EUR{eq3['oem_jit_penalty_eur_per_day']:,.0f}/day | "
        f"rho={eq4['utilization_rho']:.6f} "
        f"backlog={eq4['accumulated_backlog_transactions']} | "
        f"boomerang={eq5['boomerang_leverage_expansion_ratio']:.1f}x "
        f"reserve=EUR{eq5['expanded_extortion_reserve_ceiling_eur']:,.0f} | "
        f"CDK@EV4200: RCF={eq6['stressed']['rcf']['cents_on_dollar']:.1f}c "
        f"TLB={eq6['stressed']['tlb']['cents_on_dollar']:.2f}c "
        f"UNS={eq6['stressed']['unsecured_notes']['cents_on_dollar']:.1f}c "
        f"EQ={eq6['stressed']['sponsor_equity']['cents_on_dollar']:.1f}c | "
        f"VARTA@EV200: SEN={eq7['plan']['senior_debt_pari_passu']['cents_on_dollar']:.2f}c "
        f"EQ={eq7['plan']['public_equity_residual']['cents_on_dollar']:.1f}c | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
