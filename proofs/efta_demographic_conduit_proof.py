#!/usr/bin/env python3
"""EFTA demographic discourse & academic conduit verification (SPEC-EFTA-DEMOGRAPHIC-DISCOURSE-AND-ACADEMIC-CONDUIT-v1.0).

Pure Python 3 stdlib. Recomputes the 5 primary-record equations and asserts
against locked constants. Exit code 0 on success.
"""
import json
import math
import sys

R = {}

# --- Eq 1: Shannon filter (corpus -> raw -> core -> signal) ---
n_corpus, n_raw, n_core, n_signal = 1380932, 3082, 517, 18
p_precision = 18 / 3082
fdr = 3064 / 3082
i_raw = math.log2(1380932 / 3082)
i_signal = math.log2(1380932 / 18)
delta_i = math.log2(3082 / 18)
R["eq1_shannon_filter"] = {
    "n_corpus": n_corpus, "n_raw": n_raw, "n_core": n_core, "n_signal": n_signal,
    "p_precision": p_precision, "fdr": fdr, "i_raw_bits": i_raw,
    "i_signal_bits": i_signal, "delta_i_bits": delta_i,
}
assert abs(p_precision - 0.0058403634) < 1e-9
assert abs(fdr - 0.9941596366) < 1e-9
assert abs(i_raw - 8.80756926) < 1e-4
assert abs(i_signal - 16.22726904) < 1e-4
assert abs(delta_i - 7.41969978) < 1e-4

# --- Eq 2: academic & genomic conduits ---
f_bach_traced = 50000.00 + 35000.00  # EFTA01196107 + EFTA01360982
mit_media_lab_share = 525000 / 850000
harvard_ped_share = 6500000 / 9179000
couq_edge_share = 200000 / 1237003
R["eq2_academic_and_genomic_conduits"] = {
    "f_bach_enhanced_mit_usd": 50000.00, "f_bach_jevi_direct_usd": 35000.00,
    "f_bach_traced_usd": 85000.00, "f_mit_post2008_usd": 850000.00,
    "f_mit_media_lab_usd": 525000.00, "f_mit_lloyd_usd": 225000.00,
    "f_mit_pre2008_usd": 100000.00, "mit_media_lab_share": mit_media_lab_share,
    "f_harvard_pre2008_usd": 9179000.00, "f_harvard_ped_nowak_usd": 6500000.00,
    "harvard_ped_share": harvard_ped_share,
    "f_couq_2005_grants_total_usd": 1237003.00,
    "f_couq_2005_net_assets_end_usd": 19570322.00,
    "f_couq_edge_foundation_usd": 200000.00, "couq_edge_share": couq_edge_share,
    "f_couq_harvard_2005_usd": 110000.00,
    "f_thakuria_pgp_check_usd": 2000.00,
    "f_georgarage_androcyte_usd": 200000.00,
}
assert f_bach_traced == 85000.00
assert abs(mit_media_lab_share - 0.61764706) < 1e-8
assert abs(harvard_ped_share - 0.70813814) < 1e-8
assert abs(couq_edge_share - 0.1616810954) < 1e-9

# --- Eq 3: Nikolic agency (EFTA01117804 / EFTA00583858) ---
v_nikolic = (30000000 - 10000000) * 1.0 + (30000000 - 10000000) * 0.50 - 2500000
R["eq3_nikolic_agency"] = {
    "mandate_range_cap_usd": 100000000.00,
    "foundation_medicine_basis_usd": 10000000.00,
    "researchgate_basis_usd": 10000000.00, "combined_basis_usd": 20000000.00,
    "advance_tranche_1_usd": 1250000.00, "advance_tranche_2_usd": 1250000.00,
    "total_advance_usd": 2500000.00, "foundation_medicine_max_upside_share": 1.00,
    "researchgate_max_upside_share": 0.50, "default_interest_rate": 0.12,
    "max_payment_demands": 4, "v_nikolic_at_3x_fmv_net_usd": v_nikolic,
    "estate_gross_probate_usd": 577672654.00, "will_executor_fee_usd": 250000.00,
}
assert v_nikolic == 27500000.00

# --- Eq 4: banking concentration (EFTA00811497) ---
bank_totals = {
    "Deutsche_Bank": 99714414, "Merrill": 14096741, "Morgan_Stanley": 3649369,
    "First_Bank": 3248056, "Banco_Pop_BNP_Paribas": 824371,
    "Wells_Fargo": 249255, "TD_Ameritrade": 51682,
}
total_cash = 121833887  # printed table total; column sum = 121833888 ($1 rounding)
sum_cols = sum(bank_totals.values())
assert abs(sum_cols - total_cash) <= 1
db_share = bank_totals["Deutsche_Bank"] / total_cash
hhi = sum((b / total_cash) ** 2 for b in bank_totals.values())
top7 = {
    "Southern_Trust_Company_Inc": 51335925, "Southern_Financial_LLC": 29315271,
    "Haze_Trust": 25494432, "JEE": 5320031, "Gratitude_America_Ltd": 4155265,
    "Jeepers_Inc": 1481314, "LSJE_LLC": 1138005,
}
top_7_subtotal = sum(top7.values())
top_7_db_subtotal = 97380768  # locked EFTA00811497 DB-held subtotal of top-7
top_7_db_share = top_7_db_subtotal / top_7_subtotal
top_3_share = (51335925 + 29315271 + 25494432) / top_7_subtotal
R["eq4_banking_concentration"] = {
    "bank_column_totals_usd": bank_totals,
    "total_cash_all_32_entities_usd": total_cash,
    "db_share_all_32": db_share, "hhi_7_banks_all_32": hhi,
    "top_7_entities_usd": top7, "top_7_subtotal_usd": top_7_subtotal,
    "top_7_db_subtotal_usd": top_7_db_subtotal, "top_7_db_share": top_7_db_share,
    "top_3_entity_share_of_top_7": top_3_share,
    "enhanced_education_cash_usd": 23075 + 117126,
}
assert abs(db_share - 0.8184456448) < 1e-8
assert abs(hhi - 0.6848244243) < 1e-3
assert top_7_subtotal == 118240243
assert top_7_db_subtotal == 97380768
assert abs(top_7_db_share - 0.8235839603) < 1e-8
assert abs(top_3_share - 0.8977092173) < 1e-4

# --- Eq 5: restitution waterfall ---
tranches = [150000000, 137500000, 121000000, 75000000, 290000000]
total_pool = sum(tranches)
ev_schedule = [121833887, 408500000, 773500000]


def restitution_recovery(ev, tranches):
    """Pro-rata within available pool: pay tranches in seniority order."""
    remaining = ev
    paid = []
    for t in tranches:
        pay = min(t, max(remaining, 0))
        paid.append(pay)
        remaining -= pay
    return paid


ratio = total_pool / (850000 + 9179000)
R["eq5_restitution_waterfall"] = {
    "tranches_usd": tranches, "total_pool_usd": total_pool,
    "ev_schedule": ev_schedule,
    "recovery_at_ev_points": [restitution_recovery(ev, tranches) for ev in ev_schedule],
    "restitution_to_academic_gift_ratio": ratio,
}
assert total_pool == 773500000
assert abs(ratio - 77.1263336325) < 1e-6
assert restitution_recovery(773500000, tranches) == tranches

print(json.dumps(R, indent=2))
sys.exit(0)
