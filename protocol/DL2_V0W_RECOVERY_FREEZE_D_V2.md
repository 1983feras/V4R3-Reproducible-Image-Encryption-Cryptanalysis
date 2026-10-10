# DL2 V0W Recovery Freeze D V2

## Status

Prospective pre-execution freeze.

No neural training and no DL0-DL6 experiment had been executed when
this version was created.

Freeze D V1 remains preserved as a non-executed audit artifact.

## Reason for V2

A read-only repository audit found that the frozen protocol specified
SSIM as the primary neural endpoint but did not previously freeze a
specific SSIM implementation.

Before observing any DL2 result, V2 therefore prospectively freezes the
metric implementation.

V2 also improves fault tolerance by permitting resume from a completed
model/seed result. This does not alter scientific settings.

## Primary metric implementation

Windowed RGB SSIM is frozen as:

- window: 11 x 11
- Gaussian sigma: 1.5
- K1: 0.01
- K2: 0.03
- data range: 1.0
- local statistics computed independently per RGB channel
- valid Gaussian windows (no artificial zero padding)
- final per-image SSIM = mean across RGB channels and spatial windows

This exact implementation must be reused for subsequent neural
conditions DL0-DL6.

## Checkpoint rule

Checkpoint selection remains:

- maximize mean validation SSIM
- exact ties retain earliest epoch

Early stopping remains:

- patience = 7
- min_delta = 0.0001

The min_delta controls patience; it does not replace the strict
maximum-SSIM checkpoint rule.

## Resume rule

A completed `result.json` for a model/seed is an immutable resume point.

Incomplete model/seed execution is rerun from its frozen initial seed.
No scientific parameter changes are permitted during resume.

## Scientific settings

All other scientific settings remain those of the canonical frozen
neural configuration:

- DIV2K source split before cropping
- 640 train / 160 validation / 100 blind
- 256 x 256 RGB
- CNN and TinyUNet
- Adam lr=1e-4
- L1 loss
- batch size 4
- maximum 30 epochs
- gradient clip 1.0
- CUDA mixed precision
- seeds 17, 271, 1618, 4099, 12345
- blind evaluation once after validation-selected checkpoint
- no post-hoc tuning

## DL2 validity rule

DL2 remains the mandatory V0W fixed-to-fixed positive control.

If DL2 is not demonstrably learnable, negative V4-R3/V5-R3 neural
results must not be interpreted.

## Execution state

- Neural training: NOT EXECUTED
- DL0: NOT EXECUTED
- DL1: NOT EXECUTED
- DL2: NOT EXECUTED
- DL3: NOT EXECUTED
- DL4: NOT EXECUTED
- DL5: NOT EXECUTED
- DL6: NOT EXECUTED

V2 must be audited and persisted remotely before execution.
