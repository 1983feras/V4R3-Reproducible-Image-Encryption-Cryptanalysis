# Statistical Analysis Plan

## Units and reporting
- Never treat pixels/bytes as independent inferential replicates.
- For cryptanalytic seed-level experiments, the frozen seed is the replicate unless a higher-level source-image unit is explicitly defined.
- For neural image reconstruction, source image/evaluation identity is the primary evaluation unit; crops from one source must not be split across train and test.
- Report raw per-seed/per-image values, mean, standard deviation, and 95% uncertainty intervals where meaningful.

## V4 query/session diagnostics
Primary interpretation is descriptive relative to the predeclared random exact-byte reference `1/256`. Do not convert proximity to this reference into a formal cryptographic-security claim.

## Neural campaign
Primary endpoint: SSIM. Secondary: MSE and PSNR. Define:
`LG = SSIM_attack - SSIM_negative_control`.
Ciphertext-use diagnostic:
`CG = SSIM(correct ciphertext -> P) - SSIM(shuffled ciphertext -> P)`.
Identity-specific diagnostic:
`IG = SSIM(P_hat, P_true) - SSIM(P_hat, P_wrong)`.
Interpret V4 neural failure only if G4 demonstrates that the same pipeline learns the V0W positive control.

## V4/V5 paired ablation
For each frozen seed/evaluation unit define `d = SSIM_V4 - SSIM_V5`; positive values mean lower attacker SSIM for V5 and therefore greater observed resistance under that attack. Report paired raw differences, mean/SD, bootstrap 95% CI, and a paired test/effect size where assumptions and sample size permit. A non-significant p-value is not evidence of equivalence. Unless a practical equivalence margin is justified before results, use the wording 'no measurable advantage observed' rather than 'equivalent'.

## Multiple endpoints
SSIM is primary for neural reconstruction. MSE/PSNR are secondary and supportive; do not cherry-pick the endpoint that favors a desired conclusion.

## Performance
After warm-up, measure encryption and decryption separately over repeated runs in one frozen hardware/software environment. Preserve raw timings. Report median, mean, SD, 95% CI, and throughput (MB/s). Engineering comparisons to standardized AEAD are not security comparisons.

## Missing/failed runs
Do not silently discard failed seeds. Record failure reason. Engineering failures may be repaired without changing the frozen scientific protocol; methodological changes require a new version and explicit disclosure.
