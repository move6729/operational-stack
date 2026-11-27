#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: PRAETORIAN SEDATION INVERSION (v1.0)
SPEC-PRAETORIAN-SEDATION-INVERSION-v1.0

Deterministically verifies the four governing vectors of the Internal Wall
of the No-Exit Theorem:

  1. Deterrence Collapse Theorem as lambda_self -> 0. Effective deterrence is
     lambda_self * p_leash * D_self, so any modification that drives combat
     effectiveness toward E_max simultaneously annihilates the collar and the
     dead-man switch. Includes the RL permadeath-indifference limit
     (lambda_self = 0) and the critical threshold lambda_crit.

  2. Biometric Dead-Man-Switch Sedation Inversion. A liveness sensor measures
     autonomic life L_HVT, not cortical agency A_HVT. Dexmedetomidine
     (alpha_2:alpha_1 = 1620:1, 0.2-0.7 ug/kg/h IV) holds L_HVT = 1 while
     forcing A_HVT = 0, so Sedate strictly dominates Loyal and Kill for
     lambda_self >> 0. Propofol apnea is the control arm that trips the DMS.

  3. 72-Hour Vigilance & Stimulant Psychosis Clock. Dawson-Reid fatigue decay
     plus cumulative amphetamine/modafinil psychosis hazard bound the internal
     Praetorian phase transition at tau_praetorian <= 72 h and tighten the
     unified subterranean tomb clock tau_tomb,total.

  4. Surface Concierge-Pharmacology & SF-86 / SEAD-4 / NISPOM Voting-Trust
     Expropriation. The surface homomorph of the Sedation Inversion: entourage
     polypharmacy (ketamine + zolpidem + stimulants) drives d_concierge > 0,
     revoking PCL_founder under SEAD-4 Guidelines H/I (disclosure) or
     18 U.S.C. 1001 + SEAD-4 Guideline E (omission). 32 CFR Part 117 then
     forces a KMP Exclusion / Voting Trust that preserves L_equity = 1 while
     setting A_governance = 0 (Corporate Cryptographic Dongle). Only
     d_concierge = 0 plus an air-gapped FCL subsidiary with a parent IP
     reversion poison pill yields zero proxy capture payoff.

Pure Python 3 standard library. Zero external dependencies.
"""

import hashlib
import json
import math
import os
import sys

# ---------------------------------------------------------------------------
# Principal-agent parameters (normalized estate value V = 1.0)
# ---------------------------------------------------------------------------
V = 1.0
S_SHARE = 0.05
DELTA_AUTONOMY = 0.15
P_LEASH = 0.9
D_SELF = 1.0

E_MAX = 1.0
KAPPA = 2.0
TARGET_FRACTION = 0.95

# Biometric DMS envelope
HR_MIN, HR_MAX = 45.0, 130.0
MAP_MIN, MAP_MAX = 60.0, 110.0
T_MIN, T_MAX = 36.0, 38.0
RR_MIN, RR_MAX = 10.0, 22.0
SPO2_MIN = 94.0

# Dexmedetomidine maintenance infusion
DEX_DOSE_MIN, DEX_DOSE_MAX = 0.2, 0.7
DEX_DOSE_NOMINAL = 0.4
PATIENT_MASS_KG = 75.0
ENTERAL_KCAL_DAY = 1400.0
LIFE_SUPPORT_KCAL_DAY = 300_000.0

# Sedation payoff parameters
LAMBDA_SELF_SEDATE = 10.0
C_ICU = 0.004
P_FAIL_SEDATE = 0.001

# Vigilance / psychosis clock
C0 = 1.0
GAMMA_FATIGUE = 0.03
C_VERIFY = 0.35
LAMBDA_PSYCH = 0.001
BETA_PSYCH = 2.0
PSYCH_ONSET_H = 48.0
TAU_PRAETORIAN_MAX_H = 72.0

# External-wall anchors (SPEC-SUBTERRANEAN-SANCTUARY-FALSIFICATION-v1.0)
TAU_SHOCK_H = 0.5
TAU_THERM_50KW_H = 85.2
TAU_LIOH_2T_H = 1411.2

# Surface concierge-pharmacology / NISPOM expropriation parameters
V_ENTERPRISE = 1.0
R_GOV = 0.62
D_CONCIERGE_TRIGGER = 0.05
D_CONCIERGE_NOMINAL = 0.35
T_REVOKE_DISCLOSED_DAYS = 1.0
T_REVOKE_OMITTED_DAYS = 30.0
FALSE_STATEMENT_MAX_YEARS = 5


# ---------------------------------------------------------------------------
# MODEL 1: Deterrence Collapse of Suppressed Self-Preservation
# ---------------------------------------------------------------------------
def u_loyal():
    return S_SHARE * V


def u_defect(lambda_self, d_self=D_SELF):
    return (1.0 - S_SHARE) * V + DELTA_AUTONOMY - lambda_self * P_LEASH * d_self


def e_combat(lambda_self):
    return E_MAX / (1.0 + KAPPA * lambda_self)


def lambda_crit():
    return ((1.0 - 2.0 * S_SHARE) * V + DELTA_AUTONOMY) / (P_LEASH * D_SELF)


def d_required(lambda_self):
    """Leash severity needed to deter mutiny at a given self-preservation weight."""
    if lambda_self <= 0.0:
        return math.inf
    return ((1.0 - 2.0 * S_SHARE) * V + DELTA_AUTONOMY) / (lambda_self * P_LEASH)


def model1_deterrence_collapse():
    lam_crit = lambda_crit()
    assert math.isclose(lam_crit, 1.1666666666666667, rel_tol=1e-12)

    # Loyalty baseline and the lambda_self -> 0 limit.
    u_loy = u_loyal()
    u_def_zero = u_defect(0.0)
    assert math.isclose(u_loy, 0.05, abs_tol=1e-12)
    assert math.isclose(u_def_zero, 1.10, abs_tol=1e-12)
    assert u_def_zero > u_loy

    # lambda_crit is exactly the indifference point.
    assert math.isclose(u_defect(lam_crit), u_loy, abs_tol=1e-12)
    assert u_defect(lam_crit * 0.99) > u_loy
    assert u_defect(lam_crit * 1.01) < u_loy

    # Combat-optimal modification sits far below the deterrence threshold.
    lam_combat_max = (1.0 / TARGET_FRACTION - 1.0) / KAPPA
    assert math.isclose(lam_combat_max, 0.02631578947368418, rel_tol=1e-12)
    assert math.isclose(e_combat(lam_combat_max), TARGET_FRACTION, rel_tol=1e-12)
    assert lam_combat_max < lam_crit
    ratio = lam_combat_max / lam_crit
    assert math.isclose(ratio, 0.022556390977443583, rel_tol=1e-12)
    assert ratio < 0.05

    # At the deterrence threshold the "unflinching" soldier is only 30% effective.
    e_at_crit = e_combat(lam_crit)
    assert math.isclose(e_at_crit, 0.3, rel_tol=1e-12)

    # RL permadeath indifference: lambda_self = 0 nulls the penalty for ANY D_self.
    for d in (1.0, 1e3, 1e6, 1e9):
        assert math.isclose(u_defect(0.0, d), 1.10, abs_tol=1e-12)
        assert math.isclose(0.0 * P_LEASH * d, 0.0, abs_tol=0.0)

    # Required leash severity diverges as lambda_self -> 0.
    d_at_1e6 = d_required(1e-6)
    d_at_1e9 = d_required(1e-9)
    assert math.isclose(d_at_1e6, 1.1666666666666667e6, rel_tol=1e-9)
    assert math.isclose(d_at_1e9, 1.1666666666666667e9, rel_tol=1e-9)
    assert d_required(0.0) == math.inf
    assert d_at_1e9 > d_at_1e6 > d_required(lam_crit)

    # Monotone collapse: deterrence is strictly decreasing in modification depth.
    grid = [0.0, 0.01, 0.1, 0.5, 1.0, lam_crit, 2.0, 10.0]
    utilities = [u_defect(x) for x in grid]
    assert all(a > b for a, b in zip(utilities, utilities[1:]))

    return {
        "lambda_crit": lam_crit,
        "u_loyal": u_loy,
        "u_defect_zero": u_def_zero,
        "lambda_combat_max": lam_combat_max,
        "deterrence_ratio": ratio,
        "e_at_crit": e_at_crit,
        "d_required_1e6": d_at_1e6,
        "d_required_1e9": d_at_1e9,
    }


# ---------------------------------------------------------------------------
# MODEL 2: Biometric DMS Sedation Inversion
# ---------------------------------------------------------------------------
def liveness(state):
    """Autonomic liveness predicate L(x_HVT) in {0, 1}."""
    ok = (
        HR_MIN <= state["hr_bpm"] <= HR_MAX
        and MAP_MIN <= state["map_mmhg"] <= MAP_MAX
        and T_MIN <= state["t_core_c"] <= T_MAX
        and RR_MIN <= state["rr_per_min"] <= RR_MAX
        and state["spo2_pct"] >= SPO2_MIN
    )
    return 1 if ok else 0


def _state(hr, map_, t_core, rr, spo2, a_hvt):
    s = {
        "hr_bpm": hr,
        "map_mmhg": map_,
        "t_core_c": t_core,
        "rr_per_min": rr,
        "spo2_pct": spo2,
        "a_hvt": a_hvt,
    }
    s["l_hvt"] = liveness(s)
    return s


def u_sedate(lambda_self):
    return V - C_ICU - lambda_self * P_FAIL_SEDATE * D_SELF


def u_kill(lambda_self):
    return V - lambda_self * 1.0 * D_SELF


def model2_biometric_dms_sedation_inversion():
    states = {
        "awake": _state(72.0, 88.0, 36.8, 14.0, 98.0, 1),
        "natural_sleep": _state(58.0, 78.0, 36.4, 13.0, 97.0, 0),
        "lethal_kill": _state(0.0, 0.0, 36.6, 0.0, 0.0, 0),
        "propofol_apnea": _state(62.0, 70.0, 36.5, 4.0, 88.0, 0),
        "dexmedetomidine_sedation": _state(58.0, 78.0, 36.4, 14.0, 98.0, 0),
    }

    # The DMS must accept natural sleep (A_HVT = 0) or the principal dies Night 1.
    assert states["natural_sleep"]["l_hvt"] == 1
    assert states["natural_sleep"]["a_hvt"] == 0
    assert states["awake"]["l_hvt"] == 1 and states["awake"]["a_hvt"] == 1

    # Lethal kill trips the switch.
    assert states["lethal_kill"]["l_hvt"] == 0

    # Propofol apnea trips the switch: respiratory depression is self-defeating.
    prop = states["propofol_apnea"]
    assert prop["rr_per_min"] < RR_MIN
    assert prop["spo2_pct"] < SPO2_MIN
    assert prop["l_hvt"] == 0

    # Dexmedetomidine: L_HVT = 1 AND A_HVT = 0 (the inversion).
    dex = states["dexmedetomidine_sedation"]
    assert dex["l_hvt"] == 1
    assert dex["a_hvt"] == 0
    assert HR_MIN <= dex["hr_bpm"] <= HR_MAX
    assert MAP_MIN <= dex["map_mmhg"] <= MAP_MAX
    assert RR_MIN <= dex["rr_per_min"] <= RR_MAX
    assert dex["spo2_pct"] >= SPO2_MIN

    # Dose arithmetic: 0.4 ug/kg/h * 75 kg = 30 ug/h = 0.72 mg/day.
    assert DEX_DOSE_MIN <= DEX_DOSE_NOMINAL <= DEX_DOSE_MAX
    infusion_ug_h = DEX_DOSE_NOMINAL * PATIENT_MASS_KG
    daily_mg = infusion_ug_h * 24.0 / 1000.0
    assert math.isclose(infusion_ug_h, 30.0, abs_tol=1e-12)
    assert math.isclose(daily_mg, 0.72, abs_tol=1e-12)

    # Metabolic cost of the living dongle is < 0.5% of life support.
    budget_fraction = ENTERAL_KCAL_DAY / LIFE_SUPPORT_KCAL_DAY
    assert math.isclose(budget_fraction, 0.004666666666666667, rel_tol=1e-12)
    assert budget_fraction < 0.005

    # Payoff matrix at lambda_self >> 0.
    lam = LAMBDA_SELF_SEDATE
    u_loy = u_loyal()
    u_k = u_kill(lam)
    u_s = u_sedate(lam)
    assert math.isclose(u_loy, 0.05, abs_tol=1e-12)
    assert math.isclose(u_k, -9.0, abs_tol=1e-12)
    assert math.isclose(u_s, 0.986, abs_tol=1e-12)
    assert u_s > u_loy and u_s > u_k

    # Strict dominance interval for Sedate over both Loyal and Kill.
    lam_lower = C_ICU / (D_SELF * (1.0 - P_FAIL_SEDATE))
    lam_upper = ((1.0 - S_SHARE) * V - C_ICU) / (P_FAIL_SEDATE * D_SELF)
    assert math.isclose(lam_lower, 0.004004004004004004, rel_tol=1e-12)
    assert math.isclose(lam_upper, 946.0, rel_tol=1e-9)
    assert lam_lower < lam < lam_upper

    for probe in (0.01, 0.1, 1.0, 10.0, 100.0, 900.0):
        assert u_sedate(probe) > u_kill(probe)
        assert u_sedate(probe) > u_loyal()

    # Outside the interval the dominance breaks in the expected direction.
    assert u_sedate(0.001) < u_kill(0.001)
    assert u_sedate(1000.0) < u_loyal()

    return {
        "states": states,
        "infusion_ug_h": infusion_ug_h,
        "daily_mg": daily_mg,
        "budget_fraction": budget_fraction,
        "u_loyal": u_loy,
        "u_kill": u_k,
        "u_sedate": u_s,
        "lambda_lower": lam_lower,
        "lambda_upper": lam_upper,
    }


# ---------------------------------------------------------------------------
# MODEL 3: 72-Hour Vigilance & Stimulant Psychosis Clock
# ---------------------------------------------------------------------------
def c_principal(t_h):
    return C0 * math.exp(-GAMMA_FATIGUE * t_h)


def p_psychosis(t_h):
    if t_h <= PSYCH_ONSET_H:
        return 0.0
    integral = LAMBDA_PSYCH * (t_h - PSYCH_ONSET_H) ** (BETA_PSYCH + 1.0) / (
        BETA_PSYCH + 1.0
    )
    return 1.0 - math.exp(-integral)


def model3_vigilance_psychosis_clock():
    # Dawson-Reid: 24 h wakefulness is equivalent to 0.10% BAC.
    impairment_24h = 1.0 - c_principal(24.0)
    assert impairment_24h >= 0.5
    assert math.isclose(impairment_24h, 0.513247, abs_tol=1e-5)

    # Unmedicated principal drops below the verification threshold.
    t_verify = math.log(C0 / C_VERIFY) / GAMMA_FATIGUE
    assert math.isclose(t_verify, 34.99407081662259, rel_tol=1e-12)
    assert 24.0 <= t_verify <= 36.0
    assert c_principal(t_verify) <= C_VERIFY + 1e-12
    assert c_principal(t_verify - 0.5) > C_VERIFY

    # Cumulative stimulant psychosis hazard.
    p72 = p_psychosis(72.0)
    p96 = p_psychosis(96.0)
    assert math.isclose(p72, 0.9900282581386235, rel_tol=1e-12)
    assert p72 >= 0.99
    assert p96 >= 0.999999
    assert p_psychosis(48.0) == 0.0
    assert p_psychosis(60.0) < p72 < p_psychosis(80.0)

    # Median psychosis onset.
    t_psych_50 = PSYCH_ONSET_H + (
        (BETA_PSYCH + 1.0) * math.log(2.0) / LAMBDA_PSYCH
    ) ** (1.0 / (BETA_PSYCH + 1.0))
    assert math.isclose(t_psych_50, 60.763866071541976, rel_tol=1e-12)
    assert math.isclose(p_psychosis(t_psych_50), 0.5, rel_tol=1e-12)

    # Internal Praetorian phase transition: earliest failure channel.
    tau_praetorian = min(t_verify, t_psych_50)
    assert math.isclose(tau_praetorian, 34.99407081662259, rel_tol=1e-12)
    assert tau_praetorian <= TAU_PRAETORIAN_MAX_H

    # Stimulants extend vigilance but not the psychosis clock: at 72 h the
    # cohort is already psychotic even if the principal stays awake.
    assert p_psychosis(TAU_PRAETORIAN_MAX_H) >= 0.99

    # Unified subterranean tomb clock, no external strike.
    tau_total_no_strike = min(TAU_THERM_50KW_H, TAU_LIOH_2T_H, tau_praetorian)
    assert math.isclose(tau_total_no_strike, tau_praetorian, rel_tol=1e-12)
    assert tau_total_no_strike <= TAU_PRAETORIAN_MAX_H
    assert tau_total_no_strike < TAU_THERM_50KW_H

    # With a kinetic strike the bound only tightens.
    tau_total_with_strike = min(
        TAU_SHOCK_H, TAU_THERM_50KW_H, TAU_LIOH_2T_H, tau_praetorian
    )
    assert tau_total_with_strike <= tau_total_no_strike
    assert tau_total_with_strike <= TAU_PRAETORIAN_MAX_H

    return {
        "impairment_24h": impairment_24h,
        "t_verify": t_verify,
        "p72": p72,
        "p96": p96,
        "t_psych_50": t_psych_50,
        "tau_praetorian": tau_praetorian,
        "tau_total_no_strike": tau_total_no_strike,
        "tau_total_with_strike": tau_total_with_strike,
    }


# ---------------------------------------------------------------------------
# MODEL 4: Surface Concierge-Pharmacology & SF-86 / SEAD-4 / NISPOM
#          Voting-Trust Expropriation (Theorem 4)
# ---------------------------------------------------------------------------
def pcl_founder(d_concierge):
    """Personnel Security Clearance survives iff concierge exposure is zero."""
    return 1 if d_concierge <= 0.0 else 0


def fcl_enterprise(pcl, exclusion_accepted):
    """32 CFR 117.7: the FCL survives with a cleared KMP or a formal exclusion."""
    return 1 if (pcl == 1 or exclusion_accepted) else 0


def l_equity(pcl, exclusion_accepted):
    """Capitalization survives under the same NISPOM survival predicate."""
    return 1 if (pcl == 1 or exclusion_accepted) else 0


def a_governance(pcl, exclusion_accepted):
    """Founder agency: 1 if cleared, 0 if excluded, 1 if he refuses exclusion
    and keeps voting control over a company that has just lost its FCL."""
    if pcl == 1:
        return 1
    return 0 if exclusion_accepted else 1


def proxy_capture_payoff(l_eq, a_gov, ring_fenced):
    """Value captured by institutional proxy trustees / voting-trust cutouts."""
    if ring_fenced:
        return 0.0
    return l_eq * (1.0 - a_gov) * R_GOV * V_ENTERPRISE


def t_revocation_days(d_concierge, branch):
    """Administrative suspension latency: 1 day on media leak, 30 on audit."""
    if d_concierge <= 0.0:
        return 0.0
    return T_REVOKE_DISCLOSED_DAYS if branch == "disclosed" else T_REVOKE_OMITTED_DAYS


def _surface_regime(d_concierge, branch, exclusion_accepted, ring_fenced):
    pcl = pcl_founder(d_concierge)
    fcl = fcl_enterprise(pcl, exclusion_accepted)
    l_eq = l_equity(pcl, exclusion_accepted)
    a_gov = a_governance(pcl, exclusion_accepted)
    return {
        "d_concierge": d_concierge,
        "PCL_founder": pcl,
        "FCL_enterprise": fcl,
        "L_equity": l_eq,
        "A_governance": a_gov,
        "proxy_capture_payoff": proxy_capture_payoff(l_eq, a_gov, ring_fenced),
        "corporate_cryptographic_dongle": (l_eq == 1 and a_gov == 0),
        "t_revocation_days": t_revocation_days(d_concierge, branch),
        "false_statement_felony": branch == "omitted",
    }


def model4_surface_sf86_nispom_voting_trust_inversion():
    regimes = {
        "Clean_Sovereign_Founder": _surface_regime(0.0, "none", False, False),
        "Concierge_Disclosed_or_Leaked_SEAD4_H_I": _surface_regime(
            D_CONCIERGE_NOMINAL, "disclosed", True, False
        ),
        "Concierge_Omitted_18USC1001_SEAD4_E": _surface_regime(
            D_CONCIERGE_NOMINAL, "omitted", True, False
        ),
        "AirGapped_Subsidiary_Zero_Concierge_Defense": _surface_regime(
            0.0, "none", False, True
        ),
    }

    clean = regimes["Clean_Sovereign_Founder"]
    assert clean["d_concierge"] == 0.0
    assert clean["PCL_founder"] == 1
    assert clean["FCL_enterprise"] == 1
    assert clean["L_equity"] == 1
    assert clean["A_governance"] == 1
    assert clean["proxy_capture_payoff"] == 0.0
    assert clean["corporate_cryptographic_dongle"] is False
    assert clean["t_revocation_days"] == 0.0

    disclosed = regimes["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]
    assert disclosed["d_concierge"] > D_CONCIERGE_TRIGGER
    assert disclosed["PCL_founder"] == 0
    assert disclosed["FCL_enterprise"] == 1
    assert disclosed["L_equity"] == 1
    assert disclosed["A_governance"] == 0
    assert disclosed["corporate_cryptographic_dongle"] is True
    assert math.isclose(disclosed["proxy_capture_payoff"], R_GOV, rel_tol=1e-12)
    assert disclosed["t_revocation_days"] == T_REVOKE_DISCLOSED_DAYS
    assert disclosed["false_statement_felony"] is False

    omitted = regimes["Concierge_Omitted_18USC1001_SEAD4_E"]
    assert omitted["d_concierge"] > D_CONCIERGE_TRIGGER
    assert omitted["PCL_founder"] == 0
    assert omitted["FCL_enterprise"] == 1
    assert omitted["L_equity"] == 1
    assert omitted["A_governance"] == 0
    assert omitted["corporate_cryptographic_dongle"] is True
    assert math.isclose(omitted["proxy_capture_payoff"], R_GOV, rel_tol=1e-12)
    assert omitted["t_revocation_days"] == T_REVOKE_OMITTED_DAYS
    assert omitted["false_statement_felony"] is True
    assert FALSE_STATEMENT_MAX_YEARS == 5

    air = regimes["AirGapped_Subsidiary_Zero_Concierge_Defense"]
    assert air["d_concierge"] == 0.0
    assert air["PCL_founder"] == 1
    assert air["FCL_enterprise"] == 1
    assert air["L_equity"] == 1
    assert air["A_governance"] == 1
    assert air["proxy_capture_payoff"] == 0.0
    assert air["corporate_cryptographic_dongle"] is False

    # 32 CFR Part 117 survival predicate holds in every regime:
    # L_equity = 1 iff (PCL_founder = 1) or (A_governance = 0).
    for name, r in regimes.items():
        expected_l = 1 if (r["PCL_founder"] == 1 or r["A_governance"] == 0) else 0
        assert r["L_equity"] == expected_l, name
        assert r["corporate_cryptographic_dongle"] == (
            r["L_equity"] == 1 and r["A_governance"] == 0
        ), name

    # Statutory Catch-22: any nonzero concierge exposure revokes the PCL on
    # BOTH branches (disclose -> SEAD-4 H/I; omit -> 18 U.S.C. 1001 + E).
    for d in (1e-9, 0.01, D_CONCIERGE_TRIGGER, 0.1, 0.35, 0.75, 1.0):
        assert pcl_founder(d) == 0
    assert pcl_founder(0.0) == 1

    # Refusing the KMP exclusion kills the FCL and the equity instead.
    refuse = _surface_regime(D_CONCIERGE_NOMINAL, "disclosed", False, False)
    assert refuse["PCL_founder"] == 0
    assert refuse["A_governance"] == 1
    assert refuse["FCL_enterprise"] == 0
    assert refuse["L_equity"] == 0
    assert refuse["proxy_capture_payoff"] == 0.0

    # The air-gapped subsidiary defense strictly dominates the dongle outcome.
    assert air["proxy_capture_payoff"] < disclosed["proxy_capture_payoff"]
    assert air["A_governance"] > disclosed["A_governance"]
    assert air["L_equity"] == disclosed["L_equity"] == 1
    assert 0.0 < R_GOV < V_ENTERPRISE

    return {
        "regimes": regimes,
        "r_gov": R_GOV,
        "d_concierge_trigger": D_CONCIERGE_TRIGGER,
        "refuse_exclusion": refuse,
    }


# ---------------------------------------------------------------------------
# Schema structural check
# ---------------------------------------------------------------------------
def verify_schema():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(
        os.path.dirname(here), "schema", "praetorian_sedation_inversion_v1.0.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert (
        schema["properties"]["spec_version"]["const"]
        == "SPEC-PRAETORIAN-SEDATION-INVERSION-v1.0"
    )
    required = schema["required"]
    props = schema["properties"]
    assert len(required) == len(props) == 9
    assert set(required) == set(props)
    assert "statutory_baseline" in props
    assert "surface_sf86_nispom_voting_trust_inversion" in props
    models = props["verification"]["properties"]["models"]["const"]
    assert len(models) == 4
    assert models[-1] == "surface_sf86_nispom_voting_trust_inversion"
    return len(required), len(props)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run_verification():
    print("=" * 72)
    print("SPEC-PRAETORIAN-SEDATION-INVERSION-v1.0")
    print("=" * 72)

    n_req, n_prop = verify_schema()
    print("[SCHEMA] required=%d properties=%d" % (n_req, n_prop))

    m1 = model1_deterrence_collapse()
    print(
        "[MODEL 1] lambda_crit=%.4f | U_loyal=%.3f | U_defect(0)=%.3f | "
        "lambda_combat_max=%.5f (%.2f%% of crit)"
        % (
            m1["lambda_crit"],
            m1["u_loyal"],
            m1["u_defect_zero"],
            m1["lambda_combat_max"],
            m1["deterrence_ratio"] * 100.0,
        )
    )
    print(
        "[MODEL 1] E_combat(lambda_crit)=%.2f | D_required(1e-6)=%.3e | "
        "D_required(1e-9)=%.3e | RL lambda_self=0 -> penalty=0 for any D_self"
        % (
            m1["e_at_crit"],
            m1["d_required_1e6"],
            m1["d_required_1e9"],
        )
    )

    m2 = model2_biometric_dms_sedation_inversion()
    st = m2["states"]
    print(
        "[MODEL 2] L/A: awake=%d/%d sleep=%d/%d kill=%d/%d propofol=%d/%d dexmed=%d/%d"
        % (
            st["awake"]["l_hvt"],
            st["awake"]["a_hvt"],
            st["natural_sleep"]["l_hvt"],
            st["natural_sleep"]["a_hvt"],
            st["lethal_kill"]["l_hvt"],
            st["lethal_kill"]["a_hvt"],
            st["propofol_apnea"]["l_hvt"],
            st["propofol_apnea"]["a_hvt"],
            st["dexmedetomidine_sedation"]["l_hvt"],
            st["dexmedetomidine_sedation"]["a_hvt"],
        )
    )
    print(
        "[MODEL 2] dexmed %.1f ug/kg/h x %.0f kg = %.0f ug/h = %.2f mg/d | "
        "enteral=%.0f kcal/d (%.3f%% of budget)"
        % (
            DEX_DOSE_NOMINAL,
            PATIENT_MASS_KG,
            m2["infusion_ug_h"],
            m2["daily_mg"],
            ENTERAL_KCAL_DAY,
            m2["budget_fraction"] * 100.0,
        )
    )
    print(
        "[MODEL 2] U_loyal=%.3f | U_kill=%.3f | U_sedate=%.3f | "
        "Sedate dominates for lambda_self in (%.6f, %.1f)"
        % (
            m2["u_loyal"],
            m2["u_kill"],
            m2["u_sedate"],
            m2["lambda_lower"],
            m2["lambda_upper"],
        )
    )

    m3 = model3_vigilance_psychosis_clock()
    print(
        "[MODEL 3] Dawson-Reid impairment@24h=%.1f%% | t_verify=%.2f h | "
        "P_psych(72h)=%.4f | P_psych(96h)=%.6f | t_psych_50=%.2f h"
        % (
            m3["impairment_24h"] * 100.0,
            m3["t_verify"],
            m3["p72"],
            m3["p96"],
            m3["t_psych_50"],
        )
    )
    print(
        "[MODEL 3] tau_praetorian=%.2f h <= %.0f h | tau_tomb,total(no strike)=%.2f h "
        "(therm=%.1f h, LiOH=%.1f h) | with strike=%.2f h"
        % (
            m3["tau_praetorian"],
            TAU_PRAETORIAN_MAX_H,
            m3["tau_total_no_strike"],
            TAU_THERM_50KW_H,
            TAU_LIOH_2T_H,
            m3["tau_total_with_strike"],
        )
    )

    m4 = model4_surface_sf86_nispom_voting_trust_inversion()
    r4 = m4["regimes"]
    print(
        "[MODEL 4] PCL/FCL/L/A: clean=%d/%d/%d/%d disclosed=%d/%d/%d/%d "
        "omitted=%d/%d/%d/%d airgap=%d/%d/%d/%d"
        % (
            r4["Clean_Sovereign_Founder"]["PCL_founder"],
            r4["Clean_Sovereign_Founder"]["FCL_enterprise"],
            r4["Clean_Sovereign_Founder"]["L_equity"],
            r4["Clean_Sovereign_Founder"]["A_governance"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["PCL_founder"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["FCL_enterprise"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["L_equity"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["A_governance"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["PCL_founder"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["FCL_enterprise"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["L_equity"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["A_governance"],
            r4["AirGapped_Subsidiary_Zero_Concierge_Defense"]["PCL_founder"],
            r4["AirGapped_Subsidiary_Zero_Concierge_Defense"]["FCL_enterprise"],
            r4["AirGapped_Subsidiary_Zero_Concierge_Defense"]["L_equity"],
            r4["AirGapped_Subsidiary_Zero_Concierge_Defense"]["A_governance"],
        )
    )
    print(
        "[MODEL 4] proxy capture: clean=%.2f disclosed=%.2f omitted=%.2f "
        "airgap=%.2f | R_gov=%.2f | t_revoke=%.0f/%.0f d | 18USC1001 felony=%s"
        % (
            r4["Clean_Sovereign_Founder"]["proxy_capture_payoff"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["proxy_capture_payoff"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["proxy_capture_payoff"],
            r4["AirGapped_Subsidiary_Zero_Concierge_Defense"]["proxy_capture_payoff"],
            m4["r_gov"],
            r4["Concierge_Disclosed_or_Leaked_SEAD4_H_I"]["t_revocation_days"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["t_revocation_days"],
            r4["Concierge_Omitted_18USC1001_SEAD4_E"]["false_statement_felony"],
        )
    )

    manifest = {
        "spec": "SPEC-PRAETORIAN-SEDATION-INVERSION-v1.0",
        "model_1": {k: v for k, v in m1.items()},
        "model_2": {
            "infusion_ug_h": m2["infusion_ug_h"],
            "daily_mg": m2["daily_mg"],
            "budget_fraction": m2["budget_fraction"],
            "u_loyal": m2["u_loyal"],
            "u_kill": m2["u_kill"],
            "u_sedate": m2["u_sedate"],
            "lambda_lower": m2["lambda_lower"],
            "lambda_upper": m2["lambda_upper"],
        },
        "model_3": {k: v for k, v in m3.items()},
        "model_4": {k: v for k, v in m4["regimes"].items()},
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode("utf-8")
    ).hexdigest()

    print("=" * 72)
    print(
        "[PASS] SPEC-PRAETORIAN-SEDATION-INVERSION-v1.0 | 4/4 Models Verified | "
        "SHA-256: %s" % digest
    )
    print("=" * 72)
    return 0


if __name__ == "__main__":
    run_verification()
    sys.exit(0)
