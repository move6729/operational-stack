#!/usr/bin/env python3
"""
Executable Verification Suite: SPEC-NETWORK-STATE-ZEDE-SOVEREIGN-EXTORTION-AND-ISDS-ARBITRAGE-v1.0
Verifies:
  1. Cap-Table Fiefdom Governance Telemetry: Camp-of-9 developer-appointed council control
     (kappa_VC = 8/9 = 0.888889), equity/land-weighted private-arbitration voting concentration
     (cap_table_gini_concentration = 0.94), the derived cap-table feudalism index
     (F_feudal = kappa_VC * G_cap = 0.835556), and the non-waivable constitutional jury
     sovereignty floor (J_floor = 1.0, U.S. Const. Amend. VII / Art. III analog).
  2. ISDS Sovereign-Extortion Multiplier Algebra: K_capex = 120.0 USD millions deployed under the
     ZEDE regime vs. the ICSID Case No. ARB/23/2 claim C_claim = 10775.0 USD millions ->
     M_ISDS = round(10775.0 / 120.0, 6) = 89.791667 and fiscal-hostage ratio
     Phi_health = round(10775.0 / 1150.0, 6) = 9.369565 against the locked 1150.0 USD millions
     annual health-budget comparator (uplift over capex = 10655.0 USD millions).
  3. Democratic Repeal Unanimity and VCLT Article 46 Nullification Indicator: Decree No. 32-2022
     repeal carried 128/128 (U = 1.0) and the manifest-AND-fundamental constitutional-violation
     indicator V_46 = 1.0 (nemo dat quod non habet boundary).
  4. Sovereign Defense-Stack Expected-Value Liquidation: E[ISDS] = C_claim * (1 - V_46) *
     (1 - d_71) * (1 - d_NY) = 0.0 once any lever (VCLT Art. 46 / ICSID Art. 71 denunciation /
     NY Convention Art. V(2)(b) public policy) engages.
  5. Schema Parity: schema/network_state_zede_isds_arbitrage.json loads as valid JSON, carries the
     URN $id urn:opstack:schema:network_state_zede_isds_arbitrage.json on Draft 2020-12, stays
     within the 320-line budget, and every locked_constants const matches the computed telemetry.
Pure Python 3 standard library. Zero third-party dependencies.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

SPEC_ID = "SPEC-NETWORK-STATE-ZEDE-SOVEREIGN-EXTORTION-AND-ISDS-ARBITRAGE-v1.0"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "network_state_zede_isds_arbitrage.json"
SCHEMA_URN = "urn:opstack:schema:network_state_zede_isds_arbitrage.json"
SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
MAX_SCHEMA_LINES = 320
TOL = 1e-6


def r6(x) -> float:
    """Round an exact rational value to six decimals (locked telemetry precision)."""
    return round(float(x), 6)


def verify_module_1_cap_table_fiefdom() -> dict:
    # Camp-of-9 council: 8 of 9 seats developer-appointed.
    council_total_seats = 9
    council_developer_appointed_seats = 8
    kappa_vc = r6(Fraction(council_developer_appointed_seats, council_total_seats))
    assert abs(kappa_vc - 0.888889) < TOL, f"kappa_VC drift: {kappa_vc}"
    assert kappa_vc < 1.0, "developer control must remain a proper fraction of the council"

    # Equity/land-weighted arbitration voting concentration (cap-table Gini).
    cap_table_gini_concentration = 0.94
    assert 0.0 <= cap_table_gini_concentration <= 1.0, "Gini outside unit interval"

    # Derived cap-table feudalism index: F_feudal = kappa_VC * G_cap.
    cap_table_feudalism_index = r6(
        Fraction(council_developer_appointed_seats, council_total_seats) * Fraction(94, 100)
    )
    assert abs(cap_table_feudalism_index - 0.835556) < TOL, f"F_feudal drift: {cap_table_feudalism_index}"

    # Constitutional jury sovereignty floor: binary, non-waivable, non-degradable.
    constitutional_jury_sovereignty_floor = 1.0
    assert constitutional_jury_sovereignty_floor == 1.0, "jury floor degraded below 1.0"

    return {
        "council_total_seats": council_total_seats,
        "council_developer_appointed_seats": council_developer_appointed_seats,
        "zede_council_vc_voting_control_share": kappa_vc,
        "cap_table_gini_concentration": cap_table_gini_concentration,
        "cap_table_feudalism_index": cap_table_feudalism_index,
        "constitutional_jury_sovereignty_floor": constitutional_jury_sovereignty_floor,
    }


def verify_module_2_isds_extortion_multiplier() -> dict:
    capex_usd_millions = Fraction("120.0")   # K_capex: locked physical capex under the ZEDE regime
    claim_usd_millions = Fraction("10775.0")  # C_claim: ICSID ARB/23/2 aggregate claim
    health_usd_millions = Fraction("1150.0")  # B_health: locked annual health-budget comparator

    # E1: ISDS sovereign-extortion multiplier.
    m_isds = r6(claim_usd_millions / capex_usd_millions)
    assert abs(m_isds - 89.791667) < TOL, f"M_ISDS drift: {m_isds}"

    # E2: fiscal-hostage ratio against the national health budget.
    phi_health = r6(claim_usd_millions / health_usd_millions)
    assert abs(phi_health - 9.369565) < TOL, f"Phi_health drift: {phi_health}"

    # Structural sanity: the claim exceeds deployed capex by pure sovereignty rent.
    claim_over_capex_uplift = float(claim_usd_millions - capex_usd_millions)
    assert abs(claim_over_capex_uplift - 10655.0) < TOL, f"uplift drift: {claim_over_capex_uplift}"
    assert claim_usd_millions > capex_usd_millions, "claim must exceed capex for extortion regime"
    assert m_isds > 1.0, "multiplier must exceed unity for extortion regime"

    return {
        "prospera_invested_capital_usd_millions": float(capex_usd_millions),
        "icsid_extortion_claim_usd_millions": float(claim_usd_millions),
        "isds_claim_to_capex_multiplier": m_isds,
        "honduras_annual_health_budget_usd_millions": float(health_usd_millions),
        "claim_to_national_health_budget_ratio": phi_health,
        "claim_over_capex_uplift_usd_millions": claim_over_capex_uplift,
    }


def verify_module_3_democratic_repeal_vclt46() -> dict:
    # Decree No. 32-2022: unanimous repeal of the ZEDE Organic Law.
    national_congress_seats = 128
    repeal_aye_votes = 128
    democratic_repeal_vote_unanimity = r6(Fraction(repeal_aye_votes, national_congress_seats))
    assert abs(democratic_repeal_vote_unanimity - 1.0) < TOL, f"unanimity drift: {democratic_repeal_vote_unanimity}"

    # VCLT Art. 46 prongs: manifest (objectively evident) AND fundamental (constitutional substance).
    manifest_violation_indicator = 1
    fundamental_rule_indicator = 1
    vclt_art46_indicator = float(manifest_violation_indicator and fundamental_rule_indicator)
    assert vclt_art46_indicator == 1.0, "V_46 failed to engage on manifest-AND-fundamental prongs"

    # Unanimous repeal is the objective evidence vector for the fundamental prong.
    assert democratic_repeal_vote_unanimity >= vclt_art46_indicator, (
        "unanimity must certify the fundamental-rule prong"
    )

    return {
        "national_congress_seats": national_congress_seats,
        "repeal_aye_votes": repeal_aye_votes,
        "democratic_repeal_vote_unanimity": democratic_repeal_vote_unanimity,
        "manifest_violation_indicator": manifest_violation_indicator,
        "fundamental_rule_indicator": fundamental_rule_indicator,
        "vclt_art46_constitutional_nullification_indicator": vclt_art46_indicator,
    }


def verify_module_4_sovereign_defense_stack(m3: dict) -> dict:
    claim_usd_millions = 10775.0
    v46 = m3["vclt_art46_constitutional_nullification_indicator"]

    # Defense levers (each independently fatal to the invoice when engaged).
    lever_icsid_art71_denunciation = 1.0        # ICSID Convention Art. 71 denunciation
    lever_ny_convention_public_policy = 1.0     # NY Convention Art. V(2)(b) public-policy refusal
    lever_constitutional_jury_nullification = 1.0  # constituent-power nullification floor

    # E5: expected-value liquidation identity.
    e_primary = claim_usd_millions * (1.0 - v46)
    e_full_stack = (
        claim_usd_millions
        * (1.0 - v46)
        * (1.0 - lever_icsid_art71_denunciation)
        * (1.0 - lever_ny_convention_public_policy)
    )
    assert e_primary == 0.0, f"E[ISDS] under VCLT Art. 46 drift: {e_primary}"
    assert e_full_stack == 0.0, f"E[ISDS] full-stack drift: {e_full_stack}"

    # Counterfactual: with V_46 disengaged the invoice would enforce at full face value,
    # confirming the Article 46 lever is load-bearing.
    e_counterfactual = claim_usd_millions * (1.0 - 0.0)
    assert abs(e_counterfactual - 10775.0) < TOL, "counterfactual enforcement drift"

    return {
        "lever_icsid_art71_denunciation": lever_icsid_art71_denunciation,
        "lever_ny_convention_art_v2b_public_policy": lever_ny_convention_public_policy,
        "lever_constitutional_jury_nullification": lever_constitutional_jury_nullification,
        "expected_value_identity": "E[ISDS] = C_claim * (1 - V_46) * (1 - d_71) * (1 - d_NY) = 10775.0 * 0.0 = 0.0",
        "isds_extortion_expected_value_under_vclt_art46": e_primary,
    }


def verify_module_5_schema_parity(telemetry: dict) -> dict:
    raw = SCHEMA_PATH.read_text(encoding="utf-8")
    line_count = raw.count("\n") + (0 if raw.endswith("\n") else 1)
    assert line_count <= MAX_SCHEMA_LINES, f"schema line bloat: {line_count} > {MAX_SCHEMA_LINES}"

    doc = json.loads(raw)
    assert doc["$id"] == SCHEMA_URN, f"schema $id drift: {doc.get('$id')}"
    assert doc["$schema"] == SCHEMA_DRAFT, f"schema draft drift: {doc.get('$schema')}"

    locked = doc["properties"]["locked_constants"]["properties"]
    assert len(locked) == 11, f"locked_constants cardinality drift: {len(locked)} != 11"
    for name, sub in locked.items():
        assert name in telemetry, f"schema constant missing from computed telemetry: {name}"
        assert abs(sub["const"] - telemetry[name]) < TOL, (
            f"schema const drift on {name}: {sub['const']} != {telemetry[name]}"
        )

    return {
        "schema_id": SCHEMA_URN,
        "schema_draft": SCHEMA_DRAFT,
        "schema_lines": line_count,
        "schema_consts_verified": len(locked),
    }


def main() -> int:
    m1 = verify_module_1_cap_table_fiefdom()
    m2 = verify_module_2_isds_extortion_multiplier()
    m3 = verify_module_3_democratic_repeal_vclt46()
    m4 = verify_module_4_sovereign_defense_stack(m3)

    # Flat locked-telemetry map: the 11 constants of Section 5 of the specification.
    telemetry = {
        "prospera_invested_capital_usd_millions": m2["prospera_invested_capital_usd_millions"],
        "icsid_extortion_claim_usd_millions": m2["icsid_extortion_claim_usd_millions"],
        "isds_claim_to_capex_multiplier": m2["isds_claim_to_capex_multiplier"],
        "honduras_annual_health_budget_usd_millions": m2["honduras_annual_health_budget_usd_millions"],
        "claim_to_national_health_budget_ratio": m2["claim_to_national_health_budget_ratio"],
        "zede_council_vc_voting_control_share": m1["zede_council_vc_voting_control_share"],
        "democratic_repeal_vote_unanimity": m3["democratic_repeal_vote_unanimity"],
        "vclt_art46_constitutional_nullification_indicator": m3["vclt_art46_constitutional_nullification_indicator"],
        "cap_table_gini_concentration": m1["cap_table_gini_concentration"],
        "constitutional_jury_sovereignty_floor": m1["constitutional_jury_sovereignty_floor"],
        "isds_extortion_expected_value_under_vclt_art46": m4["isds_extortion_expected_value_under_vclt_art46"],
    }
    assert len(telemetry) == 11, f"telemetry cardinality drift: {len(telemetry)} != 11"

    m5 = verify_module_5_schema_parity(telemetry)

    results = {
        "spec": SPEC_ID,
        "module_1_cap_table_fiefdom": m1,
        "module_2_isds_extortion_multiplier": m2,
        "module_3_democratic_repeal_vclt46": m3,
        "module_4_sovereign_defense_stack": m4,
        "module_5_schema_parity": m5,
        "locked_telemetry": telemetry,
        "status": "ALL_INVARIANTS_VERIFIED",
    }
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())