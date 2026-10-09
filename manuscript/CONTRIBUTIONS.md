# Contributions

1. **Experimental architecture with explicit claim boundaries.** V4-R3 combines cryptographic session derivation, session-dependent permutation/substitution, stateful bidirectional diffusion, and authentication in a reproducible experimental image-encryption construction. It is explicitly not presented as a replacement for standardized AEAD.

2. **Cryptanalysis-guided evaluation methodology.** Instead of treating entropy/correlation/NPCR/UACI as principal security evidence, the study uses an intentionally vulnerable positive control, predeclared chosen-plaintext query budgets, same/cross-session transfer diagnostics, nonce-separation checks, and controlled neural reconstruction experiments.

3. **Falsifiable nonlinear ablation.** V5-R3 adds nonlinear dynamical material only as an ablation whose security benefit must be demonstrated against the same frozen attackers. A null or negative result is retained rather than tuned away.

4. **Evidence-first reproducibility.** Confirmatory results are tied to source commits, frozen seeds/configurations, deterministic public test vectors, raw JSON, SHA-256 manifests, CI artifacts, and a claims matrix that prevents empirical diagnostics from being promoted into formal-security statements.
