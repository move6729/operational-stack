#!/usr/bin/env python3
"""
Deterministic verification engine for
SPEC-OPEN-WEIGHT-DISTILLATION-AND-DOMESTIC-BAN-IMPOSSIBILITY-v1.0.

Actively recomputes every closed-form primitive in Spec Sections 4.1-4.4 and
asserts the governing equations, boundary regimes, and numerical sanity checks:

  [1] DeepSeek-V3 Table 1 internal consistency (2788K H800 hours x $2/hr = $5.576M)
      and Capex Compression Ratio Gamma_distill in [89.67x, 179.34x].
  [2] Blended price P_bar(rho) = (p_in + rho*p_out)/(1+rho) for the closed-o1,
      open-V3, and off-peak regimes, including convexity bounds, the rho -> 0
      and rho -> infinity boundary regimes, and monotonicity in rho.
  [3] Inference Cost Asymmetry Factors Phi_API,std = 58.31x and
      Phi_API,off = 100.00x, with the ordering Phi_off > Phi_std > 1.
  [4] Unit-margin collapse: Pi_foreign = +$7.58195, Pi_US = -$16.3750,
      operating margins +63.18% / -136.46%, and the tau_reg identity
      tau_reg = Q*(P_closed - P_open) = Pi_foreign - Pi_US.
  [5] Break-even thresholds Q_crit,US = 0.1641M and Q_crit,foreign = 9.5682M,
      the competitive-zone inequality, and the three-regime sign structure
      (both-profit / asymmetric-flip / both-loss).
  [6] Omega_capture = 13.3333x via the closed form AND via direct
      Delta_W_US / Delta_Pi_cartel surplus accounting (algebraic identity
      cross-check), plus monotonicity in eta_destroy.
  [7] Human-capital brain-drain ratchet (Spec §4.5): fixed-budget ($250k/yr)
      experimental throughput compression (299.01B vs 5.13B tokens/yr),
      Critical Brain-Drain Token Threshold Q_drain^* = 10,017.9697M tokens/yr
      (~10.0180B/yr, 27.45M/day), and net offshoring savings +$4,311,390/yr
      at 100B tokens/yr.
  [8] Falsification boundary: Phi_API -> 1.0 requires P_closed <= $0.84/M,
      which is nowhere near the current $48.75/M regime.

Pure Python 3 standard library. Exit code 0 on success.
License: Unlicense (Public Domain).
"""

import sys

TOL_EXACT = 1e-9   # exact decimal identities
TOL_4DP = 5e-5     # spec values rounded to 4 decimal places
TOL_2DP = 5e-3     # spec values rounded to 2 decimal places

# ---------------------------------------------------------------------------
# Spec §4.2 primitives (verified market pricing, USD per million tokens)
# ---------------------------------------------------------------------------
RHO = 3.0
P_IN_CLOSED, P_OUT_CLOSED = 15.00, 60.00        # openai/o1
P_IN_V3, P_OUT_V3 = 0.2574, 1.0290              # DeepSeek-V3 standard rate
P_IN_OFF, P_OUT_OFF = 0.1500, 0.6000            # off-peak / local self-hosted

# Spec §4.3 workflow primitives
R_UNIT, C_OPS, Q_TOKENS = 12.00, 4.00, 0.50     # USD, USD, millions of tokens
V_NET = R_UNIT - C_OPS                          # $8.00

# Spec §4.4 macro primitives
ETA_DESTROY, M_NET, EXPORT_LOSS_RATIO = 0.75, 0.30, 1.50

# Spec §4.5 human-capital brain-drain primitives
B_COMPUTE_USD = 250_000.0
DELTA_V_HUB_USD = 500_000.0
RELOC_ANNUAL_USD = 100_000.0
COMPLIANCE_ANNUAL_USD = 120_000.0
Q_STARTUP_M = 100_000.0  # 100B tokens/yr (in millions of tokens)


def blended_price(p_in: float, p_out: float, rho: float) -> float:
    """P_bar(rho) = (p_in + rho * p_out) / (1 + rho)   [Spec §4.2]"""
    return (p_in + rho * p_out) / (1.0 + rho)


def omega_closed_form(eta: float, m_net: float, export_ratio: float) -> float:
    """Omega_capture = (1/m_net)[1 + eta/(2(1-eta)) + export_ratio]  [Spec §4.4]"""
    return (1.0 / m_net) * (1.0 + eta / (2.0 * (1.0 - eta)) + export_ratio)


def check_capex_compression() -> None:
    """[1] Spec §4.1: DeepSeek-V3 Table 1 consistency and Gamma_distill bounds."""
    pre_k, ctx_k, post_k, total_k = 2664.0, 119.0, 5.0, 2788.0
    assert abs((pre_k + ctx_k + post_k) - total_k) < TOL_EXACT
    rental = 2.0  # USD per H800 GPU hour (arXiv:2412.19437v2, Table 1)
    assert abs(total_k * 1e3 * rental / 1e6 - 5.576) < TOL_EXACT
    assert abs(pre_k * 1e3 * rental / 1e6 - 5.328) < TOL_EXACT
    assert abs(ctx_k * 1e3 * rental / 1e6 - 0.238) < TOL_EXACT
    assert abs(post_k * 1e3 * rental / 1e6 - 0.010) < TOL_EXACT
    assert abs((5.328 + 0.238 + 0.010) - 5.576) < TOL_EXACT

    c_student = 5.576  # USD millions
    gamma_min = 500.0 / c_student
    gamma_max = 1000.0 / c_student
    assert abs(gamma_min - 89.67) < TOL_2DP, gamma_min
    assert abs(gamma_max - 179.34) < TOL_2DP, gamma_max
    assert gamma_min < gamma_max
    assert abs(gamma_max - 2.0 * gamma_min) < TOL_EXACT  # teacher band doubles
    print(f"[1] Gamma_distill = [{gamma_min:.4f}x, {gamma_max:.4f}x] ~= [89.67x, 179.34x]  OK")


def check_blended_prices() -> tuple:
    """[2] Spec §4.2: blended prices, convexity bounds, and rho boundary regimes."""
    p_closed = blended_price(P_IN_CLOSED, P_OUT_CLOSED, RHO)
    p_v3 = blended_price(P_IN_V3, P_OUT_V3, RHO)
    p_off = blended_price(P_IN_OFF, P_OUT_OFF, RHO)

    assert abs(p_closed - 48.7500) < TOL_EXACT, p_closed   # 195.00 / 4
    assert abs(p_v3 - 0.8361) < TOL_EXACT, p_v3            # 3.3444 / 4
    assert abs(p_off - 0.4875) < TOL_EXACT, p_off          # 1.9500 / 4

    # Dimensional/convexity check: P_bar is a weighted average of p_in and p_out
    # with weights 1/(1+rho) and rho/(1+rho) summing to 1, so it must lie
    # between the two component prices for every regime.
    for p_in, p_out, p_bar in (
        (P_IN_CLOSED, P_OUT_CLOSED, p_closed),
        (P_IN_V3, P_OUT_V3, p_v3),
        (P_IN_OFF, P_OUT_OFF, p_off),
    ):
        assert min(p_in, p_out) <= p_bar <= max(p_in, p_out)
        w_out = RHO / (1.0 + RHO)
        assert abs(p_bar - ((1.0 - w_out) * p_in + w_out * p_out)) < TOL_EXACT

    # Boundary regimes: rho -> 0 collapses to p_in; rho -> infinity to p_out.
    assert abs(blended_price(P_IN_CLOSED, P_OUT_CLOSED, 1e-12) - P_IN_CLOSED) < 1e-9
    assert abs(blended_price(P_IN_CLOSED, P_OUT_CLOSED, 1e12) - P_OUT_CLOSED) < 1e-3
    # Monotonicity in rho when p_out > p_in.
    assert blended_price(P_IN_V3, P_OUT_V3, 1.0) < p_v3 < blended_price(P_IN_V3, P_OUT_V3, 10.0)

    print(f"[2] P_bar_closed(3) = ${p_closed:.4f}/M, P_bar_open,V3(3) = ${p_v3:.4f}/M, "
          f"P_bar_open,off(3) = ${p_off:.4f}/M  OK")
    return p_closed, p_v3, p_off


def check_phi_asymmetry(p_closed: float, p_v3: float, p_off: float) -> None:
    """[3] Spec §4.2: Phi_API,std = 58.31x, Phi_API,off = 100.00x, and rent share theta_rent."""
    phi_std = p_closed / p_v3
    phi_off = p_closed / p_off
    assert abs(phi_std - 58.3064) < 1e-3, phi_std
    assert abs(round(phi_std, 2) - 58.31) < TOL_EXACT
    assert abs(phi_off - 100.0000) < TOL_EXACT, phi_off
    assert phi_off > phi_std > 1.0  # off-peak asymmetry strictly wider

    # Cartel Rent Share theta_rent = (P_closed - P_open) / P_closed = 1 - 1/Phi_API:
    theta_rent_std = (p_closed - p_v3) / p_closed
    theta_rent_off = (p_closed - p_off) / p_closed
    assert abs(theta_rent_std - (1.0 - 1.0 / phi_std)) < TOL_EXACT
    assert abs(theta_rent_off - (1.0 - 1.0 / phi_off)) < TOL_EXACT
    assert abs(theta_rent_std * 100.0 - 98.2849) < TOL_4DP, theta_rent_std * 100.0
    assert abs(theta_rent_off * 100.0 - 99.0000) < TOL_EXACT, theta_rent_off * 100.0
    print(f"[3] Phi_API,std = {phi_std:.4f}x ~= 58.31x (rent share {theta_rent_std*100:.4f}%), "
          f"Phi_API,off = {phi_off:.4f}x (rent share {theta_rent_off*100:.4f}%)  OK")


def check_unit_margin_collapse(p_closed: float, p_v3: float) -> None:
    """[4] Spec §4.3: Pi_foreign / Pi_US sanity check and tau_reg identity."""
    pi_foreign = V_NET - Q_TOKENS * p_v3
    pi_us = V_NET - Q_TOKENS * p_closed
    assert abs(pi_foreign - 7.58195) < TOL_EXACT, pi_foreign   # 8.00 - 0.41805
    assert abs(pi_us - (-16.3750)) < TOL_EXACT, pi_us          # 8.00 - 24.3750
    assert pi_us < 0.0 < pi_foreign                            # asymmetric flip

    margin_foreign = 100.0 * pi_foreign / R_UNIT
    margin_us = 100.0 * pi_us / R_UNIT
    assert abs(round(margin_foreign, 2) - 63.18) < TOL_EXACT, margin_foreign
    assert abs(round(margin_us, 2) - (-136.46)) < TOL_EXACT, margin_us

    # Article-rounded values (+$7.58 / -$16.38) must agree within 2dp rounding.
    assert abs(round(pi_foreign, 2) - 7.58) < TOL_EXACT
    assert abs(round(pi_us, 2) - (-16.38)) < TOL_EXACT

    # tau_reg identity: Pi_foreign - Pi_US = Q * (P_closed - P_open).
    tau_reg = pi_foreign - pi_us
    assert abs(tau_reg - Q_TOKENS * (p_closed - p_v3)) < TOL_EXACT
    assert abs(tau_reg - 23.95695) < TOL_EXACT, tau_reg
    print(f"[4] Pi_foreign = +${pi_foreign:.5f} ({margin_foreign:+.2f}%), "
          f"Pi_US = -${abs(pi_us):.4f} ({margin_us:+.2f}%), tau_reg = ${tau_reg:.5f}  OK")


def check_break_even_regimes(p_closed: float, p_v3: float) -> None:
    """[5] Spec §4.3: Q_crit thresholds, competitive zone, three-regime signs."""
    q_crit_us = V_NET / p_closed
    q_crit_foreign = V_NET / p_v3
    assert abs(q_crit_us - 0.1641) < TOL_4DP, q_crit_us        # 8.00 / 48.75
    assert abs(q_crit_foreign - 9.5682) < TOL_4DP, q_crit_foreign  # 8.00 / 0.8361
    assert q_crit_us < q_crit_foreign

    # Competitive token-intensive zone: Q*P_open < V_net < Q*P_closed.
    assert Q_TOKENS * p_v3 < V_NET < Q_TOKENS * p_closed
    # The spec's example workflow sits strictly inside the flip zone.
    assert q_crit_us < Q_TOKENS < q_crit_foreign

    # Three-regime sign structure across the ban's break-even boundaries.
    def profits(q: float) -> tuple:
        return (V_NET - q * p_closed, V_NET - q * p_v3)  # (Pi_US, Pi_foreign)

    pi_us_lo, pi_for_lo = profits(0.10)          # below Q_crit,US: both viable
    assert 0.0 < pi_us_lo and 0.0 < pi_for_lo
    pi_us_b, _ = profits(q_crit_us)              # boundary: Pi_US exactly zero
    assert abs(pi_us_b) < TOL_EXACT
    pi_us_mid, pi_for_mid = profits(Q_TOKENS)    # interior: asymmetric flip
    assert pi_us_mid < 0.0 < pi_for_mid
    _, pi_for_b = profits(q_crit_foreign)        # boundary: Pi_foreign exactly zero
    assert abs(pi_for_b) < TOL_EXACT
    pi_us_hi, pi_for_hi = profits(10.0)          # above Q_crit,foreign: both dead
    assert pi_us_hi < 0.0 and pi_for_hi < 0.0
    print(f"[5] Q_crit,US = {q_crit_us:.4f}M, Q_crit,foreign = {q_crit_foreign:.4f}M; "
          f"3-regime sign structure (both+ / flip / both-)  OK")


def check_omega_capture(p_closed: float, p_v3: float) -> None:
    """[6] Spec §4.4: Omega_capture closed form vs direct surplus accounting."""
    omega_cf = omega_closed_form(ETA_DESTROY, M_NET, EXPORT_LOSS_RATIO)
    assert abs(omega_cf - 13.3333) < TOL_4DP, omega_cf  # (1/0.30)*(1 + 1.5 + 1.5)

    # Direct accounting cross-check (scale-invariant; Q_base arbitrary in M tokens):
    # Q_ban = (1-eta)*Q_base; Delta_Pi_cartel = m_net*Q_ban*dP;
    # Delta_W = Q_ban*dP + 0.5*dP*(Q_base-Q_ban) + export_ratio*(Q_ban*dP).
    q_base = 100.0
    q_ban = (1.0 - ETA_DESTROY) * q_base
    delta_p = p_closed - p_v3
    delta_pi_cartel = M_NET * q_ban * delta_p
    direct_transfer = q_ban * delta_p
    harberger_triangle = 0.5 * delta_p * (q_base - q_ban)
    lost_downstream = EXPORT_LOSS_RATIO * direct_transfer
    delta_w = direct_transfer + harberger_triangle + lost_downstream
    omega_direct = delta_w / delta_pi_cartel
    assert abs(omega_direct - omega_cf) < 1e-9, (omega_direct, omega_cf)
    assert abs(omega_direct - 4.00 / 0.30) < 1e-9

    # Boundary regimes: Omega strictly increasing in eta_destroy on (0,1), and
    # the eta -> 0 floor with the 1.5x export term is (1/0.30)*(2.5) = 8.3333.
    assert omega_closed_form(0.25, M_NET, EXPORT_LOSS_RATIO) < \
        omega_closed_form(0.50, M_NET, EXPORT_LOSS_RATIO) < \
        omega_cf < omega_closed_form(0.90, M_NET, EXPORT_LOSS_RATIO)
    assert abs(omega_closed_form(1e-12, M_NET, EXPORT_LOSS_RATIO) - 2.5 / 0.30) < 1e-6
    assert omega_cf > 1.0  # destruction strictly exceeds captured rent
    print(f"[6] Omega_capture = {omega_cf:.4f}x (closed form) == {omega_direct:.4f}x "
          f"(direct Delta_W/Delta_Pi); monotone in eta  OK")


def check_brain_drain_ratchet(p_closed: float, p_v3: float, p_off: float) -> None:
    """[7] Spec §4.5: experimentation compression and Q_drain^* offshoring threshold."""
    n_open_m = B_COMPUTE_USD / p_v3
    n_off_m = B_COMPUTE_USD / p_off
    n_closed_m = B_COMPUTE_USD / p_closed

    assert abs(n_open_m / 1e3 - 299.0073) < TOL_4DP, n_open_m / 1e3
    assert abs(n_off_m / 1e3 - 512.8205) < TOL_4DP, n_off_m / 1e3
    assert abs(n_closed_m / 1e3 - 5.1282) < TOL_4DP, n_closed_m / 1e3
    # Throughput ratio under fixed budget equals Phi_API identically:
    assert abs((n_open_m / n_closed_m) - (p_closed / p_v3)) < TOL_EXACT

    net_hub_barrier = DELTA_V_HUB_USD + RELOC_ANNUAL_USD - COMPLIANCE_ANNUAL_USD
    assert abs(net_hub_barrier - 480_000.0) < TOL_EXACT
    spread = p_closed - p_v3
    assert abs(spread - 47.9139) < TOL_EXACT

    q_drain_crit_m = net_hub_barrier / spread
    assert abs(q_drain_crit_m - 10_017.9697) < TOL_4DP, q_drain_crit_m
    assert abs(q_drain_crit_m / 1e3 - 10.0180) < TOL_4DP
    assert abs((q_drain_crit_m / 365.0) - 27.45) < TOL_2DP

    # Two-regime relocation sign structure around Q_drain^*:
    def delta_pi_reloc(q_m: float) -> float:
        return q_m * spread + COMPLIANCE_ANNUAL_USD - (DELTA_V_HUB_USD + RELOC_ANNUAL_USD)

    assert delta_pi_reloc(5_000.0) < 0.0                          # below Q_drain^*: stay
    assert abs(delta_pi_reloc(q_drain_crit_m)) < TOL_EXACT        # boundary: indifferent
    savings_100b = delta_pi_reloc(Q_STARTUP_M)                    # 100B tokens/yr: offshore
    assert abs(savings_100b - 4_311_390.0) < TOL_EXACT, savings_100b
    assert savings_100b > 0.0

    # Physical & media density check (671B params in FP8 = 671 GB; in INT4 = 335.5 GB):
    params_b = 671.0
    fp8_gb = params_b * 1.0
    int4_gb = params_b * 0.5
    microsd_capacity_gb = 1000.0
    microsd_mass_g = 0.25
    assert int4_gb == 335.5 and fp8_gb == 671.0
    assert int4_gb < fp8_gb < microsd_capacity_gb
    assert abs((fp8_gb / microsd_mass_g) - 2684.0) < TOL_EXACT
    # 10 Gbps link (= 1.25 GB/s) transfer times:
    assert abs((int4_gb / 1.25) - 268.4) < TOL_EXACT
    assert abs((fp8_gb / 1.25) - 536.8) < TOL_EXACT
    print(f"[7] Brain-drain threshold Q_drain^* = {q_drain_crit_m:.4f}M/yr "
          f"(~{q_drain_crit_m/1e3:.4f}B/yr); Delta_Pi_reloc(100B) = +${savings_100b:,.2f}/yr; "
          f"physical checkpoint = {int4_gb:.1f}-{fp8_gb:.1f} GB (<1 TB microSD)  OK")


def check_falsification_boundary(p_closed: float, p_v3: float) -> None:
    """[8] Spec §6: Phi_API -> 1.0 convergence falsifier is far from current regime."""
    convergence_threshold = 0.84  # USD/M, spec §6 condition 2
    assert p_closed > convergence_threshold
    assert p_closed / p_v3 > 58.0  # current asymmetry nowhere near Phi -> 1.0
    # Falsifier would require closed pricing to compress by >98%:
    compression_required = 1.0 - convergence_threshold / p_closed
    assert compression_required > 0.98, compression_required
    print(f"[8] Falsification boundary: P_closed = ${p_closed:.2f}/M >> "
          f"${convergence_threshold:.2f}/M threshold (>{compression_required*100:.1f}% "
          f"compression required)  OK")


def main() -> int:
    check_capex_compression()
    p_closed, p_v3, p_off = check_blended_prices()
    check_phi_asymmetry(p_closed, p_v3, p_off)
    check_unit_margin_collapse(p_closed, p_v3)
    check_break_even_regimes(p_closed, p_v3)
    check_omega_capture(p_closed, p_v3)
    check_brain_drain_ratchet(p_closed, p_v3, p_off)
    check_falsification_boundary(p_closed, p_v3)
    print("ALL CHECKS PASSED: SPEC-OPEN-WEIGHT-DISTILLATION-AND-DOMESTIC-BAN-IMPOSSIBILITY-v1.0 "
          "invariants verified (exit 0).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
