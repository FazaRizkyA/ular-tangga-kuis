"""Dadu tiga dimensi untuk animasi lempar. Hanya kode gambar; nilai dadu tetap
ditentukan oleh class Dadu (dadu.py).

- DaduRender: memutar gambar hasil render Blender dari model dadu.glb
  (assets/dadu3d). Tampilan utama.
- Dadu3D: kubus yang digambar dengan kode (proyeksi perspektif). Cadangan
  bila file gambar Blender hilang atau rusak, agar game tidak crash."""
import json
import math
import os

import pygame

import kanvas as gfx

from config import KREM, TINTA, MERAH_CAT, resource_path


class DaduRender:
    """Dadu hasil render Blender: 6 lembar sprite, satu per angka akhir.
    Tiap lembar berisi gambar dadu berguling yang berhenti dengan angka itu di atas."""

    def __init__(self, folder=os.path.join("assets", "dadu3d")):
        self.__frame = {}
        self.__cache_skala = {}
        self.siap = False
        try:
            with open(resource_path(os.path.join(folder, "info.json")), encoding="utf-8") as f:
                info = json.load(f)
            jumlah, kolom, ukuran = info["frame"], info["kolom"], info["ukuran"]
            for n in range(1, 7):
                lembar = pygame.image.load(resource_path(os.path.join(folder, f"dadu_{n}.png")))
                if pygame.display.get_surface() is not None:
                    lembar = lembar.convert_alpha()
                # potongan gambar memakai piksel asli lembar (fisik), dibungkus sebagai Kanvas
                self.__frame[n] = [
                    gfx.Kanvas(permukaan=lembar.subsurface(((i % kolom) * ukuran, (i // kolom) * ukuran, ukuran, ukuran)))
                    for i in range(jumlah)
                ]
            self.ukuran = ukuran
            self.siap = True
        except Exception:
            # Gambar Blender tidak ada/rusak: game memakai dadu buatan kode (Dadu3D).
            self.__frame = {}
            self.siap = False

    def gambar(self, surface, pusat, nilai, progres, ukuran=None):
        """progres 0 (baru dilempar) sampai 1 (diam, angka di atas)."""
        daftar = self.__frame[nilai]
        indeks = max(0, min(len(daftar) - 1, round(progres * (len(daftar) - 1))))
        gambar = daftar[indeks]
        # ukuran logis yang diminta; disesuaikan hanya bila berbeda dari piksel gambar
        if ukuran and abs(gambar.get_width() - ukuran) > 0.5:
            kunci = (nilai, indeks, ukuran)
            skala = self.__cache_skala.get(kunci)
            if skala is None:
                skala = gfx.smoothscale(gambar, (ukuran, ukuran))
                self.__cache_skala[kunci] = skala
            gambar = skala
        lebar = gambar.get_width()
        surface.blit(gambar, (pusat[0] - lebar / 2, pusat[1] - lebar / 2))

# Tiap sisi: (normal, nilai mata, sumbu u, sumbu v). Sisi yang berhadapan berjumlah 7.
_SISI = (
    ((0, 0, 1), 1, (1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), 6, (-1, 0, 0), (0, 1, 0)),
    ((1, 0, 0), 3, (0, 0, -1), (0, 1, 0)),
    ((-1, 0, 0), 4, (0, 0, 1), (0, 1, 0)),
    ((0, 1, 0), 2, (1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), 5, (1, 0, 0), (0, 0, 1)),
)

# Rotasi (rx, ry) yang membuat sisi bernilai n menghadap pemain.
SUDUT_AKHIR = {
    1: (0.0, 0.0),
    6: (0.0, math.pi),
    3: (0.0, -math.pi / 2),
    4: (0.0, math.pi / 2),
    2: (math.pi / 2, 0.0),
    5: (-math.pi / 2, 0.0),
}

_TITIK = {
    1: [(0, 0)],
    2: [(-1, -1), (1, 1)],
    3: [(-1, -1), (0, 0), (1, 1)],
    4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
    6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
}

_CAHAYA = (-0.35, 0.75, 0.55)
_JARAK_KAMERA = 4.0
_MIRING_X, _MIRING_Y = 0.42, -0.36  # sudut pandang dari atas-kanan agar terlihat 3 sisi


def _putar(v, rx, ry, rz):
    x, y, z = v
    # Ry
    c, s = math.cos(ry), math.sin(ry)
    x, z = x * c + z * s, -x * s + z * c
    # Rx
    c, s = math.cos(rx), math.sin(rx)
    y, z = y * c - z * s, y * s + z * c
    # Rz
    c, s = math.cos(rz), math.sin(rz)
    x, y = x * c - y * s, x * s + y * c
    # sudut pandang kamera
    c, s = math.cos(_MIRING_X), math.sin(_MIRING_X)
    y, z = y * c - z * s, y * s + z * c
    c, s = math.cos(_MIRING_Y), math.sin(_MIRING_Y)
    x, z = x * c + z * s, -x * s + z * c
    return x, y, z


class Dadu3D:
    """Penggambar dadu 3D. Sudut rx, ry, rz dalam radian."""

    def __init__(self, ukuran=86):
        self.ukuran = ukuran

    def __proyeksi(self, p, pusat):
        x, y, z = p
        skala = self.ukuran * _JARAK_KAMERA / (_JARAK_KAMERA - z)
        return pusat[0] + x * skala, pusat[1] - y * skala

    def gambar(self, surface, pusat, rx, ry, rz):
        sisi_tampak = []
        for normal, nilai, u, v in _SISI:
            n = _putar(normal, rx, ry, rz)
            if n[2] <= 0.02:
                continue
            tengah = [c * 0.5 for c in normal]
            sudut = []
            for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                titik = [tengah[i] + 0.5 * (su * u[i] + sv * v[i]) for i in range(3)]
                sudut.append(_putar(titik, rx, ry, rz))
            kedalaman = sum(p[2] for p in sudut) / 4
            sisi_tampak.append((kedalaman, n, nilai, tengah, u, v, sudut))
        sisi_tampak.sort(key=lambda s: s[0])

        panjang = math.sqrt(sum(c * c for c in _CAHAYA))
        cahaya = [c / panjang for c in _CAHAYA]
        for _, n, nilai, tengah, u, v, sudut in sisi_tampak:
            terang = 0.58 + 0.42 * max(0.0, sum(n[i] * cahaya[i] for i in range(3)))
            warna = tuple(min(255, int(k * terang)) for k in KREM)
            poligon = [self.__proyeksi(p, pusat) for p in sudut]
            gfx.polygon(surface, warna, poligon)
            gfx.polygon(surface, TINTA, poligon, 3)
            warna_titik = MERAH_CAT if nilai == 1 else TINTA
            jari = 0.2 if nilai == 1 else 0.085
            for dx, dy in _TITIK[nilai]:
                pusat_titik = [tengah[i] + 0.27 * (dx * u[i] - dy * v[i]) for i in range(3)]
                lingkar = []
                for k in range(12):
                    a = k / 12 * 2 * math.pi
                    titik = [pusat_titik[i] + jari * (math.cos(a) * u[i] + math.sin(a) * v[i]) for i in range(3)]
                    lingkar.append(self.__proyeksi(_putar(titik, rx, ry, rz), pusat))
                gfx.polygon(surface, warna_titik, lingkar)
