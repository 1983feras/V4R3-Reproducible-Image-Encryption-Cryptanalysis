# Editor Cover Note — Draft (finalize only after all confirmatory experiments)

Dear Editor,

Please consider our manuscript, **"Cryptanalysis-Guided Evaluation of Adaptive Image Encryption: Stateful Bidirectional Diffusion, Cross-Session Attacks, and Nonlinear Ablation,"** for publication.

The manuscript addresses a methodological weakness common in experimental image-encryption research: strong ciphertext statistics are often treated as if they were direct evidence of adversarial security. We instead use an evidence hierarchy centered on correctness and authentication gates, an intentionally vulnerable positive cryptanalytic control, predeclared chosen-plaintext query budgets, session-transfer evaluation, controlled neural reconstruction, and a falsifiable nonlinear ablation. The experimental V4-R3 construction is not presented as a replacement for standardized authenticated encryption; a standardized AEAD is included only for engineering context.

A central feature of the work is that the nonlinear V5-R3 extension is evaluated as a genuine ablation rather than assumed to improve security. The manuscript retains null or negative ablation outcomes and explicitly distinguishes empirical attack results from formal security proofs.

The accompanying repository provides versioned source code, frozen protocols, deterministic public test vectors, raw results, SHA-256 evidence manifests, and reproducibility metadata.

[FINAL CONFIRMATORY FINDINGS TO BE INSERTED ONLY AFTER CAMPAIGN COMPLETION.]

Sincerely,
Firas Sulaiman
