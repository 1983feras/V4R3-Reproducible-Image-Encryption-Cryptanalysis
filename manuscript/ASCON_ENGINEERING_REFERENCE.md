# Standardized AEAD Engineering Reference

## Reference
NIST Special Publication 800-232, *Ascon-Based Lightweight Cryptography Standards for Constrained Devices: Authenticated Encryption, Hash, and Extendable Output Functions*, final August 2025, DOI: 10.6028/NIST.SP.800-232.

The standardized algorithm used for engineering context is **Ascon-AEAD128**. NIST specifies it as a nonce-based authenticated-encryption-with-associated-data scheme and states a 128-bit security strength in the single-key setting.

## Frozen manuscript framing
The Ascon-AEAD128 comparison is **engineering context only**. V4-R3/V5-R3 are experimental image-encryption research constructions and are not claimed to be security-equivalent or superior to Ascon-AEAD128 or any other standardized AEAD.

The final comparison may report, in one frozen environment:
- encryption time and throughput;
- decryption time and throughput;
- ciphertext/authentication expansion;
- implementation/runtime environment.

The comparison must not use entropy, NPCR, UACI, correlation, or image appearance to infer superiority over Ascon-AEAD128.

## Nonce wording
Ascon-AEAD128 is nonce based. For V4-R3, the public 128-bit nonce is also required to be unique. The V4-R3 nonce is not secret and is not counted as key-space entropy. Deliberate nonce-reuse experiments are stress diagnostics only and do not establish misuse resistance.

## Citation metadata
Turan, M. S.; McKay, K.; Kang, J.; Kelsey, J.; Chang, D. (2025). *Ascon-Based Lightweight Cryptography Standards for Constrained Devices: Authenticated Encryption, Hash, and Extendable Output Functions*. NIST SP 800-232. https://doi.org/10.6028/NIST.SP.800-232
