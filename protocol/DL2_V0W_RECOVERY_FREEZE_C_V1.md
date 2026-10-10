# Recovery Freeze C — DL2 V0W Positive-Control Runner V1

## Status

Prospective reconstruction prepared before any DL2 neural execution.

No neural training and no DL0-DL6 experiment was executed while preparing
this freeze.

## Repository lineage

Recovery Freeze C is based on the merged canonical repository state:

`c1cca50651f3de8eac2fab7bea606794230ce68c`

The Freeze B provenance reconciliation is already present on `main`.

## Canonical frozen inputs

Confirmatory configuration SHA-256:

`638c9f481347a295e424778b61d257fd946e8dd3af976dfbc06f66d4aa6eecb7`

Canonical neural recovery configuration SHA-256:

`1225748360adcb7322fbfaf4db55774c0e93a746db1428b6b376b17141d785e8`

Canonical neural model implementation SHA-256:

`102a7dfb47b10d797e2aa6f7b52a996a45fc2eb3714199bcd6cf2e2c940622da`

Canonical neural specification SHA-256:

`eba9e4010faf88b6bf8f1d04a8c33cdf3ef47aa28a692037d328dcc6c512ad6c`

Canonical neural evidence SHA-256:

`c1622f169799e8ef8665fcf06b543bf1b5778d21beefd8dcdfa45faf8e439bb4`

Freeze B provenance reconciliation JSON SHA-256:

`92df3033dd48cdb32f7c27c4c81cd5124cfcfcb3e94b825892752ab4683945ad`

Freeze B provenance reconciliation Markdown SHA-256:

`e9abc534701ad9c9b53b8df53bb536ce68c67fc304c7072511c8884f69711809`

## V0W positive control

V0W source:

`v0w_positive_control.py`

V0W SHA-256:

`20c9eca3a2bed8653d4fc7b7c57570d4c0205d34da00f133579a5c7c80f3cf6d`

The runner requires the frozen V0W API:

- H
- stream
- randbelow
- permutation
- mask_bytes
- encrypt
- required_queries
- encoded_query
- recover_structure
- recover_plaintext
- self_test

For a 256 x 256 x 3 byte image:

L = 196608 bytes.

The frozen analytical positive-control requirement is:

1 + ceil(log_256(L)) = 4 chosen-plaintext queries.

This establishes V0W as a deliberately weak positive control.

## DL2 validity role

DL2 is a mandatory validity gate for the neural cryptanalysis campaign.

Negative V4-R3 or V5-R3 neural reconstruction results must not be interpreted
if the deliberately weak V0W positive control is not demonstrably learnable.

If DL2 fails, the neural attack pipeline must be treated as invalid for
interpreting negative V4-R3/V5-R3 outcomes.

Any repair after such a failure requires a new prospective version before
inspection of V4-R3/V5-R3 neural outcomes.

## Frozen neural settings

The runner references, rather than redefines, the canonical neural recovery
configuration.

The prospective neural protocol includes:

- DIV2K RGB;
- source-identity split before cropping;
- train IDs 0001-0640;
- validation IDs 0641-0800;
- blind IDs 0801-0900;
- 256 x 256 patches;
- deterministic train crop;
- deterministic center crop for validation/blind;
- horizontal flip probability 0.5;
- no source-identity leakage;
- no dataset mean/std normalization;
- CNN and TinyUNet;
- Adam, learning rate 1e-4;
- L1 loss;
- batch size 4;
- maximum 30 epochs;
- checkpoint by maximum mean validation SSIM;
- earliest epoch on ties;
- early stopping patience 7;
- min_delta 1e-4;
- gradient clipping 1.0;
- mixed precision on CUDA;
- seeds 17, 271, 1618, 4099, 12345;
- no post-hoc tuning.

## Execution boundary

This Recovery Freeze C preparation intentionally keeps DL2 execution locked.

The runner may perform only preflight validation before remote persistence.

DL2 neural execution may be enabled only after:

1. this runner/specification/evidence are reviewed;
2. Recovery Freeze C is committed;
3. the commit is persisted remotely;
4. remote bytes are verified;
5. the frozen DIV2K dataset is restored and provenance-verified;
6. persistent result storage is configured.

## Claim boundary

Success of DL2 validates the attack pipeline against a deliberately weak
positive control. It does not establish insecurity of V4-R3 or V5-R3.

Failure of DL2 invalidates interpretation of negative V4-R3/V5-R3 neural
results until a new prospective attack-pipeline version is frozen.

## Experimental state at preparation

- neural training: NOT EXECUTED
- DL0: NOT EXECUTED
- DL1: NOT EXECUTED
- DL2: NOT EXECUTED
- DL3: NOT EXECUTED
- DL4: NOT EXECUTED
- DL5: NOT EXECUTED
- DL6: NOT EXECUTED
