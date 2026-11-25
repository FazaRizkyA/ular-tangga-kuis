"""Class Papan: menyusun petak (8x8 = 64), menghitung posisi layar, dan
menggambar papan sebagai meja stan berbingkai bohlam lengkap dengan tangga
dan ular. Letak tangga dan ular bergantung pada tingkat kesulitan."""
import math

import pygame

import kanvas as gfx

from config import (
    JUMLAH_PETAK, KOLOM, UKURAN_PETAK, PAPAN_X, PAPAN_Y, KESULITAN, KESULITAN_AWAL, LEBAR, TINGGI,
    MERAH_CAT, KAYU, KAYU_GELAP, KREM, BOHLAM_NYALA, OREN_JALUR,
)
from petak import Petak, PetakTangga, PetakUlar, PetakFinish
from tampilan import papan_cat, bohlam, campur, gambar_ular

# Posisi bidak bila beberapa pemain berada di petak yang sama.
_GESER_BIDAK = [(-17, -11), (17, -11), (-17, 19), (17, 19)]


class Papan:
    """Papan 8x8 bernomor zig-zag dari kiri bawah (1) ke kiri atas (64).

    # ENCAPSULATION: daftar petak, tangga, dan ular private; dari luar
    # petak hanya bisa diambil satu per satu lewat get_petak().
    """

    def __init__(self, kesulitan=KESULITAN_AWAL, x=PAPAN_X, y=PAPAN_Y, ukuran_petak=UKURAN_PETAK):
        self.__kesulitan = kesulitan
        self.__tangga = dict(KESULITAN[kesulitan]["tangga"])
        self.__ular = dict(KESULITAN[kesulitan]["ular"])
        self.__x = x
        self.__y = y
        self.__ukuran_petak = ukuran_petak
        self.__petak = []
        self.__cache = None
        self.__cache_skala = None
        self.__cache_area = None
        self.buat_petak()

    @property
    def kesulitan(self):
        return self.__kesulitan

    @property
    def tangga(self):
        return dict(self.__tangga)

    @property
    def ular(self):
        return dict(self.__ular)

    @property
    def rect(self):
        sisi = self.__ukuran_petak * KOLOM
        return pygame.Rect(self.__x, self.__y, sisi, sisi)

    @property
    def ukuran_petak(self):
        return self.__ukuran_petak

    def __pojok(self, nomor):
        baris = (nomor - 1) // KOLOM
        kolom = (nomor - 1) % KOLOM
        if baris % 2 == 1:
            kolom = KOLOM - 1 - kolom
        x = self.__x + kolom * self.__ukuran_petak
        y = self.__y + (KOLOM - 1 - baris) * self.__ukuran_petak
        return x, y

    def buat_petak(self):
        """Membuat objek petak yang sesuai untuk setiap nomor."""
        self.__petak = []
        for n in range(1, JUMLAH_PETAK + 1):
            x, y = self.__pojok(n)
            if n in self.__tangga:
                petak = PetakTangga(n, x, y, self.__ukuran_petak, self.__tangga[n])
            elif n in self.__ular:
                petak = PetakUlar(n, x, y, self.__ukuran_petak, self.__ular[n])
            elif n == JUMLAH_PETAK:
                petak = PetakFinish(n, x, y, self.__ukuran_petak)
            else:
                petak = Petak(n, x, y, self.__ukuran_petak)
            self.__petak.append(petak)

    def get_petak(self, nomor):
        return self.__petak[nomor - 1]

    def koordinat(self, nomor):
        """Titik tengah petak dalam piksel."""
        x, y = self.__pojok(nomor)
        return x + self.__ukuran_petak / 2, y + self.__ukuran_petak / 2

    def posisi_bidak(self, nomor, urutan, jumlah_di_petak):
        """Titik bidak; digeser bila berbagi petak dengan pemain lain."""
        cx, cy = self.koordinat(nomor)
        if jumlah_di_petak <= 1:
            return cx, cy + 6
        dx, dy = _GESER_BIDAK[urutan % 4]
        if nomor == 1:
            dy += 13  # di petak MULAI bidak agak turun agar tulisan MULAI tetap terlihat
        return cx + dx, cy + dy

    # ------------------------------------------------------------ gambar
    def __lapisan_tetap(self, huruf):
        """Bagian papan yang tidak berubah (bingkai, petak, tangga, ular, nomor)
        digambar sekali lalu disimpan, agar tiap frame cukup ditempel."""
        if self.__cache is None or self.__cache_skala != gfx.skala():
            lapis = gfx.Kanvas((LEBAR, TINGGI), pygame.SRCALPHA)
            bingkai = self.rect.inflate(36, 36)
            papan_cat(lapis, bingkai, MERAH_CAT, radius=14)
            for petak in self.__petak:
                petak.gambar(lapis, huruf)  # POLYMORPHISM: tiap jenis petak menggambar dirinya
            for bawah, atas in self.__tangga.items():
                self.__gambar_tangga(lapis, bawah, atas)
            for kepala, ekor in self.__ular.items():
                x1, y1 = self.koordinat(kepala)
                gambar_ular(lapis, (x1, y1 - 4), self.koordinat(ekor), tebal=10)
            for petak in self.__petak:
                petak.gambar_label(lapis, huruf)  # POLYMORPHISM: lapisan nomor & tanda
            self.__cache = lapis
            self.__cache_skala = gfx.skala()
            self.__cache_area = bingkai.inflate(70, 70).clip(pygame.Rect(0, 0, LEBAR, TINGGI))
        return self.__cache, self.__cache_area

    def gambar_tetap(self, surface, huruf):
        """Menempel bagian papan yang tidak berubah (dipakai untuk latar yang disimpan)."""
        lapis, area = self.__lapisan_tetap(huruf)
        surface.blit(lapis, area.topleft, area)

    def gambar(self, surface, huruf, waktu, sorot=None, petak_aktif=None, tetap=True):
        """tetap=False bila bagian diam sudah ada di latar (lebih cepat)."""
        if tetap:
            self.gambar_tetap(surface, huruf)
        self.__gambar_bohlam_bingkai(surface, self.rect.inflate(36, 36), waktu)

        if sorot:
            # Petak di luar jalur diredupkan sebentar agar rute terbaca jelas.
            for petak in self.__petak:
                if petak.nomor not in sorot:
                    redup = gfx.Kanvas(petak.rect.size, pygame.SRCALPHA)
                    redup.fill((18, 30, 60, 55))
                    surface.blit(redup, petak.rect)

        if sorot:
            for nomor, kuat in sorot.items():
                self.__sorot_petak(surface, nomor, kuat)
        if petak_aktif:
            self.__cincin_bohlam(surface, petak_aktif, waktu)

    def __gambar_bohlam_bingkai(self, surface, bingkai, waktu):
        jarak = 36
        titik = []
        for x in range(bingkai.x + 18, bingkai.right - 10, jarak):
            titik.append((x, bingkai.y + 9))
        for y in range(bingkai.y + 18 + jarak // 2, bingkai.bottom - 10, jarak):
            titik.append((bingkai.right - 9, y))
        for x in range(bingkai.right - 18, bingkai.x + 10, -jarak):
            titik.append((x, bingkai.bottom - 9))
        for y in range(bingkai.bottom - 18 - jarak // 2, bingkai.y + 10, -jarak):
            titik.append((bingkai.x + 9, y))
        for i, p in enumerate(titik):
            # Bohlam bingkai: kebanyakan padam, sesekali berkedip pelan.
            # Panas dijatah untuk petak pemain aktif dan jalur bidak.
            n = 0.55 * max(0.0, math.sin(waktu * 1.3 - i * 0.45)) ** 6
            bohlam(surface, p, n, 6)

    def __sorot_petak(self, surface, nomor, kuat):
        """Jalur bidak: garis oranye hangat dan empat bohlam menyala di sudut."""
        rect = self.get_petak(nomor).rect.inflate(-4, -4)
        lapisan = gfx.Kanvas(rect.size, pygame.SRCALPHA)
        lapisan.fill((*BOHLAM_NYALA, int(90 * kuat)))
        surface.blit(lapisan, rect)
        gfx.rect(surface, campur(KREM, OREN_JALUR, 0.4 + 0.6 * kuat), rect, 4, border_radius=4)
        dalam = rect.inflate(-12, -12)
        for p in (dalam.topleft, dalam.topright, dalam.bottomleft, dalam.bottomright):
            bohlam(surface, p, kuat, 5)

    def __cincin_bohlam(self, surface, nomor, waktu):
        """Petak pemain aktif: delapan bohlam menyala penuh mengelilinginya."""
        rect = self.get_petak(nomor).rect.inflate(-8, -8)
        titik = [
            rect.topleft, rect.midtop, rect.topright, rect.midright,
            rect.bottomright, rect.midbottom, rect.bottomleft, rect.midleft,
        ]
        for i, p in enumerate(titik):
            n = 0.85 + 0.15 * math.sin(waktu * 6 + i * 0.8)
            bohlam(surface, p, n, 5)

    def __gambar_tangga(self, surface, bawah, atas):
        x1, y1 = self.koordinat(bawah)
        x2, y2 = self.koordinat(atas)
        dx, dy = x2 - x1, y2 - y1
        panjang = math.hypot(dx, dy)
        ux, uy = dx / panjang, dy / panjang
        px, py = -uy, ux
        lebar = 11
        mulai = (x1 - ux * 12, y1 - uy * 12)
        akhir = (x2 + ux * 12, y2 + uy * 12)
        for s in (-1, 1):
            a = (mulai[0] + px * lebar * s, mulai[1] + py * lebar * s)
            b = (akhir[0] + px * lebar * s, akhir[1] + py * lebar * s)
            gfx.line(surface, KAYU_GELAP, a, b, 9)
        jarak = 18
        t = 8
        while t < panjang + 16:
            cx, cy = mulai[0] + ux * t, mulai[1] + uy * t
            a = (cx - px * lebar, cy - py * lebar)
            b = (cx + px * lebar, cy + py * lebar)
            gfx.line(surface, KAYU_GELAP, a, b, 7)
            gfx.line(surface, KAYU, a, b, 3)
            t += jarak
        for s in (-1, 1):
            a = (mulai[0] + px * lebar * s, mulai[1] + py * lebar * s)
            b = (akhir[0] + px * lebar * s, akhir[1] + py * lebar * s)
            gfx.line(surface, KAYU, a, b, 4)
