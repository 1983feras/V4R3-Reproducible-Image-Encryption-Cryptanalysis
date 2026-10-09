# Cryptanalysis-Guided Evaluation of Adaptive Image Encryption: Stateful Bidirectional Diffusion, Cross-Session Attacks, and Nonlinear Ablation

**Firas Sulaiman**

## Abstract
Conventional image-encryption studies often report entropy, correlation, NPCR, and UACI as principal evidence. This work instead adopts a cryptanalysis-guided evaluation in which a session-randomized experimental image cipher, V4-R3, is subjected to correctness/authentication gates, an intentionally weak positive control, bounded chosen-plaintext diagnostics, cross-session transfer tests, and neural reconstruction controls. V4-R3 derives session material from a 256-bit master key and a public 128-bit nonce using domain-separated HKDF-HMAC-SHA-256, applies a session-dependent permutation and bijective byte substitution, and uses two stateful directional diffusion passes followed by authentication. It is an experimental construction and is not proposed as a replacement for standardized AEAD. Confirmatory correctness/authentication tests passed 16/16 cases. The V0W positive control was completely recovered with its analytically sufficient chosen-plaintext budget, whereas the frozen V4-R3 lookup diagnostic remained near the 1/256 random byte-match reference for Q from 1 to 64 and showed no monotonic recovery gain. A simple equivalent-XOR transfer diagnostic likewise remained near random across same-session and changed-key/nonce conditions. These results are evidence against the specific tested reusable-transform hypotheses, not a formal security proof. Additional differential, neural, nonlinear-ablation, and engineering-reference results are reported only after their frozen confirmatory campaigns complete.

## 1. Introduction
Image-encryption evaluation should distinguish statistical appearance from adversarial recoverability. Near-uniform ciphertext statistics are useful diagnostics, but they do not by themselves establish resistance to known- or chosen-plaintext analysis. This study therefore asks a different question: after cryptographically keyed session derivation and stateful diffusion are present, can explicit attackers extract reusable structure, transfer learned relations between sessions, or reconstruct image-specific plaintext information?

The study contributes: (1) a reproducible experimental V4-R3 architecture with authenticated, session-randomized stateful bidirectional diffusion; (2) an evaluation methodology centered on positive cryptanalytic controls, frozen query budgets, session-transfer tests, and neural controls; and (3) a falsifiable V5-R3 nonlinear ablation designed to test whether nonlinear dynamical material adds measurable attack resistance rather than assuming that it does.

## 2. Threat Model and Claim Boundaries
Kerckhoffs' principle is assumed. The adversary knows the algorithm, equations, serialization, dimensions, block size, and evaluation protocol but not the 256-bit master key. Ciphertext-only, known-plaintext, and chosen-plaintext capabilities are evaluated under explicitly defined conditions. The nonce is public and uniqueness is required. Side channels, random-number-generator compromise, and memory/key compromise are outside scope. Empirical failure of an implemented attack is never interpreted as a formal security proof.

## 3. V4-R3 Experimental Construction
V4-R3 uses a 256-bit master secret and a fresh public 128-bit nonce. Domain-separated HKDF-HMAC-SHA-256 derives session material for permutation, substitution, forward diffusion, backward diffusion, and authentication. A rejection-sampled Fisher-Yates procedure creates a session-dependent permutation, followed by a dynamic bijective 8-bit S-box. Forward and reverse bytewise diffusion maintain cryptographic state updated from intermediate ciphertext. Authentication binds version/variant, nonce, dimensions, block size, length, context, and ciphertext; verification precedes plaintext release.

The construction is experimental. Its 256-bit master-key length is not described as '256-bit security', and the public nonce is not added to key-space estimates.

## 4. Evaluation Methodology
The evidence hierarchy is: correctness -> authentication -> positive-control cryptanalysis -> conventional statistical diagnostics -> boundary/differential diagnostics -> known/chosen-plaintext diagnostics -> cross-session transfer -> neural cryptanalysis -> V4/V5 ablation -> engineering comparison with a standardized AEAD reference. Seeds, query budgets, model families, endpoints, and claim boundaries are frozen before confirmatory interpretation.

### 4.1 Positive control
V0W deliberately uses a reusable permutation-mask relation C[i]=P[perm[i]] XOR mask[i]. A zero plaintext exposes the mask and base-256 encoded-index plaintexts expose the permutation. This positive control tests whether the harness can recover a construction known to be structurally vulnerable.

### 4.2 Query budgets
Chosen-plaintext diagnostic budgets are Q={1,2,4,8,16,32,64}. Exact-byte recovery is compared with the random byte-match reference 1/256.

### 4.3 Session transfer
The frozen key/nonce matrix separates same-key/same-nonce, same-key/new-nonce, new-key/same-nonce, and new-key/new-nonce conditions. Transfer diagnostics are interpreted only for the tested relation.

### 4.4 Neural evaluation
[CONFIRMATORY RESULTS PENDING: G4 positive control must pass before V4/V5 neural failures are interpreted. CNN and Tiny U-Net; five frozen seeds; source-identity-disjoint split; mean/random-pairing/ciphertext-use controls; SSIM primary endpoint.]

### 4.5 Nonlinear ablation
[CONFIRMATORY RESULTS PENDING: V5-R3 is an ablation only. The investigated nonlinear system is not labeled hyperchaotic without two robust positive Lyapunov exponents.]

## 5. Results
### 5.1 Correctness and authentication
At frozen run 37964345071, 16/16 confirmatory tests passed, including exact recovery and rejection of ciphertext, tag, nonce, metadata, and wrong-key modifications covered by the test suite.

### 5.2 Positive-control recovery
For V0W with length 196608 bytes, the analytically sufficient total chosen-plaintext budget was four queries. The experiment recovered permutation, mask, and target plaintext with rate 1.0. This establishes that the harness produces a strong positive result when reusable structure is deliberately present.

### 5.3 Equivalent-XOR session-transfer diagnostic
Across five frozen seeds, mean exact-byte recovery was 0.00436198 for same key/same nonce, 0.00377604 for same key/new nonce, 0.00488281 for new key/same nonce, and 0.00377604 for new key/new nonce, compared with 0.00390625 random matching. Thus the implemented reusable-XOR transformation did not yield practically useful target reconstruction in any tested condition.

### 5.4 Query-budget diagnostic
Mean V4-R3 recovery at Q={1,2,4,8,16,32,64} was {0.00384115, 0.00384115, 0.00390625, 0.00397135, 0.00429688, 0.00423177, 0.00403646}. The series remained close to 1/256 and did not show monotonic improvement as Q increased. By contrast, V0W achieved exact recovery at the first sampled budget above its analytical threshold for the 32x32x3 diagnostic.

### 5.5 Differential and boundary analysis
[CONFIRMATORY RESULTS PENDING]

### 5.6 Deliberate nonce-reuse stress
[CONFIRMATORY RESULTS PENDING. No nonce-misuse-resistance claim will be made.]

### 5.7 Neural known-plaintext evaluation
[CONFIRMATORY RESULTS PENDING]

### 5.8 V4-R3 versus V5-R3
[CONFIRMATORY RESULTS PENDING]

### 5.9 Engineering reference
[CONFIRMATORY RESULTS PENDING. A standardized AEAD reference is for engineering context, not security equivalence.]

## 6. Discussion
The completed evidence already demonstrates why positive controls and explicit attack models are more informative than reporting ciphertext statistics alone. V0W is decisively recoverable, whereas the two frozen reusable-transform diagnostics applied to V4-R3 do not produce useful recovery. This difference is meaningful only within the tested attack classes. Stronger conclusions require the remaining differential, neural, cross-session, and ablation evidence.

A central falsifiable question is whether V5-R3's nonlinear component adds measurable resistance after cryptographic session derivation and stateful diffusion are already present. A null or negligible V5 advantage is scientifically informative and will not trigger post-hoc tuning.

## 7. Limitations
This work evaluates a custom experimental cipher and cannot provide the assurance associated with extensively analyzed standardized cryptographic schemes. Empirical cryptanalysis is necessarily attack-dependent. The study therefore reports what was and was not recovered under frozen tests rather than asserting universal resistance. Timing results are implementation- and platform-dependent. Neural conclusions require successful positive and negative controls and source-identity-disjoint evaluation.

## 8. Conclusion
The study advances an evidence-first methodology for experimental image encryption: establish correctness, demonstrate attack sensitivity using a vulnerable positive control, freeze attacker capabilities and budgets, test session transfer and reconstruction directly, and treat nonlinear mechanisms as ablations whose benefit must be measured. The completed V4-R3 results reject two simple reusable-transform hypotheses under the implemented experiments while deliberately stopping short of a general security claim. Final conclusions will be limited to the complete confirmatory evidence set.

## Reproducibility
Repository artifacts include the confirmatory implementation, tests, positive control, frozen protocols, deterministic public test vector, experiment scripts, raw JSON results, and SHA-256 evidence manifests. Exact commit and artifact identifiers are recorded in `manuscript/RESULTS_LEDGER.md`.
