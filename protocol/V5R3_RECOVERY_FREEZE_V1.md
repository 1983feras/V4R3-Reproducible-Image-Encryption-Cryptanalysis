# V5-R3 Recovery Prospective Freeze V1

## Status

This document reconstructs the previously specified V5-R3 prospective
nonlinear ablation after loss of an unpushed local-only Git commit from an
ephemeral runtime.

The reconstruction occurs before execution of DL2-DL6 neural experiments.

No neural outcome was inspected in defining this recovery implementation.

## Authoritative recovery baseline

- Base Git commit: `86ed0093999a2ef3b31ea600c0202ec36ea4b8b6`
- Confirmatory configuration SHA-256:
  `638c9f481347a295e424778b61d257fd946e8dd3af976dfbc06f66d4aa6eecb7`

## Architectural relationship to V4-R3

V4-R3:

`permutation -> session S-box -> forward diffusion -> reverse diffusion -> authentication`

V5-R3 recovery ablation:

`permutation -> session S-box -> nonlinear byte mixing -> forward diffusion -> reverse diffusion -> authentication`

The intended controlled architectural difference is one invertible
nonlinear byte-mixing stage inserted after the session S-box and before
forward diffusion.

## Nonlinear recurrence

The experimental recurrence is:

`z_(n+1) = r * z_n * (1 - z_n)`

with:

- session-derived `z0` strictly inside `(0,1)`;
- `r` in `[3.99,4.0)`;
- burn-in = 256 iterations;
- `q_n = floor(2^32 * z_n) mod 256`.

Forward byte mixing:

`y_n = (x_n + q_n) mod 256`

Inverse:

`x_n = (y_n - q_n) mod 256`

## Session derivation

The nonlinear sequence is domain-separated using:

- `V5-R3-PROSPECTIVE-V1`
- `K_NONLINEAR`
- master key
- public nonce
- image/context metadata
- HMAC-SHA-256.

## Claim boundary

This is a controlled nonlinear ablation only.

The logistic recurrence is not claimed to be the cryptographic root of
security.

No hyperchaos claim is made.

No standardized primitive equivalence is claimed.

No AEAD-equivalence claim is made.

Nonce uniqueness remains required by the parent protocol.

No post-hoc V5 retuning is permitted after DL6 outcomes.

## Recovery provenance

Historical local-only identifier previously recorded:

`8174d7c6dfbcde40256e39771fca94f0e59598a8d`

That identifier is NOT reachable from the public Git remote and is not
represented as recovered.

This file defines a new auditable recovery lineage from the public
baseline.

## Neural execution state at reconstruction

- DL0: NOT EXECUTED
- DL1: NOT EXECUTED
- DL2: NOT EXECUTED
- DL3: NOT EXECUTED
- DL4: NOT EXECUTED
- DL5: NOT EXECUTED
- DL6: NOT EXECUTED

## Freeze rule

After this recovery implementation is committed and pushed to the public
remote, V5-R3 parameters and insertion point must not be altered in
response to DL6 results.

Any later architectural modification requires a new variant identifier
and a new prospective protocol.
