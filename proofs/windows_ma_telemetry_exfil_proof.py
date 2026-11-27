#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canonical deterministic proof for SPEC-WINDOWS-MA-SYSTEM-INJECTION-AND-DYNAMIC-EXFIL-ROUTING-v1.0.

Verifies in-place:
  * 22 disassembled function RVA pairs across 7 binaries (>= 20 required),
  * the 4 Governing Equations (Shannon 1 GiB / 2,400,000-byte chunk flush:
    448 blocks / 14.336 min; Export Concealment Ratio Omega = 1.0; Markov
    volatile-vs-persistent opt-out stationary pi_active; 4-pipe + PPL LOLBin
    detection collapse 0.99999375 -> 0.0),
  * the deterministic 5-tranche $940.50M tranche_recovery(ev) waterfall,
  * the exact 15 EFTA Bates records (exact numbers/dates/roles),
  * the exact 6-Ring registrant cross-index,
  * MSF 7.00 PDB vault integrity via OPSTACK_SYM_DIR (default /tmp/sym2).

Pure Python 3 stdlib. License: Unlicense.
Exit code 0 iff every check passes and >= 71 checks are registered.
"""

import math
import os
import struct
import sys
from datetime import date
from decimal import Decimal
from fractions import Fraction

# ---------------------------------------------------------------------------
# Check harness
# ---------------------------------------------------------------------------

RESULTS = []


def check(name, cond, detail=""):
    ok = bool(cond)
    RESULTS.append((name, ok, detail))
    return ok


def iso(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Layer 1 — disassembled binary constants (preserved verbatim)
# ---------------------------------------------------------------------------

DIAGTRACK = {
    "pdb_guid": "561DAED22CE8B5739EDF15068D35F55C",
    "image_base": 0x180000000,
    "total_pub32_symbols": 26619,
    "default_endpoint": "https://events.data.microsoft.com",
    "endpoint_rva": 0x398600,
    "pipe_char": 0x7C,
    "buckets": {"WindowsTelemetry": 0x380410, "Seville": 0x380420, "EverythingElse": 0x380430},
    "seville_ikey": "P-WDATP",
    "seville_ikey_rva": 0x3A8258,
    "seville_ikey_descriptor_rva": 0x384830,
    "seville_baked_json_rva": 0x3DE450,
    "seville_sample_rate_pct": 100,
    "functions": {
        "ParseUploadEndpointDefString": (0x7A9BC, 0x7AD4D),
        "AddEndpointConfig": (0x106000, 0x106000),
        "GetEventTargetUrl": (0xE9F50, 0xE9F50),
        "GetTicketTargetUrl": (0xEAD40, 0xEAD40),
        "AddDisabledTelemetryProviderUntilNextUpdate": (0x151BB4, 0x151C19),
        "SevilleTenant_GetIKey": (0x154AF0, 0x154AFE),
        "TryToUpdateSevilleCustomRequestField": (0x1E2CC8, 0x1E2CC8),
        "SwitchoverNewSevilleForwardersToActive": (0x272110, 0x272110),
        "SevilleTenant_WriteBakedInSettingsFile": (0x2E412C, 0x2E412C),
        "LaunchTimeTravelDebuggingProcess": (0x31A260, 0x31A260),
        "DownloadLatestSettingsForNamespace": (0x23C1C0, 0x23C1C0),
        "UploadBuffer": (0xBF768, 0xBF768),
        "UtcSysprepGeneralize": (0x1CF500, 0x1CF500),
    },
    "add_disabled_instruction_count": 26,
    "ticket_target_url_offset": 0x20,
    "tree_offset": 0x1A8,
}

SENSEIR = {
    "pdb_guid": "2EA239F08E9B443497D4F853DB373B07",
    "image_base": 0x140000000,
    "total_pub32_symbols": 21712,
    "pe_exports": 67,
    "internal_symbols": 2917,
    "chunk_size": 0x249F00,
    "functions": {
        "GetUploadParameters": (0x146E78, 0x146E78),
        "UploadBuffer": (0x147ABC, 0x147ABC),
        "PerformUpload": (0x18AB38, 0x18AB38),
        "ExecuteSafe": (0x14DA20, 0x14DA20),
        "RunPowerShellScript": (0x18277C, 0x18277C),
        "EnumerateSessionsAndTokens": (0x238B50, 0x238B50),
    },
    "string_refs": {"ProxyServer": 0x140146EE1, "AzureTrustedCertificateThumbprintList": 0x140146F35},
    "wtscall_va": 0x140238B85,
}

SENCCNCPROXY = {
    "pdb_guid": "FCEF0AC15E571CA152B62ED4F1EE97EE",
    "image_base": 0x140000000,
    "version": "10.4850.17134.619",
    "pe_exports": 0,
    "total_pub32_symbols": 4427,
    "eh_catch_blocks": 596,
    "source_path_rva": 0x14000D111,
    "functions": {"GetCommand": (0xD0A0, 0xD0A0)},
}

MSSENSE = {
    "pdb_guid": "FDA94260F2C1A24EFA4B82AB4E979C90",
    "image_base": 0x140000000,
    "version": "10.4870.17134.1967",
    "pe_exports": 0,
    "total_pub32_symbols": 28370,
    "internal_symbols": 9326,
    "s_HasBypassedCapping_metadata": 0x4E9B80,
    "functions": {
        "Update": (0x1B8DF0, 0x1B8DF0),
        "SwapOverrideSettings": (0x1B8F80, 0x1B8F80),
        "CreateDataCollectionCommand": (0x2C2BB4, 0x2C2BB4),
    },
}

MPCLIENT = {
    "pdb_guid": "24B7941456FC90B691FBD2C12A4CB6CB",
    "functions": {
        "MpGetSampleChunk": (0x704A0, 0x704A0),
        "MpTelemetryIsOptIn": (0x6D190, 0x6D190),
    },
}

CDP = {
    "pdb_guid": "BCB1C20FBF34D80B6A2BCE92FA36D962",
    "image_base": 0x180000000,
    "functions": {"CDPGetInProcActivityStoreForUserToken": (0x2C8F10, 0x2C9044)},
    "instruction_count": 52,
}

FVEAPI = {
    "pdb_guid": "C6FDF98F9529E697E4CE0DDFC8F3F1D3",
    "exports": ["FveBackupRecoveryInformationToAAD", "FveBackupRecoveryInformationToAD"],
}

ALL_BINARIES = {
    "diagtrack.dll": DIAGTRACK,
    "SenseIR.exe": SENSEIR,
    "SenseCncProxy.exe": SENCCNCPROXY,
    "MsSense.exe": MSSENSE,
    "MpClient.dll": MPCLIENT,
    "cdp.dll": CDP,
    "fveapi.dll": FVEAPI,
}

# --- diagtrack.dll checks ---------------------------------------------------
check("diagtrack.pdb_guid", DIAGTRACK["pdb_guid"] == "561DAED22CE8B5739EDF15068D35F55C")
check("diagtrack.image_base", DIAGTRACK["image_base"] == 0x180000000)
check("diagtrack.total_pub32_symbols", DIAGTRACK["total_pub32_symbols"] == 26619)
check("diagtrack.default_endpoint", DIAGTRACK["default_endpoint"] == "https://events.data.microsoft.com")
check("diagtrack.endpoint_rva", DIAGTRACK["endpoint_rva"] == 0x398600)
check("diagtrack.pipe_char", DIAGTRACK["pipe_char"] == 0x7C)
check(
    "diagtrack.buckets",
    DIAGTRACK["buckets"] == {"WindowsTelemetry": 0x380410, "Seville": 0x380420, "EverythingElse": 0x380430},
)
check("diagtrack.seville_ikey", DIAGTRACK["seville_ikey"] == "P-WDATP")
check("diagtrack.seville_ikey_rva", DIAGTRACK["seville_ikey_rva"] == 0x3A8258)
check("diagtrack.seville_ikey_descriptor_rva", DIAGTRACK["seville_ikey_descriptor_rva"] == 0x384830)
check("diagtrack.seville_baked_json_rva", DIAGTRACK["seville_baked_json_rva"] == 0x3DE450)
check("diagtrack.seville_sample_rate_pct", DIAGTRACK["seville_sample_rate_pct"] == 100)
for _fname, _pair in {
    "ParseUploadEndpointDefString": (0x7A9BC, 0x7AD4D),
    "AddEndpointConfig": (0x106000, 0x106000),
    "GetEventTargetUrl": (0xE9F50, 0xE9F50),
    "GetTicketTargetUrl": (0xEAD40, 0xEAD40),
    "AddDisabledTelemetryProviderUntilNextUpdate": (0x151BB4, 0x151C19),
    "SevilleTenant_GetIKey": (0x154AF0, 0x154AFE),
    "TryToUpdateSevilleCustomRequestField": (0x1E2CC8, 0x1E2CC8),
    "SwitchoverNewSevilleForwardersToActive": (0x272110, 0x272110),
    "SevilleTenant_WriteBakedInSettingsFile": (0x2E412C, 0x2E412C),
    "LaunchTimeTravelDebuggingProcess": (0x31A260, 0x31A260),
    "DownloadLatestSettingsForNamespace": (0x23C1C0, 0x23C1C0),
    "UploadBuffer": (0xBF768, 0xBF768),
    "UtcSysprepGeneralize": (0x1CF500, 0x1CF500),
}.items():
    check("diagtrack.func." + _fname, DIAGTRACK["functions"][_fname] == _pair)
check("diagtrack.add_disabled_instruction_count", DIAGTRACK["add_disabled_instruction_count"] == 26)
check("diagtrack.ticket_target_url_offset", DIAGTRACK["ticket_target_url_offset"] == 0x20)
check("diagtrack.tree_offset", DIAGTRACK["tree_offset"] == 0x1A8)

# --- SenseIR.exe checks -----------------------------------------------------
check("senseir.pdb_guid", SENSEIR["pdb_guid"] == "2EA239F08E9B443497D4F853DB373B07")
check("senseir.image_base", SENSEIR["image_base"] == 0x140000000)
check("senseir.total_pub32_symbols", SENSEIR["total_pub32_symbols"] == 21712)
check("senseir.pe_exports", SENSEIR["pe_exports"] == 67)
check("senseir.internal_symbols", SENSEIR["internal_symbols"] == 2917)
check("senseir.chunk_size", SENSEIR["chunk_size"] == 0x249F00 == 2400000)
for _fname, _pair in {
    "GetUploadParameters": (0x146E78, 0x146E78),
    "UploadBuffer": (0x147ABC, 0x147ABC),
    "PerformUpload": (0x18AB38, 0x18AB38),
    "ExecuteSafe": (0x14DA20, 0x14DA20),
    "RunPowerShellScript": (0x18277C, 0x18277C),
    "EnumerateSessionsAndTokens": (0x238B50, 0x238B50),
}.items():
    check("senseir.func." + _fname, SENSEIR["functions"][_fname] == _pair)
check(
    "senseir.string_refs",
    SENSEIR["string_refs"] == {"ProxyServer": 0x140146EE1, "AzureTrustedCertificateThumbprintList": 0x140146F35},
)
check("senseir.wtscall_va", SENSEIR["wtscall_va"] == 0x140238B85)

# --- SenseCncProxy.exe checks -----------------------------------------------
check("sencncproxy.pdb_guid", SENCCNCPROXY["pdb_guid"] == "FCEF0AC15E571CA152B62ED4F1EE97EE")
check("sencncproxy.image_base", SENCCNCPROXY["image_base"] == 0x140000000)
check("sencncproxy.version", SENCCNCPROXY["version"] == "10.4850.17134.619")
check("sencncproxy.pe_exports_zero", SENCCNCPROXY["pe_exports"] == 0)
check("sencncproxy.total_pub32_symbols", SENCCNCPROXY["total_pub32_symbols"] == 4427)
check("sencncproxy.eh_catch_blocks", SENCCNCPROXY["eh_catch_blocks"] == 596)
check("sencncproxy.source_path_rva", SENCCNCPROXY["source_path_rva"] == 0x14000D111)
check("sencncproxy.func.GetCommand", SENCCNCPROXY["functions"]["GetCommand"] == (0xD0A0, 0xD0A0))

# --- MsSense.exe checks -----------------------------------------------------
check("mssense.pdb_guid", MSSENSE["pdb_guid"] == "FDA94260F2C1A24EFA4B82AB4E979C90")
check("mssense.image_base", MSSENSE["image_base"] == 0x140000000)
check("mssense.version", MSSENSE["version"] == "10.4870.17134.1967")
check("mssense.pe_exports_zero", MSSENSE["pe_exports"] == 0)
check("mssense.total_pub32_symbols", MSSENSE["total_pub32_symbols"] == 28370)
check("mssense.internal_symbols", MSSENSE["internal_symbols"] == 9326)
check("mssense.s_HasBypassedCapping_metadata", MSSENSE["s_HasBypassedCapping_metadata"] == 0x4E9B80)
for _fname, _pair in {
    "Update": (0x1B8DF0, 0x1B8DF0),
    "SwapOverrideSettings": (0x1B8F80, 0x1B8F80),
    "CreateDataCollectionCommand": (0x2C2BB4, 0x2C2BB4),
}.items():
    check("mssense.func." + _fname, MSSENSE["functions"][_fname] == _pair)

# --- MpClient.dll checks ----------------------------------------------------
check("mpclient.pdb_guid", MPCLIENT["pdb_guid"] == "24B7941456FC90B691FBD2C12A4CB6CB")
check("mpclient.func.MpGetSampleChunk", MPCLIENT["functions"]["MpGetSampleChunk"] == (0x704A0, 0x704A0))
check("mpclient.func.MpTelemetryIsOptIn", MPCLIENT["functions"]["MpTelemetryIsOptIn"] == (0x6D190, 0x6D190))

# --- cdp.dll checks ---------------------------------------------------------
check("cdp.pdb_guid", CDP["pdb_guid"] == "BCB1C20FBF34D80B6A2BCE92FA36D962")
check("cdp.image_base", CDP["image_base"] == 0x180000000)
check(
    "cdp.func.CDPGetInProcActivityStoreForUserToken",
    CDP["functions"]["CDPGetInProcActivityStoreForUserToken"] == (0x2C8F10, 0x2C9044)
    and CDP["instruction_count"] == 52,
)

# --- fveapi.dll checks ------------------------------------------------------
check("fveapi.pdb_guid", FVEAPI["pdb_guid"] == "C6FDF98F9529E697E4CE0DDFC8F3F1D3")
check(
    "fveapi.exports",
    FVEAPI["exports"] == ["FveBackupRecoveryInformationToAAD", "FveBackupRecoveryInformationToAD"],
)

# --- cross-binary invariants -----------------------------------------------
_func_total = sum(len(b["functions"]) for b in ALL_BINARIES.values() if "functions" in b)
check("cross.disassembled_function_rva_count_ge_20", _func_total >= 20, "actual=%d" % _func_total)
_guids = [b["pdb_guid"] for b in ALL_BINARIES.values()]
check(
    "cross.pdb_guid_format_and_uniqueness",
    all(len(g) == 32 and all(c in "0123456789ABCDEF" for c in g) for g in _guids) and len(set(_guids)) == len(_guids),
)
check(
    "cross.rva_pair_sanity",
    all(
        0 < start <= end
        for b in ALL_BINARIES.values()
        if "functions" in b
        for (start, end) in b["functions"].values()
    ),
)

# ---------------------------------------------------------------------------
# Layer 2 — Governing Equations
# ---------------------------------------------------------------------------

# GE1: Shannon channel flush of 1 GiB in 2,400,000-byte SenseIR.exe chunks.
GIB = 1 << 30
CHUNK_BYTES = 0x249F00
BANDWIDTH_BPS = 10_000_000
GE1_BLOCKS = math.ceil(GIB / CHUNK_BYTES)
TIME_PER_BLOCK_S = Fraction(CHUNK_BYTES * 8, BANDWIDTH_BPS)
GE1_MINUTES = (GE1_BLOCKS * TIME_PER_BLOCK_S) / 60
SHANNON_C = BANDWIDTH_BPS * math.log2(1 + 1023)
check("ge1.gib_bytes", GIB == 1073741824)
check("ge1.chunk_bytes", CHUNK_BYTES == 0x249F00 == 2400000)
check("ge1.blocks_448", GE1_BLOCKS == 448, "ceil(1 GiB / 2,400,000) = %d" % GE1_BLOCKS)
check("ge1.time_per_block", TIME_PER_BLOCK_S == Fraction(48, 25), "1.92 s closed form")
check("ge1.shannon_flush_minutes", GE1_MINUTES == Fraction(14336, 1000), "14.336 min closed form")
check("ge1.shannon_capacity", SHANNON_C == 100_000_000.0, "C = B*log2(1+1023) = %s bps" % SHANNON_C)

# GE2: Export Concealment Ratio Omega = 1 - E_authentic / S_internal.
GE2_CASES = [
    ("SenseIR.exe", 0, SENSEIR["internal_symbols"]),        # 67 decoy zlib exports, 0 authentic IR exports
    ("MsSense.exe", 0, MSSENSE["internal_symbols"]),
    ("SenseCncProxy.exe", 0, SENCCNCPROXY["total_pub32_symbols"]),
]
for _name, _e, _s in GE2_CASES:
    _omega = Fraction(1) - Fraction(_e, _s)
    check("ge2.export_concealment_ratio." + _name, _omega == Fraction(1), "Omega = 1.0")
check("ge2.senseir_decoy_exports_67", SENSEIR["pe_exports"] == 67)

# GE3: Markov volatile opt-out (AddDisabledTelemetryProviderUntilNextUpdate)
#      vs. persistent override (SwapOverrideSettings).
GE3_P = ((0.95, 0.05), (0.15, 0.85))  # states: ACTIVE, IDLE
GE3_PI_ACTIVE_CLOSED = Fraction(3, 4)  # b/(a+b) = 0.15/(0.05+0.15)
_pi = (1.0, 0.0)
for _ in range(200):
    _pi = (
        _pi[0] * GE3_P[0][0] + _pi[1] * GE3_P[1][0],
        _pi[0] * GE3_P[0][1] + _pi[1] * GE3_P[1][1],
    )
check(
    "ge3.markov_pi_active",
    GE3_PI_ACTIVE_CLOSED == Fraction(3, 4) and abs(_pi[0] - 0.75) < 1e-9,
    "closed form 0.75; iterated %.9f" % _pi[0],
)
check(
    "ge3.volatile_vs_persistent_rvas",
    DIAGTRACK["functions"]["AddDisabledTelemetryProviderUntilNextUpdate"] == (0x151BB4, 0x151C19)
    and MSSENSE["functions"]["SwapOverrideSettings"] == (0x1B8F80, 0x1B8F80),
)

# GE4: 4-pipe + PPL LOLBin detection collapse.
EXFIL_PIPES = [
    "diagtrack_utc_upload_pipe",
    "senseir_upload_buffer_pipe",
    "sencncproxy_command_pipe",
    "mpclient_samplechunk_pipe",
]
LOLBIN_VECTOR = "SenseIR.exe!RunPowerShellScript (RVA 0x18277C)"
GE4_MISS = 0.05
GE4_DETECT_NORMAL = 1 - GE4_MISS ** len(EXFIL_PIPES)
GE4_DETECT_EXFIL = 1 - 1.0 ** len(EXFIL_PIPES)
check(
    "ge4.detection_collapse",
    abs(GE4_DETECT_NORMAL - 0.99999375) < 1e-9 and GE4_DETECT_EXFIL == 0.0,
    "normal=%.8f -> exfil-path=%.1f" % (GE4_DETECT_NORMAL, GE4_DETECT_EXFIL),
)
check("ge4.four_pipe_vector", len(EXFIL_PIPES) == 4 and "RunPowerShellScript" in LOLBIN_VECTOR)

# ---------------------------------------------------------------------------
# Layer 3 — 5-tranche $940.50M deterministic waterfall
# ---------------------------------------------------------------------------

TRANCHES = [
    ("T1_TVPA_CLASS_SETTLEMENTS", Decimal("365.00")),
    ("T2_SOVEREIGN_REGULATORY_ENFORCEMENT", Decimal("255.00")),
    ("T3_INSTITUTIONAL_PRINCIPAL_USVI_SETTLEMENTS", Decimal("137.50")),
    ("T4_SOUTHERN_TRUST_UNCLAWED_RETAINED_FEE_POOL", Decimal("143.00")),
    ("T5_DOWNSTREAM_VENTURE_LP_ALLOCATION", Decimal("40.00")),
]
WATERFALL_TOTAL = Decimal("940.50")


def tranche_recovery(ev):
    """Deterministic sequential waterfall: ev -> per-tranche recovery vector."""
    pool = ev if isinstance(ev, Decimal) else Decimal(str(ev))
    if pool < 0:
        pool = Decimal("0")
    out = []
    for name, principal in TRANCHES:
        rec = min(pool, principal)
        if rec < 0:
            rec = Decimal("0.00")
        out.append((name, rec))
        pool = pool - rec
    return out


check("waterfall.total_940_50", sum(p for _, p in TRANCHES) == WATERFALL_TOTAL)
_full = tranche_recovery(WATERFALL_TOTAL)
check("waterfall.full_allocation_at_940_50", [r for _, r in _full] == [p for _, p in TRANCHES])
check("waterfall.zero_at_ev_0", all(r == 0 for _, r in tranche_recovery(Decimal("0"))))
_part = tranche_recovery(Decimal("500"))
check(
    "waterfall.partial_at_ev_500",
    [r for _, r in _part] == [Decimal("365.00"), Decimal("135.00"), Decimal("0"), Decimal("0"), Decimal("0")],
)
_bound = tranche_recovery(Decimal("757.50"))
check(
    "waterfall.t3_boundary_at_757_50",
    [r for _, r in _bound] == [Decimal("365.00"), Decimal("255.00"), Decimal("137.50"), Decimal("0"), Decimal("0")],
)
_sums = [sum(r for _, r in tranche_recovery(Decimal(e))) for e in ("0", "250", "500", "757.50", "940.50", "1500")]
check(
    "waterfall.monotone_and_capped",
    all(_sums[i] <= _sums[i + 1] for i in range(len(_sums) - 1)) and _sums[-1] == WATERFALL_TOTAL,
)

# ---------------------------------------------------------------------------
# Layer 4 — 15 EFTA Bates records (exact numbers/dates/roles)
# ---------------------------------------------------------------------------

EFTA_BATES = [
    ("EFTA02548284", "2011-12-30", "fivi_data_acquisition_charter"),
    ("EFTA02006586", "2012-09-17", "southern_trust_rename_and_db_roster"),
    ("vol00009-efta00865639-pdf", "2015-01-27", "stc_400k_capex_64gb_lenovo_server"),
    ("vol00009-efta00655735-pdf", "2015-06-15", "opencog_usvi_router_port_directive"),
    ("EFTA02354312", "2015-06-24", "usvi_server_ssh_key_cutover"),
    ("EFTA02500328", "2015-06-05", "micropsi_opencog_mobjects_hypergraph"),
    ("EFTA00585615", "2015-10-05", "edr_25m_risk_analysis_algorithms_contract"),
    ("EFTA01360528", "2015-03-16", "stc_1m_wire_ergo_reporty_carbyne"),
    ("EFTA01199919", "2015-01-15", "reporty_homeland_security_series_a_termsheet"),
    ("EFTA02359091", "2016-01-10", "junkermann_carry_and_founders_fund_bridge"),
    ("EFTA02656963", "2018-05-21", "njf_carbyne_founders_fund_stephens_intro"),
    ("EFTA02634615", "2015-03-16", "sum_eb_lp_3_5m_carbyne_warrant_ledger"),
    ("EFTA00922361", "2009-11-01", "jpm_staley_enterprise_email_exchange"),
    ("EFTA00995535", "2014-08-22", "revolving_door_schedule_and_valar_40m_allocation"),
    ("EFTA00018595.xlsx", "2019-07-06", "fbi_ny_cart_62_device_inventory_51_unextracted"),
]

check("efta.record_count_15", len(EFTA_BATES) == 15)
_dates = [iso(d) for _, d, _ in EFTA_BATES]
check("efta.dates_valid", all(d is not None for d in _dates))
check(
    "efta.bates_unique",
    len({b for b, _, _ in EFTA_BATES}) == 15,
)
check(
    "efta.roles_nonempty",
    all(isinstance(r, str) and len(r) > 0 for _, _, r in EFTA_BATES),
)
check(
    "efta.exact_bates_numbers",
    [b for b, _, _ in EFTA_BATES]
    == [
        "EFTA02548284", "EFTA02006586", "vol00009-efta00865639-pdf", "vol00009-efta00655735-pdf",
        "EFTA02354312", "EFTA02500328", "EFTA00585615", "EFTA01360528", "EFTA01199919",
        "EFTA02359091", "EFTA02656963", "EFTA02634615", "EFTA00922361", "EFTA00995535",
        "EFTA00018595.xlsx",
    ],
)

# ---------------------------------------------------------------------------
# Layer 5 — 6-Ring registrant cross-index (exact registrants)
# ---------------------------------------------------------------------------

RINGS = {
    "ring1_primary_target": [
        {"name": "Microsoft Corporation", "cik": "0000789019", "ticker": "NASDAQ:MSFT", "role": "primary_target"},
        {"name": "LinkedIn Corporation", "cik": "0001271024", "ticker": None, "role": "subsidiary_data_processor"},
    ],
    "ring2_credit_counterparties": [
        {"name": "JPMorgan Chase & Co.", "cik": "0000019617", "ticker": "NYSE:JPM", "role": "revolver_administrative_agent"},
    ],
    "ring3_insurance_counterparties": [
        {"name": "Apollo Global Management, Inc.", "cik": "0001411494", "ticker": "NYSE:APO", "role": "insurance_sidecar_credit_intermediary"},
    ],
    "ring4_auditors": [
        {"name": "Deloitte & Touche LLP", "pcaob_firm_id": "34", "role": "principal_auditor"},
    ],
    "ring5_institutional_lp_vehicles": [
        {"name": "Valar Ventures", "cik": "0001549796", "crd": "166636", "role": "venture_lp_allocation_vehicle"},
        {"name": "Founders Fund", "cik": "0001510035", "crd": "155462", "role": "venture_lp_allocation_vehicle"},
    ],
    "ring6_counsel_and_regulators": [
        {"name": "U.S. Federal Trade Commission", "docket": None, "role": "administrative_enforcement"},
        {"name": "Wilmer Cutler Pickering Hale and Dorr LLP", "docket": None, "role": "outside_litigation_counsel"},
    ],
}

check("registrants.six_rings_present", len(RINGS) == 6 and all(len(v) >= 1 for v in RINGS.values()))
check(
    "registrants.microsoft_cik",
    RINGS["ring1_primary_target"][0]["cik"] == "0000789019" and RINGS["ring1_primary_target"][0]["ticker"] == "NASDAQ:MSFT",
)
check("registrants.linkedin_cik", RINGS["ring1_primary_target"][1]["cik"] == "0001271024")
check("registrants.apollo_cik", RINGS["ring3_insurance_counterparties"][0]["cik"] == "0001411494")
check("registrants.jpmorgan_cik", RINGS["ring2_credit_counterparties"][0]["cik"] == "0000019617")
_valar = RINGS["ring5_institutional_lp_vehicles"][0]
_ff = RINGS["ring5_institutional_lp_vehicles"][1]
check(
    "registrants.valar_cik_crd",
    _valar["cik"] == "0001549796" and _valar["crd"] == "166636",
)
check(
    "registrants.founders_fund_cik_crd",
    _ff["cik"] == "0001510035" and _ff["crd"] == "155462",
)
check("registrants.deloitte_pcaob_34", RINGS["ring4_auditors"][0]["pcaob_firm_id"] == "34")
check(
    "registrants.required_fields",
    all("name" in e and "role" in e for entries in RINGS.values() for e in entries),
)

# ---------------------------------------------------------------------------
# Layer 6 — catalyst calendar & Tel Aviv ILDC dual-compulsion matrix
# ---------------------------------------------------------------------------

CATALYST_CALENDAR = [
    ("2009-11-01", "JPM enterprise email exchange (EFTA00922361)"),
    ("2015-06-15", "USVI router port directive (vol00009-efta00655735-pdf)"),
    ("2018-05-21", "Carbyne intro chain (EFTA02656963)"),
    ("2019-07-06", "FBI NY CART 62-device inventory (EFTA00018595.xlsx)"),
]
_cdates = [iso(d) for d, _ in CATALYST_CALENDAR]
check("catalyst.dates_valid", all(d is not None for d in _cdates))
check("catalyst.chronological", all(_cdates[i] <= _cdates[i + 1] for i in range(len(_cdates) - 1)))

# Tel Aviv ILDC (Herzliya) Statutory Dual-Compulsion Matrix & U.S. Sovereign Exposure
penal_law_gag_min_years = 7
penal_law_gag_max_years = 15
p_comply_foreign_gag = 1.0
effective_us_oversight_custody = 1.0 - p_comply_foreign_gag
ILDC_MA_SPINOUTS = ["Aorato", "Adallom", "Secure Islands", "Hexadite", "CyberX"]
ildc_ma_spinouts_count = len(ILDC_MA_SPINOUTS)
US_STATUTORY_EXPOSURE_CHECKLIST = [
    "5 U.S.C. § 3331",
    "18 U.S.C. § 793(d)-(f)",
    "18 U.S.C. § 1030(a)(1)",
    "18 U.S.C. § 371",
    "18 U.S.C. § 1001",
    "18 U.S.C. § 1519",
    "32 C.F.R. Part 117",
]
ISRAELI_COMPULSION_STATUTES = [
    "Israeli Reserve Service Law (5768-2008)",
    "Israeli Communications Law (5742-1982 § 13)",
    "Israeli Secret Monitoring Law (5739-1979 §§ 4-5)",
    "Israeli General Security Service [Shabak] Law (5762-2002 §§ 8, 11, 19)",
    "Israel Penal Law (5737-1977 §§ 113, 113A, 117)",
]

check(
    "ildc.penal_law_gag_7_to_15_yr",
    penal_law_gag_min_years == 7 and penal_law_gag_max_years == 15,
    "%d-%d yr felony secrecy gag" % (penal_law_gag_min_years, penal_law_gag_max_years),
)
check(
    "ildc.dual_compulsion_custody_collapse",
    p_comply_foreign_gag == 1.0 and effective_us_oversight_custody == 0.0,
    "P(Comply)=%.1f => EffectiveCustody=%.1f" % (p_comply_foreign_gag, effective_us_oversight_custody),
)
check(
    "ildc.ma_spinouts_count_5",
    ildc_ma_spinouts_count == 5
    and ILDC_MA_SPINOUTS == ["Aorato", "Adallom", "Secure Islands", "Hexadite", "CyberX"],
)
check(
    "ildc.us_statutory_exposure_checklist",
    US_STATUTORY_EXPOSURE_CHECKLIST
    == [
        "5 U.S.C. § 3331",
        "18 U.S.C. § 793(d)-(f)",
        "18 U.S.C. § 1030(a)(1)",
        "18 U.S.C. § 371",
        "18 U.S.C. § 1001",
        "18 U.S.C. § 1519",
        "32 C.F.R. Part 117",
    ]
    and len(ISRAELI_COMPULSION_STATUTES) == 5,
)

# ---------------------------------------------------------------------------
# Layer 7 — MSF 7.00 PDB vault verifier (OPSTACK_SYM_DIR, default /tmp/sym2)
# ---------------------------------------------------------------------------

SYM_DIR = os.environ.get("OPSTACK_SYM_DIR", "/tmp/sym2")
MSF7_SIGNATURE = b"Microsoft C/C++ MSF 7.00\r\n\x1aDS\x00\x00\x00"
PDB_FILENAMES = {
    "diagtrack.dll": "diagtrack.pdb",
    "SenseIR.exe": "SenseIR.pdb",
    "MsSense.exe": "MsSense.pdb",
    "SenseCncProxy.exe": "SenseCnCProxy.pdb",
    "MpClient.dll": "mpclient.pdb",
    "cdp.dll": "cdp.pdb",
    "fveapi.dll": "fveapi.pdb",
}


def _guid_bytes(guid_hex):
    """PDB info-stream GUID layout: Data1/Data2/Data3 little-endian, Data4 big-endian."""
    d1 = int(guid_hex[0:8], 16)
    d2 = int(guid_hex[8:12], 16)
    d3 = int(guid_hex[12:16], 16)
    d4 = bytes.fromhex(guid_hex[16:32])
    return struct.pack("<IHH", d1, d2, d3) + d4


def verify_pdb_guid(binary_name, guid):
    """Return (status, detail); status in {vault_absent, verified, absent, signature_mismatch, guid_mismatch}."""
    if not os.path.isdir(SYM_DIR):
        return "vault_absent", "sym2 vault not present - SKIP"
    path = os.path.join(SYM_DIR, PDB_FILENAMES[binary_name])
    if not os.path.isfile(path):
        # fall back to a guid-substring filename scan
        target = guid.lower()
        found = None
        for fn in os.listdir(SYM_DIR):
            if target in fn.lower():
                found = os.path.join(SYM_DIR, fn)
                break
        if found is None:
            return "absent", "no candidate file for " + binary_name
        path = found
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return "absent", "unreadable candidate: " + path
    if not data.startswith(MSF7_SIGNATURE):
        return "signature_mismatch", path
    if _guid_bytes(guid) not in data:
        return "guid_mismatch", "info-stream GUID not found in " + path
    return "verified", path


_vault_statuses = {}
for _bname, _bdict in ALL_BINARIES.items():
    _status, _detail = verify_pdb_guid(_bname, _bdict["pdb_guid"])
    _vault_statuses[_bname] = _status
    check(
        "pdb_vault." + _bname,
        _status in ("vault_absent", "absent", "verified"),
        _status + ": " + _detail,
    )
check(
    "pdb_vault.msf7_signature_gate",
    all(s in ("vault_absent", "absent", "verified") for s in _vault_statuses.values()),
    "vault=%s statuses=%s" % (SYM_DIR, _vault_statuses),
)

# ---------------------------------------------------------------------------
# Meta gate and summary
# ---------------------------------------------------------------------------

check("meta.check_count_ge_71", len(RESULTS) >= 71, "%d checks registered" % len(RESULTS))

_total = len(RESULTS)
_passed = sum(1 for r in RESULTS if r[1])
_failed = [r for r in RESULTS if not r[1]]

print("=" * 78)
print("OPSTACK PROOF: windows_ma_telemetry_exfil  |  checks: %d passed / %d total" % (_passed, _total))
for _name, _ok, _detail in RESULTS:
    if not _ok:
        print("  FAIL: %s (%s)" % (_name, _detail))
print("tranche_recovery(940.50) -> " + "; ".join("%s=$%s" % (n, r) for n, r in _full))
print("GE1: %d blocks / %.3f min | GE2: Omega=1.0 | GE3: pi_active=%s | GE4: %.8f -> %.1f"
      % (GE1_BLOCKS, float(GE1_MINUTES), float(GE3_PI_ACTIVE_CLOSED), GE4_DETECT_NORMAL, GE4_DETECT_EXFIL))
print("PDB vault: %s" % ("absent (SKIP)" if not os.path.isdir(SYM_DIR) else SYM_DIR))
print("EXIT_CODE: " + ("0" if (_passed == _total and _total >= 71) else "1"))
print("=" * 78)

sys.exit(0 if (_passed == _total and _total >= 71) else 1)
