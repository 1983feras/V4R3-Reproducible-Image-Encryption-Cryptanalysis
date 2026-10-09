# Dataset Freeze V1 — Neural Cryptanalysis Campaign

Status: FROZEN BEFORE G4/V4 NEURAL RESULTS

## Purpose
This document freezes the image-corpus identity and split policy for the confirmatory neural cryptanalysis campaign. No neural result may be interpreted unless the executed corpus is materialized from the stated source and its downloaded files/manifests are hashed and archived.

## D_DL — primary neural corpus
Source: official ETH Zurich DIV2K dataset page: https://data.vision.ee.ethz.ch/cvl/DIV2K/
Dataset paper: E. Agustsson and R. Timofte, “NTIRE 2017 Challenge on Single Image Super-Resolution: Dataset and Study,” CVPR Workshops 2017, DOI 10.1109/CVPRW.2017.150.
Use: original high-resolution RGB PNG images only. Do not use low-resolution derivatives as independent source identities.
Official structure: 800 training HR images (0001–0800) and 100 validation HR images (0801–0900) publicly available from the official page. The official dataset page states academic-research-only availability and that copyright remains with original owners.

## Identity and leakage rule
The source image ID is the unit of independence. All crops/patches/augmentations derived from one source image MUST remain in exactly one partition. Patch-level random splitting is prohibited.

## Frozen split
- Train identities: DIV2K HR IDs 0001–0640 (640 source images).
- Validation identities: DIV2K HR IDs 0641–0800 (160 source images).
- Blind test identities: DIV2K validation HR IDs 0801–0900 (100 source images).

The blind test partition is never used for model selection, early stopping, hyperparameter selection, threshold choice, or checkpoint selection. It is evaluated once per frozen seed/checkpoint after training decisions are complete.

## Patch construction
Patches are generated only after identity partitioning. The exact crop size, stride/random-crop policy, augmentation policy, number of patches per identity, normalization, and deterministic sampling seeds MUST be specified in the executable G4 protocol and recorded in the result manifest before V4 interpretation. No crop from a source identity may cross partitions.

## Cryptographic pairing
Plaintext source identity and session metadata are recorded for every sample. Fixed-session, fresh-session, and unseen-nonce regimes are distinct experiments. Samples from the same source identity cannot cross train/validation/test even when ciphertext sessions differ.

## Positive/negative controls
G4 V0W is the mandatory positive control. DL0/DL1 negative controls and ciphertext-use controls must be executed before interpreting a negative V4-R3 reconstruction result. Failure to learn/recover the deliberately weak V0W control invalidates a negative neural claim about V4-R3 until the pipeline is repaired under a versioned protocol.

## D_crypto
Classical cryptographic diagnostics may use deterministic synthetic patterns and explicitly identified benchmark images. D_crypto is not silently merged with D_DL. Any natural-image corpus used for final classical tables must receive a separate manifest with source identity and SHA-256 hashes before those tables are finalized.

## Required materialization evidence
Before G4 begins, archive:
1. download/source URL and retrieval date;
2. file-level SHA-256 for every HR source image actually used;
3. a canonical manifest mapping source ID to partition;
4. aggregate manifest SHA-256;
5. preprocessing/crop configuration and software versions;
6. explicit statement that split occurred before cropping/augmentation.

If the official source cannot be materialized reproducibly, stop and version this protocol rather than substituting an unrecorded mirror.

## Claim boundary
DIV2K was created for image super-resolution, not cryptanalysis. It is used here as a diverse high-quality RGB natural-image corpus. Results generalize only to the tested corpus/regimes; they are not a proof of cryptographic security.
