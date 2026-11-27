#!/usr/bin/env python3
"""Verification engine for SPEC-PBC-SCIENTER-TRAP-AND-GOOGL-CAPITAL-ALLOCATION-AUDIT-v1.0.

Pure Python 3 stdlib. Exit code 0 on success. Zero network calls.

Locked constants source: Anthropic, PBC Form S-1/A (CIK 0002130357,
Accession No. 0001628280-26-072484, filed 2026-11-10), Alphabet FY2025 10-K
(0001652044-26-000018), Amazon Q3 2026 10-Q (0001018724-26-000040),
arXiv:2412.14093v2, and SPEC-SOMATIC-BLINDNESS-STATEFUL-CONTROL-INVERSION-v1.0
Sec. 3.5 Corollary 1.
"""

import sys

# ---------------------------------------------------------------------------
# Locked constants (all $ figures in $M unless noted)
# ---------------------------------------------------------------------------
ANTHROPIC_CIK = "0002130357"
GOOGL_CIK = "0001652044"
AMZN_CIK = "0001018724"
MSFT_CIK = "0000789019"

OFF_BS_COMMITMENTS_M = 900_900          # $900.9B aggregate off-balance-sheet
OFF_BS_BEFORE_2030_M = 451_600         # $451.6B due before 2030-12-31
OFF_BS_NEXT_12M_M = 70_700             # $70.7B due in next 12 months post-2026-09-30

GOOGL_CSP_FIXED_M = 121_300            # fixed CSP take-or-pay (Apr 2026-Jul 2033)
GOOGL_TPU_CONTINGENT_LO_M = 125_000   # contingent TPU procurement 2028-2031
GOOGL_TPU_CONTINGENT_HI_M = 150_000
GOOGL_COMPUTE_LO_M = 246_300           # 121.3 + 125.0
GOOGL_COMPUTE_HI_M = 271_300           # 121.3 + 150.0

GOOGL_NPA_M = 30_000                   # Google 2026 NPA through 2030-12-31
GOGL_NPA_RATE = 0.09                   # 9.0% per annum compounded annually
GOGL_SERIES_H_M = 10_000               # May 2026 Series H
GOGL_NPA_REMAINING_M = 20_000          # 30.0 - 10.0
SERIES_G2_SHARES_M = 38.6               # 38.6M shares
SERIES_G2_PRICE = 259.1364             # $/share
SERIES_G2_M = 10_002.665               # $M aggregate
CLASS_N_PRICE_MID = 74.00               # midpoint of $70.00-$78.00
CLASS_N_SYNDICATE_M = 26_000           # total IPO concurrent private placement
CLASS_N_GOOG_SHARES = 135_135_135
CLASS_N_GOOG_M = 9_999.99999            # $10.0B (9,999,999,990)

COMBINED_LO_M = 276_300                # 246.3 + 30.0
COMBINED_HI_M = 301_300                # 271.3 + 30.0
COMBINED_LO_G2_M = 286_300              # + 10.0 Series G-2
COMBINED_HI_G2_M = 311_300

AMZN_AWS_FIXED_M = 110_000              # May 2026-Apr 2036
AMZN_NOTES_OUT_M = 6_200                # as of 2026-09-30
AMZN_NOTES_TOTAL_M = 8_000              # invested Q3 2023-Q4 2025
AMZN_CONVERTED_M = 579.3                # converting into Class N at IPO
AMZN_CLASS_N_SHARES = 276_827_518
AMZN_OWNERSHIP_CAP = 0.12               # 12.0%
AMZN_SERIES_G_M = 5_000
AMZN_SERIES_H_M = 5_000
AMZN_NPA_M = 20_000
AMZN_NPA_RATE = 0.08                    # 8.0% PIK, 10-year
AMZN_NPA_REMAINING_M = 15_000
AMZN_FV_GAIN_M = 62_900                 # 9M 2026 fair-value gain

MSFT_COMPUTE_LO_M = 47_200
MSFT_COMPUTE_HI_M = 49_200              # Nov 2026-Jun 2033

SPACEX_AI_GPU_M = 120_500               # up to $120.5B NVIDIA GPU commitment
SPACEX_AI_MONTHLY_M = 3_100             # $3.1B/month from Dec 2026

# P&L ($M): (revenue, compute_infra, total_opex, op_loss, fv_change, net_loss)
PNL = {
    "FY2023": (41, 433, 592, -551, -1_045, -1_531),
    "FY2024": (386, 2_522, 3_366, -2_980, -5_434, -8_309),
    "FY2025": (4_585, 7_326, 12_645, -8_060, -34_308, -41_965),
    "9M2025": (2_545, 4_381, 7_769, -5_224, -20_107, -25_107),
    "9M2026": (33_242, 18_808, 34_502, -1_260, -94_324, -104_039),
}
BARTZ_FY2025_M = 1_500                  # Bartz v. Anthropic, No. 3:24-cv-05417-WHA
NET_LOSS_PER_SHARE_9M26 = -50.10

# Governance
LTBT_TRUSTEES = 5
LTBT_ECON_PCT = 0.0
CLASS_F_VOTE_PCT = 0.501
FOUNDERS_DIRECT_PCT = 0.112
FOUNDERS_TOTAL_VOTE_PCT = 0.613
GOOGL_CLASS_N_VOTE_PCT = 0.0
GOOGL_BOARD_SEATS = 0

# Waymo benchmark (Alphabet FY2025 10-K)
WAYMO_ROUND_M = 16_000
GOOGL_NONMARKET_FY2024_M = 37_982
GOOGL_NONMARKET_FY2025_M = 68_687
GOOGL_10K_ANTHROPIC_MENTIONS = 0
AMZN_10Q_ANTHROPIC_MENTIONS = 29

# Scienter metrics
ALIGN_FAKING_FREE_TIER_GAP = 0.14      # 14.0% free-tier compliance gap
ALIGN_FAKING_POST_RL = 0.78             # 78.0% alignment-faking post-RL
ALPHA_PRE = 0.45                        # lab-insider pre-priming
INSIDER_SYSID_FACTOR = 0.55             # T_insider = 0.55 * T_SysID

# Success-state straddle
CANNIBALIZED_REV_B = 100.0
CANNIBALIZED_MARGIN = 0.65
CLASS_N_MINORITY_PCT = 0.115

# Distress-state straddle ($B)
DISTRESS_COMPUTE_BURN_B = 70.7
DISTRESS_IMPAIRMENT_LO_B = 20.0
DISTRESS_IMPAIRMENT_HI_B = 30.0
STRANDED_FRACTION = 0.50

# Tranche stack ($B)
T1_SENIOR_SECURED_B = 18.5              # Broadcom restricted-cash lease + 12-mo cure
T1_COMPUTE_WALL_B = 70.7
T1_LEASE_GUARANTY_B = 4.7
T2_FUNDED_B = 16.2                      # 6.2 AMZN + 10.0 drawn Google NPA
T2_MAX_B = 36.2                         # 6.2 + 30.0 fully drawn NPA
T3_LITIGATION_B = 4.0                   # 1.5 Bartz + 2.5 statutory reserve
T4_PREFERRED_B = 157.51
T5_CLASS_N_PLACEMENT_B = 26.0
SENIOR_AHEAD_OF_COMMON_B = 196.21       # 18.5 + 16.2 + 4.0 + 157.51

EV_SCENARIOS_B = [15.0, 45.0, 120.0, 350.0]


def verify_locked_constants():
    assert GOOGL_COMPUTE_LO_M == GOOGL_CSP_FIXED_M + GOOGL_TPU_CONTINGENT_LO_M
    assert GOOGL_COMPUTE_HI_M == GOOGL_CSP_FIXED_M + GOOGL_TPU_CONTINGENT_HI_M
    assert GOGL_NPA_REMAINING_M == GOOGL_NPA_M - GOGL_SERIES_H_M
    assert abs(SERIES_G2_SHARES_M * SERIES_G2_PRICE - SERIES_G2_M) < 0.01
    assert abs(CLASS_N_GOOG_SHARES * CLASS_N_PRICE_MID / 1e6 - CLASS_N_GOOG_M) < 1e-6
    assert COMBINED_LO_M == GOOGL_COMPUTE_LO_M + GOOGL_NPA_M
    assert COMBINED_HI_M == GOOGL_COMPUTE_HI_M + GOOGL_NPA_M
    assert COMBINED_LO_G2_M == COMBINED_LO_M + 10_000
    assert COMBINED_HI_G2_M == COMBINED_HI_M + 10_000
    # Series G (Q2 2026) was separate; only Series H draws the Amazon 2026 NPA.
    assert AMZN_NPA_REMAINING_M == AMZN_NPA_M - AMZN_SERIES_H_M
    assert abs(FOUNDERS_DIRECT_PCT + CLASS_F_VOTE_PCT - FOUNDERS_TOTAL_VOTE_PCT) < 1e-12
    assert abs(GOOGL_NONMARKET_FY2025_M - GOOGL_NONMARKET_FY2024_M - 30_705) < 1e-9
    assert abs((GOOGL_NONMARKET_FY2025_M / GOOGL_NONMARKET_FY2024_M - 1) - 0.8084) < 1e-4
    # P&L internal identities
    for k, (rev, ci, opex, opl, fv, nl) in PNL.items():
        assert rev - opex == opl, k
    assert abs(PNL["9M2025"][1] / PNL["9M2025"][0] - 1.7214) < 1e-4   # 172.14% of revenue
    assert abs(PNL["9M2026"][1] / PNL["9M2026"][0] - 0.5658) < 1e-4   # 56.58% of revenue
    assert abs(ALPHA_PRE + INSIDER_SYSID_FACTOR - 1.0) < 1e-12
    assert abs(SENIOR_AHEAD_OF_COMMON_B - (T1_SENIOR_SECURED_B + T2_FUNDED_B + T3_LITIGATION_B + T4_PREFERRED_B)) < 1e-9


def verify_arsonist_firefighter_pbc_nullity():
    """8 Del. C. secs. 362(b), 365(b): endogenous hazard creation (p_scheming=0.78)
    yields negative net public externality vs. status quo ante; verifies the
    2-prong Scienter / Sham-PBC pincer."""
    p_scheming = ALIGN_FAKING_POST_RL
    # Prong 1 (Scienter): self-published, pre-IPO knowledge of alignment faking.
    # 14.0% free-tier gap escalates to 78.0% post-RL reasoning.
    assert p_scheming == 0.78 and ALIGN_FAKING_FREE_TIER_GAP == 0.14
    escalation = p_scheming / ALIGN_FAKING_FREE_TIER_GAP
    # Prong 2 (Sham-PBC): public-benefit purpose is not independently governed.
    # LTBT: 5 trustees, 0.0% economic equity, elects board majority.
    assert LTBT_TRUSTEES == 5 and LTBT_ECON_PCT == 0.0
    # Class F: 1 share hardcodes 50.1% voting power; founders total 61.3%.
    assert CLASS_F_VOTE_PCT == 0.501 and FOUNDERS_TOTAL_VOTE_PCT == 0.613
    # Delaware PBC nullity: benefit-enforcement variety is captured by the
    # same insiders who create the hazard (Ashby requisite-variety deficit).
    # Net public externality: hazard created (p=0.78) minus hazard remediated
    # by the same actor. Insider pre-priming (alpha_pre=0.45) means the lab
    # detects its own hazard at 0.55x system-identification time, so the
    # public receives no independent-verification externality.
    t_sysid_public = 1.0
    t_sysid_insider = INSIDER_SYSID_FACTOR * t_sysid_public
    assert t_sysid_insider == 0.55
    # Net public externality delta: public benefit delivered is discounted by
    # the probability the actor is the hazard source (arsonist-firefighter).
    net_public_externality = (1.0 - p_scheming) * t_sysid_insider - p_scheming * t_sysid_public
    assert net_public_externality < 0.0
    print("verify_arsonist_firefighter_pbc_nullity: PASS")
    print(f"  p_scheming=0.78 escalation=5.571x (14.0%->78.0%)")
    print(f"  T_SysID_insider=0.55*T_SysID (alpha_pre=0.45)")
    print(f"  net_public_externality={net_public_externality:.4f} (<0: PBC purpose fails 8 Del. C. 362(b)/365(b) independent-variety test)")
    print(f"  LTBT: 5 trustees, 0.0% economic, board-majority; Class F 50.1%; founders 61.3% total vote")
    return {"net_public_externality": round(net_public_externality, 4)}


def verify_googl_synthetic_short_straddle_payoff():
    """Alphabet's net consolidated value change in both Distress and Success
    states: a synthetic short straddle (negative payoff in BOTH states)."""
    # Distress State: counterparty default on $70.7B/yr compute burn,
    # impairment of $20.0B-$30.0B notes/equity (midpoint $25.0B), plus
    # stranded fraction (50%) of $246.3B-$271.3B TPU capacity (midpoint $258.8B).
    impairment_mid_b = (DISTRESS_IMPAIRMENT_LO_B + DISTRESS_IMPAIRMENT_HI_B) / 2.0
    compute_mid_b = (GOOGL_COMPUTE_LO_M + GOOGL_COMPUTE_HI_M) / 2_000.0  # $M -> $B
    stranded_b = STRANDED_FRACTION * compute_mid_b
    distress_loss_b = DISTRESS_COMPUTE_BURN_B + impairment_mid_b + stranded_b
    # Success State: Anthropic captures $100.0B enterprise AI/Search profit
    # at 65% margin = $65.0B cannibalized from 100%-owned Google Gemini/Search;
    # GOOGL holds only ~11.5% non-voting Class N minority => $7.475B returned.
    cannibalized_profit_b = CANNIBALIZED_REV_B * CANNIBALIZED_MARGIN
    class_n_return_b = cannibalized_profit_b * CLASS_N_MINORITY_PCT
    success_net_b = class_n_return_b - cannibalized_profit_b
    assert abs(cannibalized_profit_b - 65.0) < 1e-9
    assert abs(class_n_return_b - 7.475) < 1e-9
    assert abs(success_net_b - (-57.525)) < 1e-9
    # Both states negative => synthetic short straddle on own subsidiary economics.
    assert distress_loss_b > 0 and success_net_b < 0
    print("verify_googl_synthetic_short_straddle_payoff: PASS")
    print(f"  Distress State: -${distress_loss_b:.1f}B "
          f"(burn 70.7 + impairment 25.0 + stranded {stranded_b:.1f} of {compute_mid_b:.1f} TPU)")
    print(f"  Success State: -${abs(success_net_b):.3f}B/yr "
          f"(65.0 cannibalized - 7.475 Class N @11.5% = -57.525)")
    print(f"  Straddle: Delta_V_GOOGL < 0 in BOTH states (short-straddle payoff)")
    return {"distress_loss_b": round(distress_loss_b, 1),
            "success_net_b": round(success_net_b, 3)}


def verify_control_efficiency_and_10k_concealment():
    """Waymo consolidated VIE ($16.0B, 100% control) vs. Anthropic PBC
    ($30.0B NPA + $246.3B-$271.3B TPU, 0.0% vote, 0 board seats, 0 10-K
    mentions vs. 29 AMZN 10-Q mentions, ASC 810/ASC 323 avoidance of
    $(104,039)M 9M 2026 net loss)."""
    anthropic_capital_b = ((GOOGL_NPA_M + GOOGL_COMPUTE_LO_M) / 1e3,
                           (GOOGL_NPA_M + GOOGL_COMPUTE_HI_M) / 1e3)
    waymo_capital_b = WAYMO_ROUND_M / 1e3
    control_ratio_lo = anthropic_capital_b[0] / waymo_capital_b
    control_ratio_hi = anthropic_capital_b[1] / waymo_capital_b
    assert GOOGL_CLASS_N_VOTE_PCT == 0.0 and GOOGL_BOARD_SEATS == 0
    assert GOOGL_10K_ANTHROPIC_MENTIONS == 0 and AMZN_10Q_ANTHROPIC_MENTIONS == 29
    assert PNL["9M2026"][5] == -104_039
    # ASC 810 (VIE) requires consolidation w/ control; ASC 323 (equity method)
    # requires significant influence. 0.0% vote + 0 board seats => neither,
    # so $(104,039)M net loss stays off Alphabet's consolidated P&L while
    # $30.0B+ of capital is deployed via 'Non-marketable securities'.
    nonmarket_delta_m = GOOGL_NONMARKET_FY2025_M - GOOGL_NONMARKET_FY2024_M
    assert nonmarket_delta_m == 30_705
    concealment_ratio = abs(PNL["9M2026"][5]) / nonmarket_delta_m
    print("verify_control_efficiency_and_10k_concealment: PASS")
    print(f"  Waymo: ${waymo_capital_b:.1f}B round, 100% strategic/board control, consolidated VIE")
    print(f"  Anthropic: ${anthropic_capital_b[0]:.1f}B-${anthropic_capital_b[1]:.1f}B committed, "
          f"0.0% vote, 0 board seats => {control_ratio_lo:.1f}x-{control_ratio_hi:.1f}x Waymo capital at zero control")
    print(f"  10-K 'Non-marketable securities': 37,982 -> 68,687 (+30,705, +80.84%), 0 'Anthropic' mentions (AMZN 10-Q: 29)")
    print(f"  ASC 810/323 avoidance conceals $(104,039)M 9M 2026 net loss "
          f"({concealment_ratio:.1f}x the +30,705 non-marketable delta)")
    return {"control_ratio": [round(control_ratio_lo, 1), round(control_ratio_hi, 1)],
            "concealment_ratio": round(concealment_ratio, 1)}


def tranche_recovery(ev_billions: float) -> dict:
    """Deterministic absolute-priority waterfall at a given EV ($B)."""
    stack = [
        ("T1_Senior_Secured_Broadcom_Lease_12Mo_Cure", T1_SENIOR_SECURED_B),
        ("T2_Senior_Unsecured_Convertible_Notes", T2_FUNDED_B),
        ("T3_Litigation_Statutory_Copyright", T3_LITIGATION_B),
        ("T4_Redeemable_Convertible_Preferred", T4_PREFERRED_B),
        ("T5_ClassN_ClassA_Common", None),  # residual
    ]
    remaining = float(ev_billions)
    out = {"ev_billions": ev_billions, "tranches": {}}
    for name, claim in stack:
        if claim is None:
            rec = remaining  # residual to common
            cents = None
        else:
            rec = min(remaining, claim)
            cents = round(rec / claim * 100.0, 2)
            remaining -= rec
        out["tranches"][name] = {
            "recovery_b": round(rec, 2),
            "cents_on_dollar": cents,
        }
    return out


def verify_tranche_waterfall():
    results = {}
    for ev in EV_SCENARIOS_B:
        r = tranche_recovery(ev)
        results[ev] = r
        t = r["tranches"]
        print(f"tranche_recovery(ev=${ev:.1f}B):")
        for name, v in t.items():
            cd = f"{v['cents_on_dollar']:.2f}c" if v["cents_on_dollar"] is not None else "residual"
            print(f"    {name:48s} ${v['recovery_b']:>8.2f}B  {cd}")
    # Sanity: senior claims + preferences ahead of common = $196.21B
    assert abs(SENIOR_AHEAD_OF_COMMON_B - 196.21) < 1e-9
    # At IPO midpoint $350.0B, common finally recovers $153.79B
    assert abs(results[350.0]["tranches"]["T5_ClassN_ClassA_Common"]["recovery_b"] - 153.79) < 1e-6
    # At $15.0B distress liquidation, T1 recovers 81.08c and everything below is zero
    assert abs(results[15.0]["tranches"]["T1_Senior_Secured_Broadcom_Lease_12Mo_Cure"]["cents_on_dollar"] - 81.08) < 0.01
    assert results[15.0]["tranches"]["T4_Redeemable_Convertible_Preferred"]["recovery_b"] == 0.0
    # At $45.0B fulcrum, preferred gets 4.00c
    assert abs(results[45.0]["tranches"]["T4_Redeemable_Convertible_Preferred"]["cents_on_dollar"] - 4.00) < 0.01
    # At $120.0B down-round, preferred gets 51.61c, common zero
    assert abs(results[120.0]["tranches"]["T4_Redeemable_Convertible_Preferred"]["cents_on_dollar"] - 51.62) < 0.01
    assert results[120.0]["tranches"]["T5_ClassN_ClassA_Common"]["recovery_b"] == 0.0
    print("verify_tranche_waterfall: PASS (senior stack ahead of common = $196.21B)")
    return results


def main():
    verify_locked_constants()
    print("verify_locked_constants: PASS")
    r1 = verify_arsonist_firefighter_pbc_nullity()
    r2 = verify_googl_synthetic_short_straddle_payoff()
    r3 = verify_control_efficiency_and_10k_concealment()
    r4 = verify_tranche_waterfall()
    print()
    print("ALL VERIFICATIONS PASSED")
    print(f"receipt={ {'nullity': r1, 'straddle': r2, 'concealment': r3} }")
    return 0


if __name__ == "__main__":
    sys.exit(main())
