"""
V4-R3 Reproducible Reference Implementation and CPA Experiments
Author: Firas Sulaiman Daoud Al-Abd Hafiz
Purpose: Research reproducibility companion for the V4-R3 manuscript.

IMPORTANT:
- This is the Python reference implementation used for the reported research experiments.
- It is research code, not a replacement for standardized AEAD such as AES-GCM or ChaCha20-Poly1305.
- The CPA results demonstrate resistance only to the tested equivalent-keystream strategy; they are not a formal proof of CPA security.
"""

import hashlib
import hmac
import struct
import time
import numpy as np
import pandas as pd

SEED = 20261006

def H(key, msg):
    return hmac.new(key, msg, hashlib.sha256).digest()

def kdf(master, nonce, label):
    """Domain-separated HMAC-SHA-256 session derivation used in the executed reference experiment."""
    return H(master, b"V4-R3|" + label + b"|" + nonce)

def prf_stream(key, label):
    ctr = 0
    while True:
        block = H(key, label + struct.pack(">Q", ctr))
        ctr += 1
        for b in block:
            yield b

def randbelow(gen, n):
    """Unbiased rejection sampling from a 64-bit PRF-derived value."""
    lim = (1 << 64) - ((1 << 64) % n)
    while True:
        x = 0
        for _ in range(8):
            x = (x << 8) | next(gen)
        if x < lim:
            return x % n

def fisher_yates(n, key):
    a = np.arange(n, dtype=np.int64)
    g = prf_stream(key, b"PERM")
    for i in range(n - 1, 0, -1):
        j = randbelow(g, i + 1)
        a[i], a[j] = a[j], a[i]
    return a

def session_sbox(key):
    a = np.arange(256, dtype=np.uint8)
    g = prf_stream(key, b"SBOX")
    for i in range(255, 0, -1):
        j = randbelow(g, i + 1)
        a[i], a[j] = a[j], a[i]
    inv = np.empty(256, dtype=np.uint8)
    inv[a] = np.arange(256, dtype=np.uint8)
    return a, inv

def diffuse_forward(x, key):
    out = np.empty_like(x)
    st = H(key, b"IV")
    for i, xb in enumerate(x):
        m = H(key, b"M" + struct.pack(">I", i) + st)[0]
        y = int(xb) ^ m
        out[i] = y
        st = H(key, b"S" + st + bytes([y]))
    return out

def diffuse_forward_inv(y, key):
    out = np.empty_like(y)
    st = H(key, b"IV")
    for i, yb in enumerate(y):
        m = H(key, b"M" + struct.pack(">I", i) + st)[0]
        out[i] = int(yb) ^ m
        st = H(key, b"S" + st + bytes([int(yb)]))
    return out

def diffuse_reverse(x, key):
    out = x.copy()
    st = H(key, b"IV")
    for i in range(len(x) - 1, -1, -1):
        m = H(key, b"M" + struct.pack(">I", i) + st)[0]
        y = int(x[i]) ^ m
        out[i] = y
        st = H(key, b"S" + st + bytes([y]))
    return out

def diffuse_reverse_inv(y, key):
    out = y.copy()
    st = H(key, b"IV")
    for i in range(len(y) - 1, -1, -1):
        m = H(key, b"M" + struct.pack(">I", i) + st)[0]
        out[i] = int(y[i]) ^ m
        st = H(key, b"S" + st + bytes([int(y[i])]))
    return out

def v4_encrypt(p, master, nonce):
    kp = kdf(master, nonce, b"KP")
    ks = kdf(master, nonce, b"KS")
    kf = kdf(master, nonce, b"KF")
    kb = kdf(master, nonce, b"KB")
    perm = fisher_yates(len(p), kp)
    sbox, _ = session_sbox(ks)
    x = p[perm]
    x = sbox[x]
    x = diffuse_forward(x, kf)
    return diffuse_reverse(x, kb)

def v4_decrypt(c, master, nonce):
    kp = kdf(master, nonce, b"KP")
    ks = kdf(master, nonce, b"KS")
    kf = kdf(master, nonce, b"KF")
    kb = kdf(master, nonce, b"KB")
    perm = fisher_yates(len(c), kp)
    _, invs = session_sbox(ks)
    x = diffuse_reverse_inv(c, kb)
    x = diffuse_forward_inv(x, kf)
    x = invs[x]
    p = np.empty_like(x)
    p[perm] = x
    return p

def npcr(a, b):
    return 100.0 * np.mean(a != b)

def uaci(a, b):
    return 100.0 * np.mean(np.abs(a.astype(np.int16) - b.astype(np.int16)) / 255.0)

def mse(a, b):
    return np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)

def psnr(a, b):
    m = mse(a, b)
    return float("inf") if m == 0 else 10.0 * np.log10((255.0 ** 2) / m)

def weak_encrypt(p, mask):
    """Deliberately weak positive-control cipher."""
    return np.bitwise_xor(p, mask)

def single_cpa_demo(seed=SEED, L=4096):
    rng = np.random.default_rng(seed)
    master = rng.integers(0, 256, 32, dtype=np.uint8).tobytes()
    nonce = rng.integers(0, 256, 16, dtype=np.uint8).tobytes()
    nonce2 = rng.integers(0, 256, 16, dtype=np.uint8).tobytes()

    p0 = np.zeros(L, dtype=np.uint8)
    p1 = rng.integers(0, 256, L, dtype=np.uint8)
    p2 = rng.integers(0, 256, L, dtype=np.uint8)

    # Positive control: zero plaintext reveals reusable XOR mask.
    mask = rng.integers(0, 256, L, dtype=np.uint8)
    c0w = weak_encrypt(p0, mask)
    c1w = weak_encrypt(p1, mask)
    weak_recovered = np.bitwise_xor(c1w, c0w)

    # V4-R3: same zero-plaintext equivalent-XOR strategy.
    c0 = v4_encrypt(p0, master, nonce)
    c1 = v4_encrypt(p1, master, nonce)
    r1 = np.bitwise_xor(c1, c0)

    # Known-pair equivalent-XOR transfer.
    c2 = v4_encrypt(p2, master, nonce)
    equivalent = np.bitwise_xor(c1, p1)
    r2_fixed = np.bitwise_xor(c2, equivalent)

    c2_fresh = v4_encrypt(p2, master, nonce2)
    r2_fresh = np.bitwise_xor(c2_fresh, equivalent)

    assert np.array_equal(v4_decrypt(c1, master, nonce), p1)

    rows = [
        ["Weak XOR positive control", 100*np.mean(weak_recovered == p1), mse(weak_recovered,p1), psnr(weak_recovered,p1)],
        ["V4 zero-plaintext XOR / fixed nonce", 100*np.mean(r1 == p1), mse(r1,p1), psnr(r1,p1)],
        ["V4 known-pair transfer / fixed nonce", 100*np.mean(r2_fixed == p2), mse(r2_fixed,p2), psnr(r2_fixed,p2)],
        ["V4 known-pair transfer / fresh nonce", 100*np.mean(r2_fresh == p2), mse(r2_fresh,p2), psnr(r2_fresh,p2)],
    ]
    return pd.DataFrame(rows, columns=["experiment","exact_recovery_pct","MSE","PSNR_dB"])

def replicated_cpa(n_trials=20, L=4096, base_seed=950000):
    rows = []
    for t in range(n_trials):
        rr = np.random.default_rng(base_seed + t)
        master = rr.integers(0,256,32,dtype=np.uint8).tobytes()
        nonce = rr.integers(0,256,16,dtype=np.uint8).tobytes()
        nonce2 = rr.integers(0,256,16,dtype=np.uint8).tobytes()
        p0 = np.zeros(L,dtype=np.uint8)
        p1 = rr.integers(0,256,L,dtype=np.uint8)
        p2 = rr.integers(0,256,L,dtype=np.uint8)

        c0 = v4_encrypt(p0,master,nonce)
        c1 = v4_encrypt(p1,master,nonce)
        c2 = v4_encrypt(p2,master,nonce)
        c2f = v4_encrypt(p2,master,nonce2)

        tests = [
            ("Zero-plaintext XOR, fixed nonce", np.bitwise_xor(c1,c0), p1),
            ("Known-pair XOR transfer, fixed nonce", np.bitwise_xor(c2,np.bitwise_xor(c1,p1)), p2),
            ("Known-pair XOR transfer, fresh nonce", np.bitwise_xor(c2f,np.bitwise_xor(c1,p1)), p2),
        ]
        for name, recovered, truth in tests:
            rows.append([
                t, name, 100*np.mean(recovered == truth),
                mse(recovered,truth), psnr(recovered,truth)
            ])

    raw = pd.DataFrame(rows, columns=["trial","attack","exact_recovery_pct","MSE","PSNR_dB"])
    summary = raw.groupby("attack").agg(
        trials=("trial","count"),
        recovery_mean=("exact_recovery_pct","mean"),
        recovery_sd=("exact_recovery_pct","std"),
        recovery_min=("exact_recovery_pct","min"),
        recovery_max=("exact_recovery_pct","max"),
        mse_mean=("MSE","mean"),
        psnr_mean=("PSNR_dB","mean"),
    ).reset_index()
    return raw, summary

if __name__ == "__main__":
    one = single_cpa_demo()
    raw, summary = replicated_cpa()

    print("\nSingle CPA demonstration")
    print(one.to_string(index=False))
    print("\n20-seed CPA replication")
    print(summary.to_string(index=False))
    print("\nRandom exact-byte match reference = 100/256 = 0.390625%")

    one.to_csv("V4R3_single_CPA_results.csv", index=False)
    raw.to_csv("V4R3_CPA_20seed_raw.csv", index=False)
    summary.to_csv("V4R3_CPA_20seed_summary.csv", index=False)
