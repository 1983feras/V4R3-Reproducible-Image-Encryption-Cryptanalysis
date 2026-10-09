"""G5 functional session-separation gate for the frozen V4-R3 confirmatory implementation.

This is a correctness/session-separation property check, not a security proof.
It verifies: (1) exact repeatability for identical K, nonce, plaintext and metadata;
(2) changing only the public nonce changes ciphertext and tag; and
(3) the four frozen K/nonce combinations produce distinct authenticated outputs.
"""
from __future__ import annotations

import hashlib
import json

from V4R3_confirmatory_v1 import encrypt_bytes


def derive(label: str, n: int) -> bytes:
    return hashlib.sha256(("G5|" + label).encode()).digest()[:n]


def main() -> None:
    rows, cols, channels = 32, 32, 3
    n = rows * cols * channels
    p = bytes((i * 73 + 19) & 0xFF for i in range(n))
    k1, k2 = derive("K1", 32), derive("K2", 32)
    nu1, nu2 = derive("N1", 16), derive("N2", 16)

    combos = {
        "K1_N1": (k1, nu1),
        "K1_N2": (k1, nu2),
        "K2_N1": (k2, nu1),
        "K2_N2": (k2, nu2),
    }
    packets = {}
    for name, (key, nonce) in combos.items():
        pkt = encrypt_bytes(p, key, nonce, rows=rows, cols=cols, channels=channels)
        packets[name] = {
            "ciphertext_sha256": hashlib.sha256(pkt.ciphertext).hexdigest(),
            "tag_hex": pkt.tag.hex(),
            "pair_sha256": hashlib.sha256(pkt.ciphertext + pkt.tag).hexdigest(),
        }

    repeat = encrypt_bytes(p, k1, nu1, rows=rows, cols=cols, channels=channels)
    deterministic_repeat = (
        repeat.ciphertext.hex() == encrypt_bytes(p, k1, nu1, rows=rows, cols=cols, channels=channels).ciphertext.hex()
        and repeat.tag.hex() == encrypt_bytes(p, k1, nu1, rows=rows, cols=cols, channels=channels).tag.hex()
    )
    nonce_changes_ciphertext = packets["K1_N1"]["ciphertext_sha256"] != packets["K1_N2"]["ciphertext_sha256"]
    nonce_changes_tag = packets["K1_N1"]["tag_hex"] != packets["K1_N2"]["tag_hex"]
    all_pairs_distinct = len({v["pair_sha256"] for v in packets.values()}) == 4
    passed = deterministic_repeat and nonce_changes_ciphertext and nonce_changes_tag and all_pairs_distinct

    out = {
        "gate": "G5_functional_session_separation",
        "version": "v1",
        "shape": [rows, cols, channels],
        "plaintext_sha256": hashlib.sha256(p).hexdigest(),
        "deterministic_repeat_same_K_nonce_P": deterministic_repeat,
        "same_K_new_nonce_changes_ciphertext": nonce_changes_ciphertext,
        "same_K_new_nonce_changes_tag": nonce_changes_tag,
        "all_K_nonce_authenticated_outputs_distinct": all_pairs_distinct,
        "packets": packets,
        "G5_PASS": passed,
        "guardrail": "Functional session separation only; nonce uniqueness remains required and this is not a nonce-misuse-resistance or IND-CPA proof."
    }
    print(json.dumps(out, indent=2))
    if not passed:
        raise SystemExit("G5_FAIL")


if __name__ == "__main__":
    main()
