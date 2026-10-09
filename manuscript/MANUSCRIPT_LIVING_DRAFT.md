# Cryptanalysis-Guided Evaluation of Adaptive Image Encryption: Stateful Bidirectional Diffusion, Cross-Session Attacks, and Nonlinear Ablation

**Author:** Firas Sulaiman

> Living confirmatory manuscript. Numerical claims are admitted only after machine-readable evidence exists. Pending experiments remain explicitly marked and must not be converted into positive security claims.

## Abstract
Conventional image-encryption studies frequently emphasize ciphertext entropy, adjacent-pixel correlation, NPCR, and UACI. These measurements are useful diagnostics but do not establish resistance to known- or chosen-plaintext attacks. This study adopts a cryptanalysis-guided methodology for an experimental adaptive image-encryption construction, V4-R3, built around session-separated cryptographic key derivation, a session-dependent permutation and byte substitution, stateful bidirectional diffusion, and ciphertext authentication. A deliberately weak construction, V0W, is included as a positive cryptanalytic control. In the frozen confirmatory campaign, correctness and authentication gates passed, and the V0W control was completely recovered with the analytically predicted four chosen plaintexts for a 256x256x3 byte image. These results validate the experimental attack pipeline but do not establish security of V4-R3. Cross-session transfer, stronger chosen-plaintext diagnostics, neural known-plaintext cryptanalysis, nonlinear V4/V5 ablation, and standardized-AEAD engineering comparison are evaluated under a pre-registered protocol. [FINAL NUMERICAL SENTENCES PENDING CONFIRMATORY EVIDENCE.]

## 1. Introduction
Image encryption is often evaluated with statistical measurements that describe the appearance or local sensitivity of ciphertext. High entropy, weak adjacent-pixel correlation, and near-reference NPCR/UACI can be desirable, yet none directly demonstrates that an adversary cannot infer a reusable transformation. The central methodological position of this work is therefore: **security benefit should be measured against an adversary rather than inferred from mechanism or ciphertext appearance.**

The study asks whether image-specific permutation, substitution, stateful diffusion, and an additional nonlinear dynamical component provide measurable adversarial resistance once cryptographically sound session derivation is already present. V4-R3 is treated as an experimental construction, not as a replacement for standardized authenticated encryption. V5-R3 adds nonlinear dynamical material solely as a falsifiable ablation: if it does not reduce attack success relative to V4-R3, the additional complexity is not credited as a security contribution.

### Contributions
1. A session-randomized experimental architecture using cryptographically keyed permutation/substitution, stateful bidirectional diffusion, and authentication.
2. A falsification-oriented evaluation methodology with a deliberately breakable positive control, explicit query budgets, cross-session/key separation, and neural controls.
3. A paired nonlinear ablation that asks whether the V5 extension provides measurable resistance beyond V4 rather than assuming that nonlinear complexity is beneficial.

## 2. Threat Model and Research Questions
The adversary follows Kerckhoffs's principle: the algorithm, equations, serialization, block size, architecture, and methodology are public; the 256-bit master key is secret. Evaluated capabilities include ciphertext-only observation, known plaintext, and a chosen-plaintext encryption oracle. Fixed-session experiments intentionally reuse a session to expose reusable structure; cross-session experiments use distinct public 128-bit nonces. Nonce uniqueness is required and nonce-misuse resistance is not claimed. Side channels, RNG compromise, and direct key-memory compromise are outside scope.

RQ1: Does the revised stateful construction eliminate the previously observed position-dependent diffusion defect under the reproduced diagnostic?

RQ2: Can the implemented known- or chosen-plaintext attacks recover a practically useful equivalent transformation for V4-R3?

RQ3: Does attack knowledge obtained under one session transfer to an independently nonced session or independently keyed session?

RQ4: Does V5-R3 provide measurable attack resistance beyond V4-R3?

## 3. Construction Under Evaluation
V4-R3 uses a 256-bit master key and fresh public 128-bit nonce. Session subkeys are derived with RFC5869-style HKDF-HMAC-SHA-256 and domain separation. Metadata is unambiguously serialized and bound into the session context. A Fisher-Yates permutation uses rejection sampling to avoid modulo bias; a session-dependent bijective 8-bit S-box follows. Two independently keyed stateful diffusion passes operate in opposite directions. Authentication is Encrypt-then-MAC over version, variant, nonce, dimensions, block size, length, context, and ciphertext. Decryption verifies the authentication tag before releasing plaintext.

V5-R3 retains this cryptographic root and introduces quantized nonlinear dynamical material as an ablation. The nonlinear subsystem is not treated as the root of security, and no hyperchaos claim is made without the required Lyapunov evidence.

V0W is deliberately weak: C_i = P_{pi(i)} XOR Z_i with reusable permutation and mask. A zero plaintext exposes the mask and base-256 encoded-index plaintexts expose the permutation. Its analytical query requirement is 1+ceil(log_256 L).

## 4. Confirmatory Methodology
The evidence hierarchy is correctness, authentication, positive-control cryptanalysis, statistical diagnostics, boundary/internal-state diffusion, KPA/CPA, nonce and cross-session transfer, neural cryptanalysis, nonlinear ablation, and engineering comparison. Architecture and protocol are frozen before confirmatory outcomes are inspected. A broken V4-R3 is reported as such rather than repaired inside the same confirmatory campaign.

### 4.1 Validity gates
G1 requires byte-exact recovery across grayscale/RGB, multiple sizes, irregular dimensions, and synthetic edge patterns. G2 requires rejection of wrong keys and modified nonce, metadata, ciphertext, or tag. G3 requires successful V0W recovery. G4 requires learnability of the neural positive control before negative neural results for V4 can be interpreted. G5 checks session separation. G6 requires versioned configuration, seeds, hashes, and raw machine-readable results.

### 4.2 Adversarial experiments
The frozen red-team sequence includes reusable-XOR transfer, permutation recovery, equivalent-transformation CPA, differential CPA, cross-session transfer, neural KPA, and multi-session neural evaluation. Query budgets are Q={1,2,4,8,16,32,64}. The key/nonce separation matrix evaluates same key/same nonce, same key/new nonce, new key/same nonce, and new key/new nonce.

### 4.3 Neural evaluation
CNN and Tiny U-Net attackers are evaluated over five frozen seeds {17,271,1618,4099,12345}. Source-image identities are split before cropping to prevent train/test identity leakage. The primary endpoint is SSIM; MSE and PSNR are secondary. Mean-image and random-pairing controls are included, while V0W fixed-session reconstruction serves as the positive control. Correct-ciphertext versus shuffled/wrong/zero/random-ciphertext ablations are used to determine whether apparent reconstruction depends on the ciphertext rather than dataset priors.

### 4.4 Statistics
Results are reported per independent seed and summarized with mean, standard deviation, and 95% confidence intervals where justified. V4/V5 comparisons are paired by seed. A nonsignificant p-value is not interpreted as equivalence. Without a justified a-priori equivalence margin, the permitted conclusion is only that no measurable advantage was observed.

## 5. Results
### 5.1 Correctness and authentication gates
The confirmatory CI run passed all 16 registered G1/G2 tests. Exact decryption was verified over the registered test cases, and authentication tests rejected ciphertext, tag, nonce, authenticated-metadata, and wrong-key modifications. These are implementation-validity results, not proofs of confidentiality.

### 5.2 Positive-control cryptanalysis
For L=256x256x3=196,608 bytes, V0W has an analytical requirement of four chosen plaintexts. The confirmatory execution recovered the reusable mask, permutation, and target plaintext at 100%, matching the analytical prediction. This establishes that the evaluation pipeline can expose a construction with the intended structural weakness.

### 5.3 Conventional diagnostics
Exploratory/reference implementation results showed ciphertext entropy near 7.985 bits/byte and session-randomization NPCR near 99.6% with UACI near 33.3% for V4/V5. These values are retained as secondary diagnostics only and are not used as evidence of semantic or chosen-plaintext security. [CONFIRMATORY REPLICATION PENDING.]

### 5.4 Boundary and internal-state diffusion
Earlier development diagnostics found that the revised 256-bit state removed the previously detected position-dependent boundary defect under the reproduced boundary test. This is a design diagnostic rather than a security proof. [CONFIRMATORY INFLUENCE-MATRIX/STATE-AVALANCHE RESULTS PENDING.]

### 5.5 Known- and chosen-plaintext cryptanalysis
The positive-control attack succeeds as expected. V4-R3 is evaluated using the frozen equivalent-transformation and differential tests without post-outcome tuning. [CONFIRMATORY NUMBERS PENDING.]

### 5.6 Nonce reuse and cross-session transfer
The pre-registered key/nonce separation matrix measures exact-byte recovery relative to the random-byte reference 1/256. [CI RUN IN PROGRESS; INSERT MACHINE-READABLE SUMMARY ONLY AFTER COMPLETION.]

### 5.7 Neural known-plaintext cryptanalysis
[BLOCKED UNTIL G4 POSITIVE-CONTROL LEARNABILITY PASSES.]

### 5.8 Nonlinear V4/V5 ablation
Exploratory results did not show a material V5 advantage, but the final conclusion is withheld pending paired confirmatory experiments. No V5 retuning is permitted after inspecting V4 results.

### 5.9 Engineering reference
A standardized AEAD is included for engineering context rather than to establish security equivalence or superiority. Runtime, throughput, and ciphertext expansion are compared under the same benchmark protocol. [CONFIRMATORY BENCHMARK PENDING.]

## 6. Discussion
The positive control illustrates why conventional image-cipher statistics are insufficient: a construction can exhibit superficially plausible ciphertext statistics while retaining exploitable reusable structure. The study therefore separates implementation correctness, statistical diagnostics, empirical cryptanalysis, and formal security claims. Even if every implemented V4 attack fails, the supported statement is that no practically useful equivalent transformation or reconstruction was demonstrated under those experiments; it is not a proof of IND-CPA security.

The nonlinear ablation is intentionally capable of producing a negative result. If V5 does not consistently reduce attack success beyond V4, the correct conclusion is that the tested nonlinear extension did not demonstrate sufficient additional resistance to justify its complexity. This does not imply that nonlinear dynamics are universally useless; it limits the claim to the tested construction and threat model.

## 7. Limitations
This work evaluates a custom experimental image-encryption architecture and does not provide a formal reduction to a standard cryptographic assumption. The attack suite is finite, neural conclusions depend on the registered dataset/model/training regime, and timing depends on implementation and hardware. Side-channel resistance, RNG compromise, key-memory compromise, and nonce-misuse resistance are not established. Standardized AEAD remains the appropriate reference for production cryptographic deployment.

## 8. Conclusion
This work replaces mechanism-driven security inference with a falsification-oriented evaluation. The confirmatory pipeline has already established implementation correctness/authentication behavior and has independently broken the deliberately weak positive control at its predicted query complexity. Final conclusions about V4-R3, cross-session transfer, neural reconstruction, and the V5 nonlinear ablation will be admitted only from frozen confirmatory artifacts. [FINAL CONCLUSION TO BE GENERATED FROM COMPLETED ARTIFACTS.]

## Reproducibility and Artifact Availability
Cryptographic variants, positive-control attacks, session-transfer experiments, neural cryptanalysis scripts, experiment configurations, random seeds, raw per-run metrics, environment metadata, and figure-generation scripts are maintained as a versioned reproducibility artifact. Summary tables and figures are generated from raw machine-readable results rather than manually transcribed values.
