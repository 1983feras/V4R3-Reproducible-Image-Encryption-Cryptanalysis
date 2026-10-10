"""
V5-R3 prospective nonlinear ablation — recovery reconstruction V1.

Scientific status
-----------------
This file reconstructs a prospective V5-R3 ablation specification that had
been defined before any DL2-DL6 neural outcome, but whose earlier local-only
Git commit was lost when an ephemeral runtime ended before push.

V5-R3 is NOT claimed to be a standardized cipher, AEAD replacement, or
formally secure construction.

Purpose
-------
Controlled ablation of V4-R3:

    V4-R3:
        permutation
        -> session S-box
        -> forward diffusion
        -> reverse diffusion
        -> authentication

    V5-R3 recovery ablation:
        permutation
        -> session S-box
        -> invertible nonlinear byte-mixing stage
        -> forward diffusion
        -> reverse diffusion
        -> authentication

Only the additional nonlinear stage is the intended architectural change.

The logistic recurrence is used only as an experimental deterministic
session-derived nonlinear sequence generator. Its presence is NOT treated
as a cryptographic security root and no hyperchaos claim is made.
"""

from __future__ import annotations

import hashlib
import hmac
import struct
from typing import Tuple

import numpy as np

import V4R3_confirmatory_v1 as v4


VARIANT = b"V5-R3-RECOVERY-PROSPECTIVE-V1"
NONLINEAR_DOMAIN = b"V5-R3-PROSPECTIVE-V1"
NONLINEAR_LABEL = b"K_NONLINEAR"
BURN_IN = 256


def _lp(x: bytes) -> bytes:
    """Unambiguous length-prefix encoding local to the V5 derivation."""
    return struct.pack(">Q", len(x)) + x


def derive_nonlinear_seed(master: bytes, nonce: bytes, ctx: bytes) -> bytes:
    """
    Domain-separated deterministic seed for the V5 nonlinear ablation.
    """
    if not isinstance(master, (bytes, bytearray)):
        raise TypeError("master must be bytes")
    if not isinstance(nonce, (bytes, bytearray)):
        raise TypeError("nonce must be bytes")
    if not isinstance(ctx, (bytes, bytearray)):
        raise TypeError("ctx must be bytes")

    master = bytes(master)
    nonce = bytes(nonce)
    ctx = bytes(ctx)

    msg = (
        _lp(NONLINEAR_DOMAIN)
        + _lp(NONLINEAR_LABEL)
        + _lp(nonce)
        + _lp(ctx)
    )

    return hmac.new(master, msg, hashlib.sha256).digest()


def logistic_parameters(seed: bytes) -> Tuple[float, float]:
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes")

    a = int.from_bytes(seed[:16], "big")
    b = int.from_bytes(seed[16:], "big")

    z0 = (a + 1) / ((1 << 128) + 1)
    r = 3.99 + 0.01 * (b / float(1 << 128))

    if not (0.0 < z0 < 1.0):
        raise AssertionError("z0 mapping failure")
    if not (3.99 <= r < 4.0):
        raise AssertionError("r mapping failure")

    return z0, r


def nonlinear_keystream(n: int, master: bytes, nonce: bytes, ctx: bytes) -> np.ndarray:
    if n < 0:
        raise ValueError("n must be non-negative")

    seed = derive_nonlinear_seed(master, nonce, ctx)
    z, r = logistic_parameters(seed)

    for _ in range(BURN_IN):
        z = r * z * (1.0 - z)

    q = np.empty(n, dtype=np.uint8)
    scale = float(1 << 32)

    for i in range(n):
        z = r * z * (1.0 - z)
        q[i] = int(z * scale) & 0xFF

    return q


def nonlinear_forward(x: np.ndarray, master: bytes, nonce: bytes, ctx: bytes) -> np.ndarray:
    x = np.asarray(x, dtype=np.uint8)
    q = nonlinear_keystream(len(x), master, nonce, ctx)
    return ((x.astype(np.uint16) + q.astype(np.uint16)) & 0xFF).astype(np.uint8)


def nonlinear_inverse(y: np.ndarray, master: bytes, nonce: bytes, ctx: bytes) -> np.ndarray:
    y = np.asarray(y, dtype=np.uint8)
    q = nonlinear_keystream(len(y), master, nonce, ctx)
    return ((y.astype(np.int16) - q.astype(np.int16)) & 0xFF).astype(np.uint8)


def encrypt_bytes(plaintext: bytes, master: bytes, nonce: bytes, *, rows: int,
                  cols: int, channels: int, block_size: int = 16):
    if len(master) != 32:
        raise ValueError("master key must be 32 bytes")
    if len(nonce) != v4.NONCE_LEN:
        raise ValueError("nonce must be 16 bytes")

    ctx = v4.build_context(rows, cols, channels, block_size, len(plaintext))
    keys = v4.derive_keys(master, nonce, ctx)
    p = np.frombuffer(plaintext, dtype=np.uint8)
    perm = v4.fisher_yates(len(p), keys["perm"])
    sbox, _ = v4.session_sbox(keys["sbox"])

    x = sbox[p[perm]]
    x = nonlinear_forward(x, master, nonce, ctx)
    x = v4.diffuse_forward(x, keys["forward"], ctx)
    x = v4.diffuse_reverse(x, keys["backward"], ctx)

    c = x.tobytes()
    tag = v4.H(keys["auth"], v4.auth_message(nonce, ctx, c))
    return v4.Packet(nonce, rows, cols, channels, block_size, c, tag)


def decrypt_bytes(packet, master: bytes) -> bytes:
    if len(master) != 32:
        raise ValueError("master key must be 32 bytes")
    if len(packet.nonce) != v4.NONCE_LEN:
        raise ValueError("invalid nonce length")
    if len(packet.tag) != v4.TAG_LEN:
        raise ValueError("invalid tag length")

    ctx = v4.build_context(
        packet.rows, packet.cols, packet.channels, packet.block_size,
        len(packet.ciphertext)
    )
    keys = v4.derive_keys(master, packet.nonce, ctx)
    expected_tag = v4.H(keys["auth"], v4.auth_message(packet.nonce, ctx, packet.ciphertext))
    if not hmac.compare_digest(expected_tag, packet.tag):
        raise ValueError("authentication failed")

    c = np.frombuffer(packet.ciphertext, dtype=np.uint8)
    x = v4.diffuse_reverse_inv(c, keys["backward"], ctx)
    x = v4.diffuse_forward_inv(x, keys["forward"], ctx)
    x = nonlinear_inverse(x, master, packet.nonce, ctx)
    _, inv_sbox = v4.session_sbox(keys["sbox"])
    x = inv_sbox[x]
    perm = v4.fisher_yates(len(x), keys["perm"])
    out = np.empty_like(x)
    out[perm] = x
    return out.tobytes()
