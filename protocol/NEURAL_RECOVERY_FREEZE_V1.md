# Neural Recovery Freeze V1

## Status

Prospective neural implementation reconstruction after loss of an unpushed
local-only commit from an ephemeral runtime.

This reconstruction occurs before execution of DL0-DL6.

No neural outcome was inspected to define these settings.

## Recovery baseline

- Git base commit: `fcbd5cfe72a541c4a260e480f2b337624bdd329a`
- Confirmatory config SHA-256:
  `638c9f481347a295e424778b61d257fd946e8dd3af976dfbc06f66d4aa6eecb7`

Historical local-only identifier not recovered:

`134951fdbdd1c91c0fc637d770fdd6638d2640cd`

## Dataset

DIV2K RGB.

Source identity is split before cropping.

- Train: 0001-0640
- Validation: 0641-0800
- Blind: 0801-0900

No source identity may cross partitions.

## Patches

- 256 x 256
- Train: deterministic random crop
- Validation: deterministic center crop
- Blind: deterministic center crop
- One train patch per source per epoch
- One validation patch per source
- One blind patch per source
- Horizontal flip p=0.5
- No vertical flip
- No rotation
- No color jitter
- No MixUp
- No CutMix

Sampling seed:

`SHA256(protocol|split|source_id|training_seed|epoch)`

## Preprocessing

- uint8 / 255 -> [0,1]
- RGB
- no dataset mean/std normalization
- fitted preprocessing statistics, if any, must use training data only

## CNN

Fully convolutional regression attacker.

Channels:

`3 -> 64 -> 64 -> 64 -> 64 -> 32 -> 3`

All hidden convolutions:
- kernel 3
- padding 1
- ReLU

Output:
- Sigmoid

No normalization.
No skip connections.

## TinyUNet

- input/output channels: 3
- encoder: 32, 64, 128
- bottleneck: 256
- decoder: 128, 64, 32
- two convolutions per stage
- kernel 3
- padding 1
- ReLU
- MaxPool2d(2)
- bilinear upsampling then convolution
- no normalization
- Sigmoid output

## Training

- Adam
- lr = 1e-4
- betas = (0.9, 0.999)
- weight decay = 0
- L1 loss
- batch size = 4
- max epochs = 30
- checkpoint = maximum mean validation SSIM
- ties = earliest epoch
- early stopping patience = 7
- min delta = 1e-4
- gradient clipping = 1.0
- mixed precision on CUDA
- seeds = 17, 271, 1618, 4099, 12345

No post-hoc tuning is allowed.

## Endpoints

Primary:
- SSIM

Secondary:
- MSE
- PSNR_dB

Unit of evaluation:
held-out source identity/image.

Report per-image and per-seed outcomes, mean, sample SD, and 95% uncertainty.

## Conditions

1. DL2 — V0W fixed-to-fixed positive control
2. DL0 — mean-image negative control
3. DL1 — random-pairing negative control
4. DL3 — V4-R3 fixed-to-fixed
5. DL4 — V4-R3 fixed-to-unseen-session
6. DL5 — V4-R3 fresh-train-to-unseen-session PRIMARY
7. ciphertext-use ablations
8. DL6 — V5-R3 fresh-train-to-unseen-session
9. paired V4/V5 analysis

Ciphertext-use ablations:
- correct
- shuffled
- wrong
- random
- zero

## Validity rule

DL2 must be demonstrably learnable before negative V4-R3 or V5-R3 neural
results are interpreted.

If DL2 fails, stop. Do not interpret V4/V5 neural failures. Any repair must
receive a new prospective version before inspecting V4/V5 outcomes.

No V5 retuning is allowed after DL6.

A nonsignificant V4/V5 difference is not evidence of equivalence.
Use bounded wording such as:

`no measurable advantage observed`

unless an equivalence margin was prospectively specified.

## Execution state at reconstruction

- neural training: NOT EXECUTED
- DL0: NOT EXECUTED
- DL1: NOT EXECUTED
- DL2: NOT EXECUTED
- DL3: NOT EXECUTED
- DL4: NOT EXECUTED
- DL5: NOT EXECUTED
- DL6: NOT EXECUTED
