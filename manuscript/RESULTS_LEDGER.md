# Confirmatory Results Ledger

This ledger separates completed evidence from pending experiments. No pending cell may be written as a result in the manuscript.

## Completed and evidence-backed

### G1/G2 correctness and authentication
At commit `9cbf1e2d0daed667edbd7de7ad35469d6bb5b3b6`, GitHub Actions run `37964345071` completed successfully. `pytest -q test_confirmatory_v1.py` reported **16 passed in 56.23 s**. The suite covers exact recovery across frozen sizes/patterns and rejection of ciphertext/tag/nonce/metadata tampering and wrong keys.

### G3 positive cryptanalytic control
For V0W at length 196608 bytes, the full positive-control run required four total chosen-plaintext queries and recovered the mask, permutation, and target plaintext at rate 1.0. This validates that the evaluation harness can expose an intentionally reusable permutation-mask construction.

### Session-transfer equivalent-XOR diagnostic
Five seeds `{17,271,1618,4099,12345}`; 32x32x3; random byte-match reference = 0.00390625. Mean exact-byte recovery:
- same key / same nonce: 0.0043619792
- same key / new nonce: 0.0037760417
- new key / same nonce: 0.0048828125
- new key / new nonce: 0.0037760417

Interpretation is limited to the implemented equivalent-XOR diagnostic; it is not an IND-CPA proof.

### Query-budget diagnostic
Frozen budgets `Q={1,2,4,8,16,32,64}`. Mean V4-R3 exact-byte recovery across five seeds:
- Q1: 0.0038411458
- Q2: 0.0038411458
- Q4: 0.00390625
- Q8: 0.0039713542
- Q16: 0.0042968750
- Q32: 0.0042317708
- Q64: 0.0040364583

The random byte reference is 0.00390625. No monotonic increase with query budget was observed for this fixed lookup diagnostic. V0W recovered perfectly at the first sampled budget above its 32x32x3 analytical threshold: the analytical total-query threshold is 3, while the sampled grid jumps from Q=2 to Q=4.

Evidence hashes from run 37964345071:
- `query_budget_diagnostic_v1.json`: `ce29362c4ff4e1962f6579a78f79fc783ac10432674a421ceceb1497ef7f5acf`
- `session_separation_v1.json`: `4fa753c7bcd162117c308edd8e3593415f6885bdc8db697c232db2fc8a5c3037`
- uploaded artifact ZIP SHA-256: `0ba8ae6be624a31a880181441dc41999caf0e281e64a7ffca9cd18a82870e9f8`

## Pending confirmatory evidence
- G5 direct functional session-separation gate: workflow added, result pending.
- Differential/influence diagnostic: workflow added, result pending.
- Deliberate nonce-reuse simple-relation stress: workflow added, result pending.
- G4 neural positive-control learnability: pending.
- Final CNN/Tiny U-Net five-seed campaign: pending.
- V5-R3 paired nonlinear ablation: pending confirmatory implementation/campaign.
- Repeated performance benchmark and standardized AEAD engineering reference: pending.

## Claim discipline
Completed results support only the implemented diagnostics. They do not establish formal security, IND-CPA security, nonce-misuse resistance, or equivalence/superiority to standardized authenticated encryption.
