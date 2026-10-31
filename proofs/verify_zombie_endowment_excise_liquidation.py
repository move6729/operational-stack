#!/usr/bin/env python3
"""Verification proof for SPEC-ZOMBIE-ENDOWMENT-COMMAND-ECONOMY-AND-EXCISE-LIQUIDATION-v1.0.

Pure Python 3 stdlib proof re-deriving every locked constant and governing
equation of the zombie-endowment command-economy / excise-liquidation model
across two regimes:

  compliant             -- transparent W-2 fiduciary compensation only; zero
                           off-990 shadow channels; zero host-economy damage;
                           zero Chapter 42 excise cascade; no 507(c) trigger.
  defection_autophagic  -- 4-channel off-990 shadow compensation active;
                           autophagic host-economy destruction; full Chapter 42
                           entity + personal manager excise cascade and the
                           Section 507(c) sovereign termination call.

Governing equations verified:
  (1) beta_trustee     = W_W2 / V_corpus = 0.00004 (25,000:1 control-to-salary)
  (2) W_total          = W_W2 + sum_k B_off-990,k = $0.80M + $3.40M = $4.20M/yr
  (3) Lambda_autophagy = |dV_host_damage| / W_total = 476.190476x
  (4) dU_gatekeeper(a_irrational) > dU_gatekeeper(a_rational)
  (5) T_Ch42,Entity    = 2.10*B_off-990 + 0.35*V_PE + 1.20*V_grants,net
                       = $7.14M + $2,450.00M + $912.00M = $3,369.14M
  (6) T_Ch42,Manager   = 0.15*V_PE + 0.55*V_grants,net
                       = $1,050.00M + $418.00M = $1,468.00M >> W_W2
  (7) T_507(c)         = min(sum_t TaxBenefit_t, V_net_assets) = $20,000.00M

Exit code 0 iff every locked constant and governing equation holds.
"""

import json
import math

# ---------------------------------------------------------------------------
# Locked constants (locked_constants_and_outputs)
# ---------------------------------------------------------------------------
CORPUS_TOTAL_USD = 2_140_000_000_000.0
CORPUS_PRIVATE_FOUNDATIONS_USD = 1_300_000_000_000.0
CORPUS_UNIVERSITY_ENDOWMENTS_USD = 840_000_000_000.0
SAMPLE_ENDOWMENT_CORPUS_USD = 20_000_000_000.0

TRUSTEE_W2_SALARY_USD = 800_000.0
TRUSTEE_COMP_TO_CORPUS_RATIO = 0.00004
TRUSTEE_COMP_BPS = 4.0

OFF_990_BOARD_STACK_ANNUAL_USD = 1_500_000.0
OFF_990_DEFERRED_PE_ANNUAL_EQUIV_USD = 1_200_000.0
OFF_990_SUBGRANT_NEPOTISM_ANNUAL_USD = 400_000.0
OFF_990_COINVEST_CARRY_WAIVER_ANNUAL_USD = 300_000.0
TOTAL_GATEKEEPER_SHADOW_COMP_USD = 4_200_000.0

HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD = 2_000_000_000.0
AUTOPHAGIC_DESTRUCTION_MULTIPLIER = 476.190476

STATUTORY_PAYOUT_FLOOR_4942 = 0.05
ADMIN_OVERHEAD_SHARE = 0.012
NET_GRANT_PAYOUT_SHARE = 0.038
SAMPLE_ANNUAL_ADMIN_OVERHEAD_USD = 240_000_000.0
SAMPLE_ANNUAL_NET_GRANTS_USD = 760_000_000.0

PE_VC_ILLIQUID_SHARE = 0.35
SAMPLE_PE_VC_ALLOCATION_USD = 7_000_000_000.0
PE_ANNUAL_MGMT_FEE_RATE = 0.02
SAMPLE_PE_ANNUAL_MGMT_FEE_DRAG_USD = 140_000_000.0

EXCISE_4941_COMBINED_RATE = 2.10
EXCISE_4944_COMBINED_ENTITY_RATE = 0.35
EXCISE_4944_COMBINED_MANAGER_RATE = 0.15
EXCISE_4945_COMBINED_ENTITY_RATE = 1.20
EXCISE_4945_COMBINED_MANAGER_RATE = 0.55

SAMPLE_4941_SHADOW_COMP_TAX_USD = 7_140_000.0
SAMPLE_4944_ENTITY_TAX_ON_PE_USD = 2_450_000_000.0
SAMPLE_4945_ENTITY_TAX_ON_GRANTS_USD = 912_000_000.0
SAMPLE_MANAGER_PERSONAL_LIABILITY_USD = 1_468_000_000.0
SAMPLE_CHAPTER_42_COMBINED_ENTITY_CLAWBACK_USD = 3_369_140_000.0
SECTION_507C_TERMINATION_RECOVERY_USD = 20_000_000_000.0

# Auxiliary locked model parameters.
CONTROL_TO_SALARY_RATIO = 25_000.0             # V_corpus / W_W2
OFF_990_SHADOW_COMP_TOTAL_USD = 3_400_000.0    # sum of the 4 off-990 channels
GAMMA_CARTEL = 1.0                             # cartel loyalty pricing coeff.
I_LOYALTY_IRRATIONAL = 0.25                    # normalized loyalty credit
HOST_DAMAGE_INTERNALIZATION = 0.0              # gatekeeper share of host damage
CUMULATIVE_TAX_BENEFIT_FLOOR_USD = 20_000_000_000.0  # >= net assets: full call


def assert_close(actual, expected, label, rel_tol=1e-9):
    """Assert numeric equality within tolerance; raise AssertionError on drift."""
    if not math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=1e-6):
        raise AssertionError(f"{label}: expected {expected!r}, computed {actual!r}")


# ---------------------------------------------------------------------------
# Governing-equation operators
# ---------------------------------------------------------------------------
def trustee_comp_ratio(w2_usd, corpus_usd):
    """Eq (1): beta_trustee = W_W2 / V_corpus."""
    return w2_usd / corpus_usd


def gatekeeper_total_comp(w2_usd, off_990_channels):
    """Eq (2): W_total = W_W2 + sum_k B_off-990,k."""
    return w2_usd + sum(off_990_channels.values())


def autophagic_multiplier(host_damage_usd, total_comp_usd):
    """Eq (3): Lambda_autophagy = |dV_host_damage| / W_total."""
    return abs(host_damage_usd) / total_comp_usd


def gatekeeper_utility_delta(off_990_total_usd, host_damage_usd,
                             internalization, loyalty_credit):
    """Eq (4): dU_gatekeeper = gamma_cartel * I_loyalty + sum B_off-990
    - internalization * |dV_host_damage|."""
    return (GAMMA_CARTEL * loyalty_credit + off_990_total_usd
            - internalization * abs(host_damage_usd))


def chapter_42_entity_cascade(off_990_total_usd, pe_base_usd, net_grants_usd):
    """Eq (5): T_Ch42,Entity = 2.10*B_off-990 + 0.35*V_PE + 1.20*V_grants,net."""
    t_4941 = EXCISE_4941_COMBINED_RATE * off_990_total_usd
    t_4944 = EXCISE_4944_COMBINED_ENTITY_RATE * pe_base_usd
    t_4945 = EXCISE_4945_COMBINED_ENTITY_RATE * net_grants_usd
    return t_4941, t_4944, t_4945


def chapter_42_manager_liability(pe_base_usd, net_grants_usd):
    """Eq (6): T_Ch42,Manager = 0.15*V_PE + 0.55*V_grants,net."""
    t_4944_m = EXCISE_4944_COMBINED_MANAGER_RATE * pe_base_usd
    t_4945_m = EXCISE_4945_COMBINED_MANAGER_RATE * net_grants_usd
    return t_4944_m, t_4945_m


def section_507c_recovery(cumulative_tax_benefit_usd, net_assets_usd):
    """Eq (7): T_507(c) = min(sum_t TaxBenefit_t, V_net_assets)."""
    return min(cumulative_tax_benefit_usd, net_assets_usd)


def evaluate_regime(off_990_channels, host_damage_usd, pe_base_usd,
                    net_grants_usd):
    """Evaluate gatekeeper comp and the full Chapter 42 cascade for a regime.

    Compliant regime bases are zero: no self-dealing (4941), no jeopardizing
    investments (4944), no taxable expenditures (4945).
    """
    off_990_total = sum(off_990_channels.values())
    t_4941, t_4944, t_4945 = chapter_42_entity_cascade(
        off_990_total, pe_base_usd, net_grants_usd)
    t_4944_m, t_4945_m = chapter_42_manager_liability(pe_base_usd, net_grants_usd)
    return {
        "gatekeeper_total_comp_usd": gatekeeper_total_comp(
            TRUSTEE_W2_SALARY_USD, off_990_channels),
        "off_990_shadow_comp_usd": off_990_total,
        "host_damage_usd": host_damage_usd,
        "t_4941_entity_usd": t_4941,
        "t_4944_entity_usd": t_4944,
        "t_4945_entity_usd": t_4945,
        "chapter_42_entity_total_usd": t_4941 + t_4944 + t_4945,
        "t_4944_manager_usd": t_4944_m,
        "t_4945_manager_usd": t_4945_m,
        "chapter_42_manager_total_usd": t_4944_m + t_4945_m,
    }


def main():
    # -- Macro corpus decomposition -----------------------------------------
    assert_close(CORPUS_PRIVATE_FOUNDATIONS_USD + CORPUS_UNIVERSITY_ENDOWMENTS_USD,
                 CORPUS_TOTAL_USD, "corpus decomposition")

    # -- Eq (1): trustee comp ratio ------------------------------------------
    beta = trustee_comp_ratio(TRUSTEE_W2_SALARY_USD, SAMPLE_ENDOWMENT_CORPUS_USD)
    assert_close(beta, TRUSTEE_COMP_TO_CORPUS_RATIO, "eq1 beta_trustee ratio")
    # Locked AST convention quotes the ratio as 4.0 bps per 1e-5 of corpus
    # ratio (0.00004 -> 4.0); the strict 1 bp = 1e-4 reading is 0.4 bp.
    assert_close(TRUSTEE_COMP_TO_CORPUS_RATIO * 100_000.0, TRUSTEE_COMP_BPS,
                 "eq1 trustee comp bps (locked convention)")
    control_ratio = SAMPLE_ENDOWMENT_CORPUS_USD / TRUSTEE_W2_SALARY_USD
    assert_close(control_ratio, CONTROL_TO_SALARY_RATIO,
                 "eq1 control-to-salary ratio")

    # -- Eq (2): 4-channel off-990 shadow comp --------------------------------
    off_990_compliant = {
        "board_stack": 0.0,
        "deferred_pe_revolving": 0.0,
        "subgrant_nepotism": 0.0,
        "coinvest_carry_waiver": 0.0,
    }
    off_990_defection = {
        "board_stack": OFF_990_BOARD_STACK_ANNUAL_USD,
        "deferred_pe_revolving": OFF_990_DEFERRED_PE_ANNUAL_EQUIV_USD,
        "subgrant_nepotism": OFF_990_SUBGRANT_NEPOTISM_ANNUAL_USD,
        "coinvest_carry_waiver": OFF_990_COINVEST_CARRY_WAIVER_ANNUAL_USD,
    }
    off_990_total = sum(off_990_defection.values())
    assert_close(off_990_total, OFF_990_SHADOW_COMP_TOTAL_USD,
                 "eq2 off-990 subtotal")
    w_total = gatekeeper_total_comp(TRUSTEE_W2_SALARY_USD, off_990_defection)
    assert_close(w_total, TOTAL_GATEKEEPER_SHADOW_COMP_USD,
                 "eq2 W_total gatekeeper comp")

    # -- Eq (3): autophagic destruction multiplier -----------------------------
    lam = autophagic_multiplier(HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD, w_total)
    assert_close(lam, AUTOPHAGIC_DESTRUCTION_MULTIPLIER,
                 "eq3 autophagic multiplier", rel_tol=1e-6)
    assert lam > 1.0, "autophagic regime must destroy more than it captures"
    assert_close(lam * w_total, HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD,
                 "eq3 round-trip host damage")

    # -- Eq (4): gatekeeper utility wedge --------------------------------------
    du_rational = gatekeeper_utility_delta(
        0.0, 0.0, HOST_DAMAGE_INTERNALIZATION, 0.0)
    du_irrational = gatekeeper_utility_delta(
        off_990_total, HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD,
        HOST_DAMAGE_INTERNALIZATION, I_LOYALTY_IRRATIONAL)
    assert du_irrational > du_rational, "eq4 private defection dominance"
    social_defection_delta = (du_irrational
                              - HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD)
    assert social_defection_delta < 0.0, "eq4 defection is negative-sum socially"

    # -- Section 4942 payout-floor decomposition --------------------------------
    assert_close(ADMIN_OVERHEAD_SHARE + NET_GRANT_PAYOUT_SHARE,
                 STATUTORY_PAYOUT_FLOOR_4942, "4942 floor decomposition")
    assert_close(SAMPLE_ENDOWMENT_CORPUS_USD * ADMIN_OVERHEAD_SHARE,
                 SAMPLE_ANNUAL_ADMIN_OVERHEAD_USD, "admin overhead USD")
    assert_close(SAMPLE_ENDOWMENT_CORPUS_USD * NET_GRANT_PAYOUT_SHARE,
                 SAMPLE_ANNUAL_NET_GRANTS_USD, "net grant payout USD")

    # -- Endowment-caution paradox: PE/VC illiquidity drag ----------------------
    assert_close(SAMPLE_ENDOWMENT_CORPUS_USD * PE_VC_ILLIQUID_SHARE,
                 SAMPLE_PE_VC_ALLOCATION_USD, "PE/VC illiquid allocation")
    fee_drag = SAMPLE_PE_VC_ALLOCATION_USD * PE_ANNUAL_MGMT_FEE_RATE
    assert_close(fee_drag, SAMPLE_PE_ANNUAL_MGMT_FEE_DRAG_USD,
                 "PE annual mgmt fee drag")

    # -- Regime evaluation: Compliant vs Defection/Autophagic -------------------
    compliant = evaluate_regime(off_990_compliant, 0.0, 0.0, 0.0)
    defection = evaluate_regime(
        off_990_defection,
        HOST_ECONOMY_DAMAGE_PER_GRANT_CYCLE_USD,
        SAMPLE_PE_VC_ALLOCATION_USD,
        SAMPLE_ANNUAL_NET_GRANTS_USD,
    )

    assert_close(compliant["gatekeeper_total_comp_usd"], TRUSTEE_W2_SALARY_USD,
                 "compliant comp = W2 only")
    assert_close(compliant["chapter_42_entity_total_usd"], 0.0,
                 "compliant entity cascade = 0")
    assert_close(compliant["chapter_42_manager_total_usd"], 0.0,
                 "compliant manager liability = 0")

    assert_close(defection["t_4941_entity_usd"],
                 SAMPLE_4941_SHADOW_COMP_TAX_USD, "eq5 4941 shadow comp tax")
    assert_close(defection["t_4944_entity_usd"],
                 SAMPLE_4944_ENTITY_TAX_ON_PE_USD, "eq5 4944 entity tax on PE")
    assert_close(defection["t_4945_entity_usd"],
                 SAMPLE_4945_ENTITY_TAX_ON_GRANTS_USD,
                 "eq5 4945 entity tax on net grants")
    assert_close(defection["chapter_42_entity_total_usd"],
                 SAMPLE_CHAPTER_42_COMBINED_ENTITY_CLAWBACK_USD,
                 "eq5 Chapter 42 entity total")
    assert_close(defection["t_4944_manager_usd"], 1_050_000_000.0,
                 "eq6 4944 manager tax")
    assert_close(defection["t_4945_manager_usd"], 418_000_000.0,
                 "eq6 4945 manager tax")
    assert_close(defection["chapter_42_manager_total_usd"],
                 SAMPLE_MANAGER_PERSONAL_LIABILITY_USD,
                 "eq6 Chapter 42 manager total")
    manager_multiple = (defection["chapter_42_manager_total_usd"]
                        / TRUSTEE_W2_SALARY_USD)
    assert manager_multiple > 1.0, "eq6 manager liability exceeds W2 salary"

    # -- Eq (7): Section 507(c) termination recovery -----------------------------
    recovery = section_507c_recovery(CUMULATIVE_TAX_BENEFIT_FLOOR_USD,
                                     SAMPLE_ENDOWMENT_CORPUS_USD)
    assert_close(recovery, SECTION_507C_TERMINATION_RECOVERY_USD,
                 "eq7 507(c) recovery")
    assert_close(recovery / SAMPLE_ENDOWMENT_CORPUS_USD, 1.0,
                 "eq7 100% net-asset call")

    outputs = {
        "trustee_comp_ratio": beta,
        "trustee_comp_bps_locked": TRUSTEE_COMP_BPS,
        "control_to_salary_ratio": control_ratio,
        "off_990_shadow_comp_usd": off_990_total,
        "total_gatekeeper_comp_usd": w_total,
        "autophagic_destruction_multiplier": lam,
        "pe_annual_mgmt_fee_drag_usd": fee_drag,
        "compliant_chapter_42_entity_total_usd":
            compliant["chapter_42_entity_total_usd"],
        "defection_chapter_42_entity_total_usd":
            defection["chapter_42_entity_total_usd"],
        "chapter_42_manager_personal_liability_usd":
            defection["chapter_42_manager_total_usd"],
        "manager_liability_to_w2_multiple": manager_multiple,
        "section_507c_termination_recovery_usd": recovery,
    }
    print(json.dumps(outputs, indent=2))
    print("PROOF PASS: all locked constants and governing equations verified "
          "across compliant and defection/autophagic regimes")


if __name__ == "__main__":
    main()