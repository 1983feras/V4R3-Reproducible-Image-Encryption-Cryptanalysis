# Freeze B Provenance Reconciliation V1

## Purpose

This record documents a byte-level provenance divergence observed during
recovery of the prospective neural implementation freeze.

No neural training and no DL0-DL6 experiment had been executed when the
divergence was discovered or reconciled.

## Canonical repository state

Commit:

`90b87e18b5b6d95ede7aacbc56b688e67a35d26c`

## Historical locally reviewed hashes

Neural configuration:

`caf780f9815d2377d23ca23d13dce83774f45170810826fddfa71ea6ce1a19c9`

Neural implementation:

`b1e0cb8ad0cf7045483e7ab9d68b52404838f10417c20096ff481c3cc707f773`

Specification:

`eba9e4010faf88b6bf8f1d04a8c33cdf3ef47aa28a692037d328dcc6c512ad6c`

Evidence:

`2dd7c6241bb6d433f6e41091f63772c9ab6de199e862b37ac91a68f989ecc315`

## Canonical remote hashes

Neural configuration:

`1225748360adcb7322fbfaf4db55774c0e93a746db1428b6b376b17141d785e8`

Neural implementation:

`102a7dfb47b10d797e2aa6f7b52a996a45fc2eb3714199bcd6cf2e2c940622da`

Specification:

`eba9e4010faf88b6bf8f1d04a8c33cdf3ef47aa28a692037d328dcc6c512ad6c`

Evidence:

`c1622f169799e8ef8665fcf06b543bf1b5778d21beefd8dcdfa45faf8e439bb4`

Confirmatory configuration:

`638c9f481347a295e424778b61d257fd946e8dd3af976dfbc06f66d4aa6eecb7`

## Audit outcome

The canonical remote neural configuration passed the complete scientific
semantic audit.

The canonical remote CNN implementation passed:

- exact frozen channel sequence;
- 3x3 convolution kernels;
- padding 1;
- five hidden ReLU activations;
- Sigmoid output;
- absence of normalization;
- parameter count = 131,907;
- output shape = 1 x 3 x 256 x 256;
- output range in [0,1].

The canonical remote TinyUNet implementation passed:

- encoder channels 32, 64, 128;
- bottleneck 256;
- decoder channels 128, 64, 32;
- MaxPool2d downsampling;
- Sigmoid RGB output;
- absence of normalization;
- parameter count = 2,141,475;
- output shape = 1 x 3 x 256 x 256;
- output range in [0,1].

The historical evidence record correctly preserves the hashes of the
locally reviewed pre-publication artifacts.

Therefore the historical evidence file is intentionally not rewritten.

## Canonical rule

Beginning with Recovery Freeze C, all new recovery artifacts shall reference
the canonical remote hashes associated with commit:

`90b87e18b5b6d95ede7aacbc56b688e67a35d26c`

The historical hashes remain preserved solely as provenance.

## Experimental state

At reconciliation:

- neural training: NOT EXECUTED
- DL0: NOT EXECUTED
- DL1: NOT EXECUTED
- DL2: NOT EXECUTED
- DL3: NOT EXECUTED
- DL4: NOT EXECUTED
- DL5: NOT EXECUTED
- DL6: NOT EXECUTED

This reconciliation does not constitute an experimental result and does not
alter the frozen scientific protocol.
