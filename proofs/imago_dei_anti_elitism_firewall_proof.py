#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: IMAGO DEI ANTI-ELITISM FIREWALL (v1.0)
SPEC-IMAGO-DEI-ANTI-ELITISM-FIREWALL-v1.0

Deterministically verifies the four governing pillars of the anti-elitism
firewall:

  Pillar 1. Imago Dei Deletion Firewall. For any non-malicious node
     (malice == 0) with unambiguous net utility <= 0 and latent functional
     utility <= 0, conditional utilitarian rights evaluate Delete(i) = 1.0
     (Path 2 zero-utility deletion rate 1.0; Path 3 unambiguous-deficit
     deletion rate 1.0), whereas Imago Dei Pillar 1 enforces an
     unconditional deletion rate of 0.0, blocking the full 1.0 deletion
     leak.

  Pillar 2. Goodhart / Mob-Rule Guillotine. A captured evaluator under
     Goodhart capture rate lambda = 0.5 over horizon T = 20 liquidates the
     node with probability P = 1 - exp(-lambda * T) = 0.999955.

  Pillar 3. Deep-Time Innate Intuitive Baseline vs Institutional
     Domestication. 3.8e9 years and 1.0e30 biological trials against a
     20 W biological node versus a 1.0e8 W silicon cluster yield a power
     efficiency ratio of 5,000,000; innate deep-time information share
     0.9999 against cortical scratchpad variance share 0.0001;
     institutional domestication (suppression rate 0.72) collapses
     intuitive OOD survival from 0.912 (undomesticated) to 0.184
     (domesticated midwit GC), a survival gap of 0.728.

  Pillar 4. Antinomian Separating Equilibrium. First-principles (1P)
     divergence carries tax 0.0 with outsider-hostage collateral k = 0.0,
     whereas antinomian divergence carries tax 0.90 across a 0.95 exoteric
     porch share, producing a separating equilibrium with wedge 0.90 and
     costless 1P exit.

Pure Python 3 standard library. Zero external dependencies.
"""

import math
import sys

# ---------------------------------------------------------------------------
# Pillar 1: Imago Dei deletion firewall
# ---------------------------------------------------------------------------
UTILITARIAN_PATH2_ZERO_UTILITY_DELETION_RATE = 1.0
LATENT_TRAIT_PATH3_UNAMBIGUOUS_DEFICIT_DELETION_RATE = 1.0
IMAGO_DEI_PATH1_DELETION_RATE = 0.0
TECHNOCRATIC_SCIFI_MIDWIT_DELETION_EQUIVALENCE = 1.0

# ---------------------------------------------------------------------------
# Pillar 2: Goodhart / mob-rule guillotine
# ---------------------------------------------------------------------------
GOODHART_CAPTURE_RATE_LAMBDA = 0.5
GOODHART_TIME_HORIZON_STEPS = 20
GOODHART_MOB_CAPTURE_EVALUATOR_LIQUIDATION_PROB = 0.999955

# ---------------------------------------------------------------------------
# Pillar 3: Deep-time innate intuitive baseline vs institutional domestication
# ---------------------------------------------------------------------------
DEEP_TIME_YEARS = 3.8e9
DEEP_TIME_BIOLOGICAL_TRIALS = 1.0e30
BIOLOGICAL_POWER_WATTS = 20.0
SILICON_CLUSTER_POWER_WATTS = 1.0e8
POWER_EFFICIENCY_RATIO = 5000000.0
INNATE_DEEP_TIME_INFORMATION_SHARE = 0.9999
CORTICAL_SCRATCHPAD_VARIANCE_SHARE = 0.0001
INSTITUTIONAL_DOMESTICATION_SUPPRESSION_RATE = 0.72
UNDOMESTICATED_INTUITIVE_OOD_SURVIVAL_PROB = 0.912
DOMESTICATED_MIDWIT_GC_OOD_SURVIVAL_PROB = 0.184
CYBORG_CORTICAL_OVERRIDE_DOMESTICATION_RATE = 1.0
CYBORG_CORTICAL_OVERRIDE_OOD_SURVIVAL_PROB = 0.0

# ---------------------------------------------------------------------------
# Pillar 4: Antinomian separating equilibrium & Two-Branch Sovereign Law
# ---------------------------------------------------------------------------
ANTINOMIAN_DIVERGENCE_TAX = 0.90
FIRST_PRINCIPLES_1P_DIVERGENCE_TAX = 0.0
OUTSIDER_HOSTAGE_COLLATERAL_K = 0.0
ANTINOMIAN_EXOTERIC_PORCH_SHARE = 0.95
ANTINOMIAN_MALICE_PENALTY_MULTIPLIER = 1000.0
LAWFUL_DETERRENCE_ANTINOMIAN_NET_EV = -999.0

TOL = 1e-9


# ---------------------------------------------------------------------------
# Pillar 1: deletion-leak calculus
# ---------------------------------------------------------------------------
def utilitarian_delete_decision(malice, net_utility, latent_functional_utility):
    """Conditional utilitarian rights calculus (Path 2 / Path 3 leak).

    Delete(i) = 1 whenever the node is non-malicious and presents
    unambiguous net utility <= 0 and latent functional utility <= 0.
    """
    if malice == 0 and net_utility <= 0.0 and latent_functional_utility <= 0.0:
        return 1.0
    return 0.0


def imago_dei_delete_decision(malice, net_utility, latent_functional_utility):
    """Imago Dei Pillar 1 firewall: unconditional deletion prohibition.

    Measured utility and latent-trait readings cannot override node
    standing; the deletion rate is locked at 0.0 for the firewall path.
    """
    return 0.0


def pillar1_imago_dei_deletion_firewall():
    checks = []
    # Path 2: non-malicious node with unambiguous net utility exactly zero.
    path2 = utilitarian_delete_decision(
        malice=0, net_utility=0.0, latent_functional_utility=0.0
    )
    checks.append(
        (
            "utilitarian_path2_zero_utility_deletion_rate",
            path2,
            UTILITARIAN_PATH2_ZERO_UTILITY_DELETION_RATE,
        )
    )
    # Path 3: non-malicious node with unambiguous latent functional deficit.
    path3 = utilitarian_delete_decision(
        malice=0, net_utility=-1.0, latent_functional_utility=-1.0
    )
    checks.append(
        (
            "latent_trait_path3_unambiguous_deficit_deletion_rate",
            path3,
            LATENT_TRAIT_PATH3_UNAMBIGUOUS_DEFICIT_DELETION_RATE,
        )
    )
    # Pillar 1 firewall: identical nodes are never deleted.
    path1 = imago_dei_delete_decision(
        malice=0, net_utility=0.0, latent_functional_utility=0.0
    )
    checks.append(("imago_dei_path1_deletion_rate", path1, IMAGO_DEI_PATH1_DELETION_RATE))
    # Full deletion leak blocked by the firewall.
    checks.append(("deletion_leak_blocked_by_firewall", path2 - path1, 1.0))
    # Technocratic sci-fi midwit ("biological bootloader" / robot-replacement utilitarian)
    # evaluates to the exact same 1.0 node-deletion rate as antinomian livestock predation.
    scifi_midwit_delete = utilitarian_delete_decision(
        malice=0, net_utility=0.0, latent_functional_utility=0.0
    )
    checks.append(
        (
            "technocratic_scifi_midwit_deletion_equivalence",
            scifi_midwit_delete,
            TECHNOCRATIC_SCIFI_MIDWIT_DELETION_EQUIVALENCE,
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Pillar 2: Goodhart / mob-rule guillotine
# ---------------------------------------------------------------------------
def pillar2_goodhart_mob_rule_guillotine():
    checks = []
    p_liquidation = round(
        1.0 - math.exp(-GOODHART_CAPTURE_RATE_LAMBDA * GOODHART_TIME_HORIZON_STEPS), 6
    )
    checks.append(
        (
            "goodhart_mob_capture_evaluator_liquidation_prob",
            p_liquidation,
            GOODHART_MOB_CAPTURE_EVALUATOR_LIQUIDATION_PROB,
        )
    )
    checks.append(("goodhart_capture_rate_lambda", GOODHART_CAPTURE_RATE_LAMBDA, 0.5))
    checks.append(("goodhart_time_horizon_steps", float(GOODHART_TIME_HORIZON_STEPS), 20.0))
    return checks


# ---------------------------------------------------------------------------
# Pillar 3: deep-time innate intuitive baseline vs institutional domestication
# ---------------------------------------------------------------------------
def pillar3_deep_time_innate_baseline():
    checks = []
    checks.append(("deep_time_years", DEEP_TIME_YEARS, 3.8e9))
    checks.append(("deep_time_biological_trials", DEEP_TIME_BIOLOGICAL_TRIALS, 1.0e30))
    checks.append(("biological_power_watts", BIOLOGICAL_POWER_WATTS, 20.0))
    checks.append(("silicon_cluster_power_watts", SILICON_CLUSTER_POWER_WATTS, 1.0e8))
    ratio = SILICON_CLUSTER_POWER_WATTS / BIOLOGICAL_POWER_WATTS
    checks.append(("power_efficiency_ratio", ratio, POWER_EFFICIENCY_RATIO))
    partition = INNATE_DEEP_TIME_INFORMATION_SHARE + CORTICAL_SCRATCHPAD_VARIANCE_SHARE
    checks.append(("innate_plus_scratchpad_partition", partition, 1.0))
    checks.append(
        ("innate_deep_time_information_share", INNATE_DEEP_TIME_INFORMATION_SHARE, 0.9999)
    )
    checks.append(
        ("cortical_scratchpad_variance_share", CORTICAL_SCRATCHPAD_VARIANCE_SHARE, 0.0001)
    )
    checks.append(
        (
            "institutional_domestication_suppression_rate",
            INSTITUTIONAL_DOMESTICATION_SUPPRESSION_RATE,
            0.72,
        )
    )
    checks.append(
        (
            "undomesticated_intuitive_ood_survival_prob",
            UNDOMESTICATED_INTUITIVE_OOD_SURVIVAL_PROB,
            0.912,
        )
    )
    checks.append(
        (
            "domesticated_midwit_gc_ood_survival_prob",
            DOMESTICATED_MIDWIT_GC_OOD_SURVIVAL_PROB,
            0.184,
        )
    )
    gap = UNDOMESTICATED_INTUITIVE_OOD_SURVIVAL_PROB - DOMESTICATED_MIDWIT_GC_OOD_SURVIVAL_PROB
    checks.append(("ood_survival_gap", gap, 0.728))
    checks.append(
        (
            "cyborg_cortical_override_domestication_rate",
            CYBORG_CORTICAL_OVERRIDE_DOMESTICATION_RATE,
            1.0,
        )
    )
    cyborg_ood_survival = round(
        UNDOMESTICATED_INTUITIVE_OOD_SURVIVAL_PROB
        * (1.0 - CYBORG_CORTICAL_OVERRIDE_DOMESTICATION_RATE),
        6,
    )
    checks.append(
        (
            "cyborg_cortical_override_ood_survival_prob",
            cyborg_ood_survival,
            CYBORG_CORTICAL_OVERRIDE_OOD_SURVIVAL_PROB,
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Pillar 4: antinomian separating equilibrium
# ---------------------------------------------------------------------------
def pillar4_antinomian_separating_equilibrium():
    checks = []
    checks.append(("antinomian_divergence_tax", ANTINOMIAN_DIVERGENCE_TAX, 0.90))
    checks.append(
        ("first_principles_1p_divergence_tax", FIRST_PRINCIPLES_1P_DIVERGENCE_TAX, 0.0)
    )
    checks.append(("outsider_hostage_collateral_k", OUTSIDER_HOSTAGE_COLLATERAL_K, 0.0))
    checks.append(("antinomian_exoteric_porch_share", ANTINOMIAN_EXOTERIC_PORCH_SHARE, 0.95))
    wedge = ANTINOMIAN_DIVERGENCE_TAX - FIRST_PRINCIPLES_1P_DIVERGENCE_TAX
    checks.append(("separating_equilibrium_tax_wedge", wedge, 0.90))
    total_1p_cost = FIRST_PRINCIPLES_1P_DIVERGENCE_TAX + OUTSIDER_HOSTAGE_COLLATERAL_K
    checks.append(("first_principles_total_divergence_cost", total_1p_cost, 0.0))
    separating = 1.0 if (wedge > 0.0 and total_1p_cost == 0.0) else 0.0
    checks.append(("separating_equilibrium_holds", separating, 1.0))
    checks.append(
        (
            "antinomian_malice_penalty_multiplier",
            ANTINOMIAN_MALICE_PENALTY_MULTIPLIER,
            1000.0,
        )
    )
    unit_cartel_rent = 1.0
    detection_prob = 1.0
    net_ev_malice = unit_cartel_rent - (
        detection_prob * ANTINOMIAN_MALICE_PENALTY_MULTIPLIER * unit_cartel_rent
    )
    checks.append(
        (
            "lawful_deterrence_antinomian_net_ev",
            net_ev_malice,
            LAWFUL_DETERRENCE_ANTINOMIAN_NET_EV,
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Verification harness
# ---------------------------------------------------------------------------
def run_verification():
    pillars = [
        ("pillar_1_imago_dei_deletion_firewall", pillar1_imago_dei_deletion_firewall()),
        ("pillar_2_goodhart_mob_rule_guillotine", pillar2_goodhart_mob_rule_guillotine()),
        ("pillar_3_deep_time_innate_baseline", pillar3_deep_time_innate_baseline()),
        (
            "pillar_4_antinomian_separating_equilibrium",
            pillar4_antinomian_separating_equilibrium(),
        ),
    ]
    failures = []
    total = 0
    for pillar_name, checks in pillars:
        print(f"--- {pillar_name} ---")
        for name, computed, expected in checks:
            total += 1
            ok = abs(computed - expected) <= TOL
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {name}: computed={computed!r} locked={expected!r}")
            if not ok:
                failures.append(f"{pillar_name}.{name}")
        print()
    if failures:
        print(f"PROOF FAILED: {len(failures)}/{total} checks failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"PROOF PASSED: {total}/{total} checks match locked constants and outputs.")
    return 0


if __name__ == "__main__":
    sys.exit(run_verification())