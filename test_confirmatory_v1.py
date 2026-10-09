"""G1 correctness and G2 authentication tests for V4R3_confirmatory_v1.py.

These are validity gates, not security results.
"""
import dataclasses
import numpy as np
import pytest

from V4R3_confirmatory_v1 import Packet, encrypt_bytes, decrypt_bytes, public_test_vector

MASTER = bytes(range(32))
NONCE = bytes(range(16))


def patterns(rows, cols, channels):
    n = rows * cols * channels
    yield "zero", bytes(n)
    yield "all255", bytes([255]) * n
    yield "gradient", (np.arange(n, dtype=np.uint64) % 256).astype(np.uint8).tobytes()
    a = np.indices((rows, cols)).sum(axis=0) % 2
    if channels > 1:
        a = np.repeat(a[:, :, None], channels, axis=2)
    yield "checkerboard", (a.reshape(-1) * 255).astype(np.uint8).tobytes()
    impulse = np.zeros(n, dtype=np.uint8)
    impulse[n // 2] = 255
    yield "impulse", impulse.tobytes()
    rng = np.random.default_rng(rows * 1000003 + cols * 101 + channels)
    yield "random", rng.integers(0, 256, n, dtype=np.uint8).tobytes()


@pytest.mark.parametrize("rows,cols,channels", [
    (32,32,1), (32,32,3),
    (64,64,1), (64,64,3),
    (128,128,1), (128,128,3),
    (256,256,1), (256,256,3),
    (257,263,1), (257,263,3),
])
def test_g1_exact_roundtrip(rows, cols, channels):
    for name, p in patterns(rows, cols, channels):
        packet = encrypt_bytes(p, MASTER, NONCE, rows=rows, cols=cols, channels=channels)
        recovered = decrypt_bytes(packet, MASTER)
        assert recovered == p, (rows, cols, channels, name)


def base_packet():
    p = bytes((i * 17 + 3) % 256 for i in range(32 * 32 * 3))
    return encrypt_bytes(p, MASTER, NONCE, rows=32, cols=32, channels=3)


def must_reject(packet, key=MASTER):
    with pytest.raises(ValueError):
        decrypt_bytes(packet, key)


def test_g2_ciphertext_tamper_rejected():
    p = base_packet()
    c = bytearray(p.ciphertext); c[len(c)//2] ^= 1
    must_reject(dataclasses.replace(p, ciphertext=bytes(c)))


def test_g2_tag_tamper_rejected():
    p = base_packet()
    t = bytearray(p.tag); t[0] ^= 1
    must_reject(dataclasses.replace(p, tag=bytes(t)))


def test_g2_nonce_tamper_rejected():
    p = base_packet()
    n = bytearray(p.nonce); n[0] ^= 1
    must_reject(dataclasses.replace(p, nonce=bytes(n)))


def test_g2_metadata_tamper_rejected():
    p = base_packet()
    # Preserve product so rejection is attributable to authenticated metadata,
    # not only to the length sanity check.
    must_reject(dataclasses.replace(p, rows=16, cols=64))


def test_g2_wrong_key_rejected():
    p = base_packet()
    bad = bytearray(MASTER); bad[0] ^= 1
    must_reject(p, bytes(bad))


def test_public_vector_is_deterministic():
    assert public_test_vector() == public_test_vector()
