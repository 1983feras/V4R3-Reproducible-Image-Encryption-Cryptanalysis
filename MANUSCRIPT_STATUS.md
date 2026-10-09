# Manuscript status — V4-R3 confirmatory study

Working title: **Cryptanalysis-Guided Evaluation of Adaptive Image Encryption: Stateful Bidirectional Diffusion, Cross-Session Attacks, and Nonlinear Ablation**

The paper is now structured as: Abstract; Introduction; Related Work; Threat Model; V0W/V4-R3/V5-R3 constructions; Frozen Experimental Methodology; Development/Reference Results; Confirmatory Results; Discussion; Limitations; Reproducibility; Conclusion; References.

## Evidence policy

Development/reference observations are not confirmatory evidence. Confirmatory result fields remain pending until G1–G6 produce archived raw outputs. No empirical attack failure is described as a formal security proof. V4-R3 is experimental research software, not a replacement for standardized AEAD.

## Verified primary-source references for the manuscript

1. M. Li, Y. Guo, J. Huang, Y. Li, “Cryptanalysis of a chaotic image encryption scheme based on permutation-diffusion structure,” Signal Processing: Image Communication (2018), DOI 10.1016/j.image.2018.01.002.
2. “Cryptanalysis of a DNA-based image encryption scheme,” Information Sciences 520 (2020) 130–141, DOI 10.1016/j.ins.2020.02.024. Import full author metadata from publisher/BibTeX before submission.
3. “Chosen-plaintext attacks on image ciphers based on nonlinear dynamical systems,” Array 29 (2026) 100642, DOI 10.1016/j.array.2025.100642. Import full author metadata from publisher/BibTeX before submission.
4. “Cryptanalysis of an image encryption algorithm using Latin squares,” Computers & Electrical Engineering 131 (2026) 110950, DOI 10.1016/j.compeleceng.2026.110950. Import full author metadata before submission.
5. “Cryptanalysis of chaos-based image encryption using DL attack,” Procedia Computer Science 270 (2025) 106–115, DOI 10.1016/j.procs.2025.09.129. Import full author metadata before submission.
6. “Cryptanalysis of an image encryption scheme based on two-point diffusion strategy and Henon map,” Journal of Information Security and Applications (2023) 103692, DOI 10.1016/j.jisa.2023.103692. Import full author metadata before submission.
7. “Security analysis of a novel image encryption algorithm based on 3D chaos,” Journal of Information Security and Applications 97 (2026) 104332, DOI 10.1016/j.jisa.2025.104332. Import full author metadata before submission.
8. M. S. Turan, K. McKay, J. Kang, J. Kelsey, D. Chang, NIST SP 800-232, Ascon-Based Lightweight Cryptography Standards for Constrained Devices, Aug. 2025, DOI 10.6028/NIST.SP.800-232.

## Remaining blocking work before submission

1. Execute and archive G1 correctness and G2 authentication tests.
2. Execute V0W analytical positive control; for 256x256x3, expected analytical total is four chosen plaintext queries.
3. Execute V4 structural red team, nonce-reuse and cross-session/unseen-session experiments.
4. Execute neural positive control before interpreting V4 CNN/U-Net failures; then five frozen seeds.
5. Execute paired V4/V5 confirmatory ablation and repeated engineering benchmark.
6. Generate tables/figures from raw machine-readable outputs and replace only the explicitly pending confirmatory fields.
7. Import complete bibliographic metadata from primary publisher records and perform final reference audit.

The manuscript conclusion is deliberately outcome-neutral: a reproducible break of V4-R3 is a valid principal result; V5-R3 is not tuned after outcomes are observed.