# V4-R3 Confirmatory Campaign v1 — Frozen Protocol

Status: FROZEN after successful G1–G3 validity gates. This document fixes the remaining evaluation logic before observing confirmatory attack outcomes. V4-R3 is research code and is not claimed to replace standardized AEAD.

## Research question
Does the session-randomized, cryptographically keyed, stateful bidirectional V4-R3 construction prevent practically useful reuse or transfer of the pre-specified tested reconstruction strategies, and does the V5 nonlinear extension add measurable resistance beyond V4-R3?

## Threat model
Kerckhoffs setting. The evaluator knows the algorithm, equations, serialization, dimensions, block size, architecture, and experimental methodology but not the 256-bit master key. Evaluated capabilities are ciphertext-only, known-plaintext, and chosen-plaintext oracle access. Public nonces are visible. Nonce uniqueness is a requirement; no nonce-misuse resistance is claimed. Side channels, RNG compromise, endpoint compromise, and secret-memory compromise are outside scope.

## Closed validity gates
- G1: byte-exact encryption/decryption correctness across grayscale/RGB, regular/irregular dimensions, and synthetic patterns.
- G2: rejection of ciphertext, tag, nonce, metadata, and wrong-key tampering before plaintext release.
- G3: deliberately weak V0W positive control must be analytically and empirically recoverable. For L=256*256*3=196608 bytes, required chosen-plaintext queries are 1+ceil(log_256(L))=4.

Security experiments are interpretable only after G1–G3 pass.

## Frozen adversarial sequence
1. A0 reusable-XOR/equivalent-mask baseline.
2. A1 V0W permutation recovery positive control.
3. A2 equivalent-transformation known/chosen-plaintext reconstruction.
4. A3 differential chosen-plaintext diagnostics and query-budget sweep Q={1,2,4,8,16,32,64}.
5. A4 nonce-reuse and cross-session transfer.
6. A5 neural known-plaintext reconstruction with controls.
7. A6 multi-session neural reconstruction on unseen sessions.
8. V4-R3 versus V5-R3 paired nonlinear ablation.
9. Standardized AEAD engineering reference; not a security-equivalence comparison.

## Session/key separation matrix
Train/derive under K1,nu1 and evaluate under:
- K1,nu1: same key, same nonce; attacker-favorable same-session condition.
- K1,nu2: same key, independent nonce; nonce/session separation.
- K2,nu1: independent key, same public nonce value; key separation.
- K2,nu2: independent key and nonce; full separation.

Same-nonce reuse is a misuse experiment, not an advertised operating mode.

## CPA/KPA endpoints
Report exact byte recovery rate, image MSE/PSNR/SSIM where applicable, and query budget. Random exact-byte agreement reference is 1/256. Failure of a tested attack is reported only as failure of that attack; it is not a proof of IND-CPA security.

## Differential/internal-state diagnostics
For one-bit plaintext perturbations, record ciphertext influence and normalized state Hamming distance HD(Z_i,Z'_i)=Hamming(Z_i,Z'_i)/256 where instrumented. Influence matrices and distance-to-perturbation profiles are diagnostics for locality, periodicity, block structure, or directional artifacts; they are not security proofs.

## Neural protocol
Seeds: 17, 271, 1618, 4099, 12345.
Models: CNN and Tiny U-Net.
Primary endpoint: SSIM. Secondary: MSE and PSNR.
Split natural-image data by source-image identity before cropping; training and test source identities must be disjoint. Preprocessing statistics are fit on training data only. Checkpoints are selected using validation data; each seed's held-out test set is evaluated once.

Required conditions:
- DL0 mean-image negative control.
- DL1 random-pairing negative control.
- DL2 V0W fixed-session positive control.
- DL3 V4-R3 fixed-to-fixed attacker-favorable condition.
- DL4 V4-R3 fixed-to-unseen-session transfer.
- DL5 V4-R3 fresh-training-to-unseen-session PRIMARY.
- DL6 V5-R3 fresh-training-to-unseen-session ablation.

Ciphertext-use ablations compare correct ciphertext with shuffled, wrong, random, or zeroed ciphertext inputs. Interpret reconstruction as useful only if it improves over negative controls, depends on the correct ciphertext, preserves target identity rather than only dataset priors, is consistent across seeds, and transfers under the pre-specified session regime. No arbitrary post-hoc SSIM threshold is used.

## V4/V5 ablation statistics
For each paired seed define d_i = SSIM_V4,i - SSIM_V5,i, so positive d_i means the V5 attacker achieved lower SSIM. Report paired differences, mean, SD, bootstrap 95% CI, and a paired inferential test/effect size where assumptions permit. A non-significant result is not evidence of equivalence. Unless a practical equivalence margin is justified before execution, use the wording 'no measurable advantage observed' rather than 'equivalent'. V5 will not be retuned after seeing confirmatory outcomes.

## Correctness and falsification policy
Architecture, attack definitions, query budgets, seeds, primary endpoints, and interpretation rules are frozen for the confirmatory campaign. If V4-R3 breaks reproducibly, report the break. Any later repaired architecture must receive a new version identifier (e.g. V4-R4) and a new confirmatory campaign; results may not be silently pooled with V4-R3.

## Performance protocol
Warm up before timing. Measure encryption and decryption separately using repeated trials on the same environment. Preserve raw timings and report median, mean, SD, 95% CI, and throughput. Performance comparisons to a standardized AEAD are engineering context only.

## Evidence hierarchy
Correctness/authentication -> positive-control attack -> conventional ciphertext diagnostics -> boundary/state diagnostics -> KPA/CPA -> nonce/session transfer -> neural reconstruction with controls -> nonlinear ablation -> engineering benchmark.

## Claim discipline
Allowed final form only if supported by executed results: 'Under the implemented [named] experiments, no practically useful equivalent transformation or image reconstruction was demonstrated for V4-R3.' Always append that empirical findings do not constitute a formal security proof and do not establish equivalence to standardized authenticated-encryption schemes.
