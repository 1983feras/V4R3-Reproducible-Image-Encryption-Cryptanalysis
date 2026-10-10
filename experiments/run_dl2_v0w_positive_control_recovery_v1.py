#!/usr/bin/env python3
"""
DL2 V0W neural positive-control runner — Recovery V1.

IMPORTANT
---------
This runner was reconstructed prospectively before DL2 execution.

DL2 is a mandatory validity gate:
the deliberately weak V0W construction must be demonstrably learnable
before negative V4-R3/V5-R3 neural reconstruction outcomes can be
interpreted.

This file defines execution mechanics only. Merely importing the file or
calling --preflight-only performs no training.

Frozen neural settings are loaded from:
    configs/neural_recovery_freeze_v1.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import random
from pathlib import Path
from typing import Any, Dict

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]

NEURAL_CONFIG = ROOT / "configs/neural_recovery_freeze_v1.json"
MODEL_FILE = ROOT / "experiments/neural_attack_models_recovery_v1.py"

V0W_FILE = ROOT / "v0w_positive_control.py"

EXPECTED_NEURAL_CONFIG_SHA = \
    "1225748360adcb7322fbfaf4db55774c0e93a746db1428b6b376b17141d785e8"

EXPECTED_MODEL_SHA = \
    "102a7dfb47b10d797e2aa6f7b52a996a45fc2eb3714199bcd6cf2e2c940622da"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_frozen_config() -> Dict[str, Any]:

    actual_cfg = sha256_file(NEURAL_CONFIG)
    actual_model = sha256_file(MODEL_FILE)

    if actual_cfg != EXPECTED_NEURAL_CONFIG_SHA:
        raise RuntimeError(
            "Frozen neural configuration SHA-256 mismatch:\n"
            f"actual={actual_cfg}\n"
            f"expected={EXPECTED_NEURAL_CONFIG_SHA}"
        )

    if actual_model != EXPECTED_MODEL_SHA:
        raise RuntimeError(
            "Frozen neural model SHA-256 mismatch:\n"
            f"actual={actual_model}\n"
            f"expected={EXPECTED_MODEL_SHA}"
        )

    return json.loads(NEURAL_CONFIG.read_text(encoding="utf-8"))


def deterministic_seed(
    protocol: str,
    split: str,
    source_id: str,
    training_seed: int,
    epoch: int,
) -> int:

    msg = (
        f"{protocol}|{split}|{source_id}|"
        f"{training_seed}|{epoch}"
    ).encode("utf-8")

    return int.from_bytes(
        hashlib.sha256(msg).digest()[:8],
        "big",
        signed=False,
    )


def seed_everything(seed: int) -> None:

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def validate_v0w_api(v0w) -> None:

    required = [
        "H",
        "stream",
        "randbelow",
        "permutation",
        "mask_bytes",
        "encrypt",
        "required_queries",
        "encoded_query",
        "recover_structure",
        "recover_plaintext",
        "self_test",
    ]

    missing = [
        name for name in required
        if not callable(getattr(v0w, name, None))
    ]

    if missing:
        raise RuntimeError(
            "V0W API mismatch: " + ", ".join(missing)
        )


def analytical_positive_control_check(v0w) -> Dict[str, Any]:

    L = 256 * 256 * 3

    q = int(v0w.required_queries(L))

    expected_q = 1 + math.ceil(
        math.log(L, 256)
    )

    if q != expected_q or q != 4:
        raise RuntimeError(
            f"Unexpected V0W query count: {q}; "
            f"expected {expected_q}"
        )

    return {
        "length_bytes": L,
        "required_queries": q,
        "expected_queries": expected_q,
        "pass": True,
    }


def preflight() -> Dict[str, Any]:

    cfg = load_frozen_config()

    models = load_module(
        MODEL_FILE,
        "neural_attack_models_recovery_v1",
    )

    v0w = load_module(
        V0W_FILE,
        "v0w_recovery_positive_control",
    )

    validate_v0w_api(v0w)

    analytical = analytical_positive_control_check(v0w)

    cnn = models.build_model("CNN")
    unet = models.build_model("TinyUNet")

    with torch.no_grad():
        x = torch.zeros(
            1, 3, 256, 256,
            dtype=torch.float32,
        )

        y1 = cnn(x)
        y2 = unet(x)

    if tuple(y1.shape) != (1, 3, 256, 256):
        raise RuntimeError(
            f"CNN output shape mismatch: {tuple(y1.shape)}"
        )

    if tuple(y2.shape) != (1, 3, 256, 256):
        raise RuntimeError(
            f"TinyUNet output shape mismatch: {tuple(y2.shape)}"
        )

    return {
        "status": "PASS",
        "training_executed": False,
        "DL2_executed": False,
        "cuda_available": bool(torch.cuda.is_available()),
        "neural_config_sha256":
            sha256_file(NEURAL_CONFIG),
        "model_sha256":
            sha256_file(MODEL_FILE),
        "v0w_sha256":
            sha256_file(V0W_FILE),
        "analytical_positive_control":
            analytical,
        "cnn_output_shape":
            list(y1.shape),
        "tinyunet_output_shape":
            list(y2.shape),
        "frozen_config_loaded":
            True,
    }


def execute_dl2(args):
    raise RuntimeError(
        "DL2 execution is LOCKED in Recovery Freeze C preparation. "
        "Freeze/commit/push/remote-verify this runner and restore the "
        "frozen DIV2K dataset before enabling execution."
    )


def parse_args():

    p = argparse.ArgumentParser(
        description=(
            "DL2 V0W neural positive-control runner — Recovery V1"
        )
    )

    p.add_argument(
        "--preflight-only",
        action="store_true",
        help=(
            "Validate frozen configuration, model definitions, V0W API, "
            "and analytical positive-control query count. "
            "No neural training is performed."
        ),
    )

    p.add_argument(
        "--dataset-root",
        type=str,
        default=None,
        help=(
            "Frozen DIV2K root. Ignored during preflight. Execution "
            "remains locked in this freeze-preparation version."
        ),
    )

    p.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help=(
            "Persistent output directory. Ignored during preflight. "
            "Execution remains locked in this freeze-preparation version."
        ),
    )

    return p.parse_args()


def main():

    args = parse_args()

    if args.preflight_only:
        result = preflight()
        print(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
            )
        )
        print("STATUS: DL2_RECOVERY_PREFLIGHT_PASS")
        return

    execute_dl2(args)


if __name__ == "__main__":
    main()
