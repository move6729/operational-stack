# AUDIT-2026: DISINTERMEDIATING CLOUD IDENTITY & SSO TOLLBOOTHS (OPEN-IAM-v1.0)

**Classification:** System Specification & Economic Audit  
**Target Monopolies:** Okta, Ping Identity, Microsoft Entra ID  
**Protocol Ref:** `OPEN-IAM-v1.0`  
**License:** Unlicense (Public Domain)  

---

## I. MECHANISTIC MISMATCH

Centralized Identity Providers (IdPs) market cloud single sign-on (SSO) as an indispensable security requirement, charging $2–$15+/user/month and levying an "SSO Tax" on enterprise SaaS features. In computational reality:

1. **Centralized IdPs are Single Points of Failure (SPOF):** Routing all corporate authentication through a multi-tenant cloud provider creates catastrophic systemic exposure.
2. **Zero-Trust is Cryptographic Key Verification:** True zero-trust architecture relies on local public-key cryptography (Ed25519 / WebAuthn / hardware enclaves), not round-trip HTTP calls to Okta servers.
3. **Identity is Decentralized & Local-First:** Role claims and public key attestations can be verified directly between nodes using JSON-LD decentralized identifiers (DIDs) and local public key registries.

---

## II. SYSTEM ARCHITECTURE

`OPEN-IAM-v1.0` replaces proprietary cloud IAM vendors with:
- **`schema/iam_identity.json`**: Pure JSON Draft 2020-12 schema for cryptographic identity documents and role attestation vectors.
- **`proofs/iam_engine.py`**: Bare-metal Python execution proof verifying local key signatures and state transitions with zero external cloud dependencies.

---

## III. GAME-THEORETIC INVARIANTS

$$\lim_{A_p \to 1.0} C_s(\text{Cloud IAM}) = 0 \implies \text{Okta/Ping SSO Rent} \to 0$$

Authentications and authorization checks occur directly via bare-metal cryptographic signatures without per-user monthly cloud taxes.
