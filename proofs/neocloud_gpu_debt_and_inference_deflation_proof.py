#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: NEOCLOUD GPU DEBT & INFERENCE DEFLATION (v1.0)

Proves:
1. GAAP Depreciation Distortion & True Economic EBIT Margin: replacing the 6.0-year
   straight-line GPU life with the physical replacement life tau_econ yields
   m_EBIT_econ(tau) = 0.586 - 0.536 * (6.0 / tau), with operating breakeven at
   tau_crit = 5.488 years (+5.00% at 6.0 yr, -21.80% at 4.0 yr, -48.60% at 3.0 yr).
2. Box-Loan Collateral Coverage at Contract Rollover: a 5-year DDTL against a 3-year
   customer contract leaves 32.00% of initial hardware cost outstanding against 29.63%
   of residual GPU liquidation value, so CCR_roll = 0.9259 < 1.0, while 91.18% of the
   $42.151B pro-forma debt stack ($38.432B) carries parent recourse.
3. CDS-Implied Default Hazard & Refinancing Wall: 1,128-1,195 bps 5-year CDS at a 40%
   recovery implies 60.94%-63.06% cumulative default probability, and refinancing the
   $22.317B 2030-2033 wall at 15.58% versus 6.6609% adds +$1.990B/yr of cash interest.
4. Sparse-MoE Inference Deflation & Index Concentration: at rho = 0.50 the blended
   frontier dense tier is $23.333/MTok against $0.300/MTok off-peak sparse-MoE
   (77.78x compression, 333.33x output-to-input spread), while a 39.6% SPX IT weight
   transmits a -11.88% drag on a -30% IT shock versus 0.00% in SPXT.
5. SEC Note 10 18-Month Amortization Cliff: $4,413M (H2 2026) + $6,184M (2027) =
   $10,597M (29.81% of $35,551M Q2 debt principal), $15,013M (42.23%) through 2028,
   plus $3,379M of recognized 18-month lease payments = $13,976M mandatory outflows.
6. SEC Note 8 Off-Balance-Sheet Lease Overhang: $35.5B executed uncommenced leases +
   $14.7B single-site 393 MW cap = $50.2B (3.035x the $16.54B recognized lease PV;
   $79.57B total undiscounted lease commitments).
7. DDTL Spread Widening & DSCR Covenant (8-K 0001769628-26-000357): SOFR+2.25% ->
   SOFR+4.50% -> Term SOFR+5.50% (+325 bps) with DSCR >= 1.35x, plus $1,058.2M of
   cash spent on out-of-the-money capped calls.

Zero external dependencies.
"""

import hashlib
import json
import math

TOL = 1e-9

# --- Empirical baseline (Q2 2026 10-Q, pro-forma capitalization, Oct 2026 tape) ---
M_EBITDA = 0.586
M_EBIT_GAAP = 0.050
TAU_GAAP = 6.0
TOTAL_DEBT_B = 42.151
PARENT_RECOURSE_B = 38.432
NON_RECOURSE_B = 3.719
ALPHA_LTC = 0.80
TAU_DEBT = 5.0
TAU_CONTRACT = 3.0
GPU_V0 = 45000.0
GPU_V2 = 20000.0
RECOVERY = 0.40
CDS_TENOR = 5.0
DEBT_WALL_B = 22.317
CASH_INTEREST_B = 2.368
Q2_PRINCIPAL_B = 35.551
R_NEW = 0.1558
RHO = 0.50
DENSE_IN, DENSE_OUT = 10.00, 50.00
MOE_OFF_IN, MOE_OFF_OUT = 0.15, 0.60
MOE_PEAK_IN, MOE_PEAK_OUT = 0.30, 1.20
SPX_IT_WEIGHT = 0.396
SPXT_IT_WEIGHT = 0.0
IT_SHOCK = -0.30

# --- SEC Note 10 (p. 27) principal maturity schedule & Note 8 (p. 23) leases ---
Q2_DEBT_PRINCIPAL_M = 35551.0
H2_2026_DEBT_M = 4413.0
FY2027_DEBT_M = 6184.0
FY2028_DEBT_M = 4416.0
H2_2026_LEASE_M = 1028.0 + 12.0
FY2027_LEASE_M = 2116.0 + 223.0
EXECUTED_UNCOMMENCED_LEASES_B = 35.5
SINGLE_SITE_LEASE_CAP_B = 14.7
RECOGNIZED_LEASE_PV_B = 16.54
FINANCE_LEASE_UNDISCOUNTED_B = 0.235
OPERATING_LEASE_UNDISCOUNTED_B = 29.135
DDTL_4_0_SPREAD_BPS = 225.0
DDTL_5_0_SPREAD_BPS = 450.0
DDTL_5_5_SPREAD_BPS = 550.0
DSCR_COVENANT = 1.35
CAPPED_CALLS_Q2_M = 492.0
CAPPED_CALLS_SEP_M = 566.2


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def verify_depreciation_distortion():
    """
    d_GAAP = m_EBITDA - m_EBIT_GAAP
    m_EBIT_econ(tau) = m_EBITDA - d_GAAP * (tau_GAAP / tau)
    tau_crit = tau_GAAP * (d_GAAP / m_EBITDA)
    """
    d_gaap = M_EBITDA - M_EBIT_GAAP
    assert close(d_gaap, 0.536), d_gaap

    def m_ebit_econ(tau):
        return M_EBITDA - d_gaap * (TAU_GAAP / tau)

    tau_crit = TAU_GAAP * (d_gaap / M_EBITDA)
    assert close(tau_crit, 5.488, 1e-3), tau_crit
    assert close(m_ebit_econ(tau_crit), 0.0, 1e-12)

    scenarios = {}
    for tau, expected in ((6.0, 0.0500), (4.0, -0.2180), (3.0, -0.4860)):
        margin = m_ebit_econ(tau)
        assert close(margin, expected, 1e-9), (tau, margin)
        scenarios[tau] = round(margin, 6)

    # Monotone collapse: shorter economic life strictly worsens operating margin.
    assert m_ebit_econ(6.0) > m_ebit_econ(5.488) > m_ebit_econ(4.0) > m_ebit_econ(3.0)
    # Physical cadence (1.5-2.5 yr) sits far below the breakeven horizon.
    assert m_ebit_econ(2.5) < m_ebit_econ(3.0) < 0.0

    return {
        "d_gaap": round(d_gaap, 6),
        "tau_crit_years": round(tau_crit, 6),
        "scenarios": scenarios,
        "margin_at_2_5y": round(m_ebit_econ(2.5), 6),
    }


def verify_box_loan_collateral():
    """
    lambda_GPU = 0.5 * ln(V0 / V2)
    P_rem = alpha_LTC * (1 - tau_contract / tau_debt)
    V_GPU = exp(-lambda_GPU * tau_contract)
    CCR_roll = V_GPU / P_rem
    """
    lam = 0.5 * math.log(GPU_V0 / GPU_V2)
    assert close(lam, 0.405465, 1e-6), lam

    p_rem = ALPHA_LTC * (1.0 - TAU_CONTRACT / TAU_DEBT)
    v_gpu = math.exp(-lam * TAU_CONTRACT)
    ccr = v_gpu / p_rem

    assert close(p_rem, 0.3200, 1e-12), p_rem
    assert close(v_gpu, 0.2963, 1e-4), v_gpu
    assert close(ccr, 0.9259, 1e-4), ccr
    assert ccr < 1.0

    # Closed-form identity: V_GPU = (V2 / V0) ** (tau_contract / 2).
    assert close(v_gpu, (GPU_V2 / GPU_V0) ** (TAU_CONTRACT / 2.0), 1e-12)

    recourse_share = PARENT_RECOURSE_B / TOTAL_DEBT_B
    non_recourse_share = NON_RECOURSE_B / TOTAL_DEBT_B
    assert close(recourse_share, 0.9118, 1e-4), recourse_share
    assert close(non_recourse_share, 0.0882, 1e-4), non_recourse_share
    assert close(recourse_share + non_recourse_share, 1.0, 1e-12)

    # Uncollateralized tail deficit pierces the box and lands on the parent.
    tail_deficit_fraction = p_rem - v_gpu
    assert tail_deficit_fraction > 0.0
    parent_tail_usd_b = tail_deficit_fraction * PARENT_RECOURSE_B
    assert parent_tail_usd_b > 0.0

    return {
        "lambda_gpu_per_year": round(lam, 6),
        "remaining_principal_fraction": round(p_rem, 6),
        "remaining_collateral_fraction": round(v_gpu, 6),
        "collateral_coverage_ratio": round(ccr, 6),
        "coverage_breach": ccr < 1.0,
        "parent_recourse_share_pct": round(recourse_share * 100.0, 4),
        "non_recourse_share_pct": round(non_recourse_share * 100.0, 4),
        "tail_deficit_fraction": round(tail_deficit_fraction, 6),
        "parent_tail_deficit_usd_b": round(parent_tail_usd_b, 6),
    }


def verify_debt_amortization_cliff():
    """
    A_18m = P_H2_2026 + P_2027;  share_18m = A_18m / P_Q2
    A_30m = A_18m + P_2028;      share_30m = A_30m / P_Q2
    L_18m = L_H2_2026 + L_2027;  M_18m = A_18m + L_18m
    """
    a_18m = H2_2026_DEBT_M + FY2027_DEBT_M
    assert close(a_18m, 10597.0, 1e-9), a_18m
    share_18m = a_18m / Q2_DEBT_PRINCIPAL_M
    assert close(share_18m, 0.2981, 1e-4), share_18m

    a_30m = a_18m + FY2028_DEBT_M
    assert close(a_30m, 15013.0, 1e-9), a_30m
    share_30m = a_30m / Q2_DEBT_PRINCIPAL_M
    assert close(share_30m, 0.4223, 1e-4), share_30m

    l_18m = H2_2026_LEASE_M + FY2027_LEASE_M
    assert close(l_18m, 3379.0, 1e-9), l_18m
    mandatory_18m = a_18m + l_18m
    assert close(mandatory_18m, 13976.0, 1e-9), mandatory_18m

    # The cliff front-loads principal: 18-month share exceeds the 6-month share.
    assert share_18m > H2_2026_DEBT_M / Q2_DEBT_PRINCIPAL_M
    assert share_30m > share_18m
    assert mandatory_18m > a_18m

    return {
        "h2_2026_debt_principal_usd_m": H2_2026_DEBT_M,
        "fy2027_debt_principal_usd_m": FY2027_DEBT_M,
        "cumulative_18m_debt_principal_usd_m": round(a_18m, 6),
        "q2_debt_principal_usd_m": Q2_DEBT_PRINCIPAL_M,
        "share_18m_pct": round(share_18m * 100.0, 4),
        "fy2028_debt_principal_usd_m": FY2028_DEBT_M,
        "cumulative_30m_debt_principal_usd_m": round(a_30m, 6),
        "share_30m_pct": round(share_30m * 100.0, 4),
        "h2_2026_lease_payments_usd_m": H2_2026_LEASE_M,
        "fy2027_lease_payments_usd_m": FY2027_LEASE_M,
        "cumulative_18m_lease_usd_m": round(l_18m, 6),
        "mandatory_18m_outflows_usd_m": round(mandatory_18m, 6),
    }


def verify_off_balance_sheet_lease_overhang():
    """
    OBS = L_uncommenced + L_single_site
    Multiple = OBS / PV_recognized
    Total_undiscounted = L_op + L_fin + OBS
    """
    obs = EXECUTED_UNCOMMENCED_LEASES_B + SINGLE_SITE_LEASE_CAP_B
    assert close(obs, 50.2, 1e-9), obs

    multiple = obs / RECOGNIZED_LEASE_PV_B
    assert close(multiple, 3.035, 1e-3), multiple
    assert multiple > 1.0

    total_undiscounted = OPERATING_LEASE_UNDISCOUNTED_B + FINANCE_LEASE_UNDISCOUNTED_B + obs
    assert close(total_undiscounted, 79.57, 1e-9), total_undiscounted

    # Off-balance-sheet overhang dominates the recognized liability.
    assert obs > RECOGNIZED_LEASE_PV_B
    assert total_undiscounted > obs

    return {
        "executed_uncommenced_leases_usd_b": EXECUTED_UNCOMMENCED_LEASES_B,
        "single_site_lease_cap_usd_b": SINGLE_SITE_LEASE_CAP_B,
        "total_off_balance_sheet_usd_b": round(obs, 6),
        "recognized_lease_pv_usd_b": RECOGNIZED_LEASE_PV_B,
        "off_balance_sheet_multiple": round(multiple, 6),
        "total_undiscounted_lease_commitments_usd_b": round(total_undiscounted, 6),
    }


def verify_ddtl_spread_widening_and_dscr():
    """
    Delta_spread = S_DDTL5.5 - S_DDTL4.0
    Capped_calls = C_Q2 + C_Sep
    """
    widening = DDTL_5_5_SPREAD_BPS - DDTL_4_0_SPREAD_BPS
    assert close(widening, 325.0, 1e-9), widening
    assert DDTL_4_0_SPREAD_BPS < DDTL_5_0_SPREAD_BPS < DDTL_5_5_SPREAD_BPS
    assert close(DDTL_5_0_SPREAD_BPS - DDTL_4_0_SPREAD_BPS, 225.0, 1e-9)

    capped_calls = CAPPED_CALLS_Q2_M + CAPPED_CALLS_SEP_M
    assert close(capped_calls, 1058.2, 1e-9), capped_calls

    # DSCR floor implies debt service must be covered 1.35x by box cash flow.
    assert DSCR_COVENANT > 1.0
    assert capped_calls > 0.0

    return {
        "ddtl_4_0_spread_bps": DDTL_4_0_SPREAD_BPS,
        "ddtl_5_0_spread_bps": DDTL_5_0_SPREAD_BPS,
        "ddtl_5_5_spread_bps": DDTL_5_5_SPREAD_BPS,
        "spread_widening_bps": round(widening, 6),
        "dscr_covenant": DSCR_COVENANT,
        "capped_calls_q2_usd_m": CAPPED_CALLS_Q2_M,
        "capped_calls_sep_usd_m": CAPPED_CALLS_SEP_M,
        "total_capped_calls_usd_m": round(capped_calls, 6),
    }


def verify_cds_hazard_and_refinancing_wall():
    """
    h = S_CDS / (1 - R_rec);  P_def(T) = 1 - exp(-h * T)
    Delta_I_wall = D_wall * (r_new - r_old),  r_old = cash_interest / total_debt
    """
    quotes = {}
    for spread_bps, expected_pd in ((1128.0, 0.6094), (1195.0, 0.6306)):
        spread = spread_bps / 10000.0
        h = spread / (1.0 - RECOVERY)
        pd_5y = 1.0 - math.exp(-h * CDS_TENOR)
        assert close(pd_5y, expected_pd, 1e-4), (spread_bps, pd_5y)
        assert 0.0 < pd_5y < 1.0
        quotes[spread_bps] = {
            "hazard_rate": round(h, 6),
            "default_probability_5y": round(pd_5y, 6),
        }

    # Hazard monotonicity across the tape.
    assert quotes[1128.0]["hazard_rate"] < quotes[1195.0]["hazard_rate"]
    assert quotes[1128.0]["default_probability_5y"] < quotes[1195.0]["default_probability_5y"]

    r_old = CASH_INTEREST_B / Q2_PRINCIPAL_B
    assert close(r_old, 0.066609, 1e-5), r_old
    delta_interest = DEBT_WALL_B * (R_NEW - r_old)
    assert close(delta_interest, 1.9905, 1e-3), delta_interest
    pro_forma_interest = CASH_INTEREST_B + delta_interest
    assert close(pro_forma_interest, 4.3585, 1e-3), pro_forma_interest
    assert delta_interest > 0.0

    return {
        "recovery_rate": RECOVERY,
        "tenor_years": CDS_TENOR,
        "quotes": quotes,
        "r_old": round(r_old, 6),
        "r_new": R_NEW,
        "delta_interest_usd_b_per_year": round(delta_interest, 6),
        "pro_forma_interest_usd_b_per_year": round(pro_forma_interest, 6),
    }


def verify_sparse_moe_deflation():
    """
    P_bar(rho) = (p_in + rho * p_out) / (1 + rho)
    Phi_deflation = P_bar_dense_max / P_bar_moe_off
    """
    def blended(p_in, p_out, rho=RHO):
        return (p_in + rho * p_out) / (1.0 + rho)

    dense_max = blended(DENSE_IN, DENSE_OUT)
    moe_off = blended(MOE_OFF_IN, MOE_OFF_OUT)
    moe_peak = blended(MOE_PEAK_IN, MOE_PEAK_OUT)

    assert close(dense_max, 23.3333, 1e-4), dense_max
    assert close(moe_off, 0.3000, 1e-12), moe_off
    assert close(moe_peak, 0.6000, 1e-12), moe_peak

    compression = dense_max / moe_off
    spread = DENSE_OUT / MOE_OFF_IN
    assert close(compression, 77.78, 1e-2), compression
    assert close(spread, 333.33, 1e-2), spread
    assert compression > 1.0 and spread > compression

    # Onerous take-or-pay conversion: resale revenue below the fixed lease floor.
    tokens_mtok = 1_000_000.0
    take_or_pay_usd = 1_000_000.0
    tenant_gross_margin = moe_off * tokens_mtok - take_or_pay_usd
    assert tenant_gross_margin < 0.0

    return {
        "rho": RHO,
        "blended_dense_max_usd_per_mtok": round(dense_max, 6),
        "blended_moe_offpeak_usd_per_mtok": round(moe_off, 6),
        "blended_moe_peak_usd_per_mtok": round(moe_peak, 6),
        "deflation_compression_factor": round(compression, 6),
        "output_to_input_spread_factor": round(spread, 6),
        "tenant_gross_margin_usd": round(tenant_gross_margin, 6),
    }


def verify_index_allocation():
    """
    Drag = w_IT * Delta_IT
    """
    spx_drag = SPX_IT_WEIGHT * IT_SHOCK
    spxt_drag = SPXT_IT_WEIGHT * IT_SHOCK
    assert close(spx_drag, -0.1188, 1e-12), spx_drag
    assert close(spxt_drag, 0.0, 1e-12), spxt_drag
    assert spx_drag < spxt_drag
    # Rotation eliminates exactly the IT-weighted share of the shock.
    assert close(spx_drag - spxt_drag, SPX_IT_WEIGHT * IT_SHOCK, 1e-12)

    return {
        "spx_it_weight": SPX_IT_WEIGHT,
        "spxt_it_weight": SPXT_IT_WEIGHT,
        "it_shock": IT_SHOCK,
        "spx_it_drag": round(spx_drag, 6),
        "spxt_it_drag": round(spxt_drag, 6),
    }


def run_verification():
    depreciation = verify_depreciation_distortion()
    collateral = verify_box_loan_collateral()
    cliff = verify_debt_amortization_cliff()
    lease_overhang = verify_off_balance_sheet_lease_overhang()
    ddtl = verify_ddtl_spread_widening_and_dscr()
    credit = verify_cds_hazard_and_refinancing_wall()
    deflation = verify_sparse_moe_deflation()
    index = verify_index_allocation()

    manifest = {
        "spec_version": "SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0",
        "capital_structure": {
            "total_debt_principal_usd_b_min": 42.151,
            "total_debt_principal_usd_b_max": 43.551,
            "parent_recourse_usd_b": PARENT_RECOURSE_B,
            "non_recourse_usd_b": NON_RECOURSE_B,
            "fy26_free_cash_flow_usd_b": -27.0,
            "active_power_gw": 1.5,
            "contracted_power_gw": 4.2,
            "energization_gap_gw": 2.7,
            "maturity_wall_usd_b": DEBT_WALL_B,
        },
        "debt_amortization_cliff": cliff,
        "off_balance_sheet_lease_overhang": lease_overhang,
        "ddtl_spread_widening_and_dscr": ddtl,
        "gpu_depreciation": depreciation,
        "box_loan_collateral": collateral,
        "cds_hazard_and_refinancing_wall": credit,
        "sparse_moe_deflation": deflation,
        "index_allocation": index,
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0 | "
        f"tau_crit={depreciation['tau_crit_years']:.3f}yr | "
        f"m_EBIT(6/4/3)={depreciation['scenarios'][6.0]:+.4f}/"
        f"{depreciation['scenarios'][4.0]:+.4f}/{depreciation['scenarios'][3.0]:+.4f} | "
        f"CCR_roll={collateral['collateral_coverage_ratio']:.4f} | "
        f"Recourse={collateral['parent_recourse_share_pct']:.2f}% | "
        f"A_18m=${cliff['cumulative_18m_debt_principal_usd_m']:.0f}M "
        f"({cliff['share_18m_pct']:.2f}%) | "
        f"M_18m=${cliff['mandatory_18m_outflows_usd_m']:.0f}M | "
        f"OBS_leases=${lease_overhang['total_off_balance_sheet_usd_b']:.1f}B "
        f"({lease_overhang['off_balance_sheet_multiple']:.3f}x) | "
        f"DDTL_widen=+{ddtl['spread_widening_bps']:.0f}bps "
        f"DSCR>={ddtl['dscr_covenant']:.2f}x | "
        f"PD5y={credit['quotes'][1128.0]['default_probability_5y']:.4f}-"
        f"{credit['quotes'][1195.0]['default_probability_5y']:.4f} | "
        f"dI_wall=+${credit['delta_interest_usd_b_per_year']:.3f}B/yr | "
        f"Phi_deflation={deflation['deflation_compression_factor']:.2f}x | "
        f"Spread={deflation['output_to_input_spread_factor']:.2f}x | "
        f"SPX_drag={index['spx_it_drag']:.4f} | SPXT_drag={index['spxt_it_drag']:.4f} | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
