"""
Frozen neural attacker model definitions for V4-R3 neural cryptanalysis.

Recovery reconstruction V1.

No training is performed by importing this module.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        channels = [3, 64, 64, 64, 64, 32, 3]

        layers = []

        for i in range(len(channels) - 2):
            layers.append(
                nn.Conv2d(
                    channels[i],
                    channels[i + 1],
                    kernel_size=3,
                    padding=1,
                )
            )
            layers.append(nn.ReLU(inplace=False))

        layers.append(
            nn.Conv2d(
                channels[-2],
                channels[-1],
                kernel_size=3,
                padding=1,
            )
        )

        self.net = nn.Sequential(*layers)
        self.out = nn.Sigmoid()

    def forward(self, x):
        return self.out(self.net(x))


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()

        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=False),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=False),
        )

    def forward(self, x):
        return self.block(x)


class TinyUNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.enc1 = DoubleConv(3, 32)
        self.enc2 = DoubleConv(32, 64)
        self.enc3 = DoubleConv(64, 128)

        self.pool = nn.MaxPool2d(2)

        self.bottleneck = DoubleConv(128, 256)

        self.dec3_reduce = nn.Conv2d(256, 128, 3, padding=1)
        self.dec3 = DoubleConv(128 + 128, 128)

        self.dec2_reduce = nn.Conv2d(128, 64, 3, padding=1)
        self.dec2 = DoubleConv(64 + 64, 64)

        self.dec1_reduce = nn.Conv2d(64, 32, 3, padding=1)
        self.dec1 = DoubleConv(32 + 32, 32)

        self.final = nn.Conv2d(32, 3, 3, padding=1)
        self.out = nn.Sigmoid()

    def _up(self, x):
        return F.interpolate(
            x,
            scale_factor=2,
            mode="bilinear",
            align_corners=False,
        )

    def forward(self, x):

        e1 = self.enc1(x)

        e2 = self.enc2(
            self.pool(e1)
        )

        e3 = self.enc3(
            self.pool(e2)
        )

        b = self.bottleneck(
            self.pool(e3)
        )

        d3 = self._up(b)
        d3 = self.dec3_reduce(d3)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)

        d2 = self._up(d3)
        d2 = self.dec2_reduce(d2)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)

        d1 = self._up(d2)
        d1 = self.dec1_reduce(d1)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)

        return self.out(
            self.final(d1)
        )


def build_model(name: str):

    if name == "CNN":
        return CNN()

    if name == "TinyUNet":
        return TinyUNet()

    raise ValueError(
        f"Unknown frozen model: {name}"
    )
