# Final Scientific Audit Rules

Before a submission PDF/DOCX is produced, perform all checks below against repository evidence:

1. Every numeric result in Abstract/Results/Discussion/Conclusion must map to a raw result file and commit/artifact provenance.
2. Preliminary development-only results must be labeled or removed when confirmatory replacements exist.
3. No placeholder such as `[PENDING]`, `TBD`, or `[TO BE]` may remain.
4. Every cited DOI/title/author/year/page range must be verified against a primary publisher, standard, or authoritative bibliographic source.
5. Equations and serialization descriptions must match `V4R3_confirmatory_v1.py`, not an earlier conceptual draft.
6. The manuscript must state that the nonce is public and uniqueness is required.
7. Do not add nonce size, chaotic precision, or public parameters to the secret key-space estimate.
8. Do not use the terms 'hyperchaotic' or 'hyperchaos' for the V5 dynamics unless confirmatory Lyapunov evidence demonstrates the required spectrum.
9. Do not state that p>0.05 proves equivalence.
10. Do not infer security from entropy, correlation, NPCR, UACI, NIST randomness tests, or neural attack failure alone.
11. Preserve negative results, including a possible lack of V5 benefit or a reproducible V4 break.
12. State that standardized AEAD is the production reference and that the custom construction is experimental.
