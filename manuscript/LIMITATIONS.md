# Limitations

V4-R3 and V5-R3 are experimental constructions rather than standardized cryptographic primitives. The empirical campaign can falsify specific security hypotheses and expose recoverable structure, but failure of the implemented attacks cannot establish formal confidentiality security. The tested attack families, query budgets, datasets, model capacities, and compute budgets therefore bound every conclusion.

The public nonce is required to be unique; deliberate nonce reuse is evaluated only as a stress diagnostic and does not establish misuse resistance. Authentication tests demonstrate rejection of the tested modifications, not formal equivalence to standardized AEAD security notions.

Image statistics such as entropy, correlation, NPCR, and UACI are secondary diagnostics. They cannot substitute for adversarial evaluation. Neural reconstruction metrics can also reflect natural-image priors, so final interpretation requires positive/negative controls, source-identity-disjoint data, ciphertext-use ablations, unseen-session testing, and multiple seeds.

The nonlinear V5-R3 component is evaluated as an ablation. The investigated nonlinear system is not called hyperchaotic unless its Lyapunov spectrum supports that terminology. Performance measurements are implementation- and platform-dependent and are reported as engineering measurements rather than cryptographic assurance.
