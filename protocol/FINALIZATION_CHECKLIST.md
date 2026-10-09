# Finalization Checklist

The paper is not submission-ready until every mandatory item below is evidence-backed. This checklist prevents placeholder text or preliminary development numbers from being presented as confirmatory results.

- [x] G1 byte-exact correctness gate.
- [x] G2 authentication/tamper gate.
- [x] G3 vulnerable V0W positive cryptanalytic control.
- [x] Frozen session-transfer equivalent-XOR diagnostic.
- [x] Frozen query-budget diagnostic Q={1,2,4,8,16,32,64}.
- [ ] G5 direct functional session-separation gate completed and archived.
- [ ] Differential/influence campaign completed and archived.
- [ ] Deliberate nonce-reuse diagnostic completed and archived.
- [ ] D_crypto image identities and hashes frozen.
- [ ] D_DL source-image identities/license/split frozen before cropping.
- [ ] G4 neural V0W positive-control learnability passed.
- [ ] DL0/DL1 negative controls completed.
- [ ] V4 CNN/Tiny U-Net five-seed fixed/fresh/unseen-nonce campaign completed.
- [ ] Ciphertext-use ablations completed (correct/zero/random/shuffled/wrong ciphertext).
- [ ] V5-R3 implementation frozen without post-hoc tuning.
- [ ] V4/V5 paired five-seed ablation completed with uncertainty estimates.
- [ ] Repeated encryption/decryption performance benchmark completed on one frozen environment.
- [ ] Standardized AEAD engineering reference completed and described only as engineering context.
- [ ] Exact software/hardware versions, git commits, raw-result hashes, and artifact IDs archived.
- [ ] Figures/tables generated only from archived raw results.
- [ ] Literature metadata/DOIs verified from primary publisher/standards sources.
- [ ] Abstract, Results, Discussion, Limitations, and Conclusion updated from final ledger.
- [ ] No claim of formal proof, IND-CPA proof, nonce-misuse resistance, '256-bit security', or AEAD equivalence.
- [ ] V5 conclusion reflects observed evidence even if no benefit is found.

Stop rule: if a confirmatory experiment reveals a reproducible structural break, report it and analyze it. Do not modify V4-R3 inside the frozen confirmatory campaign to obtain a preferred result; any redesign becomes a separately versioned architecture.
