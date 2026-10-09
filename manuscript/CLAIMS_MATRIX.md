# Claims Matrix

| Observation | Permitted manuscript claim | Prohibited inference |
|---|---|---|
| Cipher entropy near 8 | ciphertext marginal distribution is near-uniform in tested images | secure cipher / randomness proof |
| NPCR near expected random-change level | strong tested ciphertext diffusion | CPA/IND-CPA security |
| V0W exact recovery | harness detects deliberately reusable structure | all attacks are validated |
| V4 reusable-XOR recovery near 1/256 | this implemented reusable-XOR diagnostic produced no useful recovery | secure against CPA generally |
| Query-budget curve stays near 1/256 through Q=64 | no monotonic recovery gain for the frozen lookup diagnostic | arbitrary-query CPA resistance |
| Same plaintext/key with different nonce gives different authenticated output | functional session separation under tested inputs | nonce-misuse resistance |
| Neural model near controls | no useful reconstruction demonstrated under tested model/data/regime if G4 passes | universal deep-learning resistance |
| V5 attacker metric statistically/practically indistinguishable from V4 | no measurable V5 advantage observed under tested campaign | nonlinear dynamics never help |
| Authentication rejects tested modifications | implemented integrity checks reject tested tampering | formal AEAD equivalence |
| 256-bit master key | secret-key input length is 256 bits | '256-bit security' |

The final paper must use the middle column and avoid the right column.
