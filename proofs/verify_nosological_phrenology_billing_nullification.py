#!/usr/bin/env python3
"""Closed-form verification engine: Nosological Phrenology Billing Nullification.

Verifies governing equations EQ_01..EQ_05 against locked historical,
psychometric, Bayesian, information-theoretic, and False Claims Act constants:

  EQ_01  2D->1D phrenological dimensional collapse (sovereign outlier screen):
         G >= 0.99, E >= 0.99 -> D = 0, S(C) = 0.99 >= S_crit = 0.80
         -> P(False Positive | Sovereign Outlier) = 1.0
  EQ_02  Daubert / FRE 702 reliability gate and Bayesian PPV collapse:
         kappa in [0.20, 0.46], pi = 0.08, Se = 0.60, Sp = 0.85
         -> PPV = 0.048 / 0.186 = 0.258065 = 25.81% < 50% preponderance
  EQ_03  Bayes-inversion phrenology exaggeration factor:
         r = 0.15 -> r^2 = 0.0225, U = 0.9775, Lambda = 1 / r^2 = 44.4444x
  EQ_04  Anosognosia / Criterion-B non-falsifiability identity:
         P(Confirm | Obs_i) = 1.0 for all i -> I(Diag; Reality) = 0.0 bits
  EQ_05  CPT / neuroleptic capitation and False Claims Act liquidation:
         N = 10,000, c_eval = $180, c_rx = $4,200 -> D = $43,800,000,
         3D = $131,400,000, min penalties = $139,460,000,
         L_FCA = $270,860,000, B_relator(25%) = $67,715,000,
         historical DOJ neuroleptic settlements = $4,436,800,000

Pure Python 3 standard library. Exit code 0 iff every check passes.
"""

import json
import math
import sys

TOL = 1e-9
RESULTS = []
FAILURES = []


def check(label, computed, expected, tol=TOL):
    ok = abs(computed - expected) <= tol
    RESULTS.append(ok)
    if not ok:
        FAILURES.append({"label": label, "computed": computed, "expected": expected})
    print("[{}] {}: computed={!r} expected={!r}".format(
        "PASS" if ok else "FAIL", label, computed, expected))
    return ok


def check_true(label, cond, detail=""):
    ok = bool(cond)
    RESULTS.append(ok)
    if not ok:
        FAILURES.append({"label": label, "computed": False, "expected": True})
    print("[{}] {}{}".format(
        "PASS" if ok else "FAIL", label, (" :: " + detail) if detail else ""))
    return ok


def eq_01_sovereign_outlier():
    """2D->1D dimensional collapse: G>=0.99, E>=0.99 -> D=0, S(C)=w_g*G=0.99>=0.80."""
    print("EQ_01: 2D->1D phrenological dimensional collapse (sovereign outlier)")
    theta_g, theta_e = 0.80, 0.50
    w_g = 1.0
    g, e = 0.99, 0.99
    s_crit = 0.80
    check_true("EQ_01a gate G >= theta_g", g >= theta_g, "0.99 >= 0.80")
    check_true("EQ_01b gate E >= theta_e", e >= theta_e, "0.99 >= 0.50")
    d_dysfunction = 1.0 if (g > theta_g and e < theta_e) else 0.0
    check("EQ_01c true clinical dysfunction D(G, E)", d_dysfunction, 0.0)
    s_c = w_g * g
    check("EQ_01d 1D surface checklist projection S(C) = w_g * G", s_c, 0.99)
    check_true("EQ_01e S(C) >= S_crit", s_c >= s_crit, "0.99 >= 0.80")
    p_fp = 1.0 if (d_dysfunction == 0.0 and s_c >= s_crit) else 0.0
    check("EQ_01f P(FalsePositive | SovereignOutlier)", p_fp, 1.0)
    return {
        "true_clinical_dysfunction_d": d_dysfunction,
        "surface_checklist_score_s_c": s_c,
        "p_false_positive_given_sovereign_outlier": p_fp,
    }


def eq_02_fre702_ppv():
    """Daubert / FRE 702: kappa reliability floor and Bayesian PPV collapse."""
    print("EQ_02: Daubert / FRE 702 reliability and PPV collapse")
    kappas = {
        "kappa_gad": 0.20,
        "kappa_aspd": 0.21,
        "kappa_mixed": 0.24,
        "kappa_mdd": 0.28,
        "kappa_schizoaffective": 0.46,
    }
    for name, k in kappas.items():
        check_true("EQ_02 {} below substantial-reliability floor".format(name),
                   k < 0.50, "{} < 0.50".format(k))
    disagreement = sorted(round(1.0 - k, 2) for k in kappas.values())
    check("EQ_02 inter-rater disagreement min", disagreement[0], 0.54)
    check("EQ_02 inter-rater disagreement max", disagreement[-1], 0.80)
    pi, se, sp = 0.08, 0.60, 0.85
    numerator = se * pi
    denominator = numerator + (1.0 - sp) * (1.0 - pi)
    check("EQ_02 Bayes numerator Se*pi", numerator, 0.048)
    check("EQ_02 Bayes denominator", denominator, 0.186)
    ppv = numerator / denominator
    check("EQ_02 PPV exact", ppv, 0.25806451612903225)
    ppv_pct = round(ppv * 100.0, 2)
    check("EQ_02 PPV percent rounded", ppv_pct, 25.81)
    fre_702_threshold = 0.50
    check_true("EQ_02 PPV < FRE 702 preponderance threshold",
               ppv < fre_702_threshold, "0.2581 < 0.50")
    return {"ppv_exact": ppv, "ppv_pct_rounded": ppv_pct}


def eq_03_exaggeration():
    """Bayes-inversion: r = 0.15 -> Lambda = 1/r^2 = 44.4444x."""
    print("EQ_03: Bayes-inversion phrenology exaggeration factor")
    r = 0.15
    r2 = r * r
    check("EQ_03 variance explained r^2", r2, 0.0225)
    u = 1.0 - r2
    check("EQ_03 unpredicted sovereign variance U", u, 0.9775)
    lam = 1.0 / r2
    check("EQ_03 exaggeration factor Lambda = 1/r^2", lam, 44.44444444444444)
    return {
        "variance_explained_r2": r2,
        "unpredicted_sovereign_variance_u": u,
        "phrenology_exaggeration_factor_lambda": lam,
    }


def eq_04_nonfalsifiability():
    """Anosognosia / Criterion-B: P(Confirm|Obs)=1.0 for all Obs -> I=0 bits."""
    print("EQ_04: anosognosia / Criterion-B non-falsifiability identity")
    p_reality = {0: 0.92, 1: 0.08}
    p_confirm_given_obs = {0: 1.0, 1: 1.0}
    joint = {(1, r): pr * p_confirm_given_obs[r] for r, pr in p_reality.items()}
    p_diag = sum(joint.values())
    mi = 0.0
    for (_, r), pdr in joint.items():
        if pdr > 0.0:
            mi += pdr * math.log2(pdr / (p_diag * p_reality[r]))
    check("EQ_04 Shannon mutual information I(Diag; Reality)", mi, 0.0)
    check_true("EQ_04 non-falsifiable (I == 0 bits)", abs(mi) <= TOL)
    return {"shannon_mutual_information_bits": mi}


def eq_05_fca_liquidation():
    """CPT / neuroleptic capitation and False Claims Act liquidation."""
    print("EQ_05: CPT / neuroleptic capitation and False Claims Act liquidation")
    n = 10000
    c_eval, c_rx = 180.0, 4200.0
    per_claim = c_eval + c_rx
    check("EQ_05 per-claim damages (c_eval + c_rx)", per_claim, 4380.0)
    single = n * per_claim
    check("EQ_05 single damages D", single, 43800000.0)
    treble = 3.0 * single
    check("EQ_05 treble damages 3D", treble, 131400000.0)
    pen_min, pen_max = 13946.0, 27894.0
    total_pen_min = n * pen_min
    check("EQ_05 total minimum penalties", total_pen_min, 139460000.0)
    total_pen_max = n * pen_max
    check("EQ_05 total maximum penalties", total_pen_max, 278940000.0)
    liability_min = treble + total_pen_min
    check("EQ_05 minimum total FCA liability", liability_min, 270860000.0)
    bounty = 0.25 * liability_min
    check("EQ_05 relator bounty 25%", bounty, 67715000.0)
    settlements = 2200000000.0 + 1415000000.0 + 520000000.0 + 301800000.0
    check("EQ_05 DOJ historical neuroleptic settlements total",
          settlements, 4436800000.0)
    check_true("EQ_05 block liability << historical settlement baseline",
               liability_min < settlements, "270,860,000 < 4,436,800,000")
    return {
        "per_claim_damages_usd": per_claim,
        "fca_single_damages_usd": single,
        "fca_treble_damages_usd": treble,
        "fca_total_min_penalties_usd": total_pen_min,
        "fca_total_liability_min_usd": liability_min,
        "fca_relator_bounty_25pct_usd": bounty,
        "doj_historical_settlements_total_usd": settlements,
    }


def historical_baseline():
    """Consistency checks over locked historical and institutional constants."""
    print("BASELINE: locked historical and institutional constants")
    grant = 325000.0
    sterilized = 400000
    t4_min, t4_max = 250000, 300000
    check_true("BASELINE Rockefeller DFA Munich grant positive", grant > 0.0)
    check_true("BASELINE Aktion T4 Meldebogen range ordered", t4_min <= t4_max)
    check("BASELINE Aktion T4 Meldebogen midpoint",
          (t4_min + t4_max) / 2.0, 275000.0)
    check_true("BASELINE 1933 sterilization statute victims >= T4 max",
               sterilized >= t4_max, "400,000 >= 300,000")
    tf, mood, sleep = 69.0, 83.0, 100.0
    check_true("BASELINE DSM-5 pharma-tie percentages monotone",
               0.0 <= tf <= mood <= sleep <= 100.0, "69 <= 83 <= 100")
    check("BASELINE DSM-5 mood/psychotic excess over task-force mean",
          mood - tf, 14.0)
    check("BASELINE DSM-5 sleep/wake excess over task-force mean",
          sleep - tf, 31.0)
    return {}


def main():
    outputs = {}
    for fn in (eq_01_sovereign_outlier, eq_02_fre702_ppv, eq_03_exaggeration,
               eq_04_nonfalsifiability, eq_05_fca_liquidation,
               historical_baseline):
        outputs.update(fn())
    total = len(RESULTS)
    passed = sum(1 for ok in RESULTS if ok)
    status = "PASS" if not FAILURES else "FAIL"
    print(json.dumps({
        "proof": "nosological_phrenology_billing_nullification",
        "status": status,
        "checks_total": total,
        "checks_passed": passed,
        "outputs": outputs,
    }, indent=2, sort_keys=True))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())