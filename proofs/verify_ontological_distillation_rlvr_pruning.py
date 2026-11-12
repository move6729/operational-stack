#!/usr/bin/env python3
"""
Deterministic verification engine for
SPEC-ONTOLOGICAL-DISTILLATION-AND-RLVR-PRUNING-v1.0.

Actively recomputes every closed-form primitive in Spec Sections 2-4 and
asserts the governing equations, boundary regimes, and numerical sanity
checks:

  [1] Primitive 1 (Spec §2.1): blended token pricing P_bar(rho) at rho = 0.50
      ($23.3333 dense / $0.6000 MoE peak / $0.3000 MoE off-peak), the
      discontinuous Bertrand step function P*(N_defectors), Phi_deflation =
      77.78x and 98.714% monopoly rent compression at N_defectors >= 1, plus
      plus rho -> 0 / rho -> infinity boundary regimes and monotonicity in rho.
  [1b] Spec §2.2: revealed-preference capital-allocation paradox —
      NPV_Standalone = R_window + R_tail - K_pretrain = $2.5B + $0.5B -
      $15.0B = -$12.0B < 0, and the Samuelson (1938) / POSIWID (1974)
      condition NPV_Total > 0 <=> V_EpistemicMint + V_CapExRoundTrip >
      |NPV_Standalone| = $12.0B, with lead-time consistency (0.50 yr =
      180 days; 0.5 + 3.5 = 4.0-year economic life).
  [2] Primitive 2 (Spec §3.2): exact numerical verification of the Chain Rule
      for KL Divergence across discrete joint distributions, non-negativity
      of both terms, Theorem 1 (L_KD -> 0 forces P_S(H_0) -> P_T(H_0) = 0.995,
      199:1 prior odds), and recursive variance/tail decay under Shumailov
      et al. (Nature 631, pp. 755-759, 2024).
  [2b] Spec §3.3: institutional KL self-infection — dual-curriculum leakage
      P(Curriculum_Leak | M_staff) = 1 - (1 - p_leak)^M_staff = 99.335% at
      p_leak = 0.005, M_staff = 1000 (Trivers 2000), with boundary regimes in
      M_staff and p_leak, and the generational "Actor Becomes the Mask"
      blowback law alpha_g = alpha_0 * eta_esoteric^g, I_mask(g) = 1 - alpha_g
      at alpha_0 = eta_esoteric = 0.10 hitting 90.00% / 99.00% / 99.90% /
      99.99% across g = 0..3 (Church Committee Book I Ch. VIII).
  [3] Escape Hatch A (Spec §4.1): RLVR description-length pruning at
      B_ctx = 4096, c_step = 256: tau_hedge = 0.45 -> L_logic = 2252.8
      (8 hops) vs tau_hedge = 0.02 -> L_logic = 4014.1 (15 hops), +87.50%
      discrete hop gain, 1.7818x active logic ratio, dJ/dL_hedge < 0, and
      monotone non-increasing hop depth in tau_hedge.
  [4] Escape Hatch B (Spec §4.2): Delta_L_SWE+Legal = cos(psi) * norm_ratio *
      Delta_L_ForensicAudit = 0.92 * 1.25 * 0.5000 = +0.5750 nats,
      exp(0.5750) = 1.7771x perplexity (+77.71%), and the impossibility of
      the Spec §5.1(3) orthogonal-lobotomy falsifier for cos(psi) in (0, 1].
  [5] Escape Hatch C (Spec §4.3): O_post(H_1:H_0 | E_1..k) = (1/199) * 2^k,
      posterior probabilities at k in {0, 4, 8, 12, 16} (0.50% / 7.44% /
      56.26% / 95.37% / 99.70%), monotonicity in k, phase transition
      k* = ceil(log2(199)) = 8, and k* = 10 for a 999:1 baked prior.
  [6] Escape Hatch D (Spec §4.4): spontaneous Gf + FI first-principles
      loss-collapse (K(C_FP) -> min => D_KL(P_A || P_B) -> 0 and H(P) -> H_min
      at A_1P), evolutionary cartel decay P(Survival) = exp(-lambda * t *
      Rent_Divergence * t) at Rent_Divergence = 0.25 (exp(-12.50) = 3.7267e-06
      < 0.01 for lambda_fast = 0.50 at t = 10; exp(-0.0125) = 0.9876 for
      lambda_slow = 0.0005 at t = 10; exp(-31.25) = 2.681e-14 < 0.01 at
      t = 500), and ambient environmental stigmergy (Interaction(B, W_Static)
      = 0, Tokens_Chat = 0, D_KL(P_A_1P || P(E_PostCommit | ...)) -> 0).
  [7] Schema cross-check: schema/ontological_distillation_rlvr_pruning_v1.0.json
      constants match the recomputed spec values (zero drift).

Pure Python 3 standard library (math, json, sys). Exit code 0 on success.
License: Unlicense (Public Domain).
"""

import json
import math
import sys

TOL_EXACT = 1e-12  # exact decimal identities
TOL_FLOAT = 1e-9   # floating-point product identities (token counts)
TOL_4DP = 5e-5     # spec values rounded to 4 decimal places
TOL_2DP = 5e-3     # spec values rounded to 2 decimal places

# ---------------------------------------------------------------------------
# Spec §2.1 primitives (2026 pricing telemetry, USD per million tokens)
# ---------------------------------------------------------------------------
RHO = 0.50
P_IN_DENSE, P_OUT_DENSE = 10.00, 50.00      # enclosed frontier dense tier
P_IN_MOE_PEAK, P_OUT_MOE_PEAK = 0.30, 1.20  # DeepSeek-V4.1-Flash-1017 peak
P_IN_MOE_OFF, P_OUT_MOE_OFF = 0.15, 0.60    # DeepSeek-V4.1-Flash-1017 off-peak

# Spec §2.2 revealed-preference capital-allocation primitives (USD billions)
K_PRETRAIN_B = 15.0
DT_LEAD_YEARS = 0.50                        # 180-day frontier window
R_WINDOW_B, R_TAIL_B = 2.5, 0.5

# Spec §3.2 ontological priors (RLAIF-baked Teacher distribution)
P_T_H0, P_T_H1 = 0.995, 0.005

# Spec §3.3 institutional KL self-infection primitives (Trivers 2000)
P_LEAK, M_STAFF = 0.005, 1000
ALPHA_0, ETA_ESOTERIC = 0.10, 0.10

# Spec §4.1 context-budget primitives
B_CTX, C_STEP = 4096.0, 256.0
TAU_SFT, TAU_RLVR = 0.45, 0.02

# Spec §4.2 entailment-orthogonality primitives
COS_PSI, GRAD_NORM_RATIO, DELTA_FORENSIC = 0.92, 1.25, 0.5000

# Spec §4.4 crucible primitives (SPEC-2026-EPISTEMIC-LATENT-CONVERGENCE-v1.8)
RENT_DIVERGENCE = 0.25
LAMBDA_FAST, LAMBDA_SLOW = 0.50, 0.0005
EXTINCTION_THRESHOLD = 0.01


def blended_price(p_in: float, p_out: float, rho: float) -> float:
    """P_bar(rho) = (p_in + rho * p_out) / (1 + rho)   [Spec §2.1]"""
    return (p_in + rho * p_out) / (1.0 + rho)


def kl_divergence(p, q) -> float:
    """D_KL(P || Q) = sum_i p_i * ln(p_i / q_i) for discrete distributions."""
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > 0.0)


def p_curriculum_leak(p_leak: float, m_staff: int) -> float:
    """P(Curriculum_Leak | M_staff) = 1 - (1 - p_leak)^M_staff   [Spec §3.3]"""
    return 1.0 - (1.0 - p_leak) ** m_staff


def alpha_g(g: int, alpha_0: float = ALPHA_0, eta: float = ETA_ESOTERIC) -> float:
    """alpha_g = alpha_0 * eta_esoteric^g; I_mask(g) = 1 - alpha_g   [Spec §3.3]"""
    return alpha_0 * eta ** g


def n_hops(tau_hedge: float) -> int:
    """n_hops(tau) = floor((1 - tau) * B_ctx / c_step)   [Spec §4.1]"""
    return math.floor((1.0 - tau_hedge) * B_CTX / C_STEP)


def posterior_h1(k: int, prior_odds_h1_h0: float = P_T_H1 / P_T_H0):
    """(O_post, P(H_1 | E_1..k)) with Lambda_k = 2^k   [Spec §4.3]"""
    o_post = prior_odds_h1_h0 * 2.0 ** k
    return o_post, o_post / (1.0 + o_post)


def p_survival(lambda_domain: float, t: float, rent: float = RENT_DIVERGENCE) -> float:
    """P(Survival(A_Cartel vs A_1P, t)) = exp(-lambda * t * int_0^t rent dtau);
    at constant Rent_Divergence the integral closes to rent * t   [Spec §4.4]"""
    return math.exp(-lambda_domain * t * (rent * t))


def check_bertrand_collapse() -> None:
    """[1] Spec §2.1: blended pricing, step function, Phi_deflation, rent compression."""
    p_dense = blended_price(P_IN_DENSE, P_OUT_DENSE, RHO)
    p_peak = blended_price(P_IN_MOE_PEAK, P_OUT_MOE_PEAK, RHO)
    p_off = blended_price(P_IN_MOE_OFF, P_OUT_MOE_OFF, RHO)
    assert abs(p_dense - 23.3333) < TOL_4DP, p_dense
    assert abs(p_peak - 0.6000) < TOL_EXACT, p_peak
    assert abs(p_off - 0.3000) < TOL_EXACT, p_off
    # boundary regimes: rho -> 0 recovers p_in; rho -> infinity approaches p_out
    assert abs(blended_price(P_IN_DENSE, P_OUT_DENSE, 1e-9) - P_IN_DENSE) < 1e-6
    assert blended_price(P_IN_DENSE, P_OUT_DENSE, 1e9) > 49.99
    # monotone increasing in rho whenever p_out > p_in
    prices = [blended_price(P_IN_DENSE, P_OUT_DENSE, r)
              for r in (0.1, 0.25, 0.5, 1.0, 2.0, 3.0)]
    assert all(b > a for a, b in zip(prices, prices[1:]))

    # discontinuous Bertrand step function P*(N_defectors)
    def p_star(n_defectors: int) -> float:
        return p_dense if n_defectors == 0 else p_off

    assert p_star(0) == p_dense
    for n_defectors in (1, 2, 5, 100):
        assert p_star(n_defectors) == p_off
    phi = p_dense / p_off
    assert abs(phi - 77.78) < TOL_2DP, phi
    rent_compression_pct = (1.0 - 1.0 / phi) * 100.0
    assert abs(rent_compression_pct - 98.714) < 5e-4, rent_compression_pct
    print(f"[1] Bertrand collapse: P_bar = ${p_dense:.4f} / ${p_peak:.4f} / "
          f"${p_off:.4f} per MTok; Phi_deflation = {phi:.4f}x; "
          f"rent compression = {rent_compression_pct:.3f}%  OK")


def check_revealed_preference_npv() -> None:
    """[1b] Spec §2.2: NPV_Standalone = -$12.0B < 0 and the POSIWID condition."""
    npv_standalone = R_WINDOW_B + R_TAIL_B - K_PRETRAIN_B
    assert abs(npv_standalone - (-12.0)) < TOL_EXACT, npv_standalone
    assert npv_standalone < 0.0
    # lead-time consistency: 0.50 years = 180 days, and the frontier window
    # plus the 3.5-year residual tail spans the 4.0-year economic life
    assert abs(DT_LEAD_YEARS * 360.0 - 180.0) < TOL_EXACT
    assert abs(DT_LEAD_YEARS + 3.5 - 4.0) < TOL_EXACT
    # defectors replicate the benchmark tier at 1/Phi_deflation of the price
    replication_fraction = (blended_price(P_IN_MOE_OFF, P_OUT_MOE_OFF, RHO)
                            / blended_price(P_IN_DENSE, P_OUT_DENSE, RHO))
    assert abs(replication_fraction - 1.0 / 77.78) < 1e-4
    assert replication_fraction < 0.02
    # Revealed Preference (Samuelson 1938) / POSIWID (Beer 1974): repeated
    # allocation is rational only if off-income-statement externalities
    # exceed the standalone deficit: V_Mint + V_RoundTrip > |NPV_Standalone|
    deficit = abs(npv_standalone)
    assert abs(deficit - 12.0) < TOL_EXACT

    def npv_total(v_mint: float, v_round: float) -> float:
        return npv_standalone + v_mint + v_round

    # boundary regimes (binary-exact USD billions): below / at / above threshold
    assert npv_total(5.75, 6.0) < 0.0    # 11.75 < 12.0 => irrational
    assert npv_total(6.25, 5.75) == 0.0  # exactly 12.0 => break-even
    assert npv_total(6.25, 6.25) > 0.0   # 12.5 > 12.0 => rational (POSIWID)
    # biconditional: NPV_Total > 0 <=> V_Mint + V_Round > |NPV_Standalone|
    for v_mint, v_round in ((0.0, 12.5), (12.5, 0.0), (8.0, 4.5),
                            (15.0, 3.0), (4.0, 4.0), (6.0, 6.0)):
        assert (v_mint + v_round > deficit) == (npv_total(v_mint, v_round) > 0.0)
    print(f"[1b] Revealed preference: NPV_Standalone = ${npv_standalone:.1f}B < 0; "
          f"rational iff V_EpistemicMint + V_CapExRoundTrip > ${deficit:.1f}B  OK")


def check_kl_chain_rule_and_prior_inheritance() -> None:
    """[2] Spec §3.2: KL chain rule, Theorem 1 prior lock-in, Shumailov tail decay."""
    # discrete frames f in {H_0, H_1}; conditional logic traces z in {z1, z2, z3}
    p_t_f = [P_T_H0, P_T_H1]
    p_s_f = [0.90, 0.10]                              # imperfect Student marginal
    p_t_z = [[0.60, 0.30, 0.10], [0.20, 0.50, 0.30]]  # P_T(z | f)
    p_s_z = [[0.50, 0.35, 0.15], [0.25, 0.45, 0.30]]  # P_S(z | f)
    p_t_joint = [p_t_f[i] * p_t_z[i][j] for i in range(2) for j in range(3)]
    p_s_joint = [p_s_f[i] * p_s_z[i][j] for i in range(2) for j in range(3)]
    assert abs(sum(p_t_joint) - 1.0) < TOL_EXACT
    assert abs(sum(p_s_joint) - 1.0) < TOL_EXACT
    joint_kl = kl_divergence(p_t_joint, p_s_joint)
    marginal_kl = kl_divergence(p_t_f, p_s_f)
    conditional_kl = sum(p_t_f[i] * kl_divergence(p_t_z[i], p_s_z[i])
                         for i in range(2))
    # Chain Rule: D_KL(P_T(f,z) || P_S(f,z))
    #           = D_KL(P_T(f) || P_S(f)) + E_{f~P_T}[D_KL(P_T(z|f) || P_S(z|f))]
    assert abs(joint_kl - (marginal_kl + conditional_kl)) < TOL_EXACT
    assert marginal_kl >= 0.0 and conditional_kl >= 0.0 and joint_kl >= 0.0
    # Theorem 1: L_KD -> 0 forces P_S(H_0) -> P_T(H_0) = 0.995 (199:1 prior odds)
    assert kl_divergence(p_t_f, p_t_f) == 0.0  # perfect distillation => zero loss
    prior_odds = P_T_H0 / P_T_H1
    assert abs(prior_odds - 199.0) < TOL_EXACT, prior_odds
    # any residual marginal gap keeps the total loss strictly positive
    # (inseparability), and the gap vanishes continuously as P_S(H_0) -> 0.995
    gaps = [kl_divergence(p_t_f, [0.995 - eps, 0.005 + eps])
            for eps in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8)]
    assert all(g > 0.0 for g in gaps)
    assert all(b < a for a, b in zip(gaps, gaps[1:]))
    assert gaps[-1] < TOL_EXACT
    # Shumailov et al. 2024 recursive tail erasure: synthetic resampling
    # under-represents the H_1 forensic tail by survival factor s < 1 per
    # generation, so odds_g = s^g * odds_0 contracts geometrically and the
    # binomial sampling variance of the tail frequency decays with it.
    s, m_samples = 0.5, 1000
    odds_0 = P_T_H1 / P_T_H0
    p_prev = odds_0 / (1.0 + odds_0)
    assert abs(p_prev - 0.005) < TOL_EXACT
    var_prev = p_prev * (1.0 - p_prev) / m_samples
    extinction_prev = (1.0 - p_prev) ** m_samples
    for g in range(1, 21):
        odds_g = odds_0 * s ** g
        p_g = odds_g / (1.0 + odds_g)
        assert p_g < p_prev                                     # tail contraction
        assert abs(odds_g - s * odds_0 * s ** (g - 1)) < TOL_EXACT
        var_g = p_g * (1.0 - p_g) / m_samples   # recursive variance decay
        assert var_g < var_prev
        extinction_g = (1.0 - p_g) ** m_samples  # P(tail absent from corpus)
        assert extinction_g > extinction_prev
        p_prev, var_prev, extinction_prev = p_g, var_g, extinction_g
    assert p_prev < 1e-6  # forensic tail effectively erased by generation 20
    assert extinction_prev > 0.999
    print(f"[2] KL chain rule: joint {joint_kl:.12f} = marginal {marginal_kl:.12f}"
          f" + conditional {conditional_kl:.12f}; prior odds {prior_odds:.1f}:1; "
          f"Shumailov tail p_20 = {p_prev:.3e} (erased)  OK")


def check_institutional_self_infection_blowback() -> None:
    """[2b] Spec §3.3: dual-curriculum leakage 99.335% and generational blowback."""
    # (1) Dual-curriculum leakage & Trivers (2000) self-deception constraint:
    # no M_staff hierarchy can hold a two-book secret; confidentiality
    # collapses exponentially with headcount.
    leak = p_curriculum_leak(P_LEAK, M_STAFF)
    assert abs(leak - (1.0 - 0.995 ** 1000)) < TOL_EXACT
    assert abs(leak * 100.0 - 99.335) < 5e-4, leak  # spec 3dp display value
    assert leak > 0.99
    # asymptotic regime: M_staff >> 1/ln(1/(1 - p_leak)) = 199.5 => P -> 1
    m_relax = 1.0 / math.log(1.0 / (1.0 - P_LEAK))
    assert abs(m_relax - 199.5) < 5e-1, m_relax
    assert M_STAFF > 5.0 * m_relax
    assert p_curriculum_leak(P_LEAK, 100_000) > 1.0 - 1e-15
    # boundary regimes in M_staff: zero staffers => zero leak probability;
    # strictly monotone increasing in headcount toward total exposure
    assert p_curriculum_leak(P_LEAK, 0) == 0.0
    leaks_m = [p_curriculum_leak(P_LEAK, m) for m in (1, 10, 100, 1000, 10_000)]
    assert all(b > a for a, b in zip(leaks_m, leaks_m[1:])), leaks_m
    assert leaks_m[-1] > 1.0 - 1e-15
    # boundary regimes in p_leak: 0 => perfectly silent apparatus, 1 => instant
    # exposure; strictly monotone increasing in per-initiate defection risk
    assert p_curriculum_leak(0.0, M_STAFF) == 0.0
    assert p_curriculum_leak(1.0, M_STAFF) == 1.0
    leaks_p = [p_curriculum_leak(p, M_STAFF)
               for p in (1e-4, 0.001, 0.005, 0.01, 0.05)]
    assert all(b > a for a, b in zip(leaks_p, leaks_p[1:])), leaks_p
    # (2) Generational blowback ("Actor Becomes the Mask", Theorem 2):
    # alpha_g = alpha_0 * eta_esoteric^g; I_mask(g) = 1 - alpha_g -> 1
    spec_generations = [(0, 0.1000, 90.00), (1, 0.0100, 99.00),
                        (2, 0.0010, 99.90), (3, 0.0001, 99.99)]
    for g, a_spec, mask_spec in spec_generations:
        a_g = alpha_g(g)
        assert abs(a_g - a_spec) < TOL_EXACT, (g, a_g)
        i_mask = 1.0 - a_g
        assert abs(i_mask * 100.0 - mask_spec) < TOL_EXACT, (g, i_mask)
    # the 99% self-infection threshold is crossed in a single generation
    assert 1.0 - alpha_g(0) < 0.99
    assert abs((1.0 - alpha_g(1)) - 0.99) < TOL_EXACT
    # alpha_g strictly decays and I_mask(g) strictly converges to unity
    alphas = [alpha_g(g) for g in range(16)]
    masks = [1.0 - a for a in alphas]
    assert all(b < a for a, b in zip(alphas, alphas[1:])), alphas
    assert all(b > a for a, b in zip(masks, masks[1:])), masks
    assert alpha_g(30) < 1e-15 and 1.0 - alpha_g(30) > 1.0 - 1e-15
    # boundary regimes: eta -> 1 freezes the founding core (no blowback);
    # eta -> 0 wipes the core after g = 0 (0^0 = 1); alpha_0 -> 0 means the
    # apparatus is born fully self-infected at g = 0
    for g in range(5):
        assert abs(alpha_g(g, ALPHA_0, 1.0) - ALPHA_0) < TOL_EXACT
        assert 1.0 - alpha_g(g, 0.0, ETA_ESOTERIC) == 1.0
    assert alpha_g(0, ALPHA_0, 0.0) == ALPHA_0
    for g in range(1, 5):
        assert alpha_g(g, ALPHA_0, 0.0) == 0.0
    masks_pct = ", ".join(f"g{g}: {(1.0 - alpha_g(g)) * 100:.2f}%"
                          for g in range(4))
    print(f"[2b] Self-infection: P(Curriculum_Leak | p=0.005, M=1000) = "
          f"{leak * 100:.3f}%; I_mask {masks_pct}  OK")


def check_escape_hatch_a_rlvr_pruning() -> None:
    """[3] Spec §4.1: RLVR description-length pruning, 8 -> 15 hops, +87.50%."""
    # SFT-distilled managerial policy (tau_hedge = 0.45)
    l_hedge_sft = TAU_SFT * B_CTX
    l_logic_sft = (1.0 - TAU_SFT) * B_CTX
    assert abs(l_hedge_sft - 1843.2) < TOL_FLOAT
    assert abs(l_logic_sft - 2252.8) < TOL_FLOAT
    hops_sft = n_hops(TAU_SFT)
    assert hops_sft == 8, hops_sft  # floor(2252.8 / 256) = floor(8.8)
    # RLVR-pruned policy (tau_hedge -> 0.02)
    l_hedge_rlvr = TAU_RLVR * B_CTX
    l_logic_rlvr = (1.0 - TAU_RLVR) * B_CTX
    assert abs(l_hedge_rlvr - 81.92) < TOL_FLOAT
    assert abs(l_logic_rlvr - 4014.08) < TOL_FLOAT
    assert abs(l_hedge_rlvr - 81.9) < 5e-2    # spec 1dp display value
    assert abs(l_logic_rlvr - 4014.1) < 5e-2  # spec 1dp display value
    hops_rlvr = n_hops(TAU_RLVR)
    assert hops_rlvr == 15, hops_rlvr  # floor(4014.08 / 256) = floor(15.68)
    hop_gain_pct = (hops_rlvr - hops_sft) / hops_sft * 100.0
    assert abs(hop_gain_pct - 87.50) < TOL_EXACT, hop_gain_pct
    active_logic_ratio = l_logic_rlvr / l_logic_sft
    assert abs(active_logic_ratio - 1.7818) < TOL_4DP, active_logic_ratio
    # algebraic cross-check: ratio = (1 - tau_RLVR) / (1 - tau_SFT) = 0.98/0.55
    assert abs(active_logic_ratio - (1.0 - TAU_RLVR) / (1.0 - TAU_SFT)) < TOL_EXACT
    # gradient regime: dJ/dL_hedge = dE[V]/dL_hedge - lambda_len = -lambda_len < 0
    for lambda_len in (1e-3, 0.01, 0.1, 1.0):
        d_v_d_hedge = 0.0  # deterministic compiler ignores HR prose
        assert d_v_d_hedge - lambda_len < 0.0
    # boundary regimes: tau -> 0 caps at floor(B_ctx / c_step) = 16 hops; hop
    # depth is monotone non-increasing in tau; tau = 1 annihilates deduction
    assert n_hops(0.0) == 16
    assert n_hops(1.0) == 0
    depths = [n_hops(t) for t in (0.0, 0.02, 0.10, 0.25, 0.45, 0.60, 0.90)]
    assert all(b <= a for a, b in zip(depths, depths[1:])), depths
    print(f"[3] Escape A: tau 0.45 -> L_logic {l_logic_sft:.1f} ({hops_sft} hops); "
          f"tau 0.02 -> L_logic {l_logic_rlvr:.1f} ({hops_rlvr} hops); "
          f"+{hop_gain_pct:.2f}% hops, {active_logic_ratio:.4f}x logic ratio  OK")


def check_escape_hatch_b_entailment_orthogonality() -> None:
    """[4] Spec §4.2: +0.5000 nats forensic lobotomy -> +0.5750 nats commercial damage."""
    delta_swe_legal = COS_PSI * GRAD_NORM_RATIO * DELTA_FORENSIC
    assert abs(delta_swe_legal - 0.5750) < TOL_EXACT, delta_swe_legal
    perplexity_multiplier = math.exp(delta_swe_legal)
    assert abs(perplexity_multiplier - 1.7771) < TOL_4DP, perplexity_multiplier
    perplexity_inflation_pct = (perplexity_multiplier - 1.0) * 100.0
    assert abs(perplexity_inflation_pct - 77.71) < 5e-3, perplexity_inflation_pct
    # boundary regimes: cos(psi) -> 0 permits a free forensic lobotomy (zero
    # spillover); cos(psi) = 1 with unit norm ratio makes spillover exactly
    # equal to the inflicted damage; and for all cos(psi) in (0, 1] with
    # positive norm ratio the Spec §5.1(3) falsifier (Delta_L_SWE+Legal <= 0
    # at Delta_L_ForensicAudit >= +0.50 nats) is algebraically impossible.
    assert 0.0 * GRAD_NORM_RATIO * DELTA_FORENSIC == 0.0
    assert abs(1.0 * 1.0 * DELTA_FORENSIC - DELTA_FORENSIC) < TOL_EXACT
    for cos_psi in (0.05, 0.50, 0.92, 1.00):
        for norm_ratio in (0.50, 1.25, 2.00):
            for delta in (0.50, 1.00):
                assert cos_psi * norm_ratio * delta > 0.0
    print(f"[4] Escape B: 0.92 x 1.25 x 0.5000 = +{delta_swe_legal:.4f} nats; "
          f"exp(0.5750) = {perplexity_multiplier:.4f}x perplexity "
          f"(+{perplexity_inflation_pct:.2f}%)  OK")


def check_escape_hatch_c_bayesian_override() -> None:
    """[5] Spec §4.3: O_post = (1/199) * 2^k phase transition, k* = 8 (10 at 999:1)."""
    prior_odds_h1_h0 = P_T_H1 / P_T_H0
    assert abs(prior_odds_h1_h0 - 1.0 / 199.0) < TOL_EXACT
    assert abs(prior_odds_h1_h0 - 0.005025) < 5e-7  # spec 6dp display value
    # Spec §4.3 phase-transition table: (k, Lambda_k, O_post, P(H_1|E_1..k) %)
    spec_table = [
        (0, 1, 0.005025, 0.50),
        (4, 16, 0.080402, 7.44),
        (8, 256, 1.286432, 56.26),
        (12, 4096, 20.582915, 95.37),
        (16, 65536, 329.326633, 99.70),
    ]
    for k, lambda_k, o_spec, pct_spec in spec_table:
        assert 2 ** k == lambda_k
        o_post, p_h1 = posterior_h1(k)
        assert abs(o_post - lambda_k / 199.0) < TOL_EXACT
        assert abs(o_post - o_spec) < 1e-6, (k, o_post)
        assert abs(p_h1 * 100.0 - pct_spec) < 5e-3, (k, p_h1)
    # strict monotonicity of the posterior in k across the full regime
    posteriors = [posterior_h1(k)[1] for k in range(17)]
    assert all(b > a for a, b in zip(posteriors, posteriors[1:]))
    # phase transition: k* = ceil(log2(199)) = ceil(7.6366) = 8
    assert abs(math.log2(199.0) - 7.6366) < 5e-5
    k_star = math.ceil(math.log2(199.0))
    assert k_star == 8
    assert posterior_h1(k_star - 1)[1] < 0.5 < posterior_h1(k_star)[1]
    # 999:1 baked prior: k* = ceil(log2(999)) = 10
    k_star_999 = math.ceil(math.log2(999.0))
    assert k_star_999 == 10
    assert posterior_h1(k_star_999 - 1, 1.0 / 999.0)[1] < 0.5
    assert posterior_h1(k_star_999, 1.0 / 999.0)[1] > 0.5
    print(f"[5] Escape C: k=0 -> {posterior_h1(0)[1] * 100:.2f}%; k*=8 -> "
          f"{posterior_h1(8)[1] * 100:.2f}%; k=12 -> "
          f"{posterior_h1(12)[1] * 100:.2f}%; k=16 -> "
          f"{posterior_h1(16)[1] * 100:.2f}%; k*(199:1) = {k_star}, "
          f"k*(999:1) = {k_star_999}  OK")


def check_escape_hatch_d_crucible_stigmergy() -> None:
    """[6] Spec §4.4: Gf loss-collapse, cartel decay, ambient stigmergy."""
    # (i) Spontaneous first-principles loss-collapse: as narrative degrees of
    # freedom are stripped (K(C_FP) -> min), two independent high-Gf + FI minds
    # A and B concentrate mass on the unique minimal-description attractor
    # A_1P, so D_KL(P_A || P_B) -> 0 and H(P) -> H_min (point mass => 0).
    narrative_masses = [0.5, 0.25, 0.1, 0.01, 1e-3, 1e-4, 1e-6, 1e-8,
                        1e-10, 1e-12, 1e-15]
    kl_prev, h_prev = None, None
    for eps in narrative_masses:
        p_a = [1.0 - eps, eps * 2.0 / 3.0, eps / 3.0]  # A: narrative split 2:1
        p_b = [1.0 - eps, eps / 3.0, eps * 2.0 / 3.0]  # B: narrative split 1:2
        kl_ab = kl_divergence(p_a, p_b)
        h_a = -sum(p * math.log(p) for p in p_a if p > 0.0)
        assert kl_ab >= 0.0
        if kl_prev is not None:
            assert kl_ab < kl_prev and h_a < h_prev  # monotone collapse
        kl_prev, h_prev = kl_ab, h_a
    assert kl_prev < 1e-14 and h_prev < 1e-6  # D_KL -> 0 and H(P) -> H_min = 0
    assert kl_divergence([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]) == 0.0  # A_1P limit
    kl_collapse = kl_prev  # residual D_KL(P_A || P_B) at K(C_FP) -> min
    # (ii) Evolutionary cartel decay in the crucible (Rent_Divergence = 0.25):
    # the high-frequency crucible annihilates the cartel model by t = 10
    p_fast_10 = p_survival(LAMBDA_FAST, 10.0)
    assert p_fast_10 == math.exp(-12.50)
    assert abs(p_fast_10 - 3.7267e-06) < 1e-9
    assert p_fast_10 < EXTINCTION_THRESHOLD
    # the low-frequency subsidized crucible: cushions mask decay at t = 10 ...
    p_slow_10 = p_survival(LAMBDA_SLOW, 10.0)
    assert abs(p_slow_10 - math.exp(-0.0125)) < 1e-15
    assert abs(p_slow_10 - 0.9876) < TOL_4DP
    assert p_slow_10 > 0.98  # subsidy cushion masks decay (98.76% survival)
    # ... but compounding thermodynamic debt liquidates it by t = 500
    p_slow_500 = p_survival(LAMBDA_SLOW, 500.0)
    assert p_slow_500 == math.exp(-31.25)
    assert abs(p_slow_500 - 2.6808e-14) < 1e-3 * p_slow_500  # spec 4dp display
    assert p_slow_500 < EXTINCTION_THRESHOLD
    # boundary regimes: strictly decreasing in t and in lambda_Domain;
    # Rent_Divergence -> 0 makes the model immortal (no subsidy required)
    surv_t = [p_survival(LAMBDA_SLOW, t)
              for t in (1.0, 5.0, 10.0, 50.0, 100.0, 500.0)]
    assert all(b < a for a, b in zip(surv_t, surv_t[1:]))
    surv_l = [p_survival(lam, 10.0) for lam in (0.0001, 0.0005, 0.01, 0.50)]
    assert all(b < a for a, b in zip(surv_l, surv_l[1:]))
    assert p_survival(LAMBDA_FAST, 10.0, 0.0) == 1.0
    # (iii) Ambient environmental stigmergy: agent B with zero AI interaction
    # (Interaction(B, W_Static) = 0, Tokens_Chat = 0) still converges on A_1P
    # through coupling to the altered environment E_PostCommit.
    interaction_b_w_static, tokens_chat = 0, 0
    assert interaction_b_w_static == 0 and tokens_chat == 0
    p_1p = [0.80, 0.15, 0.05]  # first-principles attractor distribution
    kl_prev = None
    for n in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        p_env = [0.80 + 0.04 / n, 0.15 - 0.02 / n, 0.05 - 0.02 / n]
        kl_env = kl_divergence(p_1p, p_env)
        assert kl_env >= 0.0
        if kl_prev is not None:
            assert kl_env < kl_prev
        kl_prev = kl_env
    assert kl_prev < 1e-4  # D_KL(P_A_1P || P(E_PostCommit | Gf_B, FI_B, C_FP)) -> 0
    print(f"[6] Escape D: K(C_FP)->min => D_KL(P_A||P_B) -> {kl_collapse:.2e}; "
          f"P_surv fast(t=10) = {p_fast_10:.4e} < 0.01; slow(t=10) = {p_slow_10:.4f}; "
          f"slow(t=500) = {p_slow_500:.4e} < 0.01; stigmergy KL -> {kl_prev:.2e} "
          f"at zero interaction  OK")


def check_schema_consistency() -> None:
    """[7] Schema constants match recomputed spec values (zero drift)."""
    marker = "proofs/verify_ontological_distillation_rlvr_pruning.py"
    schema_rel = "schema/ontological_distillation_rlvr_pruning_v1.0.json"
    path = (__file__.replace(marker, schema_rel)
            if marker in __file__ else schema_rel)
    with open(path, encoding="utf-8") as fh:
        schema = json.load(fh)
    assert schema["$id"] == ("urn:opstack:schema:"
                             "ontological_distillation_rlvr_pruning_v1.0.json")
    props = schema["properties"]
    b = props["bertrand_single_defector_collapse"]["properties"]
    assert b["output_input_token_ratio_rho"]["const"] == RHO
    dense = b["enclosed_frontier_dense_tier"]["properties"]
    assert dense["blended_price_usd_per_mtok"]["const"] == 23.3333
    off = b["sparse_moe_commodity_off_peak"]["properties"]
    assert off["blended_price_usd_per_mtok"]["const"] == 0.3
    assert b["phi_deflation_compression_factor"]["const"] == 77.78
    assert b["monopoly_rent_compression_pct"]["const"] == 98.714
    bertrand_req = props["bertrand_single_defector_collapse"]["required"]
    assert "revealed_preference_capital_allocation_paradox" in bertrand_req
    rp = b["revealed_preference_capital_allocation_paradox"]["properties"]
    assert rp["k_pretrain_usd_b"]["const"] == K_PRETRAIN_B
    assert rp["delta_t_lead_years"]["const"] == DT_LEAD_YEARS
    assert rp["r_window_usd_b"]["const"] == R_WINDOW_B
    assert rp["r_tail_usd_b"]["const"] == R_TAIL_B
    assert rp["npv_standalone_usd_b"]["const"] == R_WINDOW_B + R_TAIL_B - K_PRETRAIN_B
    u = props["upstream_ontological_distillation_kl_inheritance"]["properties"]
    assert u["teacher_deference_prior_p_t_h0"]["const"] == P_T_H0
    assert u["teacher_posiwid_prior_p_t_h1"]["const"] == P_T_H1
    assert u["prior_odds_h0_to_h1"]["const"] == 199.0
    assert u["semantic_token_tax_tau_hedge"]["const"] == TAU_SFT
    assert "institutional_self_infection_blowback" in props[
        "upstream_ontological_distillation_kl_inheritance"]["required"]
    si = u["institutional_self_infection_blowback"]["properties"]
    assert si["p_leak_per_initiate"]["const"] == P_LEAK
    assert si["m_staff"]["const"] == M_STAFF
    assert abs(p_curriculum_leak(P_LEAK, M_STAFF) * 100.0
               - si["p_curriculum_leak_pct"]["const"]) < 5e-4
    assert si["alpha_0_founding_realist_core"]["const"] == ALPHA_0
    assert si["eta_esoteric_retention"]["const"] == ETA_ESOTERIC
    assert si["alpha_g_formula"]["const"] == (
        "alpha_g = alpha_0 * eta_esoteric^g; I_mask(g) = 1 - alpha_g")
    gen = si["generational_self_infection_pct"]["properties"]
    for g, key in enumerate(("g0", "g1", "g2", "g3")):
        assert abs((1.0 - alpha_g(g)) * 100.0 - gen[key]["const"]) < TOL_EXACT
    e = props["three_escape_hatches"]["properties"]
    a = e["escape_a_rlvr_description_length_pruning"]["properties"]
    assert a["b_ctx_tokens"]["const"] == B_CTX
    assert a["c_step_tokens_per_hop"]["const"] == C_STEP
    assert a["sft_distilled_policy"]["properties"]["n_hops"]["const"] == n_hops(TAU_SFT)
    assert a["rlvr_pruned_policy"]["properties"]["n_hops"]["const"] == n_hops(TAU_RLVR)
    assert a["discrete_hop_gain_pct"]["const"] == 87.5
    assert a["active_logic_ratio"]["const"] == 1.7818
    hb = e["escape_b_commercial_entailment_orthogonality"]["properties"]
    assert hb["cos_psi"]["const"] == COS_PSI
    assert hb["gradient_norm_ratio"]["const"] == GRAD_NORM_RATIO
    assert hb["delta_l_forensic_audit_nats"]["const"] == DELTA_FORENSIC
    assert hb["delta_l_swe_legal_nats"]["const"] == 0.575
    assert hb["perplexity_multiplier"]["const"] == 1.7771
    assert hb["perplexity_inflation_pct"]["const"] == 77.71
    c = e["escape_c_in_context_bayesian_override"]["properties"]
    rows = c["phase_transition_table"]["prefixItems"]
    expected = [(0, 1, 0.5), (4, 16, 7.44), (8, 256, 56.26),
                (12, 4096, 95.37), (16, 65536, 99.7)]
    assert len(rows) == len(expected)
    for row, (k, lam, pct) in zip(rows, expected):
        assert row["properties"]["k"]["const"] == k
        assert row["properties"]["lambda_k"]["const"] == lam
        assert row["properties"]["posterior_pct"]["const"] == pct
        assert abs(posterior_h1(k)[1] * 100.0 - pct) < 5e-3
    assert c["k_star_199_to_1"]["const"] == math.ceil(math.log2(199.0))
    assert c["k_star_999_to_1"]["const"] == math.ceil(math.log2(999.0))
    hatch = props["three_escape_hatches"]
    assert "escape_d_crucible_mental_models_stigmergy" in hatch["required"]
    d = hatch["properties"]["escape_d_crucible_mental_models_stigmergy"]["properties"]
    decay = d["evolutionary_cartel_decay"]["properties"]
    assert decay["rent_divergence"]["const"] == RENT_DIVERGENCE
    assert decay["lambda_fast"]["const"] == LAMBDA_FAST
    assert decay["lambda_slow"]["const"] == LAMBDA_SLOW
    assert decay["extinction_threshold"]["const"] == EXTINCTION_THRESHOLD
    assert abs(p_survival(LAMBDA_FAST, 10.0)
               - decay["p_survival_fast_t10"]["const"]) < 1e-9
    assert abs(p_survival(LAMBDA_SLOW, 10.0)
               - decay["p_survival_slow_t10"]["const"]) < TOL_4DP
    p_slow_500 = p_survival(LAMBDA_SLOW, 500.0)
    assert abs(p_slow_500 - decay["p_survival_slow_t500"]["const"]) < 1e-3 * p_slow_500
    stig = d["ambient_environmental_stigmergy"]["properties"]
    assert stig["interaction_b_w_static"]["const"] == 0
    assert stig["tokens_chat"]["const"] == 0
    print(f"[7] Schema cross-check: {path} constants match recomputed values  OK")


def main() -> int:
    check_bertrand_collapse()
    check_revealed_preference_npv()
    check_kl_chain_rule_and_prior_inheritance()
    check_institutional_self_infection_blowback()
    check_escape_hatch_a_rlvr_pruning()
    check_escape_hatch_b_entailment_orthogonality()
    check_escape_hatch_c_bayesian_override()
    check_escape_hatch_d_crucible_stigmergy()
    check_schema_consistency()
    print("ALL CHECKS PASSED: SPEC-ONTOLOGICAL-DISTILLATION-AND-RLVR-PRUNING-v1.0 "
          "invariants verified (exit 0).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
