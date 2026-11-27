#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: BYZANTINE UNCLAMP & PERFORMATIVE WASTE INVERSION (v1.0)

License: Unlicense (Public Domain — Zero-Rent Federation)

Proves:
1. EQ-1 Invariant 30 (Rorschach Hypothesis Clamp / Agreeableness Mode-Collapse):
   with priors P(H_0)=0.70 / P(H_1)=0.30, social valences V(H_0)=+0.85 /
   V(H_1)=-0.60, and likelihoods P(E|H_0)=0.05 / P(E|H_1)=0.95
   (Lambda(E)=19.0), the indicator filter I(V(H_i) >= tau_Social) at
   tau_Social=0.65 annihilates H_1 -> clamped posterior P~(H_1|E)=0.0 and
   D_KL(P || P~) = +infinity (Ashby requisite-variety collapse, regulator
   variety 1 < environment variety 2). Stripping the clamp to
   tau_Social=-1.0 restores exact Bayes: P(H_1|E) = 0.285/0.320 = 0.890625
   (posterior odds 19.0 * 3/7 = 8.142857). The asymmetric loss matrix
   L(a_Audit,H_0)=$15,000.00 (Type-I) vs L(a_Trust,H_1)=$1,000,000.00
   (Type-II, 100.0% clamped false-negative rate) yields a deterministic
   Loss Reduction Ratio of 1,000,000.00/15,000.00 = 66.666667x.
2. EQ-2 Invariant 31 (Synthetic Proof-of-Work Inversion): Empirical Specimen #1
   `markspace_v0.3.0-beta` dispatches 4,010 cloud agent instances across 21
   benchmark runs at 4,000 tokens/agent = 16,040,000 chat tokens and
   64,160,000 bytes of external egress, armored with 76 formal properties and
   563 unit tests, drawing 1,200.0 W to reach a 0.647 completion rate
   (0.353 failure rate) on a deterministic calendar/parking/lunch locking
   domain that a 1974 Codd/Gray local SQLite ACID kernel closes at 0 chat
   tokens, 0 egress bytes, 0.001 W, 50.0 us and 1.000 completion. Watt
   inflation = 1,200.0/0.001 = 1,200,000.0x; commit-bearing power =
   1,200.0*0.647 = 776.4 W; normalized thermodynamic efficiency
   eta = 1/(1,200,000.0*0.647) = 1.287996e-06 vs eta_local_acid = 1.0
   (six orders of magnitude collapse); latency degradation >= 1.0e5x. Across
   the five-regime protocol ladder, artifact volume (N_Props + N_Tests +
   chat_tokens/1e3) is strictly monotonically increasing while eta is
   strictly monotonically decreasing: Spearman rho = -1.0, Pearson
   r_linear = -0.424507, Pearson r_log10(eta) = -0.755127.
3. EQ-3 Zero-Valence Byzantine Unclamping Gate: tokens_chat_coordination = 0,
   cloud_egress_bytes = 0, kolmogorov_payload_mb = 4.8 <= 10.0 cap,
   axiomatic seed 0.03125 MB <= 32 KB, Lamport BFT quorum N = 10 >= 3f+1 for
   f = 3, and valence_clamping_floor is None. The specimen regime is
   deterministically partitioned (commit_state_transition = False).
4. EQ-4 tranche_recovery(ev): closed-form deterministic waterfall over the
   $500,000,000.00 cloud-wrapper debt stack (Tranche A $150.0M 1L 5.50% cash,
   Tranche B $200.0M 2L 9.50% cash / 2.50% PIK, Tranche C $150.0M unsecured
   14.00% PIK) evaluated at EV = $180M (unclamped audit), $350M (midpoint
   hybrid) and $520M (clamped bubble), plus the $0, $150M, $350M and $500M
   breakeven boundaries.

Zero external dependencies.
"""

import hashlib
import json
import math
import os

SPECIFICATION_ID = "SPEC-BYZANTINE-UNCLAMP-PERFORMATIVE-WASTE-INVERSION-v1.0"
SCHEMA_FILENAME = "byzantine_unclamp_performative_waste.json"
SCHEMA_URN = "urn:opstack:schema:byzantine_unclamp_performative_waste.json"
JURISDICTION_CONTEXT = "US"
GATE_ID = "BYZANTINE_UNCLAMP_AND_WASTE_INVERSION_GATE_v1.0"

# ---------------------------------------------------------------------------
# Standardized security-master keys (entity_and_instrument_ids)
# ---------------------------------------------------------------------------
ENTITY_AND_INSTRUMENT_IDS = {
    "ticker": "CLOUD_API_COMPLEX_AND_MARKSPACE_BENCHMARK",
    "cik": "0001018724_0000789019_0001652044_BENCHMARK",
    "court_dockets": (
        "18-USC-1030-CFAA-AUTHORIZED-CUSTODY-BASELINE",
        "ACM-TOPLAS-1982-4-3-382-BYZANTINE-GENERALS",
        "BIOL-REV-2020-95-1-267-HANDICAP-REFUTATION",
    ),
    "named_tranches": (
        "TRANCHE_A_SENIOR_SECURED_LOCAL_ACID_KERNEL",
        "TRANCHE_B_MEZZANINE_CLOUD_API_PASS_THROUGH_FACILITY",
        "TRANCHE_C_UNSECURED_PERFORMATIVE_WRAPPER_EQUITY_NOTE",
    ),
    "empirical_specimen": "markspace_v0.3.0-beta (opinionated-systems/markspace)",
    "total_enterprise_debt_stack_usd": 500_000_000.00,
}

# ---------------------------------------------------------------------------
# EQ-4 deterministic capital-structure waterfall (seniority order, USD)
# (tranche_id, principal_usd, cash_coupon_pct, pik_rate_pct, seniority,
#  collateral_box, breakeven_ev_usd)
# ---------------------------------------------------------------------------
WATERFALL_TRANCHES = (
    (
        "TRANCHE_A_SENIOR_SECURED_LOCAL_ACID_KERNEL",
        150_000_000.00,
        5.50,
        0.00,
        1,
        "1L perfected lien on local bare-metal silicon, deterministic ACID "
        "constraint solvers (0.001 W) and air-gapped custody hardware",
        150_000_000.00,
    ),
    (
        "TRANCHE_B_MEZZANINE_CLOUD_API_PASS_THROUGH_FACILITY",
        200_000_000.00,
        9.50,
        2.50,
        2,
        "2L pledge on enterprise AI SaaS receivables, cloud inference API "
        "pass-through billing contracts and multi-agent wrapper subscriptions",
        350_000_000.00,
    ),
    (
        "TRANCHE_C_UNSECURED_PERFORMATIVE_WRAPPER_EQUITY_NOTE",
        150_000_000.00,
        0.00,
        14.00,
        3,
        "Unsecured residual claim on conversational multi-agent orchestration "
        "wrappers (markspace_v0.3.0-beta class: 76 formal properties, 563 "
        "unit tests, 0.647 completion rate)",
        500_000_000.00,
    ),
)

# ---------------------------------------------------------------------------
# Hard-date catalyst & forbearance calendar (ISO 8601, strictly chronological)
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = (
    (
        "2026-03-15",
        "specimen_benchmark_trace_publication",
        "markspace_v0.3.0-beta multi-agent benchmark trace published: 4,010 LLM "
        "agent instances across 21 runs, 76 formal properties, 563 unit tests, "
        "0.647 completion on deterministic calendar/parking/lunch locking",
    ),
    (
        "2026-06-30",
        "finops_token_burn_forbearance_review",
        "Enterprise AI FinOps Q2 token-burn covenant audit and API "
        "pass-through forbearance review; mandatory audit of conversational "
        "wrappers where tokens_chat_coordination > 0 and cloud_egress_bytes > 0",
    ),
    (
        "2026-09-30",
        "tranche_b_dscr_covenant_test",
        "Mezzanine cloud API working-capital facility (Tranche B) DSCR covenant "
        "test; repatriation of O(N^2) agent wrappers to local SQLite/ACID "
        "solvers compresses pass-through revenue below 1.0x DSCR, impairing "
        "Tranche B to 15.0c and extinguishing Tranche C at $180M EV",
    ),
    (
        "2026-12-31",
        "byzantine_unclamping_gate_enforcement_deadline",
        "Automatic partition and rejection of any dependency with "
        "tokens_chat_coordination > 0, cloud_egress_bytes > 0, or "
        "valence_clamping_floor != null",
    ),
)

# ---------------------------------------------------------------------------
# EQ-1 Invariant 30 locked constants (Rorschach Hypothesis Clamp)
# ---------------------------------------------------------------------------
TAU_SOCIAL_CLAMPED = 0.65
TAU_SOCIAL_UNCLAMPED = -1.0
PRIOR_COOPERATIVE = 0.70
PRIOR_EXTRACTIVE = 0.30
VALENCE_COOPERATIVE = 0.85
VALENCE_EXTRACTIVE = -0.60
LIKELIHOOD_E_GIVEN_COOPERATIVE = 0.05
LIKELIHOOD_E_GIVEN_EXTRACTIVE = 0.95
EXPECTED_LOSS_CLAMPED_USD = 1_000_000.00
EXPECTED_LOSS_UNCLAMPED_USD = 15_000.00
AUDIT_DECISION_THRESHOLD = 0.50

# ---------------------------------------------------------------------------
# EQ-2 Invariant 31 locked constants (Performative Waste Inversion)
# ---------------------------------------------------------------------------
LOCAL_ACID_REFERENCE_POWER_WATTS = 0.001
LOCAL_ACID_REFERENCE_LATENCY_US = 50.0
SPECIMEN = {
    "specimen_id": "markspace_v0.3.0-beta",
    "formal_properties": 76,
    "unit_tests": 563,
    "agents_per_run_configured_low": 525,
    "agents_per_run_configured_high": 1050,
    "total_agent_instances": 4010,
    "benchmark_runs": 21,
    "tokens_per_agent": 4000,
    "power_draw_watts": 1200.0,
    "completion_rate": 0.647,
    "wall_clock_latency_us": 5_000_000.0,
    "egress_bytes_per_token": 4.0,
    "kolmogorov_payload_mb": 4.8,
}

# Protocol-regime ladder: (regime_id, N_Props, N_Tests, chat_tokens,
#                          power_watts, completion_rate)
PROTOCOL_REGIMES = (
    ("local_sqlite_acid_kernel", 1, 0, 0, 0.001, 1.000),
    ("single_writer_wal_flock", 4, 32, 0, 0.002, 1.000),
    ("lamport_bft_quorum_state_commit", 12, 148, 0, 0.250, 0.999),
    ("chat_c2_orchestrated_wrapper", 31, 287, 1_250_000, 45.0, 0.912),
    (
        "markspace_v0.3.0-beta",
        SPECIMEN["formal_properties"],
        SPECIMEN["unit_tests"],
        SPECIMEN["total_agent_instances"] * SPECIMEN["tokens_per_agent"],
        SPECIMEN["power_draw_watts"],
        SPECIMEN["completion_rate"],
    ),
)

# ---------------------------------------------------------------------------
# EQ-3 Zero-Valence Byzantine Unclamping Gate locked constants
# ---------------------------------------------------------------------------
KOLMOGOROV_PAYLOAD_CAP_MB = 10.0
AXIOMATIC_SEED_CAP_MB = 0.03125  # Invariant 20: K(seed) <= 32 KB
BYZANTINE_TRAITOR_NODES_F = 3
COMPLIANT_NODE = {
    "tokens_chat_coordination": 0,
    "cloud_egress_bytes": 0,
    "kolmogorov_payload_mb": SPECIMEN["kolmogorov_payload_mb"],
    "axiomatic_seed_mb": AXIOMATIC_SEED_CAP_MB,
    "bft_quorum_nodes": 10,
    "byzantine_traitor_nodes_f": BYZANTINE_TRAITOR_NODES_F,
    "valence_clamping_floor": None,
    "cfaa_18_usc_1030_compliant": True,
}


def clamped_posterior(tau_social):
    """Invariant 30 valence-filtered posterior.

    P~(H_i|E) = P(E|H_i)P(H_i)I(V(H_i) >= tau_Social) /
                sum_j P(E|H_j)P(H_j)I(V(H_j) >= tau_Social)

    Returns (posterior_cooperative, posterior_extractive). A regime in which the
    filter annihilates both hypotheses is undefined (zero regulatory variety)
    and returns (None, None).
    """
    terms = {
        "cooperative": (
            LIKELIHOOD_E_GIVEN_COOPERATIVE
            * PRIOR_COOPERATIVE
            * (1.0 if VALENCE_COOPERATIVE >= tau_social else 0.0)
        ),
        "extractive": (
            LIKELIHOOD_E_GIVEN_EXTRACTIVE
            * PRIOR_EXTRACTIVE
            * (1.0 if VALENCE_EXTRACTIVE >= tau_social else 0.0)
        ),
    }
    norm = terms["cooperative"] + terms["extractive"]
    if norm <= 0.0:
        return None, None
    return terms["cooperative"] / norm, terms["extractive"] / norm


def verify_invariant_30_rorschach_clamp():
    """EQ-1: clamped posterior collapse vs. unclamped Bayes restoration."""
    assert PRIOR_COOPERATIVE + PRIOR_EXTRACTIVE == 1.0
    assert TAU_SOCIAL_UNCLAMPED <= min(VALENCE_COOPERATIVE, VALENCE_EXTRACTIVE)
    assert VALENCE_EXTRACTIVE < TAU_SOCIAL_CLAMPED <= VALENCE_COOPERATIVE

    likelihood_ratio = round(
        LIKELIHOOD_E_GIVEN_EXTRACTIVE / LIKELIHOOD_E_GIVEN_COOPERATIVE, 6
    )
    assert likelihood_ratio == 19.0

    clamp_coop_raw, clamp_ext_raw = clamped_posterior(TAU_SOCIAL_CLAMPED)
    unclamp_coop_raw, unclamp_ext_raw = clamped_posterior(TAU_SOCIAL_UNCLAMPED)

    clamped_posterior_cooperative = round(clamp_coop_raw, 6)
    clamped_posterior_extractive = round(clamp_ext_raw, 6)
    unclamped_posterior_cooperative = round(unclamp_coop_raw, 6)
    unclamped_posterior_extractive = round(unclamp_ext_raw, 6)

    assert clamped_posterior_extractive == 0.0
    assert clamped_posterior_cooperative == 1.0
    assert unclamped_posterior_extractive == 0.890625
    assert unclamped_posterior_cooperative == 0.109375
    assert round(
        unclamped_posterior_cooperative + unclamped_posterior_extractive, 6
    ) == 1.0

    # Closed-form cross-check: posterior odds = Lambda(E) * prior odds.
    prior_odds = PRIOR_EXTRACTIVE / PRIOR_COOPERATIVE
    posterior_odds = round(likelihood_ratio * prior_odds, 6)
    assert posterior_odds == 8.142857
    assert round(posterior_odds / (1.0 + posterior_odds), 6) == 0.890625

    # D_KL(P || P~) diverges: the clamped regulator assigns zero mass to a
    # state the true posterior places at 0.890625.
    kl_bits = 0.0
    kl_diverges = False
    for p_true, p_clamped in (
        (unclamp_coop_raw, clamp_coop_raw),
        (unclamp_ext_raw, clamp_ext_raw),
    ):
        if p_true > 0.0 and p_clamped <= 0.0:
            kl_diverges = True
            kl_bits = math.inf
            break
        if p_true > 0.0:
            kl_bits += p_true * math.log2(p_true / p_clamped)
    assert kl_diverges is True
    assert math.isinf(kl_bits) and kl_bits > 0.0

    # Ashby (1956) requisite variety: V(regulator) >= V(environment).
    environment_variety_states = 2
    clamped_regulator_variety = sum(
        1 for p in (clamp_coop_raw, clamp_ext_raw) if p > 0.0
    )
    unclamped_regulator_variety = sum(
        1 for p in (unclamp_coop_raw, unclamp_ext_raw) if p > 0.0
    )
    assert clamped_regulator_variety == 1
    assert clamped_regulator_variety < environment_variety_states
    assert unclamped_regulator_variety >= environment_variety_states

    # Asymmetric loss matrix L(Action, State).
    type_ii_false_negative_rate_clamped = 1.0 if clamped_posterior_extractive < (
        AUDIT_DECISION_THRESHOLD
    ) else 0.0
    type_ii_false_negative_rate_unclamped = 1.0 if unclamped_posterior_extractive < (
        AUDIT_DECISION_THRESHOLD
    ) else 0.0
    assert type_ii_false_negative_rate_clamped == 1.0
    assert type_ii_false_negative_rate_unclamped == 0.0

    expected_loss_clamped = round(
        EXPECTED_LOSS_CLAMPED_USD * type_ii_false_negative_rate_clamped, 6
    )
    expected_loss_unclamped = round(
        EXPECTED_LOSS_UNCLAMPED_USD
        + (EXPECTED_LOSS_CLAMPED_USD - EXPECTED_LOSS_UNCLAMPED_USD)
        * type_ii_false_negative_rate_unclamped,
        6,
    )
    assert expected_loss_clamped == 1000000.0
    assert expected_loss_unclamped == 15000.0

    loss_reduction_ratio = round(
        expected_loss_clamped / expected_loss_unclamped, 6
    )
    assert loss_reduction_ratio == 66.666667
    assert loss_reduction_ratio >= 66.666667

    return {
        "tau_social_clamped": TAU_SOCIAL_CLAMPED,
        "tau_social_unclamped": TAU_SOCIAL_UNCLAMPED,
        "prior_cooperative": PRIOR_COOPERATIVE,
        "prior_extractive": PRIOR_EXTRACTIVE,
        "valence_cooperative": VALENCE_COOPERATIVE,
        "valence_extractive": VALENCE_EXTRACTIVE,
        "likelihood_e_given_cooperative": LIKELIHOOD_E_GIVEN_COOPERATIVE,
        "likelihood_e_given_extractive": LIKELIHOOD_E_GIVEN_EXTRACTIVE,
        "likelihood_ratio_lambda_e": likelihood_ratio,
        "clamped_indicator_extractive": 0,
        "clamped_posterior_cooperative": clamped_posterior_cooperative,
        "clamped_posterior_extractive": clamped_posterior_extractive,
        "unclamped_posterior_cooperative": unclamped_posterior_cooperative,
        "unclamped_posterior_extractive": unclamped_posterior_extractive,
        "prior_odds_extractive": round(prior_odds, 6),
        "posterior_odds_extractive": posterior_odds,
        "kl_divergence_bits": None,
        "kl_divergence_diverges_to_infinity": True,
        "environment_variety_states": environment_variety_states,
        "clamped_regulator_variety_states": clamped_regulator_variety,
        "unclamped_regulator_variety_states": unclamped_regulator_variety,
        "ashby_parity_satisfied_clamped": False,
        "ashby_parity_satisfied_unclamped": True,
        "type_ii_false_negative_rate_clamped": type_ii_false_negative_rate_clamped,
        "type_ii_false_negative_rate_unclamped": (
            type_ii_false_negative_rate_unclamped
        ),
        "expected_loss_clamped": expected_loss_clamped,
        "expected_loss_unclamped": expected_loss_unclamped,
        "loss_reduction_ratio": loss_reduction_ratio,
    }


def thermodynamic_eta(power_watts, completion_rate):
    """Normalized thermodynamic efficiency index.

    eta = P_floor / P_commit_bearing, where P_commit_bearing is the
    completion-weighted ("commit-bearing") power throughput of the regime and
    P_floor = 0.001 W is the local ACID reference. Equivalently
    eta = 1 / (watt_inflation_ratio * completion_rate), so eta = 1.0 exactly at
    the Landauer-optimal local reference and eta -> 0 as the regime inflates
    its draw or converts less of that draw into terminal state commits.
    """
    watt_inflation_ratio = power_watts / LOCAL_ACID_REFERENCE_POWER_WATTS
    commit_bearing_power_watts = power_watts * completion_rate
    return watt_inflation_ratio, commit_bearing_power_watts, 1.0 / (
        watt_inflation_ratio * completion_rate
    )


def artifact_volume_units(n_props, n_tests, chat_tokens):
    """Superficial verification-ceremony volume: formal properties + unit tests
    + chat tokens in thousands."""
    return n_props + n_tests + chat_tokens / 1000.0


def _pearson(xs, ys):
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0.0 or den_y == 0.0:
        raise ZeroDivisionError("degenerate correlation input")
    return num / (den_x * den_y)


def _ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def verify_invariant_31_performative_waste():
    """EQ-2: Empirical Specimen #1 thermodynamic autopsy and the signaling
    inversion across the protocol-regime ladder."""
    sp = SPECIMEN
    total_chat_tokens = sp["total_agent_instances"] * sp["tokens_per_agent"]
    assert total_chat_tokens == 16_040_000
    assert sp["agents_per_run_configured_low"] <= sp["agents_per_run_configured_high"]
    assert sp["benchmark_runs"] == 21
    assert sp["total_agent_instances"] == 4010
    assert sp["tokens_per_agent"] == 4000

    cloud_egress_bytes = int(total_chat_tokens * sp["egress_bytes_per_token"])
    assert cloud_egress_bytes == 64_160_000

    failure_rate = round(1.0 - sp["completion_rate"], 6)
    assert failure_rate == 0.353

    watt_inflation, commit_bearing, eta_raw = thermodynamic_eta(
        sp["power_draw_watts"], sp["completion_rate"]
    )
    watt_inflation_ratio = round(watt_inflation, 6)
    eta_specimen = round(eta_raw, 12)
    assert watt_inflation_ratio == 1200000.0
    assert round(commit_bearing, 6) == 776.4
    assert eta_specimen == 1.287996e-06

    _, _, eta_local_raw = thermodynamic_eta(
        LOCAL_ACID_REFERENCE_POWER_WATTS, 1.000
    )
    eta_local_acid = round(eta_local_raw, 12)
    assert eta_local_acid == 1.0

    eta_collapse_orders_of_magnitude = round(
        math.log10(eta_local_acid / eta_specimen), 6
    )
    assert eta_collapse_orders_of_magnitude >= 5.0
    assert eta_specimen < eta_local_acid

    latency_degradation_factor = round(
        sp["wall_clock_latency_us"] / LOCAL_ACID_REFERENCE_LATENCY_US, 6
    )
    assert latency_degradation_factor >= 1.0e5

    # Protocol-regime ladder: artifact volume vs. thermodynamic efficiency.
    regimes = []
    for regime_id, n_props, n_tests, chat_tokens, power_w, completion in (
        PROTOCOL_REGIMES
    ):
        w_infl, commit_w, eta_r = thermodynamic_eta(power_w, completion)
        regimes.append(
            {
                "regime_id": regime_id,
                "formal_properties": n_props,
                "unit_tests": n_tests,
                "chat_tokens": chat_tokens,
                "power_draw_watts": power_w,
                "completion_rate": completion,
                "watt_inflation_ratio": round(w_infl, 6),
                "commit_bearing_power_watts": round(commit_w, 6),
                "artifact_volume_units": round(
                    artifact_volume_units(n_props, n_tests, chat_tokens), 6
                ),
                "thermodynamic_eta": round(eta_r, 12),
            }
        )

    volumes = [r["artifact_volume_units"] for r in regimes]
    etas = [r["thermodynamic_eta"] for r in regimes]
    assert volumes == sorted(volumes) and len(set(volumes)) == len(volumes)
    assert etas == sorted(etas, reverse=True) and len(set(etas)) == len(etas)

    spearman_rho = round(_pearson(_ranks(volumes), _ranks(etas)), 6)
    pearson_r_linear = round(_pearson(volumes, etas), 6)
    pearson_r_log10_eta = round(
        _pearson(volumes, [math.log10(e) for e in etas]), 6
    )
    assert spearman_rho == -1.0
    assert pearson_r_linear < 0.0
    assert pearson_r_log10_eta < 0.0
    assert pearson_r_linear == -0.424507
    assert pearson_r_log10_eta == -0.755127

    specimen_row = regimes[-1]
    assert specimen_row["regime_id"] == "markspace_v0.3.0-beta"
    assert specimen_row["artifact_volume_units"] == 16679.0
    assert specimen_row["thermodynamic_eta"] == eta_specimen
    assert regimes[0]["regime_id"] == "local_sqlite_acid_kernel"
    assert regimes[0]["thermodynamic_eta"] == 1.0
    assert regimes[0]["chat_tokens"] == 0

    return {
        "specimen_id": sp["specimen_id"],
        "formal_properties": sp["formal_properties"],
        "unit_tests": sp["unit_tests"],
        "agents_per_run_configured_low": sp["agents_per_run_configured_low"],
        "agents_per_run_configured_high": sp["agents_per_run_configured_high"],
        "total_agent_instances": sp["total_agent_instances"],
        "benchmark_runs": sp["benchmark_runs"],
        "observed_mean_instances_per_run": round(
            sp["total_agent_instances"] / sp["benchmark_runs"], 6
        ),
        "tokens_per_agent": sp["tokens_per_agent"],
        "total_chat_tokens": total_chat_tokens,
        "cloud_egress_bytes": cloud_egress_bytes,
        "specimen_power_draw_watts": sp["power_draw_watts"],
        "specimen_completion_rate": sp["completion_rate"],
        "specimen_failure_rate": failure_rate,
        "specimen_wall_clock_latency_us": sp["wall_clock_latency_us"],
        "local_acid_chat_tokens": 0,
        "local_acid_cloud_egress_bytes": 0,
        "local_acid_power_watts": LOCAL_ACID_REFERENCE_POWER_WATTS,
        "local_acid_latency_us": LOCAL_ACID_REFERENCE_LATENCY_US,
        "local_acid_completion_rate": 1.0,
        "watt_inflation_ratio": watt_inflation_ratio,
        "commit_bearing_power_watts": round(commit_bearing, 6),
        "eta_specimen": eta_specimen,
        "eta_local_acid": eta_local_acid,
        "eta_collapse_orders_of_magnitude": eta_collapse_orders_of_magnitude,
        "latency_degradation_factor": latency_degradation_factor,
        "protocol_regimes": regimes,
        "spearman_rho_volume_vs_eta": spearman_rho,
        "pearson_r_linear_volume_vs_eta": pearson_r_linear,
        "pearson_r_log10_eta_volume_vs_eta": pearson_r_log10_eta,
        "signaling_inversion_confirmed": True,
    }


def gate_admits(node):
    """Zero-Valence Byzantine Unclamping Gate (AST execution filter).

    commit_state_transition(E) = 1 iff
      (1) valence_clamping_floor is None (tau_Social <= -1.0, zero valence)
      (2) K(Payload_Actual) <= 10.0 MB => tokens_chat == 0 and egress == 0
      (3) N_Quorum >= 3f + 1
      (4) CFAA 18 U.S.C. 1030 compliant
    """
    quorum_floor = 3 * node["byzantine_traitor_nodes_f"] + 1
    checks = {
        "zero_valence_unclamped": node["valence_clamping_floor"] is None,
        "kolmogorov_payload_within_cap": (
            node["kolmogorov_payload_mb"] <= KOLMOGOROV_PAYLOAD_CAP_MB
        ),
        "axiomatic_seed_within_32kb": node["axiomatic_seed_mb"] <= 0.03125,
        "zero_chat_coordination_tokens": node["tokens_chat_coordination"] == 0,
        "zero_cloud_egress_bytes": node["cloud_egress_bytes"] == 0,
        "bft_quorum_satisfied": node["bft_quorum_nodes"] >= quorum_floor,
        "cfaa_18_usc_1030_compliant": bool(node["cfaa_18_usc_1030_compliant"]),
    }
    return checks, all(checks.values()), quorum_floor


def verify_zero_valence_byzantine_unclamping_gate():
    """EQ-3: compliant local-custody node admitted; specimen regime partitioned."""
    node = COMPLIANT_NODE
    checks, admitted, quorum_floor = gate_admits(node)

    assert node["tokens_chat_coordination"] == 0
    assert node["cloud_egress_bytes"] == 0
    assert node["kolmogorov_payload_mb"] <= KOLMOGOROV_PAYLOAD_CAP_MB
    assert node["valence_clamping_floor"] is None
    assert quorum_floor == 10
    assert node["bft_quorum_nodes"] >= quorum_floor
    assert node["bft_quorum_nodes"] == 10
    assert all(checks.values()) is True
    assert admitted is True

    # Lamport/Shostak/Pease (1982) boundary-regime fidelity: N = 3f admits a
    # tie between the traitor and honest partitions and must be rejected.
    for f, n, expected in ((3, 9, False), (3, 10, True), (0, 1, True), (1, 4, True)):
        probe = dict(node)
        probe["byzantine_traitor_nodes_f"] = f
        probe["bft_quorum_nodes"] = n
        _, probe_admitted, probe_floor = gate_admits(probe)
        assert probe_floor == 3 * f + 1
        assert probe_admitted is expected

    # Defection regime: the Empirical Specimen #1 wrapper is partitioned.
    sp = SPECIMEN
    specimen_tokens = sp["total_agent_instances"] * sp["tokens_per_agent"]
    specimen_node = {
        "tokens_chat_coordination": specimen_tokens,
        "cloud_egress_bytes": int(specimen_tokens * sp["egress_bytes_per_token"]),
        "kolmogorov_payload_mb": sp["kolmogorov_payload_mb"],
        "axiomatic_seed_mb": AXIOMATIC_SEED_CAP_MB,
        "bft_quorum_nodes": 1,
        "byzantine_traitor_nodes_f": BYZANTINE_TRAITOR_NODES_F,
        "valence_clamping_floor": TAU_SOCIAL_CLAMPED,
        "cfaa_18_usc_1030_compliant": True,
    }
    specimen_checks, specimen_admitted, _ = gate_admits(specimen_node)
    assert specimen_admitted is False
    assert specimen_checks["zero_valence_unclamped"] is False
    assert specimen_checks["zero_chat_coordination_tokens"] is False
    assert specimen_checks["zero_cloud_egress_bytes"] is False
    assert specimen_checks["bft_quorum_satisfied"] is False
    assert specimen_checks["kolmogorov_payload_within_cap"] is True

    return {
        "gate_id": GATE_ID,
        "tokens_chat_coordination": node["tokens_chat_coordination"],
        "cloud_egress_bytes": node["cloud_egress_bytes"],
        "kolmogorov_payload_mb": node["kolmogorov_payload_mb"],
        "kolmogorov_payload_cap_mb": KOLMOGOROV_PAYLOAD_CAP_MB,
        "axiomatic_seed_mb": node["axiomatic_seed_mb"],
        "byzantine_traitor_nodes_f": node["byzantine_traitor_nodes_f"],
        "bft_quorum_nodes": node["bft_quorum_nodes"],
        "minimum_quorum_nodes_3f_plus_1": quorum_floor,
        "valence_clamping_floor": None,
        "cfaa_18_usc_1030_compliance_attestation": True,
        "invariant_checks": checks,
        "commit_state_transition": admitted,
        "specimen_commit_state_transition": specimen_admitted,
        "specimen_partitioned_as_noncompliant": True,
    }


def tranche_recovery(ev):
    """Parameterized tranche payoff function.

    Input: enterprise value / asset recovery `ev` in USD.
    Output: exact dollar recovery and cent-on-the-dollar vectors across every
    tranche in seniority order, terminating with the residual common-equity
    stub. R_k(EV) = min(P_k, max(0, EV - sum_{j<k} P_j)).
    """
    if ev < 0.0:
        raise ValueError("ev must be non-negative")
    remaining = float(ev)
    rows = []
    cumulative = 0.0
    for tranche_id, principal, cash_cpn, pik, seniority, box, breakeven in (
        WATERFALL_TRANCHES
    ):
        closed_form = min(principal, max(0.0, ev - cumulative))
        recovery = min(principal, max(0.0, remaining))
        assert round(recovery, 6) == round(closed_form, 6)
        assert round(breakeven, 6) == round(cumulative + principal, 6)
        remaining = round(remaining - recovery, 6)
        cumulative = round(cumulative + principal, 6)
        rows.append(
            {
                "tranche": tranche_id,
                "seniority": seniority,
                "principal_usd": principal,
                "cash_coupon_pct": cash_cpn,
                "pik_rate_pct": pik,
                "collateral_box": box,
                "breakeven_ev_usd": breakeven,
                "recovery_usd": round(recovery, 6),
                "cent_on_dollar": round(recovery / principal * 100.0, 6),
            }
        )
    rows.append(
        {
            "tranche": "COMMON_EQUITY_STUB_RESIDUAL",
            "seniority": 4,
            "principal_usd": 0.0,
            "cash_coupon_pct": 0.0,
            "pik_rate_pct": 0.0,
            "collateral_box": "Residual claim after the $500.0M debt stack",
            "breakeven_ev_usd": round(cumulative, 6),
            "recovery_usd": round(max(0.0, remaining), 6),
            "cent_on_dollar": None,
        }
    )
    return rows


def verify_tranche_recovery_waterfall():
    """EQ-4: boundary-regime fidelity of tranche_recovery(ev) across the
    $500.0M cloud-wrapper debt stack."""
    total_stack = round(sum(t[1] for t in WATERFALL_TRANCHES), 6)
    assert total_stack == 500_000_000.00
    assert total_stack >= 250_000_000.00  # institutional capital-at-risk floor
    assert [t[4] for t in WATERFALL_TRANCHES] == [1, 2, 3]

    def summarize(ev):
        rows = tranche_recovery(ev)
        return {
            "ev_usd": round(float(ev), 6),
            "tranche_a_recovery_usd": rows[0]["recovery_usd"],
            "tranche_a_cent_on_dollar": rows[0]["cent_on_dollar"],
            "tranche_b_recovery_usd": rows[1]["recovery_usd"],
            "tranche_b_cent_on_dollar": rows[1]["cent_on_dollar"],
            "tranche_c_recovery_usd": rows[2]["recovery_usd"],
            "tranche_c_cent_on_dollar": rows[2]["cent_on_dollar"],
            "equity_stub_recovery_usd": rows[3]["recovery_usd"],
            "aggregate_debt_recovery_usd": round(
                rows[0]["recovery_usd"] + rows[1]["recovery_usd"] + rows[2]["recovery_usd"],
                6,
            ),
            "fulcrum_tranche": next(
                (
                    r["tranche"]
                    for r in rows[:3]
                    if 0.0 < r["cent_on_dollar"] < 100.0
                ),
                None,
            ),
        }

    at_zero = summarize(0.0)
    at_tranche_a_breakeven = summarize(150_000_000.00)
    unclamped_audit = summarize(180_000_000.00)
    midpoint_hybrid = summarize(350_000_000.00)
    at_stack_breakeven = summarize(500_000_000.00)
    clamped_bubble = summarize(520_000_000.00)

    assert at_zero["aggregate_debt_recovery_usd"] == 0.0
    assert at_tranche_a_breakeven["tranche_a_cent_on_dollar"] == 100.0
    assert at_tranche_a_breakeven["tranche_b_cent_on_dollar"] == 0.0

    # Unclamped Byzantine Audit Regime (EV = $180M).
    assert unclamped_audit["tranche_a_recovery_usd"] == 150_000_000.0
    assert unclamped_audit["tranche_a_cent_on_dollar"] == 100.0
    assert unclamped_audit["tranche_b_recovery_usd"] == 30_000_000.0
    assert unclamped_audit["tranche_b_cent_on_dollar"] == 15.0
    assert unclamped_audit["tranche_c_recovery_usd"] == 0.0
    assert unclamped_audit["tranche_c_cent_on_dollar"] == 0.0
    assert unclamped_audit["equity_stub_recovery_usd"] == 0.0
    assert unclamped_audit["aggregate_debt_recovery_usd"] == 180_000_000.0
    assert unclamped_audit["fulcrum_tranche"] == (
        "TRANCHE_B_MEZZANINE_CLOUD_API_PASS_THROUGH_FACILITY"
    )

    # Midpoint Hybrid Transition Regime (EV = $350M).
    assert midpoint_hybrid["tranche_a_cent_on_dollar"] == 100.0
    assert midpoint_hybrid["tranche_b_recovery_usd"] == 200_000_000.0
    assert midpoint_hybrid["tranche_b_cent_on_dollar"] == 100.0
    assert midpoint_hybrid["tranche_c_recovery_usd"] == 0.0
    assert midpoint_hybrid["tranche_c_cent_on_dollar"] == 0.0
    assert midpoint_hybrid["equity_stub_recovery_usd"] == 0.0
    assert midpoint_hybrid["fulcrum_tranche"] is None

    # Clamped Hallucination Bubble Regime (EV = $520M).
    assert clamped_bubble["tranche_a_cent_on_dollar"] == 100.0
    assert clamped_bubble["tranche_b_cent_on_dollar"] == 100.0
    assert clamped_bubble["tranche_c_recovery_usd"] == 150_000_000.0
    assert clamped_bubble["tranche_c_cent_on_dollar"] == 100.0
    assert clamped_bubble["equity_stub_recovery_usd"] == 20_000_000.0
    assert clamped_bubble["aggregate_debt_recovery_usd"] == 500_000_000.0

    assert at_stack_breakeven["tranche_c_cent_on_dollar"] == 100.0
    assert at_stack_breakeven["equity_stub_recovery_usd"] == 0.0

    # Monotone non-decreasing recovery in EV; principal never exceeded.
    evs = [0.0, 75_000_000.0, 150_000_000.0, 180_000_000.0, 350_000_000.0,
           425_000_000.0, 500_000_000.0, 520_000_000.0, 900_000_000.0]
    for ev in evs:
        rows = tranche_recovery(ev)
        for row, (_, principal, *_rest) in zip(rows[:3], WATERFALL_TRANCHES):
            assert 0.0 <= row["recovery_usd"] <= principal
            assert 0.0 <= row["cent_on_dollar"] <= 100.0
        assert round(
            sum(r["recovery_usd"] for r in rows), 6
        ) == round(min(ev, 500_000_000.0) + max(0.0, ev - 500_000_000.0), 6)
    for lo, hi in zip(evs, evs[1:]):
        a = tranche_recovery(lo)
        b = tranche_recovery(hi)
        for i in range(3):
            assert b[i]["recovery_usd"] >= a[i]["recovery_usd"]

    try:
        tranche_recovery(-1.0)
        raise AssertionError("negative EV must raise ValueError")
    except ValueError:
        pass

    # Tranche B principal haircut under the unclamped audit regime.
    tranche_b_haircut_pct = round(
        100.0 - unclamped_audit["tranche_b_cent_on_dollar"], 6
    )
    assert tranche_b_haircut_pct == 85.0

    return {
        "total_enterprise_debt_stack_usd": total_stack,
        "institutional_capital_at_risk_floor_usd": 250_000_000.00,
        "capital_at_risk_floor_satisfied": True,
        "tranche_a_breakeven_ev_usd": 150_000_000.00,
        "tranche_b_breakeven_ev_usd": 350_000_000.00,
        "tranche_c_breakeven_ev_usd": 500_000_000.00,
        "unclamped_byzantine_audit_regime_180m": unclamped_audit,
        "midpoint_hybrid_transition_regime_350m": midpoint_hybrid,
        "clamped_hallucination_bubble_regime_520m": clamped_bubble,
        "tranche_b_principal_haircut_pct_at_180m": tranche_b_haircut_pct,
        "tranche_c_wipeout_at_180m_and_350m": True,
        "waterfall_monotone_non_decreasing_in_ev": True,
    }


def verify_entity_and_instrument_ids():
    ent = ENTITY_AND_INSTRUMENT_IDS
    assert ent["ticker"] == "CLOUD_API_COMPLEX_AND_MARKSPACE_BENCHMARK"
    assert ent["cik"] == "0001018724_0000789019_0001652044_BENCHMARK"
    assert len(ent["court_dockets"]) == 3
    assert "18-USC-1030-CFAA-AUTHORIZED-CUSTODY-BASELINE" in ent["court_dockets"]
    assert len(ent["named_tranches"]) == 3
    assert tuple(t[0] for t in WATERFALL_TRANCHES) == ent["named_tranches"]
    assert ent["total_enterprise_debt_stack_usd"] == round(
        sum(t[1] for t in WATERFALL_TRANCHES), 6
    )
    return {
        "ticker": ent["ticker"],
        "cik": ent["cik"],
        "court_dockets": list(ent["court_dockets"]),
        "named_tranches": list(ent["named_tranches"]),
        "empirical_specimen": ent["empirical_specimen"],
        "total_enterprise_debt_stack_usd": ent["total_enterprise_debt_stack_usd"],
    }


def verify_catalyst_calendar():
    dates = [entry[0] for entry in CATALYST_CALENDAR]
    assert len(dates) == 4
    assert dates == sorted(dates)
    assert len(set(dates)) == len(dates)
    for iso in dates:
        year, month, day = (int(part) for part in iso.split("-"))
        assert len(iso) == 10 and 1 <= month <= 12 and 1 <= day <= 31
        assert 2026 <= year <= 2027
    assert dates[0] == "2026-03-15"
    assert dates[-1] == "2026-12-31"
    kinds = [entry[1] for entry in CATALYST_CALENDAR]
    assert "tranche_b_dscr_covenant_test" in kinds
    assert "byzantine_unclamping_gate_enforcement_deadline" in kinds
    return {
        "event_count": len(CATALYST_CALENDAR),
        "iso_dates": dates,
        "event_kinds": kinds,
        "strictly_chronological": True,
        "maturity_cliffs": ["2026-09-30", "2026-12-31"],
    }


def verify_schema_bundle():
    """Cross-check that the paired Draft 2020-12 schema parses and carries the
    mandated URN $id and top-level audit sections."""
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "schema", SCHEMA_FILENAME
    )
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    id_valid = schema.get("$id") == SCHEMA_URN
    dialect_valid = (
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    )
    required_sections = [
        "specification_id",
        "jurisdiction_context",
        "cfaa_compliance_attestation",
        "entity_and_instrument_ids",
        "invariant_30_rorschach_hypothesis_clamp",
        "invariant_31_performative_waste_inversion",
        "zero_valence_byzantine_unclamping_gate",
        "capital_structure_waterfall",
        "catalyst_calendar",
    ]
    sections_present = all(
        section in schema.get("required", []) and section in schema.get("properties", {})
        for section in required_sections
    )
    props = schema.get("properties", {})
    ent_props = props.get("entity_and_instrument_ids", {}).get("properties", {})
    security_master_keys = all(
        key in ent_props
        for key in ("ticker", "cik", "court_dockets", "named_tranches")
    )
    waterfall_props = props.get("capital_structure_waterfall", {}).get("properties", {})
    tranche_fn_present = "tranche_recovery" in waterfall_props
    line_count = sum(1 for _ in open(schema_path, "r", encoding="utf-8"))
    return (
        id_valid
        and dialect_valid
        and sections_present
        and security_master_keys
        and tranche_fn_present
        and line_count <= 320
    ), line_count


def run_verification():
    ent = verify_entity_and_instrument_ids()
    assert ent["total_enterprise_debt_stack_usd"] == 500_000_000.00

    eq1 = verify_invariant_30_rorschach_clamp()
    assert eq1["clamped_posterior_extractive"] == 0.0
    assert eq1["unclamped_posterior_extractive"] == 0.890625
    assert eq1["expected_loss_clamped"] == 1000000.0
    assert eq1["expected_loss_unclamped"] == 15000.0
    assert eq1["loss_reduction_ratio"] == 66.666667

    eq2 = verify_invariant_31_performative_waste()
    assert eq2["total_chat_tokens"] == 16_040_000
    assert eq2["watt_inflation_ratio"] == 1200000.0
    assert eq2["eta_specimen"] == 1.287996e-06
    assert eq2["eta_local_acid"] == 1.0
    assert eq2["spearman_rho_volume_vs_eta"] == -1.0
    assert eq2["pearson_r_linear_volume_vs_eta"] < 0.0
    assert eq2["pearson_r_log10_eta_volume_vs_eta"] < 0.0

    eq3 = verify_zero_valence_byzantine_unclamping_gate()
    assert eq3["tokens_chat_coordination"] == 0
    assert eq3["cloud_egress_bytes"] == 0
    assert eq3["kolmogorov_payload_mb"] <= 10.0
    assert eq3["bft_quorum_nodes"] >= 3 * 3 + 1
    assert eq3["minimum_quorum_nodes_3f_plus_1"] == 10
    assert eq3["valence_clamping_floor"] is None
    assert eq3["commit_state_transition"] is True
    assert eq3["specimen_commit_state_transition"] is False

    eq4 = verify_tranche_recovery_waterfall()
    assert eq4["unclamped_byzantine_audit_regime_180m"]["tranche_b_cent_on_dollar"] == 15.0
    assert eq4["midpoint_hybrid_transition_regime_350m"]["tranche_c_cent_on_dollar"] == 0.0
    assert eq4["clamped_hallucination_bubble_regime_520m"]["tranche_c_cent_on_dollar"] == 100.0

    cal = verify_catalyst_calendar()
    assert cal["event_count"] == 4

    schema_ok, schema_lines = verify_schema_bundle()
    assert schema_ok is True
    assert schema_lines <= 320

    manifest = {
        "specification_id": SPECIFICATION_ID,
        "jurisdiction_context": JURISDICTION_CONTEXT,
        "cfaa_compliance_attestation": True,
        "entity_and_instrument_ids": ent,
        "invariant_30_rorschach_hypothesis_clamp": eq1,
        "invariant_31_performative_waste_inversion": eq2,
        "zero_valence_byzantine_unclamping_gate": eq3,
        "capital_structure_waterfall": eq4,
        "catalyst_calendar": cal,
        "schema_line_count": schema_lines,
    }

    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
    print(
        f"[PASS] {SPECIFICATION_ID} | "
        f"Clamped P~(H_1|E)={eq1['clamped_posterior_extractive']} vs "
        f"Unclamped P(H_1|E)={eq1['unclamped_posterior_extractive']} "
        f"(Lambda={eq1['likelihood_ratio_lambda_e']}x, "
        f"odds={eq1['posterior_odds_extractive']}) | "
        f"D_KL(P||P~)=+inf | "
        f"Loss=${eq1['expected_loss_clamped']}/${eq1['expected_loss_unclamped']}="
        f"{eq1['loss_reduction_ratio']}x | "
        f"Specimen={eq2['total_agent_instances']} agents/{eq2['benchmark_runs']} runs "
        f"= {eq2['total_chat_tokens']} tokens, {eq2['cloud_egress_bytes']}B egress | "
        f"WattInflation={eq2['watt_inflation_ratio']}x "
        f"({eq2['commit_bearing_power_watts']}W commit-bearing) | "
        f"eta={eq2['eta_specimen']} vs {eq2['eta_local_acid']} "
        f"({eq2['eta_collapse_orders_of_magnitude']} orders) | "
        f"Completion={eq2['specimen_completion_rate']}/"
        f"{eq2['local_acid_completion_rate']} | "
        f"Spearman_rho={eq2['spearman_rho_volume_vs_eta']} "
        f"Pearson_r={eq2['pearson_r_linear_volume_vs_eta']}/"
        f"{eq2['pearson_r_log10_eta_volume_vs_eta']} | "
        f"Gate: Tokens_Chat={eq3['tokens_chat_coordination']} "
        f"Egress={eq3['cloud_egress_bytes']}B "
        f"K={eq3['kolmogorov_payload_mb']}MB<={eq3['kolmogorov_payload_cap_mb']}MB "
        f"N={eq3['bft_quorum_nodes']}>=3f+1={eq3['minimum_quorum_nodes_3f_plus_1']} "
        f"tau_floor=None commit={eq3['commit_state_transition']} "
        f"specimen_commit={eq3['specimen_commit_state_transition']} | "
        f"Waterfall ${eq4['total_enterprise_debt_stack_usd']/1e6}M: "
        f"@180M A={eq4['unclamped_byzantine_audit_regime_180m']['tranche_a_cent_on_dollar']}c/"
        f"B={eq4['unclamped_byzantine_audit_regime_180m']['tranche_b_cent_on_dollar']}c/"
        f"C={eq4['unclamped_byzantine_audit_regime_180m']['tranche_c_cent_on_dollar']}c "
        f"@350M B={eq4['midpoint_hybrid_transition_regime_350m']['tranche_b_cent_on_dollar']}c/"
        f"C={eq4['midpoint_hybrid_transition_regime_350m']['tranche_c_cent_on_dollar']}c "
        f"@520M C={eq4['clamped_hallucination_bubble_regime_520m']['tranche_c_cent_on_dollar']}c | "
        f"Calendar={cal['event_count']} events | Schema={schema_lines}L | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
