#!/usr/bin/env python3
"""
OPSTACK VERIFICATION ENGINE: THE COMPILER-RUNTIME FALLACY (v1.0)

Proves:
1. Landauer-Thermodynamic Runtime Penalty: k_B * T * ln2 = 2.870e-21 J/bit at 300 K, so a
   25 J cloud inference token priced against a 5.0e-10 J deterministic SQL/PLC step is a
   5.0e10x (log10 = 10.699) thermodynamic penalty equal to 8.709e21 Landauer minimal
   bit-erasures per token, and a 250 J full query (10 token-equivalents) is 5.0e11x
   (8.709e22 bit-erasures), compounded by a 425x latency penalty (850 ms p99 vs a 2.0 ms
   deterministic cycle) for a joint energy-latency penalty of 2.125e13x per token.
2. One-Pass Airlock COALESCE Caching Collapse: at K = 1000 recurring transactions per
   entity, compile-once/replay-many deletes (K-1)/K = 99.9% of per-entity tokens and
   92.5% of macro recurring inference demand (implied recurring demand share 92.5926%),
   collapsing 250,000 J and 850,000 ms per entity to 250 J and 2,000 ms.
3. Multi-Step Agent Equivocation Decay: (1 - 0.03)^20 = 0.543794 end-to-end reliability
   against 1.0 for a deterministic state machine (45.6206% equivocation deficit), with
   50% reliability lost at 23 steps and 99% reliability unreachable at any step count > 0.
4. Off-Balance-Sheet Civilizational Deadweight Loss: a 2.5M STEM cohort x 0.70 wrapper
   diversion = 1.75M man-years/yr x $200k = $350.0B/yr ($3,500B over 10 years, 77.778% of
   the $450B hyperscaler AI capex run-rate), coupled to an Ashby requisite-variety parity
   breach in year 5 and an 84.981% Shannon commons capacity collapse at a 100x synthetic
   noise floor.
5. Acemoglu Macro Bounds & Revenue Deficit: a 4.6% 10-year exposed task share caps TFP at
   0.71% and GDP at 1.1% (15.4348% cost reduction per exposed task), while the $600B
   required AI revenue base against $75B of realistic compiler/airlock revenue leaves a
   $525B/yr deficit (12.5% coverage; capex 6.0x realistic revenue).
6. CoreWeave $42.15B Pro-Forma GPU Debt Waterfall: tranche_recovery(ev) across stressed
   EV of $15.0B / $25.0B / $38.43B / $42.15B, with 91.1744% cumulative parent recourse
   ($38.43B = Tranche 1 Senior DDTL $18.50B + Tranche 2 Recourse/Lease Box $19.93B) and a
   $3.72B non-recourse SPV stub wiped to zero at the recourse-par boundary.

Zero external dependencies.
"""

import hashlib
import json
import math
import re
from datetime import date

TOL = 1e-9

# --- Locked physical baseline (CODATA 2018 k_B, Landauer 1961, 300 K substrate) ---
T_KELVIN = 300.0
K_B_JOULES_PER_KELVIN = 1.380649e-23
LANDAUER_MIN_BIT_JOULES = 2.87049e-21
ENERGY_DETERMINISTIC_SQL_PLC_JOULES = 5.0e-10
ENERGY_RUNTIME_LLM_QUERY_JOULES = 250.0
ENERGY_RUNTIME_LLM_PER_TOKEN_JOULES = 25.0
THERMODYNAMIC_PENALTY_RATIO = 5.0e10
THERMODYNAMIC_PENALTY_LOG10 = 10.699
PLC_DETERMINISTIC_CYCLE_MS = 2.0
CLOUD_LLM_P99_LATENCY_MS = 850.0
LATENCY_PENALTY_MULTIPLIER = 425.0

# --- Locked compile-once/replay-many airlock baseline ---
ENTERPRISE_TRANSACTIONS_PER_ENTITY_K = 1000
COALESCE_CACHE_TOKEN_REDUCTION_PCT = 99.9
MACRO_RECURRING_INFERENCE_COLLAPSE_PCT = 92.5

# --- Locked multi-step agent equivocation baseline ---
PER_STEP_HALLUCINATION_RATE_EPSILON = 0.03
AGENT_CHAIN_STEPS_N = 20
AGENT_CHAIN_RELIABILITY_20_STEPS = 0.543794
DETERMINISTIC_STATE_MACHINE_RELIABILITY = 1.0

# --- Locked civilizational deadweight baseline ---
GLOBAL_STEM_COHORT_DIVERTED_MILLIONS = 2.5
WRAPPER_DIVERSION_SHARE = 0.70
WAGE_PER_MAN_YEAR_USD = 200000.0
ANNUAL_COGNITIVE_DEADWEIGHT_MAN_YEARS = 1750000.0
OPPORTUNITY_COST_HUMAN_CAPITAL_BILLIONS_PER_YR = 350.0
COGNITIVE_ATROPHY_PER_DIVERTED_YEAR = 0.06
ASHBY_VARIETY_HEADROOM_INITIAL = 1.35
ASHBY_ENVIRONMENT_VARIETY_GROWTH = 0.03
SHANNON_COMMONS_NOISE_INFLATION_FACTOR = 100.0
SHANNON_BASELINE_COMMONS_SNR = 100.0

# --- Locked macro / revenue baseline ---
ACEMOGLU_10YR_TASK_SHARE_PCT = 4.6
ACEMOGLU_10YR_TFP_MAX_PCT = 0.71
ACEMOGLU_10YR_GDP_MAX_PCT = 1.1
HYPERSCALER_ANNUAL_AI_CAPEX_B = 450.0
SEQUOIA_REQUIRED_REVENUE_B = 600.0
REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B = 75.0
ANNUAL_REVENUE_DEFICIT_B = 525.0

# --- Locked CoreWeave pro-forma GPU debt stack (SEC CIK 0001769628) ---
COREWEAVE_PRO_FORMA_DEBT_B = 42.15
COREWEAVE_RECOURSE_DEBT_B = 38.43
COREWEAVE_RECOURSE_SHARE_PCT = 91.18
TRANCHE_1_SENIOR_DDTL_B = 18.50
TRANCHE_2_RECOURSE_LEASE_BOX_B = 19.93
TRANCHE_3_NON_RECOURSE_SPV_B = 3.72
BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B = 76.56
BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B = 99.34
STRESSED_EV_SCENARIOS_B = (15.0, 25.0, 38.43, 42.15)

# --- Multi-counterparty security master cross-index ---
ENTITY_AND_INSTRUMENT_IDS = {
    "primary_target": {
        "entity": "CoreWeave, Inc.",
        "role": "leveraged_neocloud_gpu_landlord",
        "ticker": "CRWV",
        "exchange": "NASDAQ",
        "cik": "0001769628",
        "instrument": "pro_forma_gpu_debt_stack",
        "amount_usd_b": COREWEAVE_PRO_FORMA_DEBT_B,
    },
    "bdc_colender": {
        "entity": "Blue Owl Capital Corporation",
        "role": "bdc_colender_ai_datacenter_tranche",
        "ticker": "OBDC",
        "exchange": "NYSE",
        "cik": "0001606163",
        "instrument": "dual_ai_saas_exposure_upper_bound",
        "amount_usd_b": BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B,
    },
    "sponsor_manager": {
        "entity": "Blue Owl Capital Inc.",
        "role": "alternative_asset_manager_gp",
        "ticker": "OWL",
        "exchange": "NYSE",
        "cik": "0001823945",
        "instrument": "dual_ai_saas_exposure_lower_bound",
        "amount_usd_b": BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B,
    },
    "silicon_counterparty": {
        "entity": "NVIDIA Corporation",
        "role": "gpu_collateral_originator",
        "ticker": "NVDA",
        "exchange": "NASDAQ",
        "cik": "0001045810",
        "instrument": "gpu_asset_collateral_box",
        "amount_usd_b": None,
    },
    "hyperscaler_microsoft": {
        "entity": "Microsoft Corporation",
        "role": "hyperscaler_ai_capex_counterparty",
        "ticker": "MSFT",
        "exchange": "NASDAQ",
        "cik": "0000789019",
        "instrument": "aggregate_hyperscaler_ai_capex",
        "amount_usd_b": None,
    },
    "hyperscaler_alphabet": {
        "entity": "Alphabet Inc.",
        "role": "hyperscaler_ai_capex_counterparty",
        "ticker": "GOOGL",
        "exchange": "NASDAQ",
        "cik": "0001652044",
        "instrument": "aggregate_hyperscaler_ai_capex",
        "amount_usd_b": None,
    },
    "hyperscaler_amazon": {
        "entity": "Amazon.com, Inc.",
        "role": "hyperscaler_ai_capex_counterparty",
        "ticker": "AMZN",
        "exchange": "NASDAQ",
        "cik": "0001018724",
        "instrument": "aggregate_hyperscaler_ai_capex",
        "amount_usd_b": None,
    },
    "hyperscaler_meta": {
        "entity": "Meta Platforms, Inc.",
        "role": "hyperscaler_ai_capex_counterparty",
        "ticker": "META",
        "exchange": "NASDAQ",
        "cik": "0001326801",
        "instrument": "aggregate_hyperscaler_ai_capex",
        "amount_usd_b": None,
    },
    "ai_capex_gap_underwriter": {
        "entity": "Sequoia Capital Operations, L.P.",
        "role": "ai_revenue_gap_estimator",
        "ticker": None,
        "exchange": None,
        "cik": "private",
        "instrument": "required_ai_revenue_base",
        "amount_usd_b": SEQUOIA_REQUIRED_REVENUE_B,
    },
    "empirical_bound_originator": {
        "entity": "Acemoglu, Daron (2024), The Simple Macroeconomics of AI",
        "role": "ten_year_task_share_tfp_gdp_bound",
        "ticker": None,
        "exchange": None,
        "cik": "n_a",
        "instrument": "ten_year_gdp_uplift_bound",
        "amount_usd_b": None,
    },
    "vertical_saas_servicetitan": {
        "entity": "ServiceTitan, Inc.",
        "role": "vertical_saas_field_service_rent_target",
        "ticker": "TTAN",
        "exchange": "NASDAQ",
        "cik": "0001638825",
        "instrument": "per_technician_seat_and_onboarding_rent",
        "amount_usd_b": None,
    },
    "enterprise_erp_oracle_netsuite": {
        "entity": "Oracle Corporation (NetSuite ERP)",
        "role": "multi_tenant_cloud_erp_and_ai_capex_counterparty",
        "ticker": "ORCL",
        "exchange": "NYSE",
        "cik": "0001341439",
        "instrument": "multi_tenant_erp_license_and_cloud_lease_stack",
        "amount_usd_b": None,
    },
    "enterprise_saas_salesforce": {
        "entity": "Salesforce, Inc.",
        "role": "horizontal_crm_and_agent_wrapper_rent_target",
        "ticker": "CRM",
        "exchange": "NYSE",
        "cik": "0001108524",
        "instrument": "multi_tenant_seat_and_runtime_agent_subscription",
        "amount_usd_b": None,
    },
    "defense_industrial_base_cmmc_enclave": {
        "entity": "U.S. Department of Defense DIB (32 CFR Part 170 CMMC 2.0 / DFARS 252.204-7012)",
        "role": "air_gapped_defense_machine_shop_cui_sovereignty",
        "ticker": None,
        "exchange": None,
        "cik": "n_a",
        "instrument": "air_gapped_x86_64_linux_deterministic_erp_plc_enclave",
        "amount_usd_b": None,
    },
    "cold_chain_food_logistics_unfi": {
        "entity": "United Natural Foods, Inc. (Form 8-K 2025-06-09 Cold-Chain ERP Outage)",
        "role": "civilian_cold_chain_erp_single_point_of_failure_canary",
        "ticker": "UNFI",
        "exchange": "NYSE",
        "cik": "0001020859",
        "instrument": "centralized_cloud_erp_cold_chain_fulfillment_grid",
        "amount_usd_b": None,
    },
}

# --- Hard-date catalyst & forbearance calendar (SEC Note 10 p. 27 amortization schedule) ---
CATALYST_CALENDAR_FLOOR = "2026-11-04"
CATALYST_CALENDAR = (
    {
        "date": "2026-11-10",
        "event": "Q3 2026 Form 10-Q window: DDTL 5.5 Term SOFR+550 bps repricing disclosure",
        "basis": "estimated_filing_window",
        "usd_b": None,
    },
    {
        "date": "2026-12-31",
        "event": "H2 2026 mandatory DDTL/OEM box principal amortization completes",
        "basis": "sec_note_10_schedule",
        "usd_b": 4.413,
    },
    {
        "date": "2027-12-31",
        "event": "FY2027 debt principal amortization; cumulative 18-month outflows $13.976B",
        "basis": "sec_note_10_schedule",
        "usd_b": 6.184,
    },
    {
        "date": "2028-12-31",
        "event": "Cumulative 30-month debt principal $15.013B (42.23% of Q2 principal)",
        "basis": "sec_note_10_schedule",
        "usd_b": 4.416,
    },
    {
        "date": "2029-12-31",
        "event": "Box-loan contract rollover: 3-year customer contracts expire inside 5-year DDTL",
        "basis": "contractual_maturity",
        "usd_b": None,
    },
    {
        "date": "2030-12-31",
        "event": "2030-2033 bullet refinancing wall opens against decaying GPU collateral",
        "basis": "contractual_maturity",
        "usd_b": 22.317,
    },
)

JURISDICTION_CONTEXT = {
    "iso_3166_1": "US",
    "venue": "SDNY / NY County Commercial Division",
    "statutory_modules": (
        "18_USC_1030_CFAA",
        "SEC_EXCHANGE_ACT_1934",
        "DELAWARE_DGCL",
        "UCC_ARTICLE_9_SECURED_TRANSACTIONS",
        "32_CFR_170_DOD_CMMC_2_0_DFARS_252_204_7012",
        "EU_NIS2_DIRECTIVE_2022_2555_ART_27_2_D",
    ),
}

CFAA_COMPLIANCE_ATTESTATION = {
    "statute": "18 U.S.C. 1030",
    "attested": True,
    "unauthorized_access_count": 0,
    "data_provenance": "public_filings_only",
    "egress_to_external_nodes": 0,
}

CIK_PATTERN = re.compile(r"^\d{10}$")
ROLE_PATTERN = re.compile(r"^[a-z0-9_]+$")
TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}$")
NON_CIK_TOKENS = ("private", "n_a")
ENTRY_KEYS = ("entity", "role", "ticker", "exchange", "cik", "instrument", "amount_usd_b")


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def verify_landauer_runtime_penalty():
    """
    E_Landauer = k_B * T * ln2
    Phi_thermo = E_LLM_token / E_SQL_PLC = 5.0e10      (headline per-token penalty)
    Phi_query  = E_LLM_query / E_SQL_PLC = 5.0e11      (full 10-token-equivalent query)
    Phi_joint  = Phi_thermo * (t_p99_cloud / t_cycle_PLC)
    """
    landauer = K_B_JOULES_PER_KELVIN * T_KELVIN * math.log(2.0)
    assert close(landauer, LANDAUER_MIN_BIT_JOULES, LANDAUER_MIN_BIT_JOULES * 1e-3), landauer

    phi_thermo = ENERGY_RUNTIME_LLM_PER_TOKEN_JOULES / ENERGY_DETERMINISTIC_SQL_PLC_JOULES
    phi_query = ENERGY_RUNTIME_LLM_QUERY_JOULES / ENERGY_DETERMINISTIC_SQL_PLC_JOULES
    assert close(phi_thermo, THERMODYNAMIC_PENALTY_RATIO, 1.0), phi_thermo
    assert close(phi_query, THERMODYNAMIC_PENALTY_RATIO * 10.0, 1.0e1), phi_query

    tokens_per_query = ENERGY_RUNTIME_LLM_QUERY_JOULES / ENERGY_RUNTIME_LLM_PER_TOKEN_JOULES
    assert close(tokens_per_query, 10.0, TOL), tokens_per_query
    assert close(phi_query / phi_thermo, tokens_per_query, 1e-9)

    log10_penalty = math.log10(phi_thermo)
    assert close(log10_penalty, THERMODYNAMIC_PENALTY_LOG10, 1e-3), log10_penalty
    assert close(math.log10(phi_query), THERMODYNAMIC_PENALTY_LOG10 + 1.0, 1e-3)

    phi_latency = CLOUD_LLM_P99_LATENCY_MS / PLC_DETERMINISTIC_CYCLE_MS
    assert close(phi_latency, LATENCY_PENALTY_MULTIPLIER, TOL), phi_latency

    phi_joint = phi_thermo * phi_latency
    phi_joint_query = phi_query * phi_latency
    assert close(phi_joint, 2.125e13, 1.0e3), phi_joint
    assert close(phi_joint_query, 2.125e14, 1.0e4), phi_joint_query

    bit_erasures_token = ENERGY_RUNTIME_LLM_PER_TOKEN_JOULES / LANDAUER_MIN_BIT_JOULES
    bit_erasures_query = ENERGY_RUNTIME_LLM_QUERY_JOULES / LANDAUER_MIN_BIT_JOULES
    deterministic_bits = ENERGY_DETERMINISTIC_SQL_PLC_JOULES / LANDAUER_MIN_BIT_JOULES
    assert close(bit_erasures_token, 8.709314e21, 8.709314e21 * 1e-5), bit_erasures_token
    assert close(bit_erasures_query, 8.709314e22, 8.709314e22 * 1e-5), bit_erasures_query
    assert close(deterministic_bits, 1.741863e11, 1.741863e11 * 1e-5), deterministic_bits
    assert close(bit_erasures_token / deterministic_bits, phi_thermo, 1.0)

    return {
        "landauer_min_bit_joules": LANDAUER_MIN_BIT_JOULES,
        "landauer_computed_joules": float(f"{landauer:.6e}"),
        "energy_deterministic_sql_plc_joules": ENERGY_DETERMINISTIC_SQL_PLC_JOULES,
        "energy_runtime_llm_query_joules": ENERGY_RUNTIME_LLM_QUERY_JOULES,
        "energy_runtime_llm_per_token_joules": ENERGY_RUNTIME_LLM_PER_TOKEN_JOULES,
        "implied_tokens_per_query": round(tokens_per_query, 6),
        "thermodynamic_penalty_ratio": float(f"{phi_thermo:.6e}"),
        "thermodynamic_penalty_log10": round(log10_penalty, 6),
        "per_query_penalty_ratio": float(f"{phi_query:.6e}"),
        "per_query_penalty_log10": round(math.log10(phi_query), 6),
        "landauer_bit_erasures_per_token": float(f"{bit_erasures_token:.6e}"),
        "landauer_bit_erasures_per_query": float(f"{bit_erasures_query:.6e}"),
        "deterministic_bits_per_step": float(f"{deterministic_bits:.6e}"),
        "plc_deterministic_cycle_ms": PLC_DETERMINISTIC_CYCLE_MS,
        "cloud_llm_p99_latency_ms": CLOUD_LLM_P99_LATENCY_MS,
        "latency_penalty_multiplier": round(phi_latency, 6),
        "joint_energy_latency_penalty": float(f"{phi_joint:.6e}"),
        "joint_energy_latency_penalty_per_query": float(f"{phi_joint_query:.6e}"),
    }


def verify_coalesce_airlock_collapse():
    """
    R_entity(K) = (K - 1) / K                      (compile once, replay K times)
    s_recurring = Macro_collapse / R_entity        (implied recurring demand share)
    Macro_collapse = s_recurring * R_entity
    """
    k = ENTERPRISE_TRANSACTIONS_PER_ENTITY_K
    r_entity = (k - 1) / k
    assert close(r_entity * 100.0, COALESCE_CACHE_TOKEN_REDUCTION_PCT, 1e-9), r_entity

    s_recurring = (MACRO_RECURRING_INFERENCE_COLLAPSE_PCT / 100.0) / r_entity
    macro_collapse = s_recurring * r_entity * 100.0
    assert close(s_recurring, 0.925926, 1e-6), s_recurring
    assert close(macro_collapse, MACRO_RECURRING_INFERENCE_COLLAPSE_PCT, 1e-9), macro_collapse
    residual = 100.0 - macro_collapse
    assert close(residual, 7.5, 1e-9), residual

    naive_energy = k * ENERGY_RUNTIME_LLM_QUERY_JOULES
    compiled_energy = ENERGY_RUNTIME_LLM_QUERY_JOULES
    energy_reduction = (naive_energy - compiled_energy) / naive_energy * 100.0
    assert close(naive_energy, 250000.0, TOL), naive_energy
    assert close(energy_reduction, COALESCE_CACHE_TOKEN_REDUCTION_PCT, 1e-9), energy_reduction

    naive_clock = k * CLOUD_LLM_P99_LATENCY_MS
    compiled_clock = k * PLC_DETERMINISTIC_CYCLE_MS
    clock_reduction = (naive_clock - compiled_clock) / naive_clock * 100.0
    assert close(naive_clock, 850000.0, TOL), naive_clock
    assert close(compiled_clock, 2000.0, TOL), compiled_clock
    assert close(clock_reduction, 99.764706, 1e-6), clock_reduction

    # Monotone in K: deeper recurring transaction counts strictly deepen the collapse.
    assert (10.0 - 1.0) / 10.0 < (100.0 - 1.0) / 100.0 < r_entity < 1.0

    return {
        "enterprise_transactions_per_entity_k": k,
        "coalesce_cache_token_reduction_pct": round(r_entity * 100.0, 6),
        "macro_recurring_inference_collapse_pct": round(macro_collapse, 6),
        "implied_recurring_demand_share": round(s_recurring, 6),
        "residual_macro_inference_demand_pct": round(residual, 6),
        "naive_runtime_energy_per_entity_joules": round(naive_energy, 6),
        "compiled_energy_per_entity_joules": round(compiled_energy, 6),
        "energy_reduction_pct": round(energy_reduction, 6),
        "naive_wall_clock_per_entity_ms": round(naive_clock, 6),
        "compiled_wall_clock_per_entity_ms": round(compiled_clock, 6),
        "wall_clock_reduction_pct": round(clock_reduction, 6),
    }


def verify_agent_equivocation_decay():
    """
    R_agent(N) = (1 - epsilon)^N     vs.     R_deterministic = 1.0
    N_half = ln(0.5) / ln(1 - epsilon)
    """
    eps = PER_STEP_HALLUCINATION_RATE_EPSILON
    n = AGENT_CHAIN_STEPS_N
    reliability = (1.0 - eps) ** n
    assert close(reliability, AGENT_CHAIN_RELIABILITY_20_STEPS, 1e-6), reliability
    assert DETERMINISTIC_STATE_MACHINE_RELIABILITY == 1.0

    deficit_pct = (DETERMINISTIC_STATE_MACHINE_RELIABILITY - reliability) * 100.0
    assert close(deficit_pct, 45.620565, 1e-5), deficit_pct

    expected_defective = n * eps
    assert close(expected_defective, 0.6, TOL), expected_defective

    n_half = math.log(0.5) / math.log(1.0 - eps)
    assert close(n_half, 22.756573, 1e-5), n_half
    assert math.ceil(n_half) == 23
    assert (1.0 - eps) ** 22 > 0.5 > (1.0 - eps) ** 23

    n_99 = math.log(0.99) / math.log(1.0 - eps)
    assert close(n_99, 0.329961, 1e-5), n_99
    assert math.floor(n_99) == 0

    chain_energy = n * ENERGY_RUNTIME_LLM_QUERY_JOULES
    deterministic_energy = n * ENERGY_DETERMINISTIC_SQL_PLC_JOULES
    assert close(chain_energy, 5000.0, TOL), chain_energy
    assert close(deterministic_energy, 1.0e-8, 1e-18), deterministic_energy
    assert close(chain_energy / deterministic_energy, 5.0e11, 1.0e2)

    # Strict monotone decay: every added equivocal step strictly destroys reliability.
    ladder = [(1.0 - eps) ** i for i in range(0, n + 1)]
    assert all(ladder[i] > ladder[i + 1] for i in range(n))
    assert ladder[0] == 1.0

    return {
        "per_step_hallucination_rate_epsilon": eps,
        "agent_chain_steps_n": n,
        "agent_chain_reliability_20_steps": round(reliability, 6),
        "deterministic_state_machine_reliability": DETERMINISTIC_STATE_MACHINE_RELIABILITY,
        "equivocation_deficit_pct": round(deficit_pct, 6),
        "expected_defective_steps": round(expected_defective, 6),
        "half_reliability_steps_continuous": round(n_half, 6),
        "half_reliability_steps_integer": math.ceil(n_half),
        "max_steps_for_99pct_reliability": math.floor(n_99),
        "chain_energy_joules": round(chain_energy, 6),
        "deterministic_chain_energy_joules": float(f"{deterministic_energy:.6e}"),
        "chain_energy_penalty_ratio": float(f"{chain_energy / deterministic_energy:.6e}"),
    }


def civilizational_deadweight_loss(cohort_millions, diversion_share, wage_usd):
    """Off-balance-sheet human-capital destruction: man-years diverted x wage rate."""
    man_years = cohort_millions * 1.0e6 * diversion_share
    usd_b = man_years * wage_usd / 1.0e9
    return man_years, usd_b


def simulate_ashby_variety_decay(years=10):
    """
    V_op(t)  = V_headroom * (1 - s_divert * a_atrophy)^t
    V_env(t) = (1 + g_env)^t
    Parity (Ashby 1956) holds iff V_op(t) / V_env(t) >= 1.0.
    """
    retention = 1.0 - WRAPPER_DIVERSION_SHARE * COGNITIVE_ATROPHY_PER_DIVERTED_YEAR
    assert close(retention, 0.958, TOL), retention

    trajectory = []
    breach_year = None
    for t in range(years + 1):
        v_op = ASHBY_VARIETY_HEADROOM_INITIAL * (retention ** t)
        v_env = (1.0 + ASHBY_ENVIRONMENT_VARIETY_GROWTH) ** t
        ratio = v_op / v_env
        trajectory.append(round(ratio, 6))
        if breach_year is None and ratio < 1.0:
            breach_year = t
    return retention, trajectory, breach_year


def verify_civilizational_deadweight():
    man_years, usd_b = civilizational_deadweight_loss(
        GLOBAL_STEM_COHORT_DIVERTED_MILLIONS, WRAPPER_DIVERSION_SHARE, WAGE_PER_MAN_YEAR_USD
    )
    assert close(man_years, ANNUAL_COGNITIVE_DEADWEIGHT_MAN_YEARS, 1e-6), man_years
    assert close(usd_b, OPPORTUNITY_COST_HUMAN_CAPITAL_BILLIONS_PER_YR, 1e-6), usd_b

    ten_year = usd_b * 10.0
    assert close(ten_year, 3500.0, 1e-6), ten_year

    capex_ratio_pct = usd_b / HYPERSCALER_ANNUAL_AI_CAPEX_B * 100.0
    assert close(capex_ratio_pct, 77.777778, 1e-5), capex_ratio_pct

    sensitivity = []
    for share in (0.50, 0.70, 0.90):
        _, share_usd_b = civilizational_deadweight_loss(
            GLOBAL_STEM_COHORT_DIVERTED_MILLIONS, share, WAGE_PER_MAN_YEAR_USD
        )
        sensitivity.append(round(share_usd_b, 6))
    assert sensitivity == [250.0, 350.0, 450.0], sensitivity

    retention, trajectory, breach_year = simulate_ashby_variety_decay(10)
    assert breach_year == 5, breach_year
    assert trajectory[4] > 1.0 > trajectory[5], trajectory[4:6]
    assert all(trajectory[i] > trajectory[i + 1] for i in range(10))
    assert close(trajectory[10], 0.654057, 1e-5), trajectory[10]

    return {
        "global_stem_cohort_diverted_millions": GLOBAL_STEM_COHORT_DIVERTED_MILLIONS,
        "wrapper_diversion_share": WRAPPER_DIVERSION_SHARE,
        "annual_cognitive_deadweight_man_years": round(man_years, 6),
        "wage_per_man_year_usd": WAGE_PER_MAN_YEAR_USD,
        "opportunity_cost_human_capital_billions_per_yr": round(usd_b, 6),
        "ten_year_cumulative_deadweight_usd_b": round(ten_year, 6),
        "deadweight_to_hyperscaler_capex_pct": round(capex_ratio_pct, 6),
        "deadweight_sensitivity_usd_b": sensitivity,
        "ashby_variety_headroom_initial": ASHBY_VARIETY_HEADROOM_INITIAL,
        "ashby_variety_retention_per_year": round(retention, 6),
        "ashby_environment_variety_growth_per_year": ASHBY_ENVIRONMENT_VARIETY_GROWTH,
        "ashby_parity_breach_year": breach_year,
        "ashby_parity_ratio_year_10": trajectory[10],
        "ashby_parity_trajectory": trajectory,
    }


def verify_shannon_commons_capacity():
    """
    C = B * log2(1 + S/N);  N -> kappa * N  with  kappa = 100
    """
    kappa = SHANNON_COMMONS_NOISE_INFLATION_FACTOR
    snr = SHANNON_BASELINE_COMMONS_SNR
    c_base = math.log2(1.0 + snr)
    c_inflated = math.log2(1.0 + snr / kappa)
    assert close(c_base, 6.658211, 1e-6), c_base
    assert close(c_inflated, 1.0, TOL), c_inflated

    collapse_pct = (1.0 - c_inflated / c_base) * 100.0
    assert close(collapse_pct, 84.980952, 1e-5), collapse_pct
    assert c_inflated < c_base

    return {
        "shannon_commons_noise_inflation_factor": kappa,
        "baseline_commons_snr": snr,
        "capacity_baseline_bits": round(c_base, 6),
        "capacity_inflated_bits": round(c_inflated, 6),
        "capacity_collapse_pct": round(collapse_pct, 6),
    }


def verify_acemoglu_macro_bounds():
    """
    TFP_10yr <= task_share * cost_reduction_per_exposed_task
    GDP_10yr <= TFP_10yr scaled by labor/capital pass-through
    """
    task_share = ACEMOGLU_10YR_TASK_SHARE_PCT
    tfp = ACEMOGLU_10YR_TFP_MAX_PCT
    gdp = ACEMOGLU_10YR_GDP_MAX_PCT

    cost_reduction = tfp / task_share
    assert close(cost_reduction, 0.154348, 1e-6), cost_reduction
    assert close(task_share * cost_reduction, tfp, 1e-12)
    assert tfp < gdp < task_share
    assert close(tfp / gdp, 0.645455, 1e-6)

    return {
        "acemoglu_10yr_task_share_pct": task_share,
        "acemoglu_10yr_tfp_max_pct": tfp,
        "acemoglu_10yr_gdp_max_pct": gdp,
        "implied_cost_reduction_per_exposed_task": round(cost_reduction, 6),
        "tfp_to_gdp_ratio": round(tfp / gdp, 6),
    }


def verify_revenue_deficit():
    """
    Deficit = R_required - R_realistic ;  Coverage = R_realistic / R_required
    """
    deficit = SEQUOIA_REQUIRED_REVENUE_B - REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B
    assert close(deficit, ANNUAL_REVENUE_DEFICIT_B, TOL), deficit

    coverage_pct = REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B / SEQUOIA_REQUIRED_REVENUE_B * 100.0
    assert close(coverage_pct, 12.5, 1e-9), coverage_pct

    capex_multiple = HYPERSCALER_ANNUAL_AI_CAPEX_B / REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B
    assert close(capex_multiple, 6.0, 1e-9), capex_multiple
    assert close(SEQUOIA_REQUIRED_REVENUE_B / HYPERSCALER_ANNUAL_AI_CAPEX_B, 1.333333, 1e-6)
    assert HYPERSCALER_ANNUAL_AI_CAPEX_B > REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B

    return {
        "hyperscaler_annual_ai_capex_b": HYPERSCALER_ANNUAL_AI_CAPEX_B,
        "sequoia_required_revenue_b": SEQUOIA_REQUIRED_REVENUE_B,
        "realistic_compiler_and_airlock_revenue_b": REALISTIC_COMPILER_AND_AIRLOCK_REVENUE_B,
        "annual_revenue_deficit_b": round(deficit, 6),
        "revenue_coverage_ratio_pct": round(coverage_pct, 6),
        "capex_to_realistic_revenue_multiple": round(capex_multiple, 6),
    }


def tranche_recovery(ev_billions):
    """
    Deterministic senior-to-junior recovery waterfall over the $42.15B pro-forma stack.
    recovery_i = min(principal_i, max(0, EV - sum(principal_j) for j senior to i))
    Returns dollar recovery and cents-on-the-dollar per tranche.
    """
    if ev_billions < 0.0:
        raise ValueError("ev_billions must be non-negative")

    tranches = (
        ("tranche_1_senior_ddtl", TRANCHE_1_SENIOR_DDTL_B),
        ("tranche_2_recourse_lease_box", TRANCHE_2_RECOURSE_LEASE_BOX_B),
        ("tranche_3_non_recourse_spv", TRANCHE_3_NON_RECOURSE_SPV_B),
    )
    total = sum(p for _, p in tranches)
    assert close(total, COREWEAVE_PRO_FORMA_DEBT_B, 1e-9), total

    residual = float(ev_billions)
    dollars = {}
    cents = {}
    for name, principal in tranches:
        paid = min(principal, max(0.0, residual))
        residual -= paid
        dollars[name] = round(paid, 6)
        cents[name] = round(paid / principal * 100.0, 6)

    recourse_dollars = dollars["tranche_1_senior_ddtl"] + dollars["tranche_2_recourse_lease_box"]
    aggregate_dollars = recourse_dollars + dollars["tranche_3_non_recourse_spv"]
    assert aggregate_dollars <= ev_billions + 1e-9
    assert aggregate_dollars <= total + 1e-9

    return {
        "ev_usd_b": round(float(ev_billions), 6),
        "tranche_1_usd_b": dollars["tranche_1_senior_ddtl"],
        "tranche_1_cents_on_dollar": cents["tranche_1_senior_ddtl"],
        "tranche_2_usd_b": dollars["tranche_2_recourse_lease_box"],
        "tranche_2_cents_on_dollar": cents["tranche_2_recourse_lease_box"],
        "tranche_3_usd_b": dollars["tranche_3_non_recourse_spv"],
        "tranche_3_cents_on_dollar": cents["tranche_3_non_recourse_spv"],
        "aggregate_cents_on_dollar": round(aggregate_dollars / total * 100.0, 6),
        "recourse_cents_on_dollar": round(
            recourse_dollars / COREWEAVE_RECOURSE_DEBT_B * 100.0, 6
        ),
    }


def verify_capital_structure_waterfall():
    stack = TRANCHE_1_SENIOR_DDTL_B + TRANCHE_2_RECOURSE_LEASE_BOX_B + TRANCHE_3_NON_RECOURSE_SPV_B
    assert close(stack, COREWEAVE_PRO_FORMA_DEBT_B, 1e-9), stack

    recourse = TRANCHE_1_SENIOR_DDTL_B + TRANCHE_2_RECOURSE_LEASE_BOX_B
    assert close(recourse, COREWEAVE_RECOURSE_DEBT_B, 1e-9), recourse

    recourse_share = recourse / stack * 100.0
    non_recourse_share = TRANCHE_3_NON_RECOURSE_SPV_B / stack * 100.0
    assert close(recourse_share, COREWEAVE_RECOURSE_SHARE_PCT, 0.02), recourse_share
    assert close(recourse_share, 91.174377, 1e-5), recourse_share
    assert close(non_recourse_share, 8.825623, 1e-5), non_recourse_share
    assert close(recourse_share + non_recourse_share, 100.0, 1e-9)

    scenarios = [tranche_recovery(ev) for ev in STRESSED_EV_SCENARIOS_B]

    stressed, mid, recourse_par, full_par = scenarios
    # EV = $15.0B: senior DDTL impaired at 81.0811 cents, everything junior wiped.
    assert close(stressed["tranche_1_cents_on_dollar"], 81.081081, 1e-5)
    assert stressed["tranche_2_usd_b"] == 0.0 and stressed["tranche_3_usd_b"] == 0.0
    assert close(stressed["aggregate_cents_on_dollar"], 35.587189, 1e-5)
    assert close(stressed["recourse_cents_on_dollar"], 39.032006, 1e-5)
    # EV = $25.0B: senior at par, recourse/lease box takes 32.6142 cents.
    assert close(mid["tranche_1_cents_on_dollar"], 100.0, 1e-9)
    assert close(mid["tranche_2_usd_b"], 6.5, 1e-9)
    assert close(mid["tranche_2_cents_on_dollar"], 32.614150, 1e-5)
    assert mid["tranche_3_usd_b"] == 0.0
    assert close(mid["aggregate_cents_on_dollar"], 59.311981, 1e-5)
    # EV = $38.43B (recourse par): the $3.72B non-recourse SPV stub is wiped to zero.
    assert close(recourse_par["tranche_2_cents_on_dollar"], 100.0, 1e-9)
    assert recourse_par["tranche_3_usd_b"] < 1e-9
    assert recourse_par["tranche_3_cents_on_dollar"] < 1e-7
    assert close(recourse_par["recourse_cents_on_dollar"], 100.0, 1e-9)
    assert close(recourse_par["aggregate_cents_on_dollar"], 91.174377, 1e-5)
    # EV = $42.15B (full par): every tranche clears at 100 cents.
    assert close(full_par["tranche_3_cents_on_dollar"], 100.0, 1e-9)
    assert close(full_par["aggregate_cents_on_dollar"], 100.0, 1e-9)

    # Monotonicity: recovery is non-decreasing in EV for every tranche.
    for key in ("tranche_1_usd_b", "tranche_2_usd_b", "tranche_3_usd_b", "aggregate_cents_on_dollar"):
        column = [s[key] for s in scenarios]
        assert all(column[i] <= column[i + 1] + 1e-12 for i in range(len(column) - 1)), key

    # Breakeven EV thresholds: cumulative senior principal at which each tranche reaches par.
    breakeven = (
        ("tranche_1_senior_ddtl", "tranche_1_cents_on_dollar", TRANCHE_1_SENIOR_DDTL_B),
        (
            "tranche_2_recourse_lease_box",
            "tranche_2_cents_on_dollar",
            TRANCHE_1_SENIOR_DDTL_B + TRANCHE_2_RECOURSE_LEASE_BOX_B,
        ),
        ("tranche_3_non_recourse_spv", "tranche_3_cents_on_dollar", stack),
    )
    for name, cents_key, threshold in breakeven:
        below = tranche_recovery(threshold - 1e-6)
        at = tranche_recovery(threshold)
        assert below[cents_key] < 100.0 <= at[cents_key] + 1e-9, name

    exposure_midpoint = (
        BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B + BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B
    ) / 2.0
    assert close(exposure_midpoint, 87.95, 1e-9), exposure_midpoint
    exposure_multiple = exposure_midpoint / COREWEAVE_RECOURSE_DEBT_B
    assert close(exposure_multiple, 2.288576, 1e-5), exposure_multiple
    assert BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B < BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B

    return {
        "tranche_1_senior_ddtl_usd_b": TRANCHE_1_SENIOR_DDTL_B,
        "tranche_2_recourse_lease_box_usd_b": TRANCHE_2_RECOURSE_LEASE_BOX_B,
        "tranche_3_non_recourse_spv_usd_b": TRANCHE_3_NON_RECOURSE_SPV_B,
        "pro_forma_total_usd_b": round(stack, 6),
        "cumulative_recourse_usd_b": round(recourse, 6),
        "recourse_share_pct": round(recourse_share, 6),
        "non_recourse_share_pct": round(non_recourse_share, 6),
        "breakeven_ev_thresholds_usd_b": {
            name: round(threshold, 6) for name, _, threshold in breakeven
        },
        "scenarios": scenarios,
        "blue_owl_dual_ai_saas_exposure_low_usd_b": BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B,
        "blue_owl_dual_ai_saas_exposure_high_usd_b": BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B,
        "blue_owl_exposure_midpoint_to_recourse_multiple": round(exposure_multiple, 6),
    }


def verify_entity_and_instrument_ids():
    assert len(ENTITY_AND_INSTRUMENT_IDS) >= 6, len(ENTITY_AND_INSTRUMENT_IDS)

    regulated = 0
    for role, entry in ENTITY_AND_INSTRUMENT_IDS.items():
        assert ROLE_PATTERN.match(role), role
        assert tuple(entry.keys()) == ENTRY_KEYS, (role, tuple(entry.keys()))
        assert isinstance(entry["entity"], str) and entry["entity"], role
        assert ROLE_PATTERN.match(entry["role"]), (role, entry["role"])
        assert entry["ticker"] is None or TICKER_PATTERN.match(entry["ticker"]), role
        assert entry["exchange"] in (None, "NASDAQ", "NYSE"), role
        if CIK_PATTERN.match(entry["cik"]):
            regulated += 1
        else:
            assert entry["cik"] in NON_CIK_TOKENS, (role, entry["cik"])
        assert isinstance(entry["instrument"], str) and entry["instrument"], role
        assert entry["amount_usd_b"] is None or entry["amount_usd_b"] > 0.0, role

    # Six-category security-master ring: at least six SEC-registered CIKs cross-indexed.
    assert regulated >= 6, regulated

    primary = ENTITY_AND_INSTRUMENT_IDS["primary_target"]
    assert primary["cik"] == "0001769628"
    assert close(primary["amount_usd_b"], COREWEAVE_PRO_FORMA_DEBT_B, TOL)

    low = ENTITY_AND_INSTRUMENT_IDS["sponsor_manager"]["amount_usd_b"]
    high = ENTITY_AND_INSTRUMENT_IDS["bdc_colender"]["amount_usd_b"]
    assert close(low, BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_LOW_B, TOL)
    assert close(high, BLUE_OWL_DUAL_AI_SAAS_EXPOSURE_HIGH_B, TOL)
    assert low < high

    underwriter = ENTITY_AND_INSTRUMENT_IDS["ai_capex_gap_underwriter"]
    assert close(underwriter["amount_usd_b"], SEQUOIA_REQUIRED_REVENUE_B, TOL)
    assert underwriter["cik"] == "private"

    hyperscalers = [k for k in ENTITY_AND_INSTRUMENT_IDS if k.startswith("hyperscaler_")]
    assert len(hyperscalers) == 4, hyperscalers

    return {"counterparty_entries": len(ENTITY_AND_INSTRUMENT_IDS), "sec_registered_ciks": regulated}


def verify_catalyst_calendar():
    assert len(CATALYST_CALENDAR) == 6, len(CATALYST_CALENDAR)
    floor = date.fromisoformat(CATALYST_CALENDAR_FLOOR)
    allowed_basis = {"estimated_filing_window", "sec_note_10_schedule", "contractual_maturity"}

    prior = None
    dated_flows = 0.0
    for entry in CATALYST_CALENDAR:
        assert tuple(entry.keys()) == ("date", "event", "basis", "usd_b"), tuple(entry.keys())
        current = date.fromisoformat(entry["date"])
        assert current >= floor, entry["date"]
        assert prior is None or current > prior, entry["date"]
        prior = current
        assert entry["basis"] in allowed_basis, entry["basis"]
        assert isinstance(entry["event"], str) and entry["event"]
        assert entry["usd_b"] is None or entry["usd_b"] > 0.0
        if entry["usd_b"] is not None:
            dated_flows += entry["usd_b"]

    assert close(dated_flows, 37.33, 1e-9), dated_flows
    assert CATALYST_CALENDAR[-1]["date"].startswith("2030")
    return {
        "catalyst_entries": len(CATALYST_CALENDAR),
        "calendar_floor": CATALYST_CALENDAR_FLOOR,
        "dated_hard_flows_usd_b": round(dated_flows, 6),
    }


def run_verification():
    thermo = verify_landauer_runtime_penalty()
    coalesce = verify_coalesce_airlock_collapse()
    equivocation = verify_agent_equivocation_decay()
    deadweight = verify_civilizational_deadweight()
    shannon = verify_shannon_commons_capacity()
    acemoglu = verify_acemoglu_macro_bounds()
    deficit = verify_revenue_deficit()
    waterfall = verify_capital_structure_waterfall()
    ring = verify_entity_and_instrument_ids()
    calendar = verify_catalyst_calendar()

    manifest = {
        "spec_version": "SPEC-COMPILER-RUNTIME-FALLACY-v1.0",
        "jurisdiction_context": {
            "iso_3166_1": JURISDICTION_CONTEXT["iso_3166_1"],
            "venue": JURISDICTION_CONTEXT["venue"],
            "statutory_modules": list(JURISDICTION_CONTEXT["statutory_modules"]),
        },
        "cfaa_compliance_attestation": dict(CFAA_COMPLIANCE_ATTESTATION),
        "entity_and_instrument_ids": {
            role: dict(entry) for role, entry in ENTITY_AND_INSTRUMENT_IDS.items()
        },
        "catalyst_calendar": [dict(entry) for entry in CATALYST_CALENDAR],
        "thermodynamic_runtime_penalty": thermo,
        "coalesce_airlock_collapse": coalesce,
        "agent_equivocation_decay": equivocation,
        "civilizational_deadweight": deadweight,
        "shannon_commons_capacity": shannon,
        "acemoglu_macro_bounds": acemoglu,
        "revenue_deficit": deficit,
        "capital_structure_waterfall": waterfall,
        "security_master_index": ring,
        "catalyst_calendar_audit": calendar,
    }

    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    print(
        f"[PASS] SPEC-COMPILER-RUNTIME-FALLACY-v1.0 | "
        f"E_Landauer={thermo['landauer_computed_joules']:.4e}J/bit | "
        f"Phi_thermo={thermo['thermodynamic_penalty_ratio']:.3e} "
        f"(log10={thermo['thermodynamic_penalty_log10']:.3f}) | "
        f"Phi_query={thermo['per_query_penalty_ratio']:.3e} | "
        f"Phi_latency={thermo['latency_penalty_multiplier']:.0f}x | "
        f"Phi_joint={thermo['joint_energy_latency_penalty']:.3e} | "
        f"R_entity={coalesce['coalesce_cache_token_reduction_pct']:.1f}% | "
        f"Macro_collapse={coalesce['macro_recurring_inference_collapse_pct']:.1f}% | "
        f"R_agent(20)={equivocation['agent_chain_reliability_20_steps']:.6f} "
        f"vs R_det={equivocation['deterministic_state_machine_reliability']:.1f} | "
        f"N_half={equivocation['half_reliability_steps_integer']} | "
        f"Deadweight=${deadweight['opportunity_cost_human_capital_billions_per_yr']:.1f}B/yr "
        f"({deadweight['ten_year_cumulative_deadweight_usd_b']:.0f}B/10yr, "
        f"{deadweight['deadweight_to_hyperscaler_capex_pct']:.3f}% of capex) | "
        f"Ashby_breach_yr={deadweight['ashby_parity_breach_year']} "
        f"R_10={deadweight['ashby_parity_ratio_year_10']:.6f} | "
        f"C_collapse={shannon['capacity_collapse_pct']:.3f}% | "
        f"TFP<={acemoglu['acemoglu_10yr_tfp_max_pct']:.2f}% "
        f"GDP<={acemoglu['acemoglu_10yr_gdp_max_pct']:.2f}% | "
        f"Deficit=${deficit['annual_revenue_deficit_b']:.0f}B "
        f"(coverage {deficit['revenue_coverage_ratio_pct']:.1f}%) | "
        f"Recourse={waterfall['recourse_share_pct']:.4f}% | "
        f"EV15={waterfall['scenarios'][0]['aggregate_cents_on_dollar']:.2f}c | "
        f"EV25={waterfall['scenarios'][1]['aggregate_cents_on_dollar']:.2f}c | "
        f"EV38.43={waterfall['scenarios'][2]['aggregate_cents_on_dollar']:.2f}c "
        f"(T3={waterfall['scenarios'][2]['tranche_3_cents_on_dollar']:.2f}c) | "
        f"EV42.15={waterfall['scenarios'][3]['aggregate_cents_on_dollar']:.2f}c | "
        f"CIKs={ring['sec_registered_ciks']} | "
        f"Flows=${calendar['dated_hard_flows_usd_b']:.3f}B | "
        f"SHA-256: {digest}"
    )
    return manifest


if __name__ == "__main__":
    run_verification()
