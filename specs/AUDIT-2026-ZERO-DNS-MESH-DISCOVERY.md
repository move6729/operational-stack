# AUDIT SPECIFICATION: OPEN-MESH-DISCOVERY-v1.0

**Module:** Zero-DNS Local Physical Mesh Discovery Engine  
**Reference:** `OPEN-MESH-DISCOVERY-v1.0`  
**License:** Unlicense (Public Domain)  

---

### I. MECHANISTIC MISMATCH & INVARIANTS

1. **Mechanistic Mismatch:** Centralized platforms rely on external DNS servers, central STUN/TURN relays, or platform registry servers that enforce rent extraction and network tracking. `OPEN-MESH-DISCOVERY-v1.0` operates directly on local socket broadcast and binary struct framing (`socket`, `struct`) to discover local peers and exchange stigmergic state marks ($\mathcal{E}$) without zero-egress breaches.
2. **Binary Framing Invariant:**
   $$\text{Packet} = \text{StructPack}(">\mathbf{I}", \text{Len}) \parallel \text{JSONPayload}$$
3. **Air-Gap & Local Discovery Invariant:** Node discovery occurs strictly within local layer-2/layer-3 physical network boundaries without requiring external internet routing or domain name resolution.
