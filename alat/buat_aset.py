"""Alat pengembang: membuat ikon aplikasi (icon.png, icon.ico) dan efek suara
(.wav) secara prosedural. Semua aset dibuat sendiri oleh skrip ini, sehingga
bebas lisensi dan 100% offline.

Jalankan dari folder source_code:  python alat/buat_aset.py
"""
import math
import os
import random
import struct
import sys
import wave

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AKAR)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402
from PIL import Image  # noqa: E402

from config import (  # noqa: E402
    TERPAL, TERPAL_GELAP, MERAH_CAT, KREM, KUNING_CAT, KAYU, KAYU_GELAP,
    ULAR_BADAN, ULAR_TUA, ULAR_GARIS, TINTA, BOHLAM_NYALA,
)

RATE = 22050


def buat_ikon():
    s = 512
    ikon = pygame.Surface((s, s), pygame.SRCALPHA)
    pygame.draw.rect(ikon, TERPAL_GELAP, (0, 0, s, s), border_radius=110)
    pygame.draw.rect(ikon, TERPAL, (14, 14, s - 28, s - 28), border_radius=98)
    papan = pygame.Rect(70, 70, 372, 372)
    pygame.draw.rect(ikon, MERAH_CAT, papan.inflate(40, 40), border_radius=40)
    for i in range(3):
        for j in range(3):
            warna = KREM if (i + j) % 2 == 0 else (252, 226, 158)
            pygame.draw.rect(ikon, warna, (papan.x + i * 124, papan.y + j * 124, 124, 124))
    # bohlam di bingkai
    for k in range(10):
        for x, y in ((papan.x - 8 + k * 39, papan.y - 13), (papan.x - 8 + k * 39, papan.bottom + 13)):
            pygame.draw.circle(ikon, BOHLAM_NYALA, (int(x) + 10, int(y)), 7)
    # tangga
    for dx in (-26, 26):
        pygame.draw.line(ikon, KAYU_GELAP, (180 + dx, 410), (300 + dx, 120), 26)
        pygame.draw.line(ikon, KAYU, (180 + dx, 410), (300 + dx, 120), 12)
    for t in range(1, 7):
        y = 410 - t * 41
        x = 180 + (300 - 180) * (t * 41) / 290
        pygame.draw.line(ikon, KAYU_GELAP, (x - 26, y), (x + 26, y), 16)
        pygame.draw.line(ikon, KAYU, (x - 26, y), (x + 26, y), 8)
    # ular
    titik = []
    for i in range(60):
        t = i / 59
        titik.append((380 - 70 * math.sin(t * math.pi * 2.2), 120 + 300 * t, t))
    for x, y, t in titik:
        pygame.draw.circle(ikon, ULAR_TUA, (int(x), int(y)), int(36 - 20 * t))
    for i, (x, y, t) in enumerate(titik):
        pygame.draw.circle(ikon, ULAR_BADAN, (int(x), int(y)), int(28 - 18 * t))
        if i % 8 == 4:
            pygame.draw.circle(ikon, ULAR_GARIS, (int(x), int(y)), int(12 - 7 * t))
    pygame.draw.circle(ikon, KREM, (366, 110), 11)
    pygame.draw.circle(ikon, KREM, (398, 110), 11)
    pygame.draw.circle(ikon, TINTA, (366, 112), 5)
    pygame.draw.circle(ikon, TINTA, (398, 112), 5)

    os.makedirs(os.path.join(AKAR, "assets"), exist_ok=True)
    png = os.path.join(AKAR, "assets", "icon.png")
    pygame.image.save(ikon, png)
    gambar = Image.open(png).convert("RGBA")
    gambar.save(os.path.join(AKAR, "icon.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("ikon dibuat: assets/icon.png, icon.ico")


def _simpan(nama, sampel):
    folder = os.path.join(AKAR, "assets", "sounds")
    os.makedirs(folder, exist_ok=True)
    with wave.open(os.path.join(folder, f"{nama}.wav"), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 30000)) for v in sampel))


def _nada(frek, durasi, volume=0.5, bentuk="sinus"):
    n = int(RATE * durasi)
    hasil = []
    for i in range(n):
        t = i / RATE
        selubung = min(1.0, i / 200) * (1 - i / n) ** 1.5
        if bentuk == "kotak":
            v = 1.0 if math.sin(2 * math.pi * frek * t) > 0 else -1.0
            v *= 0.4
        else:
            v = math.sin(2 * math.pi * frek * t) + 0.3 * math.sin(4 * math.pi * frek * t)
        hasil.append(v * selubung * volume)
    return hasil


def buat_suara():
    random.seed(7)
    # dadu: beberapa ketukan kayu acak
    dadu = []
    for _ in range(7):
        ketuk = [random.uniform(-1, 1) * (1 - i / 500) ** 3 * 0.6 for i in range(500)]
        dadu += ketuk + [0.0] * random.randint(600, 1600)
    _simpan("dadu", dadu)
    _simpan("benar", _nada(660, 0.12) + _nada(880, 0.12) + _nada(1320, 0.22))
    _simpan("salah", _nada(220, 0.18, 0.5, "kotak") + _nada(165, 0.3, 0.5, "kotak"))
    _simpan("langkah", _nada(990, 0.05, 0.35))
    _simpan("naik", sum((_nada(440 * 2 ** (k / 12), 0.06, 0.4) for k in range(0, 13, 2)), []))
    _simpan("turun", sum((_nada(660 * 2 ** (-k / 12), 0.07, 0.4) for k in range(0, 13, 2)), []))
    _simpan("menang", sum((_nada(f, 0.14) for f in (523, 659, 784, 1047, 784, 1047)), []))
    _simpan("klik", _nada(1400, 0.03, 0.25))
    print("suara dibuat: assets/sounds/*.wav")


if __name__ == "__main__":
    pygame.init()
    buat_ikon()
    buat_suara()
