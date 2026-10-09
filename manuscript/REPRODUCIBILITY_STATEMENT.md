# Reproducibility Statement

The confirmatory study uses versioned source code, frozen protocols, deterministic public test vectors, predeclared seeds and query budgets, GitHub Actions execution for lightweight gates/diagnostics, raw JSON outputs, and SHA-256 evidence manifests. Results are entered into the manuscript only after successful execution and evidence archival. Development-only numbers are explicitly separated from confirmatory evidence.

For neural experiments, the final artifact will additionally record source-image identities, dataset/license provenance, source-identity train/validation/test split, crop generation parameters, preprocessing statistics derived from training data only, model architecture, optimizer, learning rate, epochs, random seed, checkpoint-selection rule, software versions, hardware, and raw per-image metrics.

For performance experiments, the final artifact will record warm-up policy, repetition count, encryption/decryption timings, input size, throughput calculation, hardware/software environment, and standardized AEAD reference configuration.

No secret production key is published. Deterministic public test keys/nonces are test-vector material only and must never be reused operationally.
