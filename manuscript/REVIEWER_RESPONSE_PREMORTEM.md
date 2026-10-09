# Reviewer-Risk Premortem

## 'This is another custom image cipher evaluated only by entropy/NPCR.'
Response strategy: lead with the cryptanalysis-guided methodology, V0W positive control, frozen query budgets, cross-session transfer, neural controls, and V5 falsifiable ablation. Entropy/NPCR remain secondary diagnostics.

## 'Passing attacks is not a security proof.'
Agree explicitly. The paper reports failure/success of named implemented attacks and never claims IND-CPA proof or standardized-AEAD equivalence.

## 'Why invent a cipher instead of using AES-GCM/ChaCha20-Poly1305/Ascon?'
Position V4-R3 as an experimental image-specific construction used to test whether permutation/substitution/stateful diffusion/nonlinear additions provide measurable adversarial benefit. Include a standardized AEAD only as engineering context and state that production systems should prefer standardized, extensively analyzed AEAD.

## 'The nonlinear component is decorative.'
Treat V5-R3 as a predeclared ablation. If it fails to improve attack resistance, report the negative result. Do not label the investigated dynamics hyperchaotic without the required Lyapunov evidence.

## 'Neural results may only learn image priors.'
Require source-identity-disjoint splits, mean/random-pairing controls, V0W positive control, ciphertext-use ablations, identity-specific gain, five seeds, and unseen-nonce testing.

## 'Nonce reuse is dangerous.'
Agree. State nonce uniqueness as a requirement. The deliberate reuse experiment tests only whether a simple reusable relation appears and does not claim misuse resistance.

## 'Results are not reproducible.'
Provide deterministic public vector, fixed seeds/protocols, raw JSON, SHA-256 manifests, Git commit IDs, workflow artifacts, environment versions, and figure/table generation from archived raw data.
