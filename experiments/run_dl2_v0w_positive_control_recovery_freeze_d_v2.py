#!/usr/bin/env python3
"""
Recovery Freeze D V1
DL2 V0W fixed-to-fixed neural positive-control execution runner.

IMPORTANT
---------
This file was prepared prospectively before any DL2 neural training.

It DOES NOT alter Recovery Freeze C.

Scientific settings are loaded from the frozen canonical neural
configuration and must not be tuned after execution begins.

DL2 validity rule:
V0W must be demonstrably learnable before negative V4-R3/V5-R3
neural reconstruction results may be interpreted.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import random
import time
from pathlib import Path

import numpy as np
from PIL import Image

import torch
from torch.utils.data import Dataset, DataLoader


ROOT = Path(__file__).resolve().parents[1]

CONFIG = ROOT / "configs/neural_recovery_freeze_v1.json"
MODELS = ROOT / "experiments/neural_attack_models_recovery_v1.py"
V0W_FILE = ROOT / "v0w_positive_control.py"

EXPECTED_CONFIG_SHA = "1225748360adcb7322fbfaf4db55774c0e93a746db1428b6b376b17141d785e8"
EXPECTED_MODEL_SHA = "102a7dfb47b10d797e2aa6f7b52a996a45fc2eb3714199bcd6cf2e2c940622da"
EXPECTED_V0W_SHA = "20c9eca3a2bed8653d4fc7b7c57570d4c0205d34da00f133579a5c7c80f3cf6d"

PROTOCOL = "DL2_V0W_RECOVERY_FREEZE_D_V2"
CONDITION = "DL2_V0W_fixed_to_fixed_positive_control"

PATCH = 256

# Fixed V0W key for the complete DL2 condition.
# Domain-separated deterministic derivation; no post-execution choice.
V0W_KEY = hashlib.sha256(
    b"V4R3|DL2|V0W|FIXED-TO-FIXED|RECOVERY-FREEZE-D-V2"
).digest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot import " + str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def verify_frozen_inputs():
    got = {
        "config": sha256_file(CONFIG),
        "model": sha256_file(MODELS),
        "v0w": sha256_file(V0W_FILE),
    }

    expected = {
        "config": EXPECTED_CONFIG_SHA,
        "model": EXPECTED_MODEL_SHA,
        "v0w": EXPECTED_V0W_SHA,
    }

    if got != expected:
        raise RuntimeError(
            "Frozen input identity mismatch:\n" +
            json.dumps({"actual": got, "expected": expected}, indent=2)
        )

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))

    if cfg["conditions"]["DL2"] != "V0W_fixed_to_fixed_positive_control":
        raise RuntimeError("DL2 condition mismatch")

    return cfg, got


def deterministic_seed(split, source_id, training_seed, epoch):
    msg = (
        f"{PROTOCOL}|{split}|{source_id}|"
        f"{training_seed}|{epoch}"
    ).encode("utf-8")

    return int.from_bytes(
        hashlib.sha256(msg).digest()[:8],
        "big",
        signed=False,
    )


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def find_sources(dataset_root):
    root = Path(dataset_root)

    files = {}

    for p in root.rglob("*.png"):
        sid = p.stem[:4]
        if len(sid) == 4 and sid.isdigit() and 1 <= int(sid) <= 900:
            if sid in files:
                raise RuntimeError(f"Duplicate DIV2K source identity: {sid}")
            files[sid] = p

    if len(files) != 900:
        raise RuntimeError(
            f"Expected 900 DIV2K identities; found {len(files)}"
        )

    return files


def split_ids(split):
    if split == "train":
        return [f"{i:04d}" for i in range(1, 641)]
    if split == "validation":
        return [f"{i:04d}" for i in range(641, 801)]
    if split == "blind":
        return [f"{i:04d}" for i in range(801, 901)]
    raise ValueError(split)


def crop_image(img, split, source_id, training_seed, epoch):
    w, h = img.size

    if w < PATCH or h < PATCH:
        raise RuntimeError(
            f"Source {source_id} smaller than {PATCH}x{PATCH}"
        )

    if split == "train":
        s = deterministic_seed(
            split, source_id, training_seed, epoch
        )
        rng = random.Random(s)

        left = rng.randrange(0, w - PATCH + 1)
        top = rng.randrange(0, h - PATCH + 1)

        patch = img.crop(
            (left, top, left + PATCH, top + PATCH)
        )

        # Same deterministic sample RNG controls the frozen p=0.5 flip.
        if rng.random() < 0.5:
            patch = patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return patch

    left = (w - PATCH) // 2
    top = (h - PATCH) // 2

    return img.crop(
        (left, top, left + PATCH, top + PATCH)
    )


def image_to_bytes(img):
    a = np.asarray(img, dtype=np.uint8)

    if a.shape != (PATCH, PATCH, 3):
        raise RuntimeError(f"Unexpected patch shape {a.shape}")

    return np.ascontiguousarray(a).tobytes()


def bytes_to_tensor(b):
    a = np.frombuffer(b, dtype=np.uint8).copy()
    a = a.reshape(PATCH, PATCH, 3)

    return torch.from_numpy(
        a.transpose(2, 0, 1)
    ).float().div_(255.0)


class DL2Dataset(Dataset):
    def __init__(
        self,
        files,
        split,
        training_seed,
        epoch,
        v0w,
    ):
        self.files = files
        self.split = split
        self.ids = split_ids(split)
        self.training_seed = int(training_seed)
        self.epoch = int(epoch)
        self.v0w = v0w

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index):
        sid = self.ids[index]
        path = self.files[sid]

        with Image.open(path) as im:
            im = im.convert("RGB")
            patch = crop_image(
                im,
                self.split,
                sid,
                self.training_seed,
                self.epoch,
            )

        pt = image_to_bytes(patch)

        # DL2 fixed-to-fixed: same deliberately weak construction/key.
        ct = self.v0w.encrypt(pt, V0W_KEY)

        x = bytes_to_tensor(ct)
        y = bytes_to_tensor(pt)

        return x, y, sid


def windowed_ssim_batch(pred, target):
    """
    Prospectively frozen RGB windowed SSIM.

    Parameters
    ----------
    window_size = 11
    gaussian_sigma = 1.5
    K1 = 0.01
    K2 = 0.03
    data_range = 1.0

    Computation
    -----------
    Gaussian local statistics are computed independently for each RGB
    channel using grouped convolution. The SSIM map is then averaged
    over channels and spatial positions to obtain one value per image.

    The same implementation must be used for DL2 and all subsequent
    neural conditions DL0-DL6.
    """
    import torch.nn.functional as F

    pred = pred.float()
    target = target.float()

    if pred.shape != target.shape:
        raise RuntimeError("SSIM shape mismatch")

    if pred.ndim != 4 or pred.shape[1] != 3:
        raise RuntimeError("SSIM expects N x 3 x H x W RGB tensors")

    window_size = 11
    sigma = 1.5
    k1 = 0.01
    k2 = 0.03
    data_range = 1.0

    coords = torch.arange(
        window_size,
        device=pred.device,
        dtype=pred.dtype,
    ) - (window_size - 1) / 2.0

    g = torch.exp(-(coords ** 2) / (2.0 * sigma ** 2))
    g = g / g.sum()

    window = torch.outer(g, g)
    window = window / window.sum()

    window = window.view(
        1, 1, window_size, window_size
    ).repeat(3, 1, 1, 1)

    # Valid local windows avoid introducing artificial zero-padding
    # structure at image boundaries.
    mu_x = F.conv2d(
        pred, window, groups=3
    )
    mu_y = F.conv2d(
        target, window, groups=3
    )

    mu_x2 = mu_x * mu_x
    mu_y2 = mu_y * mu_y
    mu_xy = mu_x * mu_y

    sigma_x2 = (
        F.conv2d(pred * pred, window, groups=3) - mu_x2
    )
    sigma_y2 = (
        F.conv2d(target * target, window, groups=3) - mu_y2
    )
    sigma_xy = (
        F.conv2d(pred * target, window, groups=3) - mu_xy
    )

    c1 = (k1 * data_range) ** 2
    c2 = (k2 * data_range) ** 2

    numerator = (
        (2.0 * mu_xy + c1) *
        (2.0 * sigma_xy + c2)
    )

    denominator = (
        (mu_x2 + mu_y2 + c1) *
        (sigma_x2 + sigma_y2 + c2)
    )

    ssim_map = numerator / denominator.clamp_min(1e-12)

    return ssim_map.mean(dim=(1, 2, 3))

def metrics_batch(pred, target):
    mse = ((pred.float() - target.float()) ** 2).mean(
        dim=(1, 2, 3)
    )

    psnr = torch.where(
        mse > 0,
        -10.0 * torch.log10(mse),
        torch.full_like(mse, float("inf")),
    )

    ssim = windowed_ssim_batch(pred, target)

    return mse, psnr, ssim


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()

    rows = []

    for x, y, sid in loader:
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)

        pred = model(x)

        mse, psnr, ssim = metrics_batch(pred, y)

        for i in range(len(sid)):
            rows.append({
                "source_id": sid[i],
                "MSE": float(mse[i].cpu()),
                "PSNR_dB": float(psnr[i].cpu()),
                "SSIM": float(ssim[i].cpu()),
            })

    return rows


def mean_metric(rows, name):
    return float(np.mean([r[name] for r in rows]))


def build_loader(
    files,
    split,
    seed,
    epoch,
    v0w,
    batch_size,
    shuffle,
):
    ds = DL2Dataset(
        files=files,
        split=split,
        training_seed=seed,
        epoch=epoch,
        v0w=v0w,
    )

    generator = torch.Generator()
    generator.manual_seed(
        deterministic_seed(
            "loader_" + split,
            "ALL",
            seed,
            epoch,
        ) % (2**63 - 1)
    )

    return DataLoader(
        ds,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=2,
        pin_memory=torch.cuda.is_available(),
        generator=generator,
        persistent_workers=False,
    )


def atomic_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    os.replace(tmp, path)


def run_seed(
    seed,
    cfg,
    files,
    v0w,
    models,
    output_dir,
    device,
):
    training = cfg["training"]

    seed_everything(seed)

    model_name_results = {}

    for model_name in ["CNN", "TinyUNet"]:
        print("\n" + "=" * 80)
        print("DL2", model_name, "seed", seed)
        print("=" * 80)

        model_dir = (
            Path(output_dir) /
            f"seed_{seed}" /
            model_name
        )
        model_dir.mkdir(parents=True, exist_ok=True)

        completed_model = model_dir / "result.json"

        # Prospective fault tolerance:
        # completed model/seed results are immutable resume points.
        if completed_model.exists():
            print(
                "RESUME: completed model",
                model_name,
                "seed",
                seed,
            )
            model_name_results[model_name] = json.loads(
                completed_model.read_text(encoding="utf-8")
            )
            continue

        seed_everything(seed)

        model = models.build_model(model_name).to(device)

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=float(training["learning_rate"]),
            betas=tuple(training["betas"]),
            weight_decay=float(training["weight_decay"]),
        )

        criterion = torch.nn.L1Loss()

        use_amp = (
            bool(training["mixed_precision_on_cuda"])
            and device.type == "cuda"
        )

        scaler = torch.amp.GradScaler(
            "cuda",
            enabled=use_amp,
        )

        best_ssim = -float("inf")
        best_epoch = None
        epochs_without_improvement = 0
        history = []

        checkpoint = model_dir / "best.pt"

        for epoch in range(1, int(training["max_epochs"]) + 1):
            model.train()

            train_loader = build_loader(
                files,
                "train",
                seed,
                epoch,
                v0w,
                int(training["batch_size"]),
                True,
            )

            total_loss = 0.0
            count = 0
            start = time.time()

            for x, y, _ in train_loader:
                x = x.to(device, non_blocking=True)
                y = y.to(device, non_blocking=True)

                optimizer.zero_grad(set_to_none=True)

                with torch.autocast(
                    device_type=device.type,
                    dtype=torch.float16,
                    enabled=use_amp,
                ):
                    pred = model(x)
                    loss = criterion(pred, y)

                scaler.scale(loss).backward()

                scaler.unscale_(optimizer)

                torch.nn.utils.clip_grad_norm_(
                    model.parameters(),
                    float(training["gradient_clip_norm"]),
                )

                scaler.step(optimizer)
                scaler.update()

                total_loss += float(loss.detach().cpu()) * x.shape[0]
                count += x.shape[0]

            # Frozen validation center crop. Epoch argument does not alter
            # validation pixels because validation uses deterministic center.
            val_loader = build_loader(
                files,
                "validation",
                seed,
                epoch,
                v0w,
                int(training["batch_size"]),
                False,
            )

            val_rows = evaluate(model, val_loader, device)
            val_ssim = mean_metric(val_rows, "SSIM")

            epoch_record = {
                "epoch": epoch,
                "train_L1": total_loss / count,
                "validation_mean_SSIM": val_ssim,
                "seconds": time.time() - start,
            }

            history.append(epoch_record)

            print(json.dumps(epoch_record))

            # Frozen rule:
            # maximize mean validation SSIM;
            # ties retain earliest epoch.
            if val_ssim > best_ssim:
                delta = val_ssim - best_ssim
                best_ssim = val_ssim
                best_epoch = epoch

                torch.save(
                    {
                        "protocol": PROTOCOL,
                        "condition": CONDITION,
                        "model_name": model_name,
                        "training_seed": seed,
                        "epoch": epoch,
                        "validation_mean_SSIM": val_ssim,
                        "state_dict": model.state_dict(),
                    },
                    checkpoint,
                )

                # Patience reset only when improvement exceeds frozen
                # min_delta. Checkpoint still follows exact max SSIM.
                if (
                    math.isinf(delta)
                    or delta > float(
                        training["early_stopping_min_delta"]
                    )
                ):
                    epochs_without_improvement = 0
                else:
                    epochs_without_improvement += 1
            else:
                epochs_without_improvement += 1

            atomic_json(
                model_dir / "history.json",
                history,
            )

            if epochs_without_improvement >= int(
                training["early_stopping_patience"]
            ):
                print(
                    "Early stopping:",
                    model_name,
                    seed,
                    "epoch",
                    epoch,
                )
                break

        if best_epoch is None:
            raise RuntimeError("No checkpoint selected")

        state = torch.load(
            checkpoint,
            map_location=device,
            weights_only=False,
        )

        model.load_state_dict(state["state_dict"])

        # Blind test exactly once after validation-selected checkpoint.
        blind_loader = build_loader(
            files,
            "blind",
            seed,
            best_epoch,
            v0w,
            int(training["batch_size"]),
            False,
        )

        blind_rows = evaluate(model, blind_loader, device)

        result = {
            "model": model_name,
            "training_seed": seed,
            "best_epoch": best_epoch,
            "best_validation_mean_SSIM": best_ssim,
            "blind": {
                "per_image": blind_rows,
                "mean_SSIM": mean_metric(blind_rows, "SSIM"),
                "mean_MSE": mean_metric(blind_rows, "MSE"),
                "mean_PSNR_dB": mean_metric(
                    blind_rows,
                    "PSNR_dB",
                ),
            },
            "history": history,
            "checkpoint_sha256": sha256_file(checkpoint),
        }

        atomic_json(
            model_dir / "result.json",
            result,
        )

        model_name_results[model_name] = result

        # Copying result/checkpoint into output_dir happens continuously
        # because output_dir itself is required to be persistent.

    return model_name_results


def preflight(dataset_root):
    cfg, identities = verify_frozen_inputs()

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU required for confirmatory DL2 execution"
        )

    files = find_sources(dataset_root)

    models = load_module(MODELS, "freeze_d_models")
    v0w = load_module(V0W_FILE, "freeze_d_v0w")

    if int(v0w.required_queries(PATCH * PATCH * 3)) != 4:
        raise RuntimeError("V0W 4-query validation gate mismatch")

    # Dataset construction smoke test only.
    ds = DL2Dataset(
        files,
        "validation",
        17,
        0,
        v0w,
    )

    x, y, sid = ds[0]

    if tuple(x.shape) != (3, PATCH, PATCH):
        raise RuntimeError("Ciphertext tensor shape mismatch")

    if tuple(y.shape) != (3, PATCH, PATCH):
        raise RuntimeError("Plaintext tensor shape mismatch")

    # Exact DL2 fixed-to-fixed determinism.
    x2, y2, sid2 = ds[0]

    if sid != sid2:
        raise RuntimeError("Source identity instability")

    if not torch.equal(x, x2):
        raise RuntimeError("DL2 ciphertext not deterministic")

    if not torch.equal(y, y2):
        raise RuntimeError("DL2 target not deterministic")

    return {
        "status": "PASS",
        "training_executed": False,
        "DL2_executed": False,
        "cuda_available": True,
        "gpu": torch.cuda.get_device_name(0),
        "source_count": len(files),
        "DL2_condition": cfg["conditions"]["DL2"],
        "v0w_fixed_key_sha256": hashlib.sha256(V0W_KEY).hexdigest(),
        "frozen_inputs": identities,
        "sample_source": sid,
        "sample_ciphertext_shape": list(x.shape),
        "sample_plaintext_shape": list(y.shape),
        "required_queries": int(
            v0w.required_queries(PATCH * PATCH * 3)
        ),
    }


def execute(args):
    cfg, identities = verify_frozen_inputs()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")

    if args.dataset_root is None:
        raise RuntimeError("--dataset-root is required")

    if args.output_dir is None:
        raise RuntimeError(
            "--output-dir is required and must be persistent storage"
      )

    files = find_sources(args.dataset_root)

    models = load_module(MODELS, "freeze_d_models_exec")
    v0w = load_module(V0W_FILE, "freeze_d_v0w_exec")

    device = torch.device("cuda")

    seeds = list(cfg["training"]["training_seeds"])

    campaign = {
        "protocol": PROTOCOL,
        "condition": CONDITION,
        "frozen_inputs": identities,
        "fixed_v0w_key_sha256":
            hashlib.sha256(V0W_KEY).hexdigest(),
        "dataset_root": str(Path(args.dataset_root).resolve()),
        "device": torch.cuda.get_device_name(0),
        "seeds": seeds,
        "models": ["CNN", "TinyUNet"],
        "results": {},
    }

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    atomic_json(out / "campaign_state.json", campaign)

    for seed in seeds:
        seed_key = str(seed)

        # Resume at completed-seed granularity.
        seed_summary = out / f"seed_{seed}" / "seed_complete.json"

        if seed_summary.exists():
            print("RESUME: completed seed", seed)
            campaign["results"][seed_key] = json.loads(
                seed_summary.read_text()
            )
            continue

        result = run_seed(
            seed,
            cfg,
            files,
            v0w,
            models,
            out,
            device,
        )

        atomic_json(seed_summary, result)

        campaign["results"][seed_key] = result
        atomic_json(out / "campaign_state.json", campaign)

    campaign["DL2_executed"] = True
    campaign["training_executed"] = True
    campaign["status"] = "COMPLETE"

    atomic_json(out / "DL2_FINAL_RESULTS.json", campaign)

    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "DL2_executed": True,
                "training_executed": True,
                "seeds_completed": list(campaign["results"].keys()),
                "output_dir": str(out),
            },
            indent=2,
        )
    )

    print("STATUS: DL2_FREEZE_D_EXECUTION_COMPLETE")


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("--preflight-only", action="store_true")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--dataset-root", type=str)
    p.add_argument("--output-dir", type=str)

    return p.parse_args()


def main():
    args = parse_args()

    if args.preflight_only and args.execute:
        raise RuntimeError(
            "--preflight-only and --execute are mutually exclusive"
        )

    if args.preflight_only:
        if args.dataset_root is None:
            raise RuntimeError(
                "--dataset-root required for Freeze D preflight"
            )

        result = preflight(args.dataset_root)

        print(json.dumps(result, indent=2, sort_keys=True))
        print("STATUS: FREEZE_D_PREFLIGHT_PASS")
        return

    if args.execute:
        execute(args)
        return

    raise RuntimeError(
        "Explicit --preflight-only or --execute is required. "
        "No implicit training is permitted."
    )


if __name__ == "__main__":
    main()
