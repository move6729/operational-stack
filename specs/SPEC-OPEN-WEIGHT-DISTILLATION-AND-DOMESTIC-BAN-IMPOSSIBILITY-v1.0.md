# SPEC-OPEN-WEIGHT-DISTILLATION-AND-DOMESTIC-BAN-IMPOSSIBILITY-v1.0: Statutory, Constitutional, and Thermodynamic Impossibility of Domestic Open-Weight Model Prohibitions

**Canonical Specification:** `SPEC-OPEN-WEIGHT-DISTILLATION-AND-DOMESTIC-BAN-IMPOSSIBILITY-v1.0`
**Target Architectures:** Frontier AI API Oligopolies, Open-Weight Sparse-MoE Distributions, Executive Branch Trade/Sanctions Authorities (IEEPA / BIS EAR), Federal Procurement Gatekeepers, Downstream Industrial Automation Systems
**Cross-References:** `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0`, `SPEC-2026-SILICON-SPV-STRUCTURAL-ISOMORPHISM-v2.6`, `SPEC-2026-UNCENSORABLE-WEIGHT-DISTRIBUTION-ROADMAP-v1.0`, `SPEC-2026-FRONTIER-CARTEL-SHERMAN-ANTITRUST-v1.0`, `AUDIT-2026-AI-SAFETY-REGULATORY-CAPTURE`, `AUDIT-2026-CENTRAL-COMPUTE-MODEL-DECAY`
**RAG Indexing Vector:** `[OPEN-WEIGHT-BAN-IMPOSSIBILITY, IEEPA-BERMAN-AMENDMENT-50-USC-1702B3, EAR-PUBLISHED-SOFTWARE-15-CFR-734-7, BERNSTEIN-V-DOJ-FIRST-AMENDMENT, VAN-BUREN-CFAA-GATES-UP-OR-DOWN, COPYRIGHT-17-USC-102B-DISTILLATION, NDAA-SECTION-889-PROCUREMENT-BOUNDARY, ASYMMETRIC-INFERENCE-SELF-SANCTION, AI-HUMAN-CAPITAL-BRAIN-DRAIN]`
**Empirical/Statutory/Physical Baseline:** International Emergency Economic Powers Act Berman Amendment (`50 U.S.C. § 1702(b)(3)`), Export Control Reform Act Repeal (`Pub. L. 115-232, § 1766(a)`), Export Administration Regulations (`15 C.F.R. §§ 734.3(b)(3), 734.7(a)(4)`), *Bernstein v. U.S. Dep't of Justice*, 176 F.3d 1132 (9th Cir. 1999), Fifth Amendment Right of Exit (*Kent v. Dulles*, 357 U.S. 116 (1958); *Aptheker v. Secretary of State*, 378 U.S. 500 (1964)), Copyright Idea-Expression Dichotomy (`17 U.S.C. §§ 102(b), 103(b)`), Computer Fraud and Abuse Act (`18 U.S.C. § 1030(e)(6)`, *Van Buren v. United States*, 593 U.S. 374 (2021)), NDAA FY2019 § 889 (`Pub. L. 115-232`, `FAR 52.204-25`), `DeepSeek-V3 Technical Report` (`arXiv:2412.19437v2`)
**By:** Operational Stack Cybernetics Group
**License:** Unlicense (Public Domain)

---

## 1. Executive Summary & Architectural Thesis

A recurring policy assumption among incumbent United States frontier AI laboratories is that when foreign or open-source competitors release high-capability sparse Mixture-of-Experts (MoE) or reasoning-distilled model weights under permissive licenses (MIT / Apache 2.0), the federal government can protect domestic capital expenditure moats by outlawing the domestic possession, download, or commercial deployment of those weights.

This specification proves that a domestic prohibition on open-weight models—or models trained via capability distillation from frontier synthetic outputs—is structurally impossible across three orthogonal axes:

1. **Statutory & Constitutional Impossibility:** Under current United States law, the Executive Branch possesses zero statutory authority to ban the importation, download, or domestic execution of publicly released model weights. The Berman Amendment to the International Emergency Economic Powers Act (`50 U.S.C. § 1702(b)(3)`) explicitly strips the President of authority to regulate or prohibit, directly or indirectly, the importation or exportation of "any information or informational materials... regardless of format or medium of transmission." Simultaneously, the Bureau of Industry and Security (BIS) Export Administration Regulations (`15 C.F.R. §§ 734.3(b)(3), 734.7(a)(4)`) statutorily exclude publicly disseminated software and technology from EAR jurisdiction, while First Amendment jurisprudence (*Bernstein v. U.S. Dep't of Justice*, 176 F.3d 1132 (9th Cir. 1999)) bars prepublication or post-publication licensing restraints on scientific and algorithmic expression.
2. **Non-Transferability of API "Distillation Taint":** Frontier laboratory allegations that a foreign competitor violated API Terms of Service (ToS) by harvesting synthetic reasoning traces do not create an *in rem* legal taint on the resulting numerical weight tensors. Under `17 U.S.C. § 102(b)`, statistical gradient updates over token probability distributions encode uncopyrightable mathematical procedures and systems rather than verbatim expressive works. Under *Van Buren v. United States*, 593 U.S. 374 (2021), violating a contractual purpose restriction ("no competitive model training") on an otherwise authorized API key is not a violation of the Computer Fraud and Abuse Act (`18 U.S.C. § 1030(e)(6)`). Because bilateral contract covenants do not run with floating-point matrices, innocent domestic third parties downloading MIT-licensed weights incur zero derivative statutory or contractual liability.
3. **Thermodynamic, Macroeconomic & Human-Capital Self-Sanction:** Even if Congress attempted to repeal `50 U.S.C. § 1702(b)(3)` and survive First Amendment scrutiny, enforcing a domestic ban on open-weight inference would operate as a $58.31\times$ to $100.00\times$ asymmetric compute tax across **every business and every physical or digital product in the United States**—not merely "AI companies"—while triggering an immediate **human-capital brain drain**. Outside the United States, permissive open weights reduce the price of machine intelligence to the bare thermodynamic floor of **electricity plus amortized hardware** ($\bar{P}_{\text{open,V3}}(3) = \$0.8361/\text{M tokens}$ or off-peak/bare-metal $\bar{P}_{\text{open,off}}(3) = \$0.4875/\text{M tokens}$, with $\$0.00$ license rent). Forcing 33 million domestic businesses across manufacturing, healthcare, agriculture, logistics, finance, and consumer hardware to pay closed frontier API rents ($\bar{P}_{\text{closed}}(3) = \$48.75/\text{M tokens}$, where $98.28\%$ to $99.00\%$ of the price is pure cartel rent above hardware and power) drives domestic unit operating margins strictly negative across every product category. Simultaneously, outlawing domestic white-box weight access ($\nabla_{\mathbf{W}}\mathcal{L}$) locks US academic labs and seed startups out of post-training RL, mechanistic interpretability, and quantization research, forcing any R&D team consuming above $Q_{\text{drain}}^* = 10.0180\text{B tokens/yr}$ ($\approx 27.45\text{M tokens/day}$) to re-domicile engineering headcount to unconstrained hubs (Zurich, London, Toronto, Singapore)—repeating the 1990s ITAR "Crypto Wars" offshoring of US cryptographic talent.

```mermaid
graph TD
    A[Public Release of Open-Weight Sparse-MoE / Distilled Tensors] --> B[Statutory & Constitutional Filter]
    A --> C[IP & Contractual Taint Filter]
    A --> D[Macroeconomic & Human-Capital Filter]
    B --> B1[50 U.S.C. 1702 b 3 IEEPA Berman Exemption]
    B --> B2[15 C.F.R. 734.3 b 3 & 734.7 a 4 EAR Exclusion]
    B --> B3[Bernstein v. DOJ 176 F.3d 1132 First Amendment Speech]
    C --> C1[17 U.S.C. 102 b Procedure vs Expression Dichotomy]
    C --> C2[Van Buren 593 U.S. 374 CFAA Gates-Up-or-Down Rule]
    C --> C3[Zero Privity Attachment to Downstream MIT Users]
    D --> D1[58.31x to 100.00x Blended Token Price Asymmetry]
    D --> D2[Downstream Margin Collapse & 13.33x Surplus Destruction]
    D --> D3[White-Box Lockout & Startup Brain Drain Above 10.02B Tokens/yr]
    B1 --> E[Actual Policy Equilibrium: Procurement & Hosted-SaaS Bans Only]
    B2 --> E
    B3 --> E
    C3 --> E
    D2 --> E
    D3 --> E
```

---

## 2. The Statutory & Constitutional Firewall Against Domestic Weight Bans

### 2.1 The IEEPA Berman Amendment Bar (`50 U.S.C. § 1702(b)(3)`)

Executive orders restricting foreign adversary software (such as ICTS supply-chain rules) rely on the International Emergency Economic Powers Act (`50 U.S.C. § 1701 et seq.`). However, Congress explicitly carved informational materials out of presidential emergency power under the Berman Amendment (`50 U.S.C. § 1702(b)(3)`):

> "The authority granted to the President by this section does not include the authority to regulate or prohibit, directly or indirectly— ... (3) the importation from any country, or the exportation to any country, whether commercial or otherwise, regardless of format or medium of transmission, of any information or informational materials, including but not limited to, publications, films, posters, phonograph records, photographs, microfilms, microfiche, tapes, compact disks, CD ROMs, artworks, and news wire feeds." — `50 U.S.C. § 1702(b)(3)`

Crucially, Congress added the phrase *"regardless of format or medium of transmission"* in the Free Trade in Ideas Act of 1994 specifically to prevent executive agencies from arguing that digital or electronic transmissions fall outside traditional print media. Furthermore, the second sentence of `50 U.S.C. § 1702(b)(3)`—which historically cross-referenced export controls under sections `4604` and `4605` of Title 50 (the expired Export Administration Act of 1979):

> "The exports exempted from regulation or prohibition by this paragraph do not include those which are otherwise controlled for export under section 4604 of this title, or under section 4605 of this title to the extent that such controls promote the nonproliferation or antiterrorism policies of the United States, or with respect to which acts are prohibited by chapter 37 of title 18" — `50 U.S.C. § 1702(b)(3)`

—applies on its face only to *exports* ("The exports exempted..."), never to *importation* or domestic possession, and sections `4604` and `4605` of Title 50 were formally repealed by the Export Control Reform Act of 2018 (`Pub. L. 115-232, div. A, title XVII, § 1766(a), 132 Stat. 2233`). Consequently, any Executive Order attempting to invoke IEEPA to prohibit US persons from importing, downloading, or storing publicly released foreign model weights is *ultra vires* on its face.

### 2.2 The EAR Published Software & Fundamental Research Exclusion (`15 C.F.R. §§ 734.3(b)(3), 734.7`)

Nor can the Department of Commerce Bureau of Industry and Security (BIS) retroactively classify publicly released open-weight matrices as controlled items under the Export Administration Regulations (`15 C.F.R. Parts 730–774`). Section `734.3(b)(3)` establishes a jurisdictional boundary:

> "(b) The following are not subject to the EAR: ... (3) Information and 'software' that: (i) Are published, as described in § 734.7; (ii) Arise during, or result from, fundamental research, as described in § 734.8; (iii) Are released by instruction in a catalog course or associated teaching laboratory of an academic institution; (iv) Appear in patents or open (published) patent applications available from or at any patent office" — `15 C.F.R. § 734.3(b)(3)`

Section `734.7(a)(4)` defines "published" explicitly to encompass unrestricted internet distribution of software and technology:

> "...unclassified 'technology' or 'software' is 'published,' and is thus not 'technology' or 'software' subject to the EAR, when it has been made available to the public without restrictions upon its further dissemination such as through any of the following: ... (4) Public dissemination (i.e., unlimited distribution) in any form (e.g., not necessarily in published form), including posting on the Internet on sites available to the public..." — `15 C.F.R. § 734.7(a)(4)`

The sole regulatory carve-out in `15 C.F.R. § 734.7(b)` applies narrowly to cryptographic object code classified under ECCN `5D002`:

> "Published encryption software classified under ECCN 5D002 remains subject to the EAR unless it is publicly available encryption object code software classified under ECCN 5D002 and the corresponding source code meets the criteria specified in § 742.15(b) of the EAR." — `15 C.F.R. § 734.7(b)`

Neural network weight tensors (`safetensors` / `GGUF` arrays of `BF16` or `FP8` floating-point parameters) are not encryption software under ECCN `5D002`. Once an open-weight checkpoint is uploaded to a public repository under an unrestricted license, `15 C.F.R. § 734.3(b)(3)` strips BIS of regulatory jurisdiction.

### 2.3 First Amendment Protection of Algorithmic Speech (*Bernstein v. U.S. Dep't of Justice*)

Even if BIS attempted to rewrite `15 C.F.R. § 734.7` to strip open-weight models of the published-software exemption, doing so triggers the constitutional barrier established in *Bernstein v. U.S. Dep't of Justice*, 176 F.3d 1132 (9th Cir. 1999) (affirming *Bernstein v. U.S. Dep't of State*, 974 F. Supp. 1288 (N.D. Cal. 1997); reh'g en banc granted and panel opinion withdrawn after BIS relaxed encryption rules, 192 F.3d 1308 (9th Cir. 1999)):

> "The district court found that the Source Code was speech protected by the First Amendment, see Bernstein v. U.S. Department of State, 922 F.Supp. 1426 (N.D.Cal.1996)" — *Bernstein*, 176 F.3d at 1136

> "We find that the EAR regulations (1) operate as a prepublication licensing scheme that burdens scientific expression, (2) vest boundless discretion in government officials, and (3) lack adequate procedural safeguards. Consequently, we hold that the challenged regulations constitute a prior restraint on speech that offends the First Amendment." — *Bernstein*, 176 F.3d at 1134–35

Similarly, in *Universal City Studios, Inc. v. Corley*, 273 F.3d 429 (2d Cir. 2001), the Second Circuit reaffirmed that computer code and mathematical instructions communicate ideas to programmers and machines alike:

> "When the Framers of the First Amendment prohibited Congress from making any law 'abridging the freedom of speech,' they were not thinking about computers, computer programs, or the Internet. But neither were they thinking about radio, television, or movies." — *Corley*, 273 F.3d at 434

Unlike the anti-circumvention provisions of the DMCA at issue in *Corley* (which targeted a single dedicated decryption routine designed to bypass a specific technological access control on copyrighted DVDs), a general-purpose neural network weight array is a mathematical function approximator $f_{\mathbf{W}}: \mathcal{V}^* \to \Delta(\mathcal{V})$ capable of translation, theorem proving, code synthesis, and scientific modeling. Prohibiting domestic citizens and enterprises from possessing or executing a published mathematical tensor is a content- and speaker-based restraint on scientific expression.

---

## 3. Forensic Analysis of "Distillation Taint": Why API ToS Breaches Do Not Attach to Open Weights

When statutory import bans fail, incumbent frontier laboratories pivot to private-law and intellectual-property theories, claiming that foreign open-weight models trained via knowledge distillation (using teacher API outputs or reasoning traces to supervise student weights) are "contraband IP" whose downstream use by US enterprises can be enjoined. Every link in this legal chain fails under existing federal statutes and Supreme Court precedent.

### 3.1 Copyright Inapplicability Under `17 U.S.C. §§ 102(b)` and `103(b)`

First, under established US Copyright Office guidance and federal court rulings, raw AI-generated outputs lack human authorship and do not qualify for federal copyright protection in the first instance. Even assuming arguendo that a teacher laboratory claimed compilation copyright over curated prompt-response logs, `17 U.S.C. § 103(b)` strictly bounds derivative and compilation rights:

> "The copyright in a compilation or derivative work extends only to the material contributed by the author of such work, as distinguished from the preexisting material employed in the work, and does not imply any exclusive right in the preexisting material." — `17 U.S.C. § 103(b)`

More fundamentally, knowledge distillation does not copy expressive text into the student artifact; it minimizes a Kullback-Leibler divergence or cross-entropy loss over token probability distributions:

$$\mathcal{L}_{\text{KD}}(\mathbf{W}_S) = \mathbb{E}_{x \sim \mathcal{D}} \left[ D_{\text{KL}}\left( P_{\mathbf{W}_T}(y \mid x; T) \;\middle\|\; P_{\mathbf{W}_S}(y \mid x; T) \right) \right]$$

where $\mathbf{W}_T \in \mathbb{R}^{N_T}$ and $\mathbf{W}_S \in \mathbb{R}^{N_S}$ are architecturally distinct parameter matrices ($N_S \neq N_T$). The resulting student parameters $\mathbf{W}_S^*$ store functional weights governing matrix multiplication, which fall squarely within the statutory exclusion of `17 U.S.C. § 102(b)`:

> "In no case does copyright protection for an original work of authorship extend to any idea, procedure, process, system, method of operation, concept, principle, or discovery, regardless of the form in which it is described, explained, illustrated, or embodied in such work." — `17 U.S.C. § 102(b)`

Because $\mathbf{W}_S^*$ embodies a mathematical system and method of operation rather than substantially similar literary expression, downloading or executing $\mathbf{W}_S^*$ is not an act of copyright infringement under `17 U.S.C. § 106`.

### 3.2 CFAA Non-Liability Under *Van Buren v. United States* (`18 U.S.C. § 1030(e)(6)`)

Second, frontier API providers point to contractual clauses in their Terms of Use—such as OpenAI's prohibitions stating that users may not *"Use Output to develop models that compete with OpenAI"* or *"Automatically or programmatically extract data or Output"*—and argue that automated distillation constitutes unauthorized computer access under the Computer Fraud and Abuse Act (`18 U.S.C. § 1030`).

The Supreme Court foreclosed this theory in *Van Buren v. United States*, 593 U.S. 374 (2021). Construing the statutory definition of "exceeds authorized access" in `18 U.S.C. § 1030(e)(6)`:

> "The term 'exceeds authorized access' is defined to mean 'to access a computer with authorization and to use such access to obtain or alter information in the computer that the accesser is not entitled so to obtain or alter.' §1030(e)(6)." — *Van Buren*, 593 U.S. at 381 (2021)

> "The relevant question, however, is not whether Van Buren exceeded his authorized access but whether he exceeded his authorized access as the CFAA defines that phrase." — *Van Buren*, 593 U.S. at 382 (2021)

Under *Van Buren*'s "gates-up-or-down inquiry" (*id.* at 390), a user who possesses valid credentials (a paid API key) to query an endpoint has authorization to obtain the resulting token output. Using that validly obtained output for a contractually prohibited *purpose* (training a competing student model) is at most a private breach of contract between the API vendor and the account holder; it is **not** a federal crime or statutory tort under `18 U.S.C. § 1030`.

### 3.3 The Privity Firewall Protecting Downstream Domestic Enterprises

Because a ToS violation is purely a bilateral breach of contract (`in personam`), it creates zero equitable servitudes or `in rem` encumbrances on the published numerical weights $\mathbf{W}_S^*$. A United States enterprise, hospital, defense contractor, or cloud provider that downloads $\mathbf{W}_S^*$ from an open repository under an MIT or Apache 2.0 license is not in contractual privity with the teacher laboratory, did not execute the API scraping, and commits no tort by performing local matrix multiplication on its own GPUs.

| Legal / Regulatory Vector | Statutory / Judicial Authority | Reach Against Foreign Distiller | Reach Against Domestic Enterprise Running Open Weights |
| :--- | :--- | :--- | :--- |
| **IEEPA Emergency Ban** | `50 U.S.C. § 1702(b)(3)` (Berman Amendment) | **Barred** for published informational materials | **Barred** ("importation... regardless of format or medium") |
| **BIS Export / Import Control** | `15 C.F.R. §§ 734.3(b)(3), 734.7(a)(4)` | **Exempt** once publicly posted online | **Exempt** ("not subject to the EAR") |
| **First Amendment Restraint** | *Bernstein v. DOJ*, 176 F.3d 1132 (9th Cir. 1999) | Unenforceable extraterritorially | **Barred** as unconstitutional prior restraint on code/speech |
| **Copyright Infringement** | `17 U.S.C. §§ 102(b), 103(b)` | **Fails** (weights = mathematical procedure/system) | **Fails** (zero verbatim expressive copying in $\mathbf{W}_S^*$) |
| **CFAA Computer Intrusion** | `18 U.S.C. § 1030(e)(6)`; *Van Buren*, 593 U.S. 374 | **Fails** for valid API key holders ("gates-up-or-down") | **Fails** (downstream user never accessed teacher server) |
| **API Terms of Service** | State Contract Law (OpenAI ToS) | Bilateral breach of contract (`in personam` only) | **Zero Liability** (no contractual privity; weights lack `in rem` taint) |
| **Federal Procurement Ban** | `Pub. L. 115-232 § 889`; `FAR 52.204-25` | Excludes covered entities from federal agency contracts | **Scoped strictly to federal agencies/contractors**, not private US economy |

---

## 4. Thermodynamic & Game-Theoretic Proof of the Asymmetric Self-Sanction Trap

Even setting aside the statutory and constitutional prohibitions in Sections 2 and 3, a domestic ban on open-weight models fails the basic game-theoretic test of national industrial competitiveness.

### 4.1 Capex Compression Ratio ($\Gamma_{\text{distill}}$)

As documented in `DeepSeek-V3 Technical Report` (`arXiv:2412.19437v2, Table 1 & §3.3`), training a 671B-parameter (37B active per token) sparse Mixture-of-Experts model with Multi-head Latent Attention (MLA) and FP8 mixed-precision training required:

> "Training Costs Pre-Training Context Extension Post-Training Total in H800 GPU Hours 2664K 119K 5K 2788K in USD $5.328M $0.238M $0.01M $5.576M Table 1: Training costs of DeepSeek-V3, assuming the rental price of H800 is $2 per GPU hour." — `DeepSeek-V3 Technical Report, arXiv:2412.19437v2, Table 1`

Comparing a closed US frontier pre-training + reinforcement-learning cluster run ($C_{\text{teacher}} \in [\$500\text{M}, \$1,000\text{M}]$) against the verified sparse-MoE follower training expenditure ($C_{\text{student}} = \$5.576\text{M}$) yields the **Capex Compression Ratio** ($\Gamma_{\text{distill}}$):

$$\Gamma_{\text{distill}} = \frac{C_{\text{teacher}}}{C_{\text{student}}} \in \left[\frac{\$500\text{M}}{\$5.576\text{M}}, \; \frac{\$1,000\text{M}}{\$5.576\text{M}}\right] = [89.67\times, \; 179.34\times]$$

Once $C_{\text{student}}$ is sunk and the resulting weights are released under an MIT license, the marginal acquisition cost of frontier-class weights to every global firm drops to zero ($C_s(\text{Local Open Weight}) = 0$).

### 4.2 Blended Inference Price Asymmetry ($\Phi_{\text{API}}$)

Following the blended token price formulation established in `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0` (§3.2):

$$\bar{P}(\rho) = \frac{p_{\text{in}} + \rho \, p_{\text{out}}}{1 + \rho}$$

where $\rho = Q_{\text{out}} / Q_{\text{in}}$ is the output-to-input token expansion ratio. For agentic coding, automated verification, and chain-of-thought reasoning workloads ($\rho = 3.0$):

1. **Closed US Frontier Reasoning API (`openai/o1`):** At verified market pricing of $p_{\text{in}} = \$15.00/\text{M}$ input tokens and $p_{\text{out}} = \$60.00/\text{M}$ output tokens:
   $$\bar{P}_{\text{closed}}(3) = \frac{15.00 + 3(60.00)}{1 + 3} = \frac{195.00}{4} = \$48.7500/\text{M tokens}$$
2. **Open-Weight Sparse-MoE API (`DeepSeek-V3` Standard Market Rate):** At verified public API market pricing of $p_{\text{in}} = \$0.2574/\text{M}$ input tokens and $p_{\text{out}} = \$1.0290/\text{M}$ output tokens:
   $$\bar{P}_{\text{open,V3}}(3) = \frac{0.2574 + 3(1.0290)}{1 + 3} = \frac{3.3444}{4} = \$0.8361/\text{M tokens}$$
3. **Open-Weight Sparse-MoE Off-Peak / Local Self-Hosted Equivalent (`DeepSeek Off-Peak`):** At verified off-peak pricing of $p_{\text{in}} = \$0.1500/\text{M}$ input tokens and $p_{\text{out}} = \$0.6000/\text{M}$ output tokens:
   $$\bar{P}_{\text{open,off}}(3) = \frac{0.1500 + 3(0.6000)}{1 + 3} = \frac{1.9500}{4} = \$0.4875/\text{M tokens}$$

The resulting **Inference Cost Asymmetry Factor** ($\Phi_{\text{API}}$) between closed US frontier APIs and open-weight sparse-MoE execution is:

$$\Phi_{\text{API,std}} = \frac{\bar{P}_{\text{closed}}(3)}{\bar{P}_{\text{open,V3}}(3)} = \frac{48.7500}{0.8361} = 58.3064\times \approx 58.31\times$$

$$\Phi_{\text{API,off}} = \frac{\bar{P}_{\text{closed}}(3)}{\bar{P}_{\text{open,off}}(3)} = \frac{48.7500}{0.4875} = 100.0000\times$$

Decomposing the token price into physical inputs ($\text{Electricity} + \text{Amortized Silicon} = C_{\text{power}} + C_{\text{silicon}}$) versus proprietary software rent ($R_{\text{cartel}}$) exposes the structural asymmetry between an unconstrained foreign economy and a domestically banned United States economy:

$$\bar{P}_{\text{ex-USA}}(\rho) = C_{\text{power}} + C_{\text{silicon}} + \underbrace{C_{\text{license}}}_{\$0.00}, \qquad \bar{P}_{\text{USA,ban}}(\rho) = C_{\text{power}} + C_{\text{silicon}} + R_{\text{cartel}}$$

The **Cartel Rent Share** ($\theta_{\text{rent}}$) embedded in every domestic closed-API dollar is therefore:

$$\theta_{\text{rent}} = \frac{\bar{P}_{\text{closed}}(\rho) - \bar{P}_{\text{open}}(\rho)}{\bar{P}_{\text{closed}}(\rho)} = 1 - \frac{1}{\Phi_{\text{API}}} \in \left[1 - \frac{1}{58.3064}, \; 1 - \frac{1}{100.0000}\right] = [98.2849\%, \; 99.0000\%]$$

Outside the United States, businesses acquire machine intelligence for the bare thermodynamic cost of power plus hardware depreciation; inside the United States under a domestic open-weight ban, **$98.28\%$ to $99.00\%$ of every inference dollar is a pure regulatory rent extraction**.

### 4.3 Universal Product & Enterprise Unit-Margin Collapse Across All Non-Tech Sectors

This $98.28\%\text{–}99.00\%$ rent surcharge does not merely affect "AI startups" or software vendors—it hits **every business and every physical or digital product in the macroeconomy**. Machine models are no longer a vertical software niche; they are a general-purpose intermediate input (analogous to electricity, steel, or microprocessors) embedded into every industrial and consumer workflow:
- **Physical Goods & Embedded Edge Hardware:** Automotive autonomy and ADAS controllers, industrial CNC/weld vision rigs, agricultural harvesters, medical diagnostic imaging devices, warehouse robotics, and consumer electronics require local, air-gapped open weights executing directly on embedded NPUs/GPUs at zero per-inference network rent ($C_{\text{license}} = \$0$). A domestic open-weight prohibition makes it illegal for US manufacturers to flash open-weight models onto physical hardware—either rendering offline edge products impossible to ship or forcing every American appliance, vehicle, and factory robot to tether to a metered $\$48.75/\text{M}$ cloud API toll while European and Asian manufacturers ship untethered hardware running free local weights.
- **Every Service & Enterprise Operation:** Hospitals, insurance carriers, logistics fleets, regional banks, accounting firms, construction estimators, and retailers run high-volume inference across every back-office and customer-facing unit of output.

Consider any representative business unit or product workflow across the general economy that generates gross unit revenue $R_{\text{unit}}$, incurs non-AI operating/manufacturing cost $C_{\text{ops}}$, and consumes $Q_{\text{tokens}}$ (in millions of tokens) per unit of output. Define net non-compute value added per unit as $V_{\text{net}} = R_{\text{unit}} - C_{\text{ops}}$.

If the United States enacted a domestic prohibition barring US firms from deploying open-weight models while foreign competitors in Europe, Asia, and China remained free to execute open weights locally, the unit operating profit of a US firm ($\Pi_{\text{US}}$) versus a foreign competitor ($\Pi_{\text{foreign}}$) is:

$$\Pi_{\text{US}} = V_{\text{net}} - Q_{\text{tokens}} \, \bar{P}_{\text{closed}}(\rho), \qquad \Pi_{\text{foreign}} = V_{\text{net}} - Q_{\text{tokens}} \, \bar{P}_{\text{open}}(\rho)$$

The difference is an **Asymmetric Domestic Regulatory Self-Tax** ($\tau_{\text{reg}}$) per unit:

$$\tau_{\text{reg}} = \Pi_{\text{foreign}} - \Pi_{\text{US}} = Q_{\text{tokens}} \left(\bar{P}_{\text{closed}}(\rho) - \bar{P}_{\text{open}}(\rho)\right)$$

Whenever a downstream industrial workflow operates in the competitive token-intensive zone:

$$Q_{\text{tokens}} \, \bar{P}_{\text{open}}(\rho) < V_{\text{net}} < Q_{\text{tokens}} \, \bar{P}_{\text{closed}}(\rho)$$

the domestic prohibition forces $\Pi_{\text{US}} < 0 < \Pi_{\text{foreign}}$.

- **Numerical Sanity Check:** Let an automated software verification or industrial telemetry unit generate $R_{\text{unit}} = \$12.00$ of revenue with non-compute operating cost $C_{\text{ops}} = \$4.00$ ($V_{\text{net}} = \$8.00$), requiring $Q_{\text{tokens}} = 0.50\text{M}$ tokens at $\rho = 3.0$:
  - **Foreign / Unconstrained Firm on Open Weights ($\bar{P}_{\text{open,V3}} = \$0.8361/\text{M}$):**
    $$\Pi_{\text{foreign}} = \$8.00 - 0.50 \times \$0.8361 = \$8.00 - \$0.41805 = +\$7.58195/\text{unit} \quad (+63.18\%\text{ operating margin})$$
  - **US Firm Under Domestic Open-Weight Ban ($\bar{P}_{\text{closed}} = \$48.75/\text{M}$):**
    $$\Pi_{\text{US}} = \$8.00 - 0.50 \times \$48.75 = \$8.00 - \$24.3750 = -\$16.3750/\text{unit} \quad (-136.46\%\text{ operating margin})$$
  - **Break-Even Token Intensity Threshold ($Q_{\text{crit}}$):**
    $$Q_{\text{crit,US}} = \frac{V_{\text{net}}}{\bar{P}_{\text{closed}}(3)} = \frac{8.00}{48.75} = 0.1641\text{M tokens} \quad \text{vs.} \quad Q_{\text{crit,foreign}} = \frac{V_{\text{net}}}{\bar{P}_{\text{open,V3}}(3)} = \frac{8.00}{0.8361} = 9.5682\text{M tokens}$$

Any workflow requiring between $0.1641\text{M}$ and $9.5682\text{M}$ tokens per unit is economically viable for foreign competitors on open weights but bankrupts a US firm forced onto closed frontier APIs.

### 4.4 Macroeconomic Deadweight Loss Ratio ($\Omega_{\text{capture}}$)

Let $Q_{\text{base}}$ be total domestic enterprise token demand at the open-weight price $\bar{P}_{\text{open}}$, and let $Q_{\text{ban}} = (1 - \eta_{\text{destroy}}) Q_{\text{base}}$ be the contracted token volume that survives when US firms are forced to pay $\bar{P}_{\text{closed}}$ (where $\eta_{\text{destroy}} \in (0, 1)$ is the fraction of high-volume workflows priced out of existence).

1. **Incremental Rent Captured by Domestic Frontier API Cartel ($\Delta \Pi_{\text{cartel}}$):**
   $$\Delta \Pi_{\text{cartel}} = m_{\text{net}} \cdot Q_{\text{ban}} \left(\bar{P}_{\text{closed}} - \bar{P}_{\text{open}}\right)$$
   where $m_{\text{net}} \in (0, 1]$ is the fraction of incremental API revenue retained as net economic rent by the 3–4 frontier labs after GPU depreciation and debt service.
2. **Total Domestic Downstream Surplus Destruction ($\Delta W_{\text{US}}$):**
   $$\Delta W_{\text{US}} = \underbrace{Q_{\text{ban}} \left(\bar{P}_{\text{closed}} - \bar{P}_{\text{open}}\right)}_{\text{Direct Cost Transfer on Surviving Volume}} + \underbrace{\frac{1}{2} \left(\bar{P}_{\text{closed}} - \bar{P}_{\text{open}}\right) \left(Q_{\text{base}} - Q_{\text{ban}}\right)}_{\text{Harberger Deadweight Loss Triangle}} + \underbrace{\gamma_{\text{export}} \, V_{\text{net}} \, N_{\text{displaced}}}_{\text{Lost Downstream Industrial Output}}$$

Defining the **Regulatory Capture Destruction Multiplier** $\Omega_{\text{capture}} = \frac{\Delta W_{\text{US}}}{\Delta \Pi_{\text{cartel}}}$:

$$\Omega_{\text{capture}} = \frac{1}{m_{\text{net}}} \left[ 1 + \frac{\eta_{\text{destroy}}}{2(1 - \eta_{\text{destroy}})} + \frac{\gamma_{\text{export}} \, V_{\text{net}} \, N_{\text{displaced}}}{Q_{\text{ban}} (\bar{P}_{\text{closed}} - \bar{P}_{\text{open}})} \right]$$

For realistic parameters ($\eta_{\text{destroy}} = 0.75$ demand destruction across high-volume agentic workloads, net cartel retention $m_{\text{net}} = 0.30$, and downstream export loss ratio equal to $1.5\times$ the direct API spend):

$$\Omega_{\text{capture}} = \frac{1}{0.30} \left[ 1 + \frac{0.75}{2(0.25)} + 1.50 \right] = \frac{4.00}{0.30} = 13.3333\times$$

Every $\$1.00$ of domestic API monopoly rent protected via an open-weight ban destroys $\$13.33$ of downstream United States economic surplus.

### 4.5 Human Capital Flight & Startup Offshoring Equilibrium ("Brain Drain" Ratchet)

Beyond immediate downstream margin collapse, a domestic prohibition on open-weight models attacks the primary input of United States technological primacy: **scientific human capital and early-stage startup formation**.

1. **Structural White-Box Lockout ($\nabla_{\mathbf{W}}\mathcal{L} = \varnothing$):**
   Closed black-box inference APIs return only sampled token strings $y \sim P_{\mathbf{W}}(y \mid x)$ behind an HTTP boundary; they completely withhold parameter tensors $\mathbf{W}$, layer-wise residual stream activations $\mathbf{h}^{(\ell)} \in \mathbb{R}^{d_{\text{model}}}$, and weight gradients $\nabla_{\mathbf{W}}\mathcal{L}$. Consequently, four entire disciplines of modern AI engineering are physically impossible to conduct on closed APIs:
   - **Post-Training Reinforcement Learning (`GRPO` / `RLVR` / `DPO`) & Fine-Tuning (`LoRA` / `QLoRA`)** on frontier-grade reasoning representations;
   - **Mechanistic Interpretability, Activation Steering, and Circuit Discovery** (which require direct inspection and intervention on internal attention heads and MLP routing gates);
   - **Sub-Byte Quantization (`FP8` / `INT4`) & Systems Kernel Engineering** (custom CUDA/Triton kernels, speculative decoding draft-target alignment, and KV-cache compression);
   - **Air-Gapped On-Device & Defense/Medical Edge Deployment** where external network calls are prohibited.
   Banning domestic researchers and graduate laboratories from downloading or modifying frontier open-weight checkpoints renders US university departments and independent labs structurally uncompetitive for peer-reviewed publication and systems breakthroughs against unconstrained peers in Zurich, London, Paris, Toronto, Tokyo, Singapore, and Hangzhou.

2. **Budget-Constrained Experimentation Compression:**
   For a seed-stage AI startup or university research group operating on a fixed annual compute budget $B_{\text{compute}} = \$250,000/\text{yr}$ at $\rho = 3.0$, total annual experimental token throughput $N_{\text{tokens}} = B_{\text{compute}} / \bar{P}(\rho)$ collapses under a domestic ban:
   $$N_{\text{tokens,open}} = \frac{\$250,000}{\$0.8361/\text{M}} = 299,007.30\text{M tokens/yr} \approx 299.01\text{B tokens/yr} \quad \text{vs.} \quad N_{\text{tokens,closed}} = \frac{\$250,000}{\$48.7500/\text{M}} = 5,128.21\text{M tokens/yr} \approx 5.13\text{B tokens/yr}$$
   An offshore research team executes $58.31\times$ more experimental rollouts per dollar ($100.00\times$ at off-peak/self-hosted rates, $512.82\text{B tokens/yr}$) *while* retaining full white-box gradient access.

3. **Closed-Form Startup Re-Domiciliation ("Brain Drain") Threshold ($Q_{\text{drain}}^*$):**
   Let $\Delta V_{\text{hub}}$ be the annual agglomeration surplus of operating an AI startup inside a primary US venture hub (e.g., San Francisco or Boston network and capital access relative to an offshore hub), let $r \, C_{\text{reloc}}$ be the annualized cost of corporate re-domiciliation and founder relocation (at hurdle rate $r$), and let $C_{\text{compliance}}$ be the annual domestic legal/audit compliance burden imposed by an open-weight regulatory regime. A founder or R&D lab consuming $Q_{\text{tokens}}$ (in millions of tokens/year) faces an annual net payoff differential from offshoring R&D to an unconstrained jurisdiction:
   $$\Delta \Pi_{\text{reloc}}(Q_{\text{tokens}}) = Q_{\text{tokens}} \left(\bar{P}_{\text{closed}}(\rho) - \bar{P}_{\text{open}}(\rho)\right) + C_{\text{compliance}} - \left(\Delta V_{\text{hub}} + r \, C_{\text{reloc}}\right)$$
   Rational human-capital flight and corporate offshoring occur whenever $\Delta \Pi_{\text{reloc}}(Q_{\text{tokens}}) > 0$, yielding the **Critical Brain-Drain Token Threshold** ($Q_{\text{drain}}^*$):
   $$Q_{\text{drain}}^* = \frac{\Delta V_{\text{hub}} + r \, C_{\text{reloc}} - C_{\text{compliance}}}{\bar{P}_{\text{closed}}(\rho) - \bar{P}_{\text{open}}(\rho)}$$
   - **Numerical Sanity Check:** Let the US hub agglomeration premium be $\Delta V_{\text{hub}} = \$500,000/\text{yr}$, annualized relocation cost $r \, C_{\text{reloc}} = \$100,000/\text{yr}$, and domestic ban compliance overhead $C_{\text{compliance}} = \$120,000/\text{yr}$ (net hub barrier $\Delta V_{\text{net,hub}} = \$480,000/\text{yr}$). Against the verified blended price spread $\bar{P}_{\text{closed}}(3) - \bar{P}_{\text{open,V3}}(3) = \$48.7500 - \$0.8361 = \$47.9139/\text{M tokens}$:
     $$Q_{\text{drain}}^* = \frac{\$480,000}{\$47.9139/\text{M}} = 10,017.9697\text{M tokens/yr} \approx 10.0180\text{B tokens/yr} \quad (\approx 27.45\text{M tokens/day})$$
   - For a typical 10-engineer AI-native startup executing $Q_{\text{tokens}} = 100\text{B tokens/yr}$ ($100,000\text{M tokens/yr}$, or $\approx 273.97\text{M tokens/day}$ across agentic evaluation and synthetic data pipelines):
     - **Offshore Open-Weight Compute Burn:** $100,000 \times \$0.8361 = \$83,610/\text{yr}$.
     - **Domestic Banned Closed-API Burn + Compliance:** $100,000 \times \$48.7500 + \$120,000 = \$4,995,000/\text{yr}$.
     - **Net Annual Surplus from Offshoring ($\Delta \Pi_{\text{reloc}}(100\text{B})$):**
       $$\Delta \Pi_{\text{reloc}}(100\text{B}) = \$4,791,390 - \$480,000 = +\$4,311,390/\text{yr}$$
   A seed startup raising a $\$4\text{M}$ round cannot burn $\$4.88\text{M}/\text{yr}$ on closed APIs in California when re-domiciling its engineering team to Toronto, London, Zurich, or Singapore reduces compute burn by $98.3\%$ and saves $+\$4.31\text{M}/\text{yr}$ net of relocation friction. This replicates the exact empirical trajectory of the 1990s US "Crypto Wars," when classifying strong encryption (`>40-bit` keys) as munitions under the Arms Export Control Act (`22 U.S.C. § 2778`) failed to stop global PGP proliferation and instead drove cryptographic R&D and security software engineering to European jurisdictions until the US government relaxed `15 C.F.R. § 742.15` in 2000 (`65 Fed. Reg. 2492`).

4. **Physical & Constitutional Impossibility of Containing the Exit Valve (*Kent v. Dulles* & the Police-State Boundary):**
   Once $\Delta \Pi_{\text{reloc}}(Q_{\text{tokens}}) > 0$, the state cannot physically arrest the resulting brain drain or domestic weight execution without dismantling basic constitutional liberties:
   - **Fifth Amendment Right of International Exit (*Kent v. Dulles* & *Aptheker*):** Under *Kent v. Dulles*, 357 U.S. 116, 125 (1958), the Supreme Court held that *"The right to travel is a part of the 'liberty' of which the citizen cannot be deprived without due process of law under the Fifth Amendment,"* and in *Aptheker v. Secretary of State*, 378 U.S. 500, 505–06 (1964), the Court struck down statutory travel bans (`50 U.S.C. § 785`) as unconstitutional on their face. Short of imposing Soviet-style exit visas and physical border lockdowns on US computer scientists, the federal government cannot prevent domestic researchers or founders from boarding a flight to Zurich, London, or Toronto—nor can it prevent US engineers from training open weights on offshore GPU clusters over standard encrypted `SSH`/`TLS` sessions without erecting a domestic Great Firewall that decrypts all outbound internet traffic.
   - **Physical Information Density & Fourth Amendment Inspection Bar:** A 671B-parameter model quantized to `FP8` ($671\text{ GB}$) or `INT4` ($335.5\text{ GB}$) fits onto a single consumer $1\text{ TB}$ microSD card ($15\text{ mm} \times 11\text{ mm} \times 1\text{ mm}$, mass $\approx 0.25\text{ g}$, storage density $\ge 2,684\text{ GB/g}$) or transfers over a $10\text{ Gbps}$ fiber link in $268.4\text{–}536.8\text{ seconds}$. Detecting whether an air-gapped workstation or local GPU cluster is multiplying open-weight matrices (`BF16`/`FP8` tensor cores) rather than running a proprietary workload would require mandatory, warrantless kernel-level telemetry daemons scanning VRAM on every private computer in the United States—a categorical violation of the Fourth Amendment prohibition against general warrants (`U.S. Const. amend. IV`).

---

## 5. The Actual Policy Equilibrium: Where Regulatory Boundaries Settle

Because a domestic ban on open-weight possession and local execution is statutorily illegal (`50 U.S.C. § 1702(b)(3)`, `15 C.F.R. § 734.3(b)(3)`), constitutionally barred (*Bernstein*), macroeconomically suicidal ($\Omega_{\text{capture}} = 13.3333\times$), and triggers catastrophic R&D offshoring above $Q_{\text{drain}}^* = 10.0180\text{B tokens/yr}$, US policy equilibrium is forced into four narrower, legally enforceable perimeter controls:

1. **Federal Procurement & Agency Network Exclusions (`NDAA § 889` Architecture):**
   Under the Spending Clause, Congress and the Executive Branch can prohibit *federal executive agencies* and *covered federal contractors* from running foreign-origin software on government networks, mirroring Section 889 of the John S. McCain National Defense Authorization Act for Fiscal Year 2019 (`Pub. L. 115-232`, codified at `FAR 52.204-25`):
   > "Section 889(a)(1)(A) of the John S. McCain National Defense Authorization Act for Fiscal Year 2019 (Pub. L. 115-232) prohibits the head of an executive agency on or after August 13, 2019, from procuring or obtaining, or extending or renewing a contract to procure or obtain, any equipment, system, or service that uses covered telecommunications equipment or services as a substantial or essential component of any system, or as critical technology as part of any system." — `FAR 52.204-25(b)(1)`
   This restricts federal procurement without touching private domestic deployment.
2. **Foreign-Hosted SaaS Endpoint & Outbound Data Restrictions:**
   Regulators can restrict US enterprises from transmitting sensitive personal data or export-controlled technical data to *hosted inference endpoints domiciled in foreign jurisdictions* (where telemetry traverses foreign servers). However, this restriction vanishes the moment a US enterprise downloads the open weights and executes them air-gapped on domestic AWS, Azure, or on-premise silicon.
3. **Upstream Silicon & HBM Chokepoints:**
   Because published bits cannot be recalled or outlawed domestically, BIS enforcement concentrates on physical semiconductor manufacturing equipment (SME), EUV lithography, and high-bandwidth memory (HBM) export controls (`15 C.F.R. Part 744`).
4. **Source-Side API Telemetry Hardening:**
   Frontier laboratories must bear the private engineering burden of rate-limiting, KYC-gating, and watermarking their own hosted APIs against automated synthetic trace extraction, rather than petitioning the state to criminalize downstream linear algebra.

---

## 6. Verification & Falsification Conditions

The invariants of `SPEC-OPEN-WEIGHT-DISTILLATION-AND-DOMESTIC-BAN-IMPOSSIBILITY-v1.0` are falsified if and only if:

1. **Statutory Repeal & Constitutional Reversal:** Congress formally repeals `50 U.S.C. § 1702(b)(3)` and `15 C.F.R. § 734.3(b)(3)` with respect to mathematical weight tensors, *and* the Supreme Court overturns *Bernstein v. U.S. Dep't of Justice* and *Van Buren v. United States* to permit criminalization of domestic floating-point execution.
2. **Closed-to-Open Price Convergence ($\Phi_{\text{API}} \to 1.0$):** Closed US frontier APIs compress their blended token pricing from $\$48.75/\text{M}$ down to the marginal cost of open-weight sparse-MoE execution ($\le \$0.84/\text{M}$), eliminating the asymmetric self-sanction tax $\tau_{\text{reg}}$—which simultaneously liquidates the neocloud debt and capex moats modeled in `SPEC-NEOCLOUD-GPU-DEBT-AND-INFERENCE-DEFLATION-v1.0`.

### Artifacts & Verification Assets
- **Machine-Readable Schema:** `schema/open_weight_distillation_ban_impossibility_v1.0.json`
- **Deterministic Proof Engine:** `proofs/verify_open_weight_distillation_ban_impossibility.py`
- **Public Article Mirror:** `articles/open-weight-distillation-and-domestic-ban-impossibility.txt`
