# Final Tables Template

## Table I. Architecture and threat-model summary
| Item | V4-R3 |
|---|---|
| Master secret | 256-bit key |
| Public session input | 128-bit nonce; uniqueness required |
| Session derivation | Domain-separated HKDF-HMAC-SHA-256 |
| Spatial stage | Rejection-sampled Fisher-Yates permutation |
| Byte substitution | Session-dependent bijective 8-bit S-box |
| Diffusion | Stateful forward + reverse bytewise passes |
| Integrity | HMAC-based authentication; verify before release |
| Claim boundary | Experimental construction; not standardized AEAD |

## Table II. Confirmatory gates
| Gate | Evidence | Status |
|---|---|---|
| G1 correctness | 16-test suite | PASS |
| G2 authentication/tamper | same suite | PASS |
| G3 V0W positive control | exact recovery | PASS |
| G4 neural positive control | pending | PENDING |
| G5 functional session separation | workflow executing/pending evidence | PENDING |
| G6 provenance | hashes/artifacts available for completed CI; final campaign manifest pending | PARTIAL |

## Table III. Session-transfer diagnostic
| Condition | Mean byte recovery | Random reference |
|---|---:|---:|
| same K / same nonce | 0.00436198 | 0.00390625 |
| same K / new nonce | 0.00377604 | 0.00390625 |
| new K / same nonce | 0.00488281 | 0.00390625 |
| new K / new nonce | 0.00377604 | 0.00390625 |

## Table IV. Query-budget diagnostic
| Q | V4-R3 mean byte recovery |
|---:|---:|
| 1 | 0.00384115 |
| 2 | 0.00384115 |
| 4 | 0.00390625 |
| 8 | 0.00397135 |
| 16 | 0.00429688 |
| 32 | 0.00423177 |
| 64 | 0.00403646 |

Random byte-match reference: 0.00390625.

## Table V. Differential/influence results
PENDING CONFIRMATORY EVIDENCE.

## Table VI. Neural controls and V4-R3 reconstruction
PENDING G4 AND FIVE-SEED CAMPAIGN.

## Table VII. V4-R3 vs V5-R3 paired ablation
PENDING CONFIRMATORY V5 CAMPAIGN.

## Table VIII. Performance and standardized AEAD engineering reference
PENDING REPEATED BENCHMARK.
