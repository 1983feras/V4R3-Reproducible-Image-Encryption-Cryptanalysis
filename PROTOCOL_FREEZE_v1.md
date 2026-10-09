# V4-R3 Red-Team Confirmatory Protocol v1

Status: **FROZEN BEFORE CONFIRMATORY OUTCOMES**

This protocol separates development/reference observations from the final confirmatory campaign. It is intentionally falsification-oriented: a reproducible break of V4-R3 is an admissible scientific outcome.

## Research questions

**H1 / session-structure hypothesis.** Under the implemented attacks, session-randomized V4-R3 prevents practically useful reuse of an equivalent transformation across independent nonces.

**H2 / nonlinear-ablation hypothesis.** V5-R3 provides measurable adversarial resistance beyond V4-R3 under the same attacks and data splits.

Failure to support either hypothesis is reportable and must not trigger post-hoc tuning of the frozen variant.

## Scope and claim policy

V4-R3 and V5-R3 are experimental image-encryption constructions. They are not claimed to replace standardized AEAD and no empirical experiment is treated as a formal IND-CPA/AEAD security proof. Entropy, histogram, correlation, NPCR, and UACI are secondary diagnostics, not primary evidence of cryptographic security.

The master secret is 256 bits. The public nonce is not counted as secret entropy. Derived nonlinear states or parameters are not added to the master-key size to inflate a key-space claim.

Side-channel, cache, power, fault-injection, RNG-compromise, and memory-compromise attacks are outside this software-level study.

## Frozen evaluation order and gates

### G1 — Correctness

Required byte-exact round trips for grayscale and RGB at 32x32, 64x64, 128x128, 256x256, and irregular 257x263 dimensions, including zero, all-255, gradient, checkerboard, impulse, and random inputs where applicable.

Pass condition: recovered plaintext equals input byte-for-byte; mismatched bytes = 0; MSE = 0.

If G1 fails, stop all security experiments.

### G2 — Authentication and metadata integrity

The authenticated variant must reject wrong-key verification and independent tampering of ciphertext, tag, nonce, and authenticated metadata. Variable-length serialized fields must be unambiguous (fixed-width or length-prefixed). No unauthenticated plaintext is released to the caller.

If G2 fails, stop all security experiments that rely on the authenticated construction.

### G3 — Positive-control cryptanalysis

V0W is the deliberately vulnerable control:

`C = P_pi XOR Z`

For L = 256*256*3 = 196608 bytes, base-256 encoded-index recovery has analytical chosen-plaintext query requirement:

`Q = 1 + ceil(log_256(L)) = 4`.

The attack pipeline must empirically recover the intended V0W structure. Evaluate query budgets Q in {1,2,4,8,16,32,64}. Primary endpoint: byte-recovery rate BR(Q).

If the positive control does not behave as analytically expected, the CPA pipeline is invalid and V4 attack failures are not interpretable as evidence.

### G4 — V4-R3 structural red team

Run, without architecture modification:

1. reusable-XOR/equivalent-mask probes;
2. known-pair equivalent-transformation transfer;
3. structured chosen-plaintext differential probes;
4. boundary-directed bit flips around 256-byte boundaries;
5. influence-matrix analysis;
6. same-session attack transfer;
7. deliberate nonce-reuse stress test;
8. same-key cross-nonce transfer;
9. multi-session training/derivation followed by an unseen nonce;
10. one-bit master-key and nonce sensitivity as diagnostics only.

A successful attack is retained and reported; it is not removed by modifying V4-R3 during this campaign. Any repaired architecture receives a new version identifier.

### G5 — Neural attack validity

Before interpreting neural failure against V4-R3, the same neural pipeline must demonstrate learnability on a deliberately vulnerable positive control.

Primary architectures: CNN and Tiny U-Net.

Frozen training seeds: 17, 271, 1618, 4099, 12345.

Source-image identities must be split before cropping. Training, validation, and test source identities are disjoint. Nonce/session splits are also created before encrypted examples are generated. Model/checkpoint selection uses validation data only; held-out test metrics are not used for tuning.

Required controls:

- mean-image negative control;
- random-pairing negative control;
- V0W fixed-session positive control;
- V4 fixed-session attacker-favorable condition;
- V4 cross/unseen-session condition;
- V4 fresh/multi-session to unseen-session primary condition;
- V5 corresponding unseen-session ablation.

Primary neural endpoint: per-evaluation-unit SSIM. Secondary: MSE and PSNR. Also evaluate dependence on the correct ciphertext by shuffled/wrong-ciphertext controls and identity-specific reconstruction using wrong-plaintext comparisons.

The statistical unit is the held-out source image/evaluation unit, not individual pixels.

### G6 — Nonlinear ablation

V5-R3 is a controlled ablation of V4-R3. Nonlinear dynamics are not treated as the root of cryptographic security and are not tuned after V4/V5 outcomes are observed.

For paired held-out units compute a consistently signed V4-vs-V5 attack metric difference, mean, SD, paired bootstrap 95% CI, and an appropriate paired comparison. A non-significant p-value alone is not interpreted as equivalence. Without a justified equivalence margin, use the wording `no measurable advantage observed` rather than `equivalent`.

## Primary endpoints

1. CPA: BR(Q), the correctly recovered plaintext-byte fraction versus query budget.
2. Cross-session: attack recovery/reconstruction on an independent nonce relative to its negative/control reference.
3. Neural: held-out SSIM relative to negative controls, with ciphertext-dependence and identity-dependence checks.
4. V4/V5 ablation: paired attack-performance difference on identical evaluation units.
5. Engineering: encryption/decryption latency and throughput, reported separately from security claims.

Entropy, correlation, histogram, NPCR, UACI, and key/nonce avalanche diagnostics remain secondary.

## Influence-matrix diagnostic

For a base plaintext P and a one-bit perturbation at input position j and bit b, compute ciphertexts C and C'. Record whether ciphertext position k changes. Average over b to obtain an input-output influence matrix. Inspect pre-specified structural signatures: diagonal/triangular structure, periodicity, block boundaries, dead regions, and direction-dependent propagation. Also summarize change probability as a function of relative distance k-j.

This is a structural diagnostic, not a formal differential-security proof.

## Nonce model

The nonce is public. Correct-use experiments require nonce uniqueness under a fixed master key. Nonce-reuse experiments are deliberate misuse stress tests. Unless separately demonstrated, V4-R3 is not claimed to provide nonce-misuse resistance.

Cross-session attackers know both the algorithm and public nonce values.

## Reproducibility requirements

Each run must record at minimum:

- protocol/version and variant;
- source-code commit;
- experiment identifier;
- seed;
- query budget where applicable;
- nonce regime;
- hashes of input/evaluation manifests;
- software versions and hardware summary;
- raw per-unit metrics;
- runtime measurements;
- output-file SHA-256.

Raw results are immutable evidence. Summary tables and figures must be regenerated from raw machine-readable results rather than manually transcribed values.

Public deterministic test vectors should include a fixed public test key and nonce, plaintext hash, selected intermediate digests sufficient to detect implementation drift, final ciphertext hash/tag, and recovered-plaintext hash. Test-vector keys are public reproducibility material, not operational secrets.

## Interpretation policy

Allowed conclusion form if attacks do not yield useful recovery:

> Under the implemented chosen-plaintext, known-plaintext, cross-session, differential, and neural reconstruction experiments, no practically useful equivalent transformation or image reconstruction was demonstrated for V4-R3. These empirical findings do not constitute a formal security proof or establish equivalence to standardized authenticated-encryption schemes.

Allowed V5 conclusion when supported:

> The nonlinear V5-R3 extension did not demonstrate a measurable attack-resistance improvement sufficient to justify its additional complexity under the evaluated attacks.

If V4-R3 is reproducibly broken, report the break as the principal result. Do not silently patch the frozen variant; any redesign is a new version and a new protocol.