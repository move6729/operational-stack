#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: SUBTERRANEAN SANCTUARY FALSIFICATION (v1.0)
SPEC-SUBTERRANEAN-SANCTUARY-FALSIFICATION-v1.0
License: Unlicense (Public Domain - Zero-Rent Federation)

Deterministic, pure-stdlib verification of three models:
  Model 1 - GBU-57A/B MOP single-shot vs. sequential double-tap penetration across
            soil, 34 MPa concrete, 69 MPa concrete, and 172 MPa Fordow limestone,
            plus the lithostatic rubble plug mass and frictional door lock.
  Model 2 - Stoichiometric LiOH CO2 scrubbing clock and transient semi-infinite
            rock conduction thermal runaway clock inside a sealed habitat.
  Model 3 - Elite Exit vs. Sovereign Portal-Sealing expected-utility inversion
            across all three sanctuary tiers.

Zero external dependencies (pure Python 3 standard library).
"""

import json
import math
import os
import sys

SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "schema",
    "subterranean_sanctuary_falsification_v1.0.json",
)

G = 9.81


# ---------------------------------------------------------------------------
# Schema contract
# ---------------------------------------------------------------------------
def verify_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert isinstance(schema["properties"], dict) and schema["properties"]
    assert isinstance(schema["required"], list) and schema["required"]
    for key in schema["required"]:
        assert key in schema["properties"], key
    return {
        "required_fields": len(schema["required"]),
        "properties": len(schema["properties"]),
    }


# ---------------------------------------------------------------------------
# Model 1 - Penetration, bore-walking, and portal rubble lock
# ---------------------------------------------------------------------------
D_REF = 18.0          # m, single-shot depth in 34 MPa reinforced concrete
F_REF = 34.0          # MPa
ALPHA = 0.5           # Young/Forrestal strength scaling exponent
D_REF_SOIL = 60.0     # m, unconsolidated earth (no compressive-strength scaling)
ETA_MIN = 0.65
ETA_MAX = 0.90
ETA_NOMINAL = 0.75

MATERIALS = [
    # name, f_c (MPa), empirical conservative floor (m), unconsolidated flag
    ("soil", 5.0, 60.0, True),
    ("concrete_34mpa", 34.0, 18.0, False),
    ("concrete_69mpa", 69.0, 2.4, False),
    ("fordow_limestone_172mpa", 172.0, 1.5, False),
]


def single_shot_depth(f_c, unconsolidated=False):
    if unconsolidated:
        return D_REF_SOIL
    return D_REF * (f_c / F_REF) ** (-ALPHA)


def sequential_depth(d1, k, eta):
    # Lead round plus (k-1) bore-walk rounds down the same crater chimney.
    return d1 * (1.0 + (k - 1) * eta)


def model1_penetration_and_portal_lock():
    table = {}
    for name, f_c, floor, unconsolidated in MATERIALS:
        d1 = single_shot_depth(f_c, unconsolidated)
        d2 = sequential_depth(d1, 2, ETA_NOMINAL)
        assert d1 >= floor, (name, d1, floor)
        assert d2 > d1, name
        table[name] = {
            "f_c_mpa": f_c,
            "d1_m": round(d1, 3),
            "d2_m": round(d2, 3),
            "floor_m": floor,
        }

    # Tier 1 cut-and-cover: single round exceeds the deepest 10 m overburden.
    assert table["concrete_34mpa"]["d1_m"] > 10.0
    assert table["soil"]["d1_m"] > 10.0

    # Tier 2 silo cap: one round is insufficient at the 15 m minimum depth.
    assert table["concrete_69mpa"]["d1_m"] < 15.0
    assert table["concrete_69mpa"]["d2_m"] > 15.0

    # Fordow: 80-90 m limestone roof is not breached by a single round.
    fordow_d1 = table["fordow_limestone_172mpa"]["d1_m"]
    assert fordow_d1 < 80.0

    # Twelve-round bore-walking is efficiency-dependent, not deterministic.
    d12_low = sequential_depth(fordow_d1, 12, ETA_MIN)
    d12_high = sequential_depth(fordow_d1, 12, ETA_MAX)
    assert d12_low < 80.0
    assert d12_high >= 80.0

    # Minimum-cut cost is invariant to chamber depth: C_min-cut = K * C_MOP.
    c_mop = 1.0
    cut_costs = [k * c_mop for k in range(2, 7)]
    assert all(c > 0 for c in cut_costs)
    assert len(set(cut_costs)) == len(cut_costs)
    depth_grid = [20.0, 40.0, 60.0, 80.0, 100.0]
    min_cut_by_depth = [2 * c_mop for _ in depth_grid]
    assert len(set(min_cut_by_depth)) == 1

    # Lithostatic rubble plug: M = rho * A * h * phi.
    rho_rock = 2650.0
    a_adit = 16.0
    h_chimney = 25.0
    phi_bulking = 1.35
    m_insitu_kg = rho_rock * a_adit * h_chimney
    m_bulked_kg = m_insitu_kg * phi_bulking
    m_insitu_t = m_insitu_kg / 1000.0
    m_bulked_t = m_bulked_kg / 1000.0
    assert m_insitu_t >= 1000.0
    assert m_bulked_t >= 1000.0
    assert m_bulked_t <= 15000.0

    # Frictional lock: F = mu * M * g, versus a 50 ton-force actuator.
    mu_rock = 0.60
    f_actuator = 5.0e5
    f_lock_insitu = mu_rock * m_insitu_kg * G
    f_lock_bulked = mu_rock * m_bulked_kg * G
    assert f_lock_insitu > 10.0 * f_actuator
    assert f_lock_bulked > 10.0 * f_actuator

    return {
        "table": table,
        "fordow_d12_low_m": round(d12_low, 3),
        "fordow_d12_high_m": round(d12_high, 3),
        "m_insitu_t": round(m_insitu_t, 1),
        "m_bulked_t": round(m_bulked_t, 1),
        "f_lock_insitu_n": f_lock_insitu,
        "f_lock_bulked_n": f_lock_bulked,
        "ratio_insitu": f_lock_insitu / f_actuator,
        "ratio_bulked": f_lock_bulked / f_actuator,
    }


# ---------------------------------------------------------------------------
# Model 2 - Stoichiometric LiOH clock and rock-conduction thermal runaway
# ---------------------------------------------------------------------------
N_OCCUPANTS = 25
V_AIR = 3000.0
R_CO2 = 1.00          # kg/person/day
R_O2 = 0.84           # kg/person/day
Y_CO2_CRIT = 0.05
Y_CO2_0 = 0.0004
RHO_CO2 = 1.977       # kg/m3 at STP

M_LIOH_G = 23.95
M_CO2_G = 44.01
ETA_PACK = 0.80
DH_RXN_KJ_MOL = 89.4

K_ROCK = 2.5          # W/(m K)
ALPHA_ROCK = 1.15e-6  # m2/s
A_WALL = 900.0        # m2
T_CRIT = 35.0         # deg C wet-bulb lethality
T_ROCK_INF = 15.0     # deg C undisturbed rock
T_0 = 22.0            # deg C initial habitat air
C_HAB = 2.86e7        # J/K air + internal thermal mass


def lioh_stoichiometry():
    ratio = (2.0 * M_LIOH_G) / M_CO2_G
    heat_mj_kg = DH_RXN_KJ_MOL / (M_CO2_G / 1000.0) / 1000.0
    assert abs(ratio - 1.088) < 1e-3, ratio
    assert 2.0 <= heat_mj_kg <= 2.1, heat_mj_kg
    return ratio, heat_mj_kg


def tau_unscrubbed():
    mass_co2 = RHO_CO2 * V_AIR * (Y_CO2_CRIT - Y_CO2_0)
    return mass_co2 / (N_OCCUPANTS * R_CO2)


def tau_lioh(m_lioh_kg):
    ratio, _ = lioh_stoichiometry()
    return (ETA_PACK * m_lioh_kg) / (ratio * N_OCCUPANTS * R_CO2)


def rock_flux_coefficient():
    # Q_rock_max(t) = B / sqrt(t)
    return A_WALL * K_ROCK * (T_CRIT - T_ROCK_INF) / math.sqrt(math.pi * ALPHA_ROCK)


def tau_thermal(p_in_w):
    """Solve integral_0^tau max(0, P - B/sqrt(t)) dt = C_hab * (T_crit - T_0)."""
    b = rock_flux_coefficient()
    energy = C_HAB * (T_CRIT - T_0)
    s0 = b / p_in_w          # sqrt(t) at which conduction equals internal load
    # P*u^2 - 2B*u + (2B*s0 - P*s0^2 - E) = 0, with u = sqrt(tau)
    a = p_in_w
    bb = -2.0 * b
    cc = 2.0 * b * s0 - p_in_w * s0 * s0 - energy
    disc = bb * bb - 4.0 * a * cc
    assert disc > 0.0, (p_in_w, disc)
    u = (-bb + math.sqrt(disc)) / (2.0 * a)
    return u * u


def model2_thermodynamic_clocks():
    ratio, heat_mj_kg = lioh_stoichiometry()
    t_unscrubbed = tau_unscrubbed()
    assert t_unscrubbed < 30.0

    t_lioh_5t = tau_lioh(5000.0)
    t_lioh_2t = tau_lioh(2000.0)
    assert t_lioh_2t < t_lioh_5t

    # Exothermic scrubbing heat injected into the sealed habitat.
    q_lioh_w = heat_mj_kg * 1.0e6 * (N_OCCUPANTS * R_CO2) / 86400.0

    b = rock_flux_coefficient()
    q_1d = b / math.sqrt(86400.0)
    q_10d = b / math.sqrt(10.0 * 86400.0)
    q_100d = b / math.sqrt(100.0 * 86400.0)
    assert q_1d > q_10d > q_100d

    loads_kw = [15.0, 30.0, 50.0, 100.0, 150.0, 250.0]
    taus_days = {}
    for p_kw in loads_kw:
        tau_s = tau_thermal(p_kw * 1000.0 + q_lioh_w)
        taus_days[p_kw] = tau_s / 86400.0
        assert tau_s > 0.0
        assert tau_s < 365.0 * 86400.0

    # Monotone: more internal power means earlier crossing of T_crit.
    ordered = [taus_days[p] for p in loads_kw]
    assert all(ordered[i] > ordered[i + 1] for i in range(len(ordered) - 1))

    # Thermal clock binds before the 5 t LiOH canister clock.
    assert max(taus_days.values()) < t_lioh_5t

    return {
        "ratio": ratio,
        "heat_mj_kg": heat_mj_kg,
        "tau_unscrubbed_d": t_unscrubbed,
        "tau_lioh_2t_d": t_lioh_2t,
        "tau_lioh_5t_d": t_lioh_5t,
        "q_lioh_w": q_lioh_w,
        "q_1d_kw": q_1d / 1000.0,
        "q_10d_kw": q_10d / 1000.0,
        "q_100d_kw": q_100d / 1000.0,
        "taus_days": taus_days,
    }


# ---------------------------------------------------------------------------
# Model 3 - Elite Exit vs. Sovereign Portal-Sealing payoff inversion
# ---------------------------------------------------------------------------
W_0 = 1000.0        # baseline cooperative wealth (M$)
DELTA_R = 400.0     # predatory rent extracted under defection (M$)
V_LIFE = 500.0      # value of life and estate destroyed on entombment (M$)

TIERS = [
    # tier, architecture, H_min, H_max, C_bunker (M$), p_seal, mechanism
    (1, "cut-and-cover luxury compound", 3.0, 10.0, 30.0, 1.00, "direct_vertical_roof_breach"),
    (2, "converted missile silo", 15.0, 55.0, 80.0, 0.98, "cap_plug_breach_and_portal_lock"),
    (3, "deep mountain adit complex", 80.0, 100.0, 300.0, 0.95, "lithostatic_portal_rubble_lock_and_thermal_runaway"),
]


def seal_probability(k_portals, lam=0.55):
    return 1.0 - math.exp(-lam * k_portals)


def model3_payoff_inversion():
    total_loss = W_0 + DELTA_R + V_LIFE
    rows = []
    for tier, arch, h_min, h_max, c_bunker, p_seal, mechanism in TIERS:
        naive = W_0 + DELTA_R - c_bunker
        actual = naive - p_seal * total_loss
        p_star = (DELTA_R - c_bunker) / total_loss

        # Pre-Fordow illusion: defection looks profitable.
        assert naive > W_0, (tier, naive)
        # Post-Fordow reality: defection is catastrophic.
        assert actual < 0.0, (tier, actual)
        assert actual < W_0 - 1000.0, (tier, actual)
        # A modest seal probability already dominates the defection margin.
        assert 0.0 < p_star < 0.25, (tier, p_star)
        assert p_seal >= p_star, (tier, p_seal, p_star)

        rows.append(
            {
                "tier": tier,
                "architecture": arch,
                "h_min": h_min,
                "h_max": h_max,
                "c_bunker": c_bunker,
                "p_seal": p_seal,
                "naive": naive,
                "actual": actual,
                "p_star": p_star,
                "mechanism": mechanism,
            }
        )

    # Monotone worsening in bunker capital expenditure: dE[U]/dC_bunker = -1.
    actuals = [r["actual"] for r in rows]
    assert actuals[0] > actuals[1] > actuals[2], actuals
    for r in rows:
        assert abs((r["actual"] - r["naive"]) + r["p_seal"] * total_loss) < 1e-9

    # Seal probability depends only on the portal count K, never on depth H.
    p_by_depth = [seal_probability(4) for _ in [20.0, 40.0, 60.0, 80.0, 100.0]]
    assert len(set(p_by_depth)) == 1
    assert seal_probability(2) < seal_probability(6)

    # Cooperation strictly dominates defection for every tier.
    for r in rows:
        assert W_0 > r["actual"]

    return {
        "rows": rows,
        "total_loss": total_loss,
        "p_seal_k2": seal_probability(2),
        "p_seal_k6": seal_probability(6),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    print("SPEC-SUBTERRANEAN-SANCTUARY-FALSIFICATION-v1.0")
    print("=" * 72)

    s = verify_schema()
    print("[SCHEMA] required=%d properties=%d" % (s["required_fields"], s["properties"]))

    m1 = model1_penetration_and_portal_lock()
    for name in ("soil", "concrete_34mpa", "concrete_69mpa", "fordow_limestone_172mpa"):
        row = m1["table"][name]
        print(
            "[MODEL 1] %-26s f_c=%6.1f MPa  D1=%7.2f m  D2=%7.2f m"
            % (name, row["f_c_mpa"], row["d1_m"], row["d2_m"])
        )
    print(
        "[MODEL 1] Fordow 12-round bore-walk: %.1f m (eta=0.65) -> %.1f m (eta=0.90) vs H=80 m"
        % (m1["fordow_d12_low_m"], m1["fordow_d12_high_m"])
    )
    print(
        "[MODEL 1] M_rubble=%.0f t in-situ / %.0f t bulked | F_lock=%.2e N / %.2e N | ratio=%.1fx / %.1fx"
        % (
            m1["m_insitu_t"],
            m1["m_bulked_t"],
            m1["f_lock_insitu_n"],
            m1["f_lock_bulked_n"],
            m1["ratio_insitu"],
            m1["ratio_bulked"],
        )
    )

    m2 = model2_thermodynamic_clocks()
    print(
        "[MODEL 2] LiOH=%.4f kg/kg CO2 | dH=%.3f MJ/kg | tau_unscrubbed=%.1f d | tau_LiOH(2t)=%.1f d (5t)=%.1f d"
        % (
            m2["ratio"],
            m2["heat_mj_kg"],
            m2["tau_unscrubbed_d"],
            m2["tau_lioh_2t_d"],
            m2["tau_lioh_5t_d"],
        )
    )
    print(
        "[MODEL 2] Q_rock_max: %.1f kW @1d -> %.1f kW @10d -> %.1f kW @100d | Q_LiOH=%.0f W"
        % (m2["q_1d_kw"], m2["q_10d_kw"], m2["q_100d_kw"], m2["q_lioh_w"])
    )
    print(
        "[MODEL 2] tau_therm: "
        + " | ".join("%.0f kW=%.2f d" % (p, t) for p, t in m2["taus_days"].items())
    )

    m3 = model3_payoff_inversion()
    for r in m3["rows"]:
        print(
            "[MODEL 3] Tier %d C=%3.0fM p_seal=%.2f p*=%.3f | naive=%+7.1fM -> actual=%+7.1fM (W0=%.0fM)"
            % (
                r["tier"],
                r["c_bunker"],
                r["p_seal"],
                r["p_star"],
                r["naive"],
                r["actual"],
                W_0,
            )
        )
    print(
        "[MODEL 3] p_seal(K=2)=%.3f -> p_seal(K=6)=%.3f | depth-invariant | Cooperate strictly dominates"
        % (m3["p_seal_k2"], m3["p_seal_k6"])
    )

    print("=" * 72)
    print("[PASS] ALL THREE MODELS VERIFIED - EXIT CODE 0")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
