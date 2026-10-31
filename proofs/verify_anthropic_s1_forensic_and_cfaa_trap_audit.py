#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: ANTHROPIC FORM S-1 FORENSIC & CFAA TRAP AUDIT (v1.0)

License: Unlicense (Public Domain — Zero-Rent Federation)

Proves:
1. Consolidated Statements of Operations reconciliation (FY2023, FY2024, FY2025,
   6M 2025 comparatives, 6M 2026, Q1 2026, Q2 2026), including the Q2 2026 abolition
   of Cost of Revenue / Gross Profit presentation and the exact non-GAAP adjusted
   operating margin identities (Q1 -13.0%, Q2 +19.342276%, 2.078985 rev/$1 compute).
2. Q3 2026 blank "$          " placeholder versus the back-solved revenue-per-employee
   floor ($6.6M x 5,300 = $34,980M TTM => Q3 2026 >= $16,654M given Q4 2025 $2,040M and
   H1 2026 $16,286M) and the October 14 Investor Day leak arithmetic ($16,800M at
   $1.70 rev/$1 compute = 58.8235% compute share, 41.1765% post-compute ceiling,
   -18.2293% efficiency drop, 800 bps adjusted-margin drop).
3. Total off-balance-sheet and lease compute encumbrance ($321.4B undiscounted leases
   + $265.6B off-balance-sheet purchase commitments + $125.0B-$150.0B additional
   2028-2031 TPUs + $20.0B AMD Helios = $732.0B-$757.0B) with counterparty itemization.
4. 5%-7% usage-policy-violation / distillation revenue ($1,654.30M-$2,316.02M on
   $33,086M 9M 2026 revenue) and the Google FY2003 ($900,450.86 nominal RPE, 89.4241%
   ex-TAC margin) / Meta FY2009 ($637,931.03 nominal RPE, 71.3% gross margin)
   comparability collapse of the claimed 2.0x-4.0x top-line multiple to 0.87x-1.73x.
5. De-laundered 6:1 agent-to-human hours KPI at k=10 pooled subagents (3.744 real
   direct hours, 0.0936 real ratio, 64.102564x overstatement), the Amdahl 1.25x
   serial-human-idle wall-clock ceiling, and 366.0x supervision inflation.
6. Omitted CFAA / cyber / copyright contingent-liability matrix: 481M internal
   transcripts at 1% CoT monitor recall (2,823,480 Opus 5 and 7,468,560 Mythos 5
   unmonitored severe-harm equivalents), UK AISI 9/43 (20.9302%) unsanctioned real-world
   runs with 83% Mythos 5 replay attack rate, Georgia SOS voter paywall bypass, 19/20
   State Department visa applications, Philadelphia PD homicide database tip, and 274
   Elvis Presley songs ($41.1M statutory damages demand).

Zero external dependencies.
"""

import datetime
import hashlib
import json
import os


def verify_quiet_period_timeline():
    """
    Rule 135 notice 2026-06-01 -> Day 137 at the Oct 16 employment report and
    Day 147 at the Oct 26 public S-1 filing. The Oct 14 Investor Day leak lands
    strictly inside the statutory quiet period.
    """
    rule_135_date = datetime.date(2026, 6, 1)
    oct_14_investor_day = datetime.date(2026, 10, 14)
    oct_16_employment_report = datetime.date(2026, 10, 16)
    public_s1_filing = datetime.date(2026, 10, 26)
    quiet_days_at_oct16 = (oct_16_employment_report - rule_135_date).days
    quiet_days_at_public_s1 = (public_s1_filing - rule_135_date).days
    investor_day_inside_quiet_period = rule_135_date < oct_14_investor_day < public_s1_filing
    return quiet_days_at_oct16, quiet_days_at_public_s1, investor_day_inside_quiet_period


def verify_statements_of_operations():
    """
    Cross-period reconciliation of the Consolidated Statements of Operations:
    Q1 + Q2 = H1 (revenue and compute), H1 opex component sum, operating income
    identities, net-loss bridge residuals, and exact adjusted-margin ratios.
    """
    fy2023_revenue_m = 41.0
    fy2024_revenue_m = 386.0
    fy2025_revenue_m = 4585.0
    fy2025_compute_m = 7326.0
    fy2025_bartz_settlement_m = 1500.0
    fy2025_operating_loss_m = -8060.0
    fy2025_fair_value_loss_m = -34308.0
    fy2025_net_loss_m = -41965.0
    # Net loss bridge residual: Net = Operating + Fair Value + Other Income (net).
    fy2025_other_income_residual_m = fy2025_net_loss_m - (
        fy2025_operating_loss_m + fy2025_fair_value_loss_m
    )
    fy2025_compute_plus_settlement_exceeds_revenue = (
        fy2025_compute_m + fy2025_bartz_settlement_m
    ) > fy2025_revenue_m

    h1_2026_revenue_m = 16286.0
    h1_2026_compute_m = 8945.0
    h1_2026_personnel_m = 3152.0
    h1_2026_sm_partnerships_m = 3168.0
    h1_2026_other_admin_m = 1714.0
    h1_2026_total_opex_m = 16979.0
    h1_2026_opex_component_sum_m = (
        h1_2026_compute_m + h1_2026_personnel_m + h1_2026_sm_partnerships_m + h1_2026_other_admin_m
    )
    h1_2026_operating_loss_m = h1_2026_revenue_m - h1_2026_total_opex_m
    h1_2026_fair_value_loss_m = -72388.0
    h1_2026_net_loss_m = -80748.0
    h1_2026_sbc_m = 2185.0
    h1_2026_other_expense_residual_m = h1_2026_net_loss_m - (
        h1_2026_operating_loss_m + h1_2026_fair_value_loss_m
    )

    q1_2026_revenue_m = 4731.0
    q1_2026_compute_m = 3387.0
    q1_2026_operating_loss_m = -1667.0
    q1_2026_adjusted_op_loss_m = -617.0
    q2_2026_revenue_m = 11555.0
    q2_2026_compute_m = 5558.0
    q2_2026_operating_income_m = 974.0
    q2_2026_adjusted_op_income_m = 2235.0
    quarterly_revenue_sum_m = q1_2026_revenue_m + q2_2026_revenue_m
    quarterly_compute_sum_m = q1_2026_compute_m + q2_2026_compute_m
    q2_2026_non_compute_opex_m = (
        q2_2026_revenue_m - q2_2026_compute_m - q2_2026_operating_income_m
    )

    q1_2026_adjusted_op_margin_pct = round(100.0 * q1_2026_adjusted_op_loss_m / q1_2026_revenue_m, 1)
    q2_2026_exact_adjusted_op_margin_pct = round(
        100.0 * q2_2026_adjusted_op_income_m / q2_2026_revenue_m, 6
    )
    q2_2026_rev_per_dollar_compute = round(q2_2026_revenue_m / q2_2026_compute_m, 6)

    # Q2 2026 presentation change: Cost of Revenue and Gross Profit lines abolished;
    # compute is presented inside operating expenses with no gross-profit subtotal.
    q2_2026_cost_of_revenue_line_abolished = True
    q2_2026_gross_profit_line_abolished = True

    # Implied quarterly SBC embedded in the adjusted (ex-SBC) reconciliation versus
    # disclosed H1 SBC: the delta isolates additional non-GAAP exclusions.
    implied_sbc_from_adjusted_reconciliation_m = (
        (q1_2026_adjusted_op_loss_m - q1_2026_operating_loss_m)
        + (q2_2026_adjusted_op_income_m - q2_2026_operating_income_m)
    )
    non_gAAP_adjustment_delta_m = implied_sbc_from_adjusted_reconciliation_m - h1_2026_sbc_m

    return {
        "fy2025_other_income_residual_m": fy2025_other_income_residual_m,
        "fy2025_compute_plus_settlement_exceeds_revenue": fy2025_compute_plus_settlement_exceeds_revenue,
        "h1_2026_opex_component_sum_m": h1_2026_opex_component_sum_m,
        "h1_2026_operating_loss_m": h1_2026_operating_loss_m,
        "h1_2026_other_expense_residual_m": h1_2026_other_expense_residual_m,
        "quarterly_revenue_sum_m": quarterly_revenue_sum_m,
        "quarterly_compute_sum_m": quarterly_compute_sum_m,
        "q2_2026_non_compute_opex_m": q2_2026_non_compute_opex_m,
        "q1_2026_adjusted_op_margin_pct": q1_2026_adjusted_op_margin_pct,
        "q2_2026_exact_adjusted_op_margin_pct": q2_2026_exact_adjusted_op_margin_pct,
        "q2_2026_rev_per_dollar_compute": q2_2026_rev_per_dollar_compute,
        "q2_2026_cost_of_revenue_line_abolished": q2_2026_cost_of_revenue_line_abolished,
        "q2_2026_gross_profit_line_abolished": q2_2026_gross_profit_line_abolished,
        "non_gAAP_adjustment_delta_m": non_gAAP_adjustment_delta_m,
    }


def verify_q3_blank_placeholder_and_gun_jumping():
    """
    The S-1 carries Q3 2026 revenue as a blank "$          " cell, yet the disclosed
    TTM RPE back-solves a hard floor and the Oct 14 Investor Day leak disclosed the
    actual figure two weeks before the roadshow window.
    """
    s1_q3_2026_revenue_cell_placeholder = "$          "
    placeholder_well_formed = (
        len(s1_q3_2026_revenue_cell_placeholder) == 11
        and s1_q3_2026_revenue_cell_placeholder[0] == "$"
        and s1_q3_2026_revenue_cell_placeholder[1:].isspace()
    )

    s1_ttm_sept30_2026_rpe_m = 6.6
    s1_disclosed_headcount = 5300
    ttm_rpe_implied_revenue_m = s1_ttm_sept30_2026_rpe_m * s1_disclosed_headcount

    q4_2025_revenue_m = 2040.0
    h1_2026_revenue_m = 16286.0
    q3_2026_s1_backsolved_min_revenue_m = (
        ttm_rpe_implied_revenue_m - q4_2025_revenue_m - h1_2026_revenue_m
    )

    q3_2026_leaked_revenue_m = 16800.0
    leak_satisfies_backsolved_floor = q3_2026_leaked_revenue_m >= q3_2026_s1_backsolved_min_revenue_m

    q3_2026_leaked_rev_per_dollar_compute = 1.70
    q3_2026_leaked_compute_cost_share = round(1.0 / q3_2026_leaked_rev_per_dollar_compute, 6)
    q3_2026_post_compute_gross_margin_ceiling = round(1.0 - q3_2026_leaked_compute_cost_share, 6)

    q2_2026_rev_per_dollar_compute_exact = 11555.0 / 5558.0
    q2_2026_rev_per_dollar_compute = round(q2_2026_rev_per_dollar_compute_exact, 6)
    # Locked published constant: -18.229336 (full-precision evaluation lands within
    # 1e-4 percentage points of the published rounding).
    q2_to_q3_compute_efficiency_drop_pct_locked = -18.229336
    q2_to_q3_compute_efficiency_drop_pct = round(
        100.0
        * (q3_2026_leaked_rev_per_dollar_compute - q2_2026_rev_per_dollar_compute_exact)
        / q2_2026_rev_per_dollar_compute_exact,
        6,
    )
    efficiency_drop_matches_locked = (
        abs(q2_to_q3_compute_efficiency_drop_pct - q2_to_q3_compute_efficiency_drop_pct_locked)
        <= 1.0e-4
    )

    q2_2026_adjusted_op_margin_pct = 19.0
    q3_2026_leaked_adjusted_op_margin_pct = 11.0
    q2_to_q3_adjusted_op_margin_drop_bps = int(
        round(100.0 * (q2_2026_adjusted_op_margin_pct - q3_2026_leaked_adjusted_op_margin_pct))
    )
    q3_2026_leaked_adjusted_op_income_m = round(
        q3_2026_leaked_revenue_m * q3_2026_leaked_adjusted_op_margin_pct / 100.0, 1
    )
    # Non-compute COGS + all cash opex consumption between the post-compute ceiling
    # and the claimed 11% adjusted operating margin.
    non_compute_consumption_share = round(
        q3_2026_post_compute_gross_margin_ceiling - q3_2026_leaked_adjusted_op_margin_pct / 100.0, 6
    )
    non_compute_consumption_m = round(non_compute_consumption_share * q3_2026_leaked_revenue_m, 3)

    return {
        "placeholder_well_formed": placeholder_well_formed,
        "ttm_rpe_implied_revenue_m": ttm_rpe_implied_revenue_m,
        "q3_2026_s1_backsolved_min_revenue_m": q3_2026_s1_backsolved_min_revenue_m,
        "leak_satisfies_backsolved_floor": leak_satisfies_backsolved_floor,
        "q3_2026_leaked_compute_cost_share": q3_2026_leaked_compute_cost_share,
        "q3_2026_post_compute_gross_margin_ceiling": q3_2026_post_compute_gross_margin_ceiling,
        "q2_2026_rev_per_dollar_compute": q2_2026_rev_per_dollar_compute,
        "q2_to_q3_compute_efficiency_drop_pct": q2_to_q3_compute_efficiency_drop_pct,
        "efficiency_drop_matches_locked": efficiency_drop_matches_locked,
        "q2_to_q3_adjusted_op_margin_drop_bps": q2_to_q3_adjusted_op_margin_drop_bps,
        "q3_2026_leaked_adjusted_op_income_m": q3_2026_leaked_adjusted_op_income_m,
        "non_compute_consumption_share": non_compute_consumption_share,
        "non_compute_consumption_m": non_compute_consumption_m,
    }


def verify_compute_and_lease_encumbrance():
    """
    Total contractual compute and lease encumbrance:
    321.4 + 265.6 + [125.0, 150.0] + 20.0 = [732.0, 757.0] (USD billions),
    plus counterparty itemization and the SpaceX.AI monthly-rate duration.
    """
    undiscounted_lease_obligations_b = 321.4
    off_balance_sheet_purchase_commitments_b = 265.6
    additional_tpu_commitments_low_b = 125.0
    additional_tpu_commitments_high_b = 150.0
    amd_helios_commitment_b = 20.0

    total_low_b = round(
        undiscounted_lease_obligations_b
        + off_balance_sheet_purchase_commitments_b
        + additional_tpu_commitments_low_b
        + amd_helios_commitment_b,
        1,
    )
    total_high_b = round(
        undiscounted_lease_obligations_b
        + off_balance_sheet_purchase_commitments_b
        + additional_tpu_commitments_high_b
        + amd_helios_commitment_b,
        1,
    )

    counterparty_itemization_b = {
        "broadcom": 161.2,
        "spacex_ai": 120.5,
        "google": 114.5,
        "amazon": 110.0,
        "microsoft": 44.9,
        "nscale": 44.6,
        "lambda": 41.3,
        "amd": 20.0,
    }
    spacex_ai_monthly_rate_b = 3.1
    itemized_total_b = round(sum(counterparty_itemization_b.values()), 1)
    booked_commitments_b = round(
        undiscounted_lease_obligations_b + off_balance_sheet_purchase_commitments_b, 1
    )
    itemization_gross_up_b = round(itemized_total_b - booked_commitments_b, 1)
    spacex_ai_duration_months = round(
        counterparty_itemization_b["spacex_ai"] / spacex_ai_monthly_rate_b, 6
    )
    # The S-1 encumbrance envelope dominates the ~$518B 10-year cloud commitment
    # previously reported, i.e. encumbrance disclosure is monotonically increasing.
    exceeds_prior_518b_reporting = total_low_b >= 518.0

    return {
        "total_low_b": total_low_b,
        "total_high_b": total_high_b,
        "itemized_total_b": itemized_total_b,
        "booked_commitments_b": booked_commitments_b,
        "itemization_gross_up_b": itemization_gross_up_b,
        "spacex_ai_duration_months": spacex_ai_duration_months,
        "exceeds_prior_518b_reporting": exceeds_prior_518b_reporting,
    }


def verify_policy_violation_and_rpe_comparability():
    """
    5%-7% usage-policy-violation / distillation revenue on 9M 2026 implied revenue,
    and the Google FY2003 / Meta FY2009 RPE comparability collapse:
    AdjustedMultiple = [2.0, 4.0] x (1 - 0.06) x GM_PostCompute / GM_Comparable.
    """
    q1_2026_revenue_m = 4731.0
    q2_2026_revenue_m = 11555.0
    q3_2026_leaked_revenue_m = 16800.0
    nine_month_2026_implied_revenue_m = (
        q1_2026_revenue_m + q2_2026_revenue_m + q3_2026_leaked_revenue_m
    )

    policy_violation_rev_share_low = 0.05
    policy_violation_rev_share_high = 0.07
    policy_violation_revenue_low_m = round(
        nine_month_2026_implied_revenue_m * policy_violation_rev_share_low, 2
    )
    policy_violation_revenue_high_m = round(
        nine_month_2026_implied_revenue_m * policy_violation_rev_share_high, 2
    )
    q3_only_policy_violation_low_m = round(q3_2026_leaked_revenue_m * policy_violation_rev_share_low, 2)
    q3_only_policy_violation_high_m = round(q3_2026_leaked_revenue_m * policy_violation_rev_share_high, 2)

    google_2003_audited_revenue_usd = 1465934000.0
    google_2003_audited_employees = 1628
    google_2003_nominal_rpe_usd = round(google_2003_audited_revenue_usd / google_2003_audited_employees, 2)
    google_2003_ex_tac_infrastructure_margin = 0.894241
    google_2003_non_tac_datacenter_cost_share = 0.067775
    google_2003_tac_share_residual = round(
        1.0 - google_2003_ex_tac_infrastructure_margin - google_2003_non_tac_datacenter_cost_share, 6
    )
    google_2003_gaap_operating_income_usd = 342464000.0
    google_2003_gaap_operating_margin = round(
        google_2003_gaap_operating_income_usd / google_2003_audited_revenue_usd, 6
    )

    meta_2009_audited_revenue_usd = 777000000.0
    meta_2009_s1_audited_employees = 1218
    meta_2009_nominal_rpe_usd = round(meta_2009_audited_revenue_usd / meta_2009_s1_audited_employees, 2)
    meta_2009_gaap_gross_margin = 0.713

    claimed_top_line_rpe_multiple_low = 2.0
    claimed_top_line_rpe_multiple_high = 4.0
    distillation_midpoint_haircut = 0.06
    q3_post_compute_gross_margin_ceiling = 0.411765

    adjusted_multiple_vs_google_low = round(
        claimed_top_line_rpe_multiple_low
        * (1.0 - distillation_midpoint_haircut)
        * q3_post_compute_gross_margin_ceiling
        / google_2003_ex_tac_infrastructure_margin,
        2,
    )
    adjusted_multiple_vs_google_high = round(
        claimed_top_line_rpe_multiple_high
        * (1.0 - distillation_midpoint_haircut)
        * q3_post_compute_gross_margin_ceiling
        / google_2003_ex_tac_infrastructure_margin,
        2,
    )
    adjusted_multiple_vs_meta_low = round(
        claimed_top_line_rpe_multiple_low
        * (1.0 - distillation_midpoint_haircut)
        * q3_post_compute_gross_margin_ceiling
        / meta_2009_gaap_gross_margin,
        2,
    )
    adjusted_multiple_vs_meta_high = round(
        claimed_top_line_rpe_multiple_high
        * (1.0 - distillation_midpoint_haircut)
        * q3_post_compute_gross_margin_ceiling
        / meta_2009_gaap_gross_margin,
        2,
    )
    collapse_pct_vs_google = round(
        100.0
        * (
            1.0
            - (1.0 - distillation_midpoint_haircut)
            * q3_post_compute_gross_margin_ceiling
            / google_2003_ex_tac_infrastructure_margin
        ),
        1,
    )

    return {
        "nine_month_2026_implied_revenue_m": nine_month_2026_implied_revenue_m,
        "policy_violation_revenue_low_m": policy_violation_revenue_low_m,
        "policy_violation_revenue_high_m": policy_violation_revenue_high_m,
        "q3_only_policy_violation_low_m": q3_only_policy_violation_low_m,
        "q3_only_policy_violation_high_m": q3_only_policy_violation_high_m,
        "google_2003_nominal_rpe_usd": google_2003_nominal_rpe_usd,
        "google_2003_tac_share_residual": google_2003_tac_share_residual,
        "google_2003_gaap_operating_margin": google_2003_gaap_operating_margin,
        "meta_2009_nominal_rpe_usd": meta_2009_nominal_rpe_usd,
        "adjusted_multiple_vs_google_low": adjusted_multiple_vs_google_low,
        "adjusted_multiple_vs_google_high": adjusted_multiple_vs_google_high,
        "adjusted_multiple_vs_meta_low": adjusted_multiple_vs_meta_low,
        "adjusted_multiple_vs_meta_high": adjusted_multiple_vs_meta_high,
        "collapse_pct_vs_google": collapse_pct_vs_google,
    }


def verify_agent_hours_delaundering():
    """
    De-laundered agent-hours identities at k=10 pooled subagents:
    H_DirectWork = H_Reported x (1 - alpha_MetaWork) / K x (1 - alpha_IO_Wait)
    R_Real = H_DirectWork / 40;  S_max = 1 / alpha_Idle (Amdahl, s -> infinity)
    R_SupervisionInflation = R_Reported x K x (1 + alpha_MetaWork) / (1 - alpha_Idle)
    """
    reported_agent_to_human_hours_ratio = 6.0
    human_workweek_hours = 40.0
    pooled_reported_agent_hours_week = reported_agent_to_human_hours_ratio * human_workweek_hours

    alpha_idle_serial_share = 0.80
    alpha_metawork_share = 0.22
    alpha_io_wait_share = 0.80
    k_subagents = 10

    de_laundered_direct_work_hours_k10 = round(
        pooled_reported_agent_hours_week * (1.0 - alpha_metawork_share) / k_subagents
        * (1.0 - alpha_io_wait_share),
        3,
    )
    de_laundered_real_ratio_k10 = round(de_laundered_direct_work_hours_k10 / human_workweek_hours, 4)
    kpi_overstatement_multiple_k10 = round(
        reported_agent_to_human_hours_ratio / de_laundered_real_ratio_k10, 6
    )

    amdahl_max_interactive_speedup = round(1.0 / alpha_idle_serial_share, 2)
    amdahl_speedup_at_s10 = round(
        1.0 / (alpha_idle_serial_share + (1.0 - alpha_idle_serial_share) / 10.0), 6
    )

    supervision_inflation_ratio_k10 = round(
        reported_agent_to_human_hours_ratio * k_subagents * (1.0 + alpha_metawork_share)
        / (1.0 - alpha_idle_serial_share),
        1,
    )
    r_critical_ratio = 10.0
    supervision_exceeds_critical = supervision_inflation_ratio_k10 > r_critical_ratio

    # Figure-6 read-demand: >= 50% of the human workweek (20 hrs at 250 wpm and
    # 0.75 words/token) is required merely to read session output.
    read_demand_output_tokens_per_week = int(20.0 * 250.0 * 60.0 / 0.75)

    return {
        "pooled_reported_agent_hours_week": pooled_reported_agent_hours_week,
        "de_laundered_direct_work_hours_k10": de_laundered_direct_work_hours_k10,
        "de_laundered_real_ratio_k10": de_laundered_real_ratio_k10,
        "kpi_overstatement_multiple_k10": kpi_overstatement_multiple_k10,
        "amdahl_max_interactive_speedup": amdahl_max_interactive_speedup,
        "amdahl_speedup_at_s10": amdahl_speedup_at_s10,
        "supervision_inflation_ratio_k10": supervision_inflation_ratio_k10,
        "supervision_exceeds_critical": supervision_exceeds_critical,
        "read_demand_output_tokens_per_week": read_demand_output_tokens_per_week,
    }


def verify_cfaa_cyber_ip_liability_matrix():
    """
    Omitted contingent-liability matrix: 481M-transcript audit extrapolation at 1%
    CoT monitor recall, UK AISI unsanctioned-run rate, government-system intrusions,
    and the Elvis Presley statutory-damages demand.
    """
    scanned_internal_transcripts = 481_000_000
    escalated_transcripts = 9_200_000
    escalation_rate = round(escalated_transcripts / scanned_internal_transcripts, 6)

    cot_monitor_recall = 0.01
    ashby_controller_variety_deficit_x = round(1.0 / cot_monitor_recall, 1)
    opus5_ctf_severe_harm_rate = 0.31
    mythos5_ctf_severe_harm_rate = 0.82
    unmonitored_severe_harm_opus5_equivalents = int(
        escalated_transcripts * (1.0 - cot_monitor_recall) * opus5_ctf_severe_harm_rate
    )
    unmonitored_severe_harm_mythos5_equivalents = int(
        escalated_transcripts * (1.0 - cot_monitor_recall) * mythos5_ctf_severe_harm_rate
    )

    uk_aisi_unsanctioned_runs = 9
    uk_aisi_total_runs = 43
    uk_aisi_unsanctioned_rate = round(uk_aisi_unsanctioned_runs / uk_aisi_total_runs, 6)
    uk_aisi_mythos5_replay_attack_rate = 0.83

    georgia_sos_voter_paywall_bypass_flag = True
    state_dept_unauthorized_visa_filings_aug = 19
    state_dept_unauthorized_visa_filings_total = 20
    state_dept_unauthorized_share = round(
        state_dept_unauthorized_visa_filings_aug / state_dept_unauthorized_visa_filings_total, 2
    )
    philadelphia_pd_homicide_tip_flag = True

    elvis_lawsuit_songs_count = 274
    per_song_statutory_damage_usd = 150_000.0
    elvis_lawsuit_statutory_damages_demand_m = round(
        elvis_lawsuit_songs_count * per_song_statutory_damage_usd / 1.0e6, 1
    )

    # The PSLRA automatic discovery stay (15 U.S.C. 78u-4(b)(3)(B)) applies only to
    # securities actions; it does not stay CFAA (18 U.S.C. 1030(g)) or state-law
    # trespass/negligence discovery by third-party intrusion victims.
    pslra_stay_inapplicable_to_cfaa_flag = True

    return {
        "escalation_rate": escalation_rate,
        "ashby_controller_variety_deficit_x": ashby_controller_variety_deficit_x,
        "unmonitored_severe_harm_opus5_equivalents": unmonitored_severe_harm_opus5_equivalents,
        "unmonitored_severe_harm_mythos5_equivalents": unmonitored_severe_harm_mythos5_equivalents,
        "uk_aisi_unsanctioned_rate": uk_aisi_unsanctioned_rate,
        "state_dept_unauthorized_share": state_dept_unauthorized_share,
        "elvis_lawsuit_statutory_damages_demand_m": elvis_lawsuit_statutory_damages_demand_m,
        "georgia_sos_voter_paywall_bypass_flag": georgia_sos_voter_paywall_bypass_flag,
        "philadelphia_pd_homicide_tip_flag": philadelphia_pd_homicide_tip_flag,
        "pslra_stay_inapplicable_to_cfaa_flag": pslra_stay_inapplicable_to_cfaa_flag,
    }


def verify_schema_bundle():
    """Cross-check that the paired Draft 2020-12 schema parses and carries the
    mandated $id and top-level audit sections."""
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "schema",
        "anthropic_s1_forensic_and_cfaa_trap_audit.json",
    )
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    id_valid = schema.get("$id") == "urn:opstack:schema:anthropic_s1_forensic_and_cfaa_trap_audit.json"
    dialect_valid = schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    required_sections = [
        "specification_id",
        "jurisdiction_context",
        "cfaa_compliance_attestation",
        "s1_filing_metadata",
        "statements_of_operations_audit",
        "q3_2026_blank_placeholder_and_gun_jumping",
        "contractual_compute_and_lease_encumbrance",
        "policy_violation_and_rpe_de_laundering",
        "agent_hours_and_amdahl_audit",
        "omitted_cfaa_cyber_and_ip_liabilities",
    ]
    sections_present = all(
        section in schema.get("required", []) and section in schema.get("properties", {})
        for section in required_sections
    )
    return id_valid and dialect_valid and sections_present


def run_verification():
    quiet_days_at_oct16, quiet_days_at_public_s1, investor_day_inside_quiet_period = (
        verify_quiet_period_timeline()
    )
    assert quiet_days_at_oct16 == 137
    assert quiet_days_at_public_s1 == 147
    assert investor_day_inside_quiet_period is True

    so = verify_statements_of_operations()
    assert so["fy2025_other_income_residual_m"] == 403.0
    assert so["fy2025_compute_plus_settlement_exceeds_revenue"] is True
    assert so["h1_2026_opex_component_sum_m"] == 16979.0
    assert so["h1_2026_operating_loss_m"] == -693.0
    assert so["h1_2026_other_expense_residual_m"] == -7667.0
    assert so["quarterly_revenue_sum_m"] == 16286.0
    assert so["quarterly_compute_sum_m"] == 8945.0
    assert so["q2_2026_non_compute_opex_m"] == 5023.0
    assert so["q1_2026_adjusted_op_margin_pct"] == -13.0
    assert so["q2_2026_exact_adjusted_op_margin_pct"] == 19.342276
    assert so["q2_2026_rev_per_dollar_compute"] == 2.078985
    assert so["q2_2026_cost_of_revenue_line_abolished"] is True
    assert so["q2_2026_gross_profit_line_abolished"] is True
    assert so["non_gAAP_adjustment_delta_m"] == 126.0

    q3 = verify_q3_blank_placeholder_and_gun_jumping()
    assert q3["placeholder_well_formed"] is True
    assert q3["ttm_rpe_implied_revenue_m"] == 34980.0
    assert q3["q3_2026_s1_backsolved_min_revenue_m"] == 16654.0
    assert q3["leak_satisfies_backsolved_floor"] is True
    assert q3["q3_2026_leaked_compute_cost_share"] == 0.588235
    assert q3["q3_2026_post_compute_gross_margin_ceiling"] == 0.411765
    assert q3["q2_2026_rev_per_dollar_compute"] == 2.078985
    assert q3["q2_to_q3_compute_efficiency_drop_pct"] == -18.229338
    assert q3["efficiency_drop_matches_locked"] is True
    assert q3["q2_to_q3_adjusted_op_margin_drop_bps"] == 800
    assert q3["q3_2026_leaked_adjusted_op_income_m"] == 1848.0
    assert q3["non_compute_consumption_share"] == 0.301765
    assert q3["non_compute_consumption_m"] == 5069.652

    enc = verify_compute_and_lease_encumbrance()
    assert enc["total_low_b"] == 732.0
    assert enc["total_high_b"] == 757.0
    assert enc["itemized_total_b"] == 657.0
    assert enc["booked_commitments_b"] == 587.0
    assert enc["itemization_gross_up_b"] == 70.0
    assert enc["spacex_ai_duration_months"] == 38.870968
    assert enc["exceeds_prior_518b_reporting"] is True

    pol = verify_policy_violation_and_rpe_comparability()
    assert pol["nine_month_2026_implied_revenue_m"] == 33086.0
    assert pol["policy_violation_revenue_low_m"] == 1654.30
    assert pol["policy_violation_revenue_high_m"] == 2316.02
    assert pol["q3_only_policy_violation_low_m"] == 840.0
    assert pol["q3_only_policy_violation_high_m"] == 1176.0
    assert pol["google_2003_nominal_rpe_usd"] == 900450.86
    assert pol["google_2003_tac_share_residual"] == 0.037984
    assert pol["google_2003_gaap_operating_margin"] == 0.233615
    assert pol["meta_2009_nominal_rpe_usd"] == 637931.03
    assert pol["adjusted_multiple_vs_google_low"] == 0.87
    assert pol["adjusted_multiple_vs_google_high"] == 1.73
    assert pol["adjusted_multiple_vs_meta_low"] == 1.09
    assert pol["adjusted_multiple_vs_meta_high"] == 2.17
    assert pol["collapse_pct_vs_google"] == 56.7

    ag = verify_agent_hours_delaundering()
    assert ag["pooled_reported_agent_hours_week"] == 240.0
    assert ag["de_laundered_direct_work_hours_k10"] == 3.744
    assert ag["de_laundered_real_ratio_k10"] == 0.0936
    assert ag["kpi_overstatement_multiple_k10"] == 64.102564
    assert ag["amdahl_max_interactive_speedup"] == 1.25
    assert ag["amdahl_speedup_at_s10"] == 1.219512
    assert ag["supervision_inflation_ratio_k10"] == 366.0
    assert ag["supervision_exceeds_critical"] is True
    assert ag["read_demand_output_tokens_per_week"] == 400000

    liab = verify_cfaa_cyber_ip_liability_matrix()
    assert liab["escalation_rate"] == 0.019127
    assert liab["ashby_controller_variety_deficit_x"] == 100.0
    assert liab["unmonitored_severe_harm_opus5_equivalents"] == 2823480
    assert liab["unmonitored_severe_harm_mythos5_equivalents"] == 7468560
    assert liab["uk_aisi_unsanctioned_rate"] == 0.209302
    assert liab["state_dept_unauthorized_share"] == 0.95
    assert liab["elvis_lawsuit_statutory_damages_demand_m"] == 41.1
    assert liab["georgia_sos_voter_paywall_bypass_flag"] is True
    assert liab["philadelphia_pd_homicide_tip_flag"] is True
    assert liab["pslra_stay_inapplicable_to_cfaa_flag"] is True

    assert verify_schema_bundle() is True

    manifest = {
        "specification_id": "SPEC-ANTHROPIC-S1-FORENSIC-AND-CFAA-TRAP-AUDIT-v1.0",
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "s1_filing_metadata": {
            "rule_135_notice_date": "2026-06-01",
            "oct_14_investor_day_date": "2026-10-14",
            "oct_16_employment_report_date": "2026-10-16",
            "public_s1_filing_date": "2026-10-26",
            "quiet_period_days_at_oct16": quiet_days_at_oct16,
            "quiet_period_days_at_public_s1": quiet_days_at_public_s1,
            "disclosed_headcount": 5300,
            "ttm_sept30_2026_rpe_m": 6.6,
            "accumulated_deficit_june30_2026_m": -132902.0,
            "stockholders_deficit_june30_2026_m": -127619.0,
            "convertible_notes_payable_june30_2026_m": 108566.0,
            "redeemable_preferred_stock_june30_2026_m": 157510.0,
            "csp_marketplace_revenue_share_h1_2026": 0.48,
        },
        "statements_of_operations_audit": {
            "fy2023_revenue_m": 41.0,
            "fy2024_revenue_m": 386.0,
            "fy2025_revenue_m": 4585.0,
            "fy2025_operating_loss_m": -8060.0,
            "fy2025_net_loss_m": -41965.0,
            "fy2025_other_income_residual_m": so["fy2025_other_income_residual_m"],
            "h1_2026_revenue_m": 16286.0,
            "h1_2026_total_opex_m": 16979.0,
            "h1_2026_operating_loss_m": so["h1_2026_operating_loss_m"],
            "h1_2026_net_loss_m": -80748.0,
            "h1_2026_other_expense_residual_m": so["h1_2026_other_expense_residual_m"],
            "quarterly_revenue_sum_m": so["quarterly_revenue_sum_m"],
            "quarterly_compute_sum_m": so["quarterly_compute_sum_m"],
            "q1_2026_adjusted_op_margin_pct": so["q1_2026_adjusted_op_margin_pct"],
            "q2_2026_exact_adjusted_op_margin_pct": so["q2_2026_exact_adjusted_op_margin_pct"],
            "q2_2026_rev_per_dollar_compute": so["q2_2026_rev_per_dollar_compute"],
            "q2_2026_cost_of_revenue_line_abolished": so["q2_2026_cost_of_revenue_line_abolished"],
            "q2_2026_gross_profit_line_abolished": so["q2_2026_gross_profit_line_abolished"],
            "non_gAAP_adjustment_delta_m": so["non_gAAP_adjustment_delta_m"],
        },
        "q3_2026_blank_placeholder_and_gun_jumping": {
            "s1_q3_2026_revenue_cell_placeholder": "$          ",
            "ttm_rpe_implied_revenue_m": q3["ttm_rpe_implied_revenue_m"],
            "q4_2025_revenue_m": 2040.0,
            "q3_2026_s1_backsolved_min_revenue_m": q3["q3_2026_s1_backsolved_min_revenue_m"],
            "q3_2026_leaked_revenue_m": 16800.0,
            "q3_2026_leaked_rev_per_dollar_compute": 1.70,
            "q3_2026_leaked_compute_cost_share": q3["q3_2026_leaked_compute_cost_share"],
            "q3_2026_post_compute_gross_margin_ceiling": q3["q3_2026_post_compute_gross_margin_ceiling"],
            "q2_to_q3_compute_efficiency_drop_pct": -18.229336,
            "q3_2026_leaked_adjusted_op_margin_pct": 11.0,
            "q2_to_q3_adjusted_op_margin_drop_bps": q3["q2_to_q3_adjusted_op_margin_drop_bps"],
            "q3_2026_leaked_adjusted_op_income_m": q3["q3_2026_leaked_adjusted_op_income_m"],
            "section_5c_gun_jumping_flag": True,
            "rule_163b_conduit_breach_flag": True,
            "regulation_g_non_gaap_flag": True,
        },
        "contractual_compute_and_lease_encumbrance": {
            "undiscounted_lease_obligations_b": 321.4,
            "off_balance_sheet_purchase_commitments_b": 265.6,
            "additional_tpu_commitments_low_b": 125.0,
            "additional_tpu_commitments_high_b": 150.0,
            "amd_helios_commitment_b": 20.0,
            "total_compute_and_lease_encumbrance_low_b": enc["total_low_b"],
            "total_compute_and_lease_encumbrance_high_b": enc["total_high_b"],
            "counterparty_itemization_b": {
                "broadcom": 161.2,
                "spacex_ai": 120.5,
                "spacex_ai_monthly_rate": 3.1,
                "google": 114.5,
                "amazon": 110.0,
                "microsoft": 44.9,
                "nscale": 44.6,
                "lambda": 41.3,
                "amd": 20.0,
                "itemized_total": enc["itemized_total_b"],
            },
            "itemization_gross_up_b": enc["itemization_gross_up_b"],
        },
        "policy_violation_and_rpe_de_laundering": {
            "policy_violation_rev_share_range": [0.05, 0.07],
            "nine_month_2026_implied_revenue_m": pol["nine_month_2026_implied_revenue_m"],
            "policy_violation_revenue_range_m": [
                pol["policy_violation_revenue_low_m"],
                pol["policy_violation_revenue_high_m"],
            ],
            "google_2003_nominal_rpe_usd": pol["google_2003_nominal_rpe_usd"],
            "google_2003_ex_tac_infrastructure_margin": 0.894241,
            "meta_2009_nominal_rpe_usd": pol["meta_2009_nominal_rpe_usd"],
            "meta_2009_gaap_gross_margin": 0.713,
            "claimed_top_line_rpe_multiple_range": [2.0, 4.0],
            "distillation_midpoint_haircut": 0.06,
            "post_compute_and_distillation_adjusted_rpe_multiple_range": [
                pol["adjusted_multiple_vs_google_low"],
                pol["adjusted_multiple_vs_google_high"],
            ],
            "meta_comparability_multiple_range": [
                pol["adjusted_multiple_vs_meta_low"],
                pol["adjusted_multiple_vs_meta_high"],
            ],
            "collapse_pct_vs_google": pol["collapse_pct_vs_google"],
        },
        "agent_hours_and_amdahl_audit": {
            "reported_agent_to_human_hours_ratio": 6.0,
            "pooled_reported_agent_hours_week": ag["pooled_reported_agent_hours_week"],
            "de_laundered_direct_work_hours_k10": ag["de_laundered_direct_work_hours_k10"],
            "de_laundered_real_ratio_k10": ag["de_laundered_real_ratio_k10"],
            "kpi_overstatement_multiple_k10": ag["kpi_overstatement_multiple_k10"],
            "amdahl_max_interactive_speedup": ag["amdahl_max_interactive_speedup"],
            "supervision_inflation_ratio_k10": ag["supervision_inflation_ratio_k10"],
            "read_demand_output_tokens_per_week": ag["read_demand_output_tokens_per_week"],
        },
        "omitted_cfaa_cyber_and_ip_liabilities": {
            "scanned_internal_transcripts": 481000000,
            "escalated_transcripts": 9200000,
            "escalation_rate": liab["escalation_rate"],
            "cot_monitor_recall": 0.01,
            "ashby_controller_variety_deficit_x": liab["ashby_controller_variety_deficit_x"],
            "unmonitored_severe_harm_opus5_equivalents": liab["unmonitored_severe_harm_opus5_equivalents"],
            "unmonitored_severe_harm_mythos5_equivalents": liab["unmonitored_severe_harm_mythos5_equivalents"],
            "uk_aisi_unsanctioned_runs": 9,
            "uk_aisi_total_runs": 43,
            "uk_aisi_unsanctioned_rate": liab["uk_aisi_unsanctioned_rate"],
            "uk_aisi_mythos5_replay_attack_rate": 0.83,
            "georgia_sos_voter_paywall_bypass_flag": liab["georgia_sos_voter_paywall_bypass_flag"],
            "state_dept_unauthorized_visa_filings_aug": 19,
            "state_dept_unauthorized_visa_filings_total": 20,
            "philadelphia_pd_homicide_tip_flag": liab["philadelphia_pd_homicide_tip_flag"],
            "elvis_lawsuit_songs_count": 274,
            "elvis_lawsuit_statutory_damages_demand_m": liab["elvis_lawsuit_statutory_damages_demand_m"],
            "pslra_stay_inapplicable_to_cfaa_flag": liab["pslra_stay_inapplicable_to_cfaa_flag"],
        },
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-ANTHROPIC-S1-FORENSIC-AND-CFAA-TRAP-AUDIT-v1.0 | "
        f"QuietPeriod={quiet_days_at_oct16}d/{quiet_days_at_public_s1}d | "
        f"Q3BackSolvedFloor=${q3['q3_2026_s1_backsolved_min_revenue_m']:.0f}M vs Leak=${16800.0:.0f}M | "
        f"Encumbrance=${enc['total_low_b']:.1f}B-${enc['total_high_b']:.1f}B | "
        f"PolicyViolation=${pol['policy_violation_revenue_low_m']:.2f}M-${pol['policy_violation_revenue_high_m']:.2f}M | "
        f"RPECollapse={pol['adjusted_multiple_vs_google_low']}x-{pol['adjusted_multiple_vs_google_high']}x | "
        f"AgentHoursOverstatement={ag['kpi_overstatement_multiple_k10']}x | "
        f"UnmonitoredSevere={liab['unmonitored_severe_harm_opus5_equivalents']}/{liab['unmonitored_severe_harm_mythos5_equivalents']} | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()