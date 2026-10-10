# Freeze D V2 Remote Byte Reconciliation V1

## Status

Provenance-only reconciliation performed before any neural training or DL0–DL6 execution.

## Context

The prospectively audited local Freeze D V2 runner had SHA-256:

`e42ffccb2afefd28dea805604696837b751137a7fecc19976e742a5b7bb587fb`

After PR #6 was merged, the runner present on `main` had SHA-256:

`bca899081068c5e9384462355060cea14ab32e598140a84fb701807ef8942921`

The Freeze D V2 specification and pre-execution evidence remained byte-identical to the audited versions:

- specification: `b79fe59e7d89f4c9a16acdb95498697ce0a08d11d045ad35c6893408ca4cfe9e`
- evidence: `91c3930b3185920cb8d744cabdfa438907c637a394548c397859b167d4f8483d`

## Exact runner differences

A read-only comparison against local audited commit `d6db6e59445454291ec1f24335fa11f87a759c66` found exactly two textual differences in the merged runner:

1. The preflight error message text changed from `V0W 4-query validity gate mismatch` to `V0W 4-query validation gate mismatch`.
2. The closing parenthesis of the `--output-dir is required and must be persistent storage` RuntimeError block has different indentation.

Neither difference changes executed scientific logic, model architecture, dataset construction, V0W encryption, crop sampling, seeds, optimization, checkpoint selection, early stopping, SSIM computation, blind evaluation, resume behavior, or any DL2 endpoint.

## Semantic audit

The merged runner was checked before execution and retained all critical frozen semantics:

- protocol `DL2_V0W_RECOVERY_FREEZE_D_V2`;
- DL2 fixed-to-fixed positive-control condition;
- 256×256 RGB patches;
- DIV2K source-identity split 1–640 / 641–800 / 801–900;
- deterministic crop seed rule and horizontal flip;
- fixed V0W key;
- CNN and TinyUNet attackers;
- Adam optimizer and L1 loss;
- gradient clipping and CUDA mixed precision;
- prospectively frozen 11×11 Gaussian-window RGB SSIM, sigma 1.5, K1 0.01, K2 0.03, data range 1.0;
- validation checkpointing and blind-test-once rule;
- atomic JSON output and completed-model/seed resume points;
- explicit `--execute` boundary.

All critical checks passed. No V4/V5 experimental execution was introduced.

## Execution boundary

At reconciliation time:

- neural training executed: FALSE
- DL0 executed: FALSE
- DL1 executed: FALSE
- DL2 executed: FALSE
- DL3 executed: FALSE
- DL4 executed: FALSE
- DL5 executed: FALSE
- DL6 executed: FALSE

## Authoritative execution identity

Because the merged runner was semantically audited before any outcome was observed, the remote runner SHA-256

`bca899081068c5e9384462355060cea14ab32e598140a84fb701807ef8942921`

is designated the authoritative execution identity for Recovery Freeze D V2. Subsequent DL2 execution must use this exact runner byte identity. No scientific setting is changed by this reconciliation.
