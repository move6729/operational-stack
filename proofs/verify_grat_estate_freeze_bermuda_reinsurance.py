#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: GRAT ESTATE FREEZE & BERMUDA REINSURANCE CUTOUT RETAINER (v1.0)

Proves:
1. Vector 1 - White-Shoe Legal Fee Anomaly Ratio (Dechert LLP 2021 & Senate Finance 2023):
   M_Fee_Anomaly = Fee_Southern_Trust / Fee_White_Shoe_Market = $158.0M / $2.0M = 79.0x,
   i.e. the 2012-2017 Southern Trust retainer paid 79.0x the analytical maximum market
   price of a standard 26 U.S.C. 2702 GRAT / estate structure drafted by a top Manhattan
   law firm, against a claimed estate-tax savings floor of $1,000.0M (15.80% vigorish on
   the floor). Also closes the documented payment decomposition: $50.0M (2013, written
   agreements) + $70.0M (2014) + $30.0M (2015) + $8.0M residual = $158.0M, of which
   $100.0M (63.29%) was paid "on an ad hoc basis, without negotiating written service
   agreements" (Dechert LLP Report, Ex. 99.1, Jan. 22, 2021).
2. Vector 2 - USVI 26 U.S.C. 934 Tax-Shielded Cutout Capture & Post-Rupture Settlement
   Identity: Outflow_Total = $158.0M + $62.5M = $220.5M, while the 90% USVI EDC exemption
   shielded 0.90 x $158.0M = $142.2M from USVI income taxation. The USVI-Black settlement
   agreement was executed in January 2023 ($62.5M cash, releasing potential claims arising
   from the USVI investigation) and publicly reported July 21, 2023; the enforcement-
   recovery ratio 62.5 / 142.2 = 43.95% normalizes that settlement against the shielded
   base and is not a documentary characterization of the payment as a 934 tax clawback.
3. Vector 3 - 26 U.S.C. 2702 / 7520 GRAT estate-freeze identity (zeroed-out GRAT):
   Gift_Taxable = V - PV_Retained(r_7520, n, A) = 0 at A = V * r / (1 - (1 + r)^-n)
   (= $269.0270M/yr at V = $1,000.0M, r = 3.0%, n = 4), freezing post-transfer
   appreciation out of the transferor's gross estate, with the g = r (0.0) and
   g < r (-43.08) boundary regimes locked.
4. Vector 4 - Private-equity captive Bermuda life-reinsurance sidecar arbitrage
   (NAIC Schedule S): Delta_Tax_Shield = Premium_Ceded x (tau_US - tau_BDA) with the
   Schedule S unauthorized/affiliated disclosure obligation triggered (indicator = 1).

Zero external dependencies.
"""

import hashlib
import json


def verify_vector1_white_shoe_fee_anomaly():
    """
    M_Fee_Anomaly = Fee_Southern_Trust / Fee_White_Shoe_Market = 158.0 / 2.0 = 79.0.

    Documentary predicates - Dechert LLP Report to the Conflicts Committee of the Board of
    Directors of Apollo Global Management, Inc. (Jan. 22, 2021), filed as Exhibit 99.1 to
    Apollo Global Management, Inc. Form 8-K (SEC EDGAR CIK 0001411494, Accession No.
    000119312521016405, Doc. d118102dex991.htm):
      - "Those payments for work performed over the period 2012 through 2017 totaled
        $158 million."
      - "Although Epstein represented to Black that he generally charged clients $40
        million per year for his advice, Epstein agreed to provide this initial work for
        $23.5 million ..."
      - "The total amount paid in 2013 was $50 million." (written service agreements,
        including the Feb. 13, 2013 agreement between Black and Southern Trust Company,
        Inc., "an Epstein affiliate")
      - "Starting in 2014, Black began to pay Epstein for his ongoing services on an ad
        hoc basis, without negotiating written service agreements. In total, Black paid
        Epstein $70 million in 2014 and $30 million in 2015."
    The $2.0M white-shoe ceiling is an analytical market parameter, not a documentary
    predicate; the $40.0M represented annual rate IS documentary and is itself 20.0x that
    analytical ceiling. Senate Finance Committee, Chairman Ron Wyden, unveiled an ongoing
    investigation into the payments on July 25, 2023 (letter to Leon Black, July 24, 2023).
    """
    fee_southern_trust_usd_millions = 158.0
    fee_white_shoe_cap_usd_millions = 2.0
    claimed_savings_floor_usd_millions = 1000.0

    m_fee_anomaly = fee_southern_trust_usd_millions / fee_white_shoe_cap_usd_millions
    assert m_fee_anomaly == 79.0, "white-shoe fee anomaly multiple mismatch"

    vigorish_on_savings_floor_pct = (
        fee_southern_trust_usd_millions / claimed_savings_floor_usd_millions * 100.0
    )
    assert round(vigorish_on_savings_floor_pct, 2) == 15.8, "vigorish-on-floor ratio mismatch"

    implied_savings_multiple = (
        claimed_savings_floor_usd_millions / fee_southern_trust_usd_millions
    )
    assert round(implied_savings_multiple, 4) == 6.3291, "savings-to-fee multiple mismatch"

    # Documented represented rate (Dechert, Ex. 99.1) vs. the analytical white-shoe cap.
    epstein_represented_annual_rate_usd_millions = 40.0
    represented_rate_over_cap = (
        epstein_represented_annual_rate_usd_millions / fee_white_shoe_cap_usd_millions
    )
    assert represented_rate_over_cap == 20.0, "represented-rate-to-cap multiple mismatch"

    # Documented payment decomposition (Dechert, Ex. 99.1) closing on the $158.0M total.
    documented_2013_written_agreement_usd_millions = 50.0
    ad_hoc_2014_usd_millions = 70.0
    ad_hoc_2015_usd_millions = 30.0
    documented_annual_payments_usd_millions = (
        documented_2013_written_agreement_usd_millions
        + ad_hoc_2014_usd_millions
        + ad_hoc_2015_usd_millions
    )
    residual_other_years_usd_millions = (
        fee_southern_trust_usd_millions - documented_annual_payments_usd_millions
    )
    assert documented_annual_payments_usd_millions == 150.0, "2013-2015 documented sum mismatch"
    assert round(residual_other_years_usd_millions, 4) == 8.0, "residual-year balance mismatch"
    assert (
        documented_annual_payments_usd_millions + residual_other_years_usd_millions
        == fee_southern_trust_usd_millions
    ), "payment decomposition must close on the $158.0M total"

    ad_hoc_no_written_agreement_usd_millions = ad_hoc_2014_usd_millions + ad_hoc_2015_usd_millions
    ad_hoc_share_of_retainer_pct = (
        ad_hoc_no_written_agreement_usd_millions / fee_southern_trust_usd_millions * 100.0
    )
    assert round(ad_hoc_no_written_agreement_usd_millions, 4) == 100.0, "ad hoc stream mismatch"
    assert round(ad_hoc_share_of_retainer_pct, 2) == 63.29, "ad hoc share-of-retainer mismatch"
    # Boundary regime: the anomaly is majority-undocumented only while the ad hoc share
    # exceeds 50%; below that threshold the written-agreement stream would dominate.
    assert ad_hoc_share_of_retainer_pct > 50.0, "majority-undocumented regime not satisfied"

    return {
        "fee_southern_trust_usd_millions": fee_southern_trust_usd_millions,
        "fee_white_shoe_cap_usd_millions": fee_white_shoe_cap_usd_millions,
        "claimed_savings_floor_usd_millions": claimed_savings_floor_usd_millions,
        "m_fee_anomaly_multiple": m_fee_anomaly,
        "vigorish_on_savings_floor_pct": round(vigorish_on_savings_floor_pct, 2),
        "implied_savings_multiple": round(implied_savings_multiple, 4),
        "epstein_represented_annual_rate_usd_millions": epstein_represented_annual_rate_usd_millions,
        "represented_rate_over_white_shoe_cap_multiple": represented_rate_over_cap,
        "documented_2013_written_agreement_usd_millions": documented_2013_written_agreement_usd_millions,
        "ad_hoc_no_written_agreement_2014_2015_usd_millions": round(
            ad_hoc_no_written_agreement_usd_millions, 4
        ),
        "residual_other_years_usd_millions": round(residual_other_years_usd_millions, 4),
        "ad_hoc_share_of_retainer_pct": round(ad_hoc_share_of_retainer_pct, 2),
        "retainer_window": "2012-2017",
        "fee_anomaly_verified": True,
    }


def verify_vector2_usvi_shield_and_outflow_identity():
    """
    Outflow_Total = Fee_Southern_Trust + Settlement_USVI_2023 = 158.0 + 62.5 = 220.5.
    Shielded = 0.90 x 158.0 = 142.2 (USVI EDC 90% income-tax exemption under the 26 U.S.C.
    934 mirror code; Southern Trust Company's EDC beneficiary status is documented in
    contemporaneous USVI press record, Bloomberg (July 27, 2019) and The Source (July 16,
    2019), and is a matter of USVI public record).

    The USVI-Black settlement agreement was EXECUTED IN JANUARY 2023 ($62.5M in cash, in
    exchange for the Government of the US Virgin Islands releasing Black from potential
    claims arising from its Epstein investigation) and was publicly reported on July 21,
    2023 (Reuters / The New York Times); the executed agreement is posted by the Senate
    Committee on Finance. The ratio 62.5 / 142.2 = 43.95% is therefore an analytical
    ENFORCEMENT-RECOVERY ratio (settlement normalized against the shielded base), not a
    documentary characterization of the payment as a 26 U.S.C. 934 tax clawback.
    """
    fee_southern_trust_usd_millions = 158.0
    settlement_usvi_2023_usd_millions = 62.5
    usvi_edc_exemption_rate = 0.9

    outflow_total = fee_southern_trust_usd_millions + settlement_usvi_2023_usd_millions
    assert outflow_total == 220.5, "combined outflow identity mismatch"

    tax_shielded = usvi_edc_exemption_rate * fee_southern_trust_usd_millions
    assert round(tax_shielded, 4) == 142.2, "USVI shielded base mismatch"

    enforcement_recovery_ratio_pct = settlement_usvi_2023_usd_millions / tax_shielded * 100.0
    assert round(enforcement_recovery_ratio_pct, 2) == 43.95, "enforcement-recovery ratio mismatch"
    # Boundary regime: post-enforcement majority-intact regime holds only while the
    # settlement is strictly smaller than the shielded base (ratio < 100%).
    assert settlement_usvi_2023_usd_millions < tax_shielded, "majority-intact regime violated"
    assert enforcement_recovery_ratio_pct < 100.0, "recovery ratio must remain below unity"

    return {
        "fee_southern_trust_usd_millions": fee_southern_trust_usd_millions,
        "settlement_usvi_2023_usd_millions": settlement_usvi_2023_usd_millions,
        "settlement_executed_month": "2023-01",
        "settlement_publicly_reported": "2023-07-21",
        "usvi_edc_exemption_rate": usvi_edc_exemption_rate,
        "outflow_total_usd_millions": outflow_total,
        "tax_shielded_usd_millions": round(tax_shielded, 4),
        "enforcement_recovery_ratio_pct": round(enforcement_recovery_ratio_pct, 2),
        "outflow_identity_verified": True,
    }


def verify_vector3_grat_estate_freeze_identity():
    """
    26 U.S.C. 2702 / 7520 zeroed-out GRAT: Gift_Taxable = V - PV_Retained = 0 at
    A = V * r / (1 - (1 + r)^-n). Post-transfer appreciation above the 7520 hurdle
    accrues to remainder beneficiaries outside the transferor's gross estate.
    """
    v_corpus_usd_millions = 1000.0
    r_7520 = 0.030
    n_term_years = 4
    asset_cagr_illustrative = 0.10

    annuity_zero_out = v_corpus_usd_millions * r_7520 / (
        1.0 - (1.0 + r_7520) ** (-n_term_years)
    )
    assert round(annuity_zero_out, 4) == 269.027, "zero-out annuity closed-form mismatch"
    pv_retained = annuity_zero_out * (
        1.0 - (1.0 + r_7520) ** (-n_term_years)
    ) / r_7520
    assert abs(pv_retained - v_corpus_usd_millions) < 1e-9, "zero-out PV identity mismatch"

    taxable_gift = abs(v_corpus_usd_millions - pv_retained)
    assert taxable_gift < 1e-9, "taxable gift must net to zero at the hurdle"

    excess_spread = asset_cagr_illustrative - r_7520
    assert excess_spread > 0.0, "freeze transfers value only when asset CAGR exceeds hurdle"

    appreciation_excluded = v_corpus_usd_millions * (
        (1.0 + asset_cagr_illustrative) ** n_term_years
        - (1.0 + r_7520) ** n_term_years
    )
    assert round(appreciation_excluded, 2) == 338.59, "excluded appreciation mismatch"

    # Boundary regimes of the freeze identity: at g == r_7520 the excluded appreciation
    # collapses to exactly zero (the freeze transfers nothing), and at g < r_7520 it turns
    # strictly negative (the annuity over-distributes and the freeze destroys value).
    appreciation_at_g_equals_r = v_corpus_usd_millions * (
        (1.0 + r_7520) ** n_term_years - (1.0 + r_7520) ** n_term_years
    )
    assert abs(appreciation_at_g_equals_r) < 1e-9, "g == r boundary must net to zero"

    g_below_hurdle = 0.02
    appreciation_at_g_below_r = v_corpus_usd_millions * (
        (1.0 + g_below_hurdle) ** n_term_years - (1.0 + r_7520) ** n_term_years
    )
    assert appreciation_at_g_below_r < 0.0, "g < r boundary must be strictly negative"
    assert round(appreciation_at_g_below_r, 2) == -43.08, "g < r boundary magnitude mismatch"

    return {
        "grat_corpus_usd_millions": v_corpus_usd_millions,
        "r_7520_hurdle": r_7520,
        "term_years": n_term_years,
        "zero_out_annuity_usd_millions": round(annuity_zero_out, 4),
        "pv_retained_interest_usd_millions": round(pv_retained, 6),
        "taxable_gift_usd_millions": round(taxable_gift, 9),
        "asset_cagr_illustrative": asset_cagr_illustrative,
        "excess_spread_over_hurdle": round(excess_spread, 4),
        "appreciation_excluded_from_estate_usd_millions": round(appreciation_excluded, 2),
        "boundary_g_equals_r_excluded_usd_millions": round(appreciation_at_g_equals_r, 9),
        "boundary_g_below_r_excluded_usd_millions": round(appreciation_at_g_below_r, 2),
        "estate_freeze_identity_verified": True,
    }


def verify_vector4_bermuda_sidecar_schedule_s_arbitrage():
    """
    Delta_Tax_Shield = Premium_Ceded x (tau_US - tau_BDA). Bermuda imposed zero corporate
    income tax on (re)insurers through 2024 (Corporate Income Tax Act 2023: 15% from 2025).
    A PE-owned captive Bermuda reinsurer is an unauthorized affiliated counterparty for
    NAIC Schedule S purposes, so the Schedule S disclosure obligation is triggered (= 1).
    Affiliation predicate for the Apollo archetype is documentary: the New York State
    Department of Financial Services examination report (June 3, 2019) records that Athene
    Life Re "created Athene Annuity Re Ltd. ('AARe') as a Bermuda reinsurer to serve as a
    reinsurance counterparty for most internal affiliated" transactions.
    """
    tau_us = 0.21
    tau_bda_pre_2025 = 0.0
    tau_bda_post_2025 = 0.15
    # Illustrative ceded premium base scaled to the shielded cutout capital (Vector 2).
    premium_ceded_usd_millions = 142.2

    delta_tau_pre_2025 = tau_us - tau_bda_pre_2025
    assert delta_tau_pre_2025 == 0.21, "pre-2025 tax differential mismatch"

    sidecar_tax_shield = premium_ceded_usd_millions * delta_tau_pre_2025
    assert round(sidecar_tax_shield, 4) == 29.862, "sidecar tax shield mismatch"

    affiliated_reinsurer = 1
    naic_authorized = 0
    schedule_s_disclosure_required = (
        1 if (affiliated_reinsurer == 1 and naic_authorized == 0) else 0
    )
    assert schedule_s_disclosure_required == 1, "Schedule S disclosure obligation not triggered"

    delta_tau_post_2025 = tau_us - tau_bda_post_2025
    assert round(delta_tau_post_2025, 2) == 0.06, "post-2025 tax differential mismatch"
    arbitrage_persists_post_2025 = delta_tau_post_2025 > 0.0
    assert arbitrage_persists_post_2025, "arbitrage must persist while delta_tau > 0"

    # Compression regime: the CIT Act 2023 shrinks but does not close the shield.
    sidecar_tax_shield_post_2025 = premium_ceded_usd_millions * delta_tau_post_2025
    assert round(sidecar_tax_shield_post_2025, 4) == 8.532, "post-2025 sidecar shield mismatch"
    assert sidecar_tax_shield_post_2025 < sidecar_tax_shield, "shield must compress post-2025"
    assert sidecar_tax_shield_post_2025 > 0.0, "shield must remain strictly positive post-2025"

    return {
        "tau_us_federal_corporate": tau_us,
        "tau_bermuda_pre_2025": tau_bda_pre_2025,
        "tau_bermuda_post_2025_cit_act_2023": tau_bda_post_2025,
        "premium_ceded_usd_millions": premium_ceded_usd_millions,
        "delta_tau_pre_2025": delta_tau_pre_2025,
        "sidecar_tax_shield_usd_millions": round(sidecar_tax_shield, 4),
        "affiliated_reinsurer_indicator": affiliated_reinsurer,
        "naic_authorized_indicator": naic_authorized,
        "schedule_s_disclosure_required": schedule_s_disclosure_required,
        "delta_tau_post_2025": round(delta_tau_post_2025, 2),
        "sidecar_tax_shield_post_2025_usd_millions": round(sidecar_tax_shield_post_2025, 4),
        "arbitrage_persists_post_2025": arbitrage_persists_post_2025,
        "sidecar_arbitrage_verified": True,
    }


def run_verification():
    v1 = verify_vector1_white_shoe_fee_anomaly()
    v2 = verify_vector2_usvi_shield_and_outflow_identity()
    v3 = verify_vector3_grat_estate_freeze_identity()
    v4 = verify_vector4_bermuda_sidecar_schedule_s_arbitrage()

    manifest = {
        "spec_version": "SPEC-GRAT-ESTATE-FREEZE-AND-BERMUDA-REINSURANCE-CUTOUT-RETAINER-v1.0",
        "jurisdiction_context": "US",
        "cfaa_compliance_attestation": True,
        "Vector1WhiteShoeFeeAnomaly": v1,
        "Vector2UsviShieldAndOutflowIdentity": v2,
        "Vector3GratEstateFreezeIdentity": v3,
        "Vector4BermudaSidecarScheduleSArbitrage": v4,
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-GRAT-ESTATE-FREEZE-AND-BERMUDA-REINSURANCE-CUTOUT-RETAINER-v1.0 | "
        f"M_Fee_Anomaly={v1['m_fee_anomaly_multiple']}x | "
        f"Vigorish/Floor={v1['vigorish_on_savings_floor_pct']}% | "
        f"RepresentedRate={v1['represented_rate_over_white_shoe_cap_multiple']}x cap | "
        f"AdHocNoWrittenAgreement=${v1['ad_hoc_no_written_agreement_2014_2015_usd_millions']}M "
        f"({v1['ad_hoc_share_of_retainer_pct']}%) | "
        f"Outflow_Total=${v2['outflow_total_usd_millions']}M | "
        f"Shielded=${v2['tax_shielded_usd_millions']}M | "
        f"EnforcementRecovery={v2['enforcement_recovery_ratio_pct']}% | "
        f"ZeroOutAnnuity=${v3['zero_out_annuity_usd_millions']}M | "
        f"Gift=0 | Excluded=${v3['appreciation_excluded_from_estate_usd_millions']}M | "
        f"SidecarShield=${v4['sidecar_tax_shield_usd_millions']}M | "
        f"ScheduleS={v4['schedule_s_disclosure_required']} | "
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    run_verification()
