"""V4-R3 confirmatory reference implementation v1.

Research code for the frozen confirmatory protocol. It is not a replacement
for standardized AEAD and does not imply a formal security proof.

Design goals implemented here:
- RFC 5869 HKDF-HMAC-SHA-256 with domain-separated subkeys
- public 128-bit nonce bound to image metadata/context
- unbiased Fisher-Yates permutation
- session-dependent bijective byte S-box
- independent stateful forward and reverse diffusion
- Encrypt-then-MAC authentication over unambiguous serialized metadata+ciphertext
- deterministic public test vector support

No confirmatory security outcomes are embedded in this source file.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import struct
from typing import Dict, Tuple
import numpy as np

VERSION = b"V4-R3-CONF-v1"
VARIANT = b"V4-R3"
TAG_LEN = 32
NONCE_LEN = 16
MASTER_KEY_LEN = 32


def H(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if not salt:
        salt = bytes(hashlib.sha256().digest_size)
    return H(salt, ikm)


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    if length < 0 or length > 255 * hashlib.sha256().digest_size:
        raise ValueError("invalid HKDF output length")
    out = bytearray()
    t = b""
    counter = 1
    while len(out) < length:
        t = H(prk, t + info + bytes([counter]))
        out.extend(t)
        counter += 1
    return bytes(out[:length])


def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int = 32) -> bytes:
    return hkdf_expand(hkdf_extract(salt, ikm), info, length)


def lp(x: bytes) -> bytes:
    """Length-prefix a byte string with an unsigned 64-bit big-endian length."""
    return struct.pack(">Q", len(x)) + x


def u64(x: int) -> bytes:
    if x < 0:
        raise ValueError("negative integer")
    return struct.pack(">Q", x)


def build_context(rows: int, cols: int, channels: int, block_size: int, payload_len: int) -> bytes:
    fields = [VERSION, VARIANT]
    return (
        b"CTX" + b"".join(lp(x) for x in fields)
        + u64(rows) + u64(cols) + u64(channels) + u64(block_size) + u64(payload_len)
    )


def derive_keys(master: bytes, nonce: bytes, ctx: bytes) -> Dict[str, bytes]:
    if len(master) != MASTER_KEY_LEN:
        raise ValueError("master key must be 32 bytes")
    if len(nonce) != NONCE_LEN:
        raise ValueError("nonce must be 16 bytes")
    # Public nonce is a per-session HKDF salt; metadata is bound through info.
    prk = hkdf_extract(nonce, master)
    labels = {
        "perm": b"K_PERM",
        "sbox": b"K_SBOX",
        "forward": b"K_DIFF_F",
        "backward": b"K_DIFF_B",
        "auth": b"K_AUTH",
    }
    return {name: hkdf_expand(prk, lp(VERSION) + lp(label) + lp(ctx), 32)
            for name, label in labels.items()}


def prf_bytes(key: bytes, domain: bytes):
    ctr = 0
    while True:
        block = H(key, lp(domain) + struct.pack(">Q", ctr))
        ctr += 1
        yield from block


def randbelow(gen, n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    lim = (1 << 64) - ((1 << 64) % n)
    while True:
        x = 0
        for _ in range(8):
            x = (x << 8) | next(gen)
        if x < lim:
            return x % n


def fisher_yates(n: int, key: bytes) -> np.ndarray:
    a = np.arange(n, dtype=np.int64)
    g = prf_bytes(key, b"PERM")
    for i in range(n - 1, 0, -1):
        j = randbelow(g, i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def session_sbox(key: bytes) -> Tuple[np.ndarray, np.ndarray]:
    s = np.arange(256, dtype=np.uint8)
    g = prf_bytes(key, b"SBOX")
    for i in range(255, 0, -1):
        j = randbelow(g, i + 1)
        s[i], s[j] = s[j], s[i]
    inv = np.empty(256, dtype=np.uint8)
    inv[s] = np.arange(256, dtype=np.uint8)
    return s, inv


def _initial_state(key: bytes, direction: bytes, ctx: bytes) -> bytes:
    return H(key, lp(b"STATE-IV") + lp(direction) + lp(ctx))


def diffuse_forward(x: np.ndarray, key: bytes, ctx: bytes) -> np.ndarray:
    out = np.empty_like(x)
    st = _initial_state(key, b"F", ctx)
    for i, xb in enumerate(x):
        idx = struct.pack(">Q", i)
        mask = H(key, lp(b"MASK-F") + idx + st)[0]
        y = int(xb) ^ mask
        out[i] = y
        st = H(key, lp(b"STATE-F") + st + idx + bytes([y]))
    return out


def diffuse_forward_inv(y: np.ndarray, key: bytes, ctx: bytes) -> np.ndarray:
    out = np.empty_like(y)
    st = _initial_state(key, b"F", ctx)
    for i, yb in enumerate(y):
        idx = struct.pack(">Q", i)
        mask = H(key, lp(b"MASK-F") + idx + st)[0]
        out[i] = int(yb) ^ mask
        st = H(key, lp(b"STATE-F") + st + idx + bytes([int(yb)]))
    return out


def diffuse_reverse(x: np.ndarray, key: bytes, ctx: bytes) -> np.ndarray:
    out = np.empty_like(x)
    st = _initial_state(key, b"B", ctx)
    for i in range(len(x) - 1, -1, -1):
        idx = struct.pack(">Q", i)
        mask = H(key, lp(b"MASK-B") + idx + st)[0]
        y = int(x[i]) ^ mask
        out[i] = y
        st = H(key, lp(b"STATE-B") + st + idx + bytes([y]))
    return out


def diffuse_reverse_inv(y: np.ndarray, key: bytes, ctx: bytes) -> np.ndarray:
    out = np.empty_like(y)
    st = _initial_state(key, b"B", ctx)
    for i in range(len(y) - 1, -1, -1):
        idx = struct.pack(">Q", i)
        mask = H(key, lp(b"MASK-B") + idx + st)[0]
        out[i] = int(y[i]) ^ mask
        st = H(key, lp(b"STATE-B") + st + idx + bytes([int(y[i])]))
    return out


def auth_message(nonce: bytes, ctx: bytes, ciphertext: bytes) -> bytes:
    return b"AUTH" + lp(VERSION) + lp(VARIANT) + lp(nonce) + lp(ctx) + lp(ciphertext)


@dataclass(frozen=True)
class Packet:
    nonce: bytes
    rows: int
    cols: int
    channels: int
    block_size: int
    ciphertext: bytes
    tag: bytes

    def context(self) -> bytes:
        return build_context(self.rows, self.cols, self.channels, self.block_size, len(self.ciphertext))


def encrypt_bytes(plaintext: bytes, master: bytes, nonce: bytes, *, rows: int,
                  cols: int, channels: int, block_size: int = 256) -> Packet:
    if rows <= 0 or cols <= 0 or channels <= 0 or block_size <= 0:
        raise ValueError("invalid metadata")
    expected = rows * cols * channels
    if expected != len(plaintext):
        raise ValueError("metadata does not match plaintext length")
    ctx = build_context(rows, cols, channels, block_size, len(plaintext))
    keys = derive_keys(master, nonce, ctx)
    p = np.frombuffer(plaintext, dtype=np.uint8).copy()
    perm = fisher_yates(len(p), keys["perm"])
    sbox, _ = session_sbox(keys["sbox"])
    x = sbox[p[perm]]
    x = diffuse_forward(x, keys["forward"], ctx)
    x = diffuse_reverse(x, keys["backward"], ctx)
    c = x.tobytes()
    tag = H(keys["auth"], auth_message(nonce, ctx, c))
    return Packet(nonce, rows, cols, channels, block_size, c, tag)


def decrypt_bytes(packet: Packet, master: bytes) -> bytes:
    if len(packet.nonce) != NONCE_LEN or len(packet.tag) != TAG_LEN:
        raise ValueError("invalid packet")
    ctx = packet.context()
    if packet.rows * packet.cols * packet.channels != len(packet.ciphertext):
        raise ValueError("metadata does not match ciphertext length")
    keys = derive_keys(master, packet.nonce, ctx)
    expected_tag = H(keys["auth"], auth_message(packet.nonce, ctx, packet.ciphertext))
    if not hmac.compare_digest(expected_tag, packet.tag):
        raise ValueError("authentication failed")
    c = np.frombuffer(packet.ciphertext, dtype=np.uint8).copy()
    perm = fisher_yates(len(c), keys["perm"])
    _, inv = session_sbox(keys["sbox"])
    x = diffuse_reverse_inv(c, keys["backward"], ctx)
    x = diffuse_forward_inv(x, keys["forward"], ctx)
    x = inv[x]
    p = np.empty_like(x)
    p[perm] = x
    return p.tobytes()


def public_test_vector() -> dict:
    """Deterministic public vector; values are generated, not hard-coded claims."""
    master = bytes(range(32))
    nonce = bytes(range(16))
    rows, cols, channels = 4, 4, 3
    plaintext = bytes(range(rows * cols * channels))
    packet = encrypt_bytes(plaintext, master, nonce, rows=rows, cols=cols, channels=channels)
    recovered = decrypt_bytes(packet, master)
    assert recovered == plaintext
    ctx = packet.context()
    keys = derive_keys(master, nonce, ctx)
    perm = fisher_yates(len(plaintext), keys["perm"])
    sbox, _ = session_sbox(keys["sbox"])
    return {
        "version": VERSION.decode(),
        "master_key_hex": master.hex(),
        "nonce_hex": nonce.hex(),
        "shape": [rows, cols, channels],
        "plaintext_sha256": hashlib.sha256(plaintext).hexdigest(),
        "context_sha256": hashlib.sha256(ctx).hexdigest(),
        "perm_first_16": perm[:16].tolist(),
        "sbox_sha256": hashlib.sha256(sbox.tobytes()).hexdigest(),
        "ciphertext_sha256": hashlib.sha256(packet.ciphertext).hexdigest(),
        "tag_hex": packet.tag.hex(),
        "recovered_sha256": hashlib.sha256(recovered).hexdigest(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(public_test_vector(), indent=2))
