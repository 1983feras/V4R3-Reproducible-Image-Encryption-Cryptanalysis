"""V0W deliberately weak positive control for CPA validation.

V0W: C[i] = P[perm[i]] XOR mask[i].
A zero query reveals mask. Base-256 encoded-index queries reveal the
source index at every ciphertext position. This file exists to validate
that the chosen-plaintext attack pipeline can recover a construction
with a known analytical break before attack failures on V4-R3 are interpreted.
"""
from __future__ import annotations
import math
import hashlib
import hmac
import struct
import numpy as np


def H(k: bytes, m: bytes) -> bytes:
    return hmac.new(k, m, hashlib.sha256).digest()


def stream(k: bytes, label: bytes):
    ctr = 0
    while True:
        b = H(k, label + struct.pack(">Q", ctr)); ctr += 1
        yield from b


def randbelow(g, n: int) -> int:
    lim = (1 << 64) - ((1 << 64) % n)
    while True:
        x = 0
        for _ in range(8): x = (x << 8) | next(g)
        if x < lim: return x % n


def permutation(n: int, key: bytes) -> np.ndarray:
    p = np.arange(n, dtype=np.int64)
    g = stream(key, b"V0W-PERM")
    for i in range(n - 1, 0, -1):
        j = randbelow(g, i + 1); p[i], p[j] = p[j], p[i]
    return p


def mask_bytes(n: int, key: bytes) -> np.ndarray:
    g = stream(key, b"V0W-MASK")
    return np.fromiter((next(g) for _ in range(n)), dtype=np.uint8, count=n)


def encrypt(pt: bytes, key: bytes) -> bytes:
    x = np.frombuffer(pt, dtype=np.uint8)
    p = permutation(len(x), key)
    z = mask_bytes(len(x), key)
    return np.bitwise_xor(x[p], z).tobytes()


def required_queries(n: int) -> int:
    if n <= 0: raise ValueError("n must be positive")
    digits = 0; capacity = 1
    while capacity < n:
        capacity *= 256; digits += 1
    return 1 + digits


def encoded_query(n: int, digit: int) -> bytes:
    idx = np.arange(n, dtype=np.uint64)
    return ((idx // (256 ** digit)) % 256).astype(np.uint8).tobytes()


def recover_structure(n: int, oracle) -> tuple[np.ndarray, np.ndarray]:
    q = required_queries(n)
    digits = q - 1
    mask = np.frombuffer(oracle(bytes(n)), dtype=np.uint8).copy()
    recovered = np.zeros(n, dtype=np.uint64)
    for d in range(digits):
        c = np.frombuffer(oracle(encoded_query(n, d)), dtype=np.uint8)
        observed = np.bitwise_xor(c, mask).astype(np.uint64)
        recovered += observed * (256 ** d)
    return recovered.astype(np.int64), mask


def recover_plaintext(ciphertext: bytes, recovered_perm: np.ndarray, mask: np.ndarray) -> bytes:
    c = np.frombuffer(ciphertext, dtype=np.uint8)
    permuted_plain = np.bitwise_xor(c, mask)
    out = np.empty_like(permuted_plain)
    out[recovered_perm] = permuted_plain
    return out.tobytes()


def self_test(n: int = 256 * 256 * 3) -> dict:
    key = hashlib.sha256(b"V0W-public-positive-control-key").digest()
    oracle = lambda p: encrypt(p, key)
    recovered_perm, recovered_mask = recover_structure(n, oracle)
    true_perm = permutation(n, key)
    true_mask = mask_bytes(n, key)
    rng = np.random.default_rng(2026)
    target = rng.integers(0, 256, n, dtype=np.uint8).tobytes()
    target_c = oracle(target)
    recovered = recover_plaintext(target_c, recovered_perm, recovered_mask)
    return {
        "length": n,
        "analytical_queries": required_queries(n),
        "permutation_recovery_rate": float(np.mean(recovered_perm == true_perm)),
        "mask_recovery_rate": float(np.mean(recovered_mask == true_mask)),
        "plaintext_byte_recovery_rate": float(np.mean(np.frombuffer(recovered,dtype=np.uint8) == np.frombuffer(target,dtype=np.uint8))),
        "exact_plaintext_recovery": recovered == target,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(self_test(), indent=2))
