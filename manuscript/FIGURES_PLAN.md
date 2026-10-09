# Frozen Figure Plan

1. **Figure 1 — V4-R3 architecture.** Master key + public nonce -> HKDF domain-separated session material -> permutation -> bijective substitution -> forward stateful diffusion -> reverse stateful diffusion -> authentication.
2. **Figure 2 — Evidence hierarchy and confirmatory gates.** Correctness/authentication -> V0W positive control -> bounded CPA/session transfer -> differential diagnostics -> neural controls -> V5 ablation -> engineering reference.
3. **Figure 3 — Query-budget recovery.** V4-R3 mean exact-byte recovery versus Q={1,2,4,8,16,32,64}, horizontal random reference 1/256, and V0W positive-control recovery shown separately so its 1.0 scale does not visually flatten V4-R3.
4. **Figure 4 — Key/nonce session-separation matrix.** Same/new key crossed with same/new nonce, with exact-byte recovery and direct functional output-separation status.
5. **Figure 5 — Boundary-directed differential diffusion.** NPCR/UACI or influence profile at frozen boundary positions; label explicitly as diffusion diagnostics, not proof of security.
6. **Figure 6 — Neural evaluation design.** Source-identity split before cropping; DL0/DL1 controls; V0W positive control; V4 fixed/fresh/unseen; V5 ablation; blind test after validation selection.
7. **Figure 7 — Neural leakage results.** Five-seed SSIM distributions with mean-image/random-pairing and ciphertext-use controls. Generate only after G4 passes.
8. **Figure 8 — V4/V5 paired ablation.** Paired seed-wise SSIM differences with uncertainty interval. Generate regardless of whether V5 helps.
9. **Figure 9 — Engineering performance.** Encryption/decryption throughput and ciphertext expansion for V4-R3 and standardized AEAD reference, explicitly labeled engineering context only.

No figure may be populated from preliminary development-only numbers when a confirmatory result is required.
