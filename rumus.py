"""Penata rumus: menggambar teks soal yang berisi rumus matematika seperti
tulisan di buku, yaitu pecahan bersusun dengan garis datar, pangkat kecil di
atas, akar dengan garis atas, dan simbol komposisi fungsi.

Tanda khusus di soal.json (teks lain digambar apa adanya):
    \\frac{a}{b}   pecahan a per b
    x^{12}        pangkat; x^2 juga boleh untuk satu angka/huruf
    √{48}         akar; √48 juga boleh untuk satu angka/huruf
    ∘             komposisi fungsi, misalnya (f ∘ g)(x)
"""
import os

import pygame

import kanvas as gfx

from config import resource_path, FOLDER_FONT


class PenataRumus:
    """Mengukur, membungkus, dan menggambar teks berisi rumus."""

    def __init__(self, file_font, ukuran):
        self.__file = file_font
        self.__ukuran = ukuran
        self.__cache_font = {}

    # ------------------------------------------------------------ font
    def __font(self, ukuran):
        ukuran = max(11, int(round(ukuran)))
        font = self.__cache_font.get(ukuran)
        if font is None:
            # dibuat di ukuran fisik layar; file hilang -> font bawaan (di dalam HurufSkala)
            font = gfx.HurufSkala(resource_path(os.path.join(FOLDER_FONT, self.__file)), ukuran)
            self.__cache_font[ukuran] = font
        return font

    # ------------------------------------------------------------ parser
    @staticmethod
    def __kelompok(teks, i):
        """Membaca {...} mulai di teks[i] == '{'; mengembalikan (isi, indeks setelahnya)."""
        tingkat, j = 0, i
        while j < len(teks):
            if teks[j] == "{":
                tingkat += 1
            elif teks[j] == "}":
                tingkat -= 1
                if tingkat == 0:
                    return teks[i + 1:j], j + 1
            j += 1
        return teks[i + 1:], len(teks)

    def __argumen(self, teks, i):
        """Argumen setelah ^ atau √: {kelompok} atau satu deret angka/huruf."""
        if i < len(teks) and teks[i] == "{":
            isi, j = self.__kelompok(teks, i)
            return self.urai(isi), j
        j = i
        if j < len(teks) and teks[j] == "-":
            j += 1
        while j < len(teks) and teks[j].isalnum():
            j += 1
        return [("teks", teks[i:j])], j

    def urai(self, teks):
        """Mengubah teks bertanda menjadi daftar simpul rumus."""
        simpul, buffer, i = [], "", 0

        def lepas():
            nonlocal buffer
            for k, bagian in enumerate(buffer.split(" ")):
                if k:
                    simpul.append(("spasi",))
                if bagian:
                    simpul.append(("teks", bagian))
            buffer = ""

        while i < len(teks):
            c = teks[i]
            if teks.startswith("\\frac", i):
                lepas()
                atas, i = self.__kelompok(teks, i + 5)
                bawah, i = self.__kelompok(teks, i)
                simpul.append(("pecahan", self.urai(atas), self.urai(bawah)))
            elif c == "^":
                lepas()
                isi, i = self.__argumen(teks, i + 1)
                simpul.append(("pangkat", isi))
            elif c == "√":
                lepas()
                isi, i = self.__argumen(teks, i + 1)
                simpul.append(("akar", isi))
            elif c == "∘":
                lepas()
                simpul.append(("komposisi",))
                i += 1
            else:
                buffer += c
                i += 1
        lepas()
        return simpul

    # ------------------------------------------------------------ ukuran
    def ukur(self, simpul, ukuran=None):
        """(lebar, tinggi di atas garis dasar, tinggi di bawah garis dasar)."""
        ukuran = ukuran or self.__ukuran
        lebar, naik, turun = 0, 0, 0
        font = self.__font(ukuran)
        for s in simpul:
            w, a, d = self.__ukur_satu(s, ukuran, font)
            lebar += w
            naik, turun = max(naik, a), max(turun, d)
        if not simpul:
            naik, turun = font.get_ascent(), -font.get_descent()
        return lebar, naik, turun

    def __ukur_satu(self, s, ukuran, font):
        jenis = s[0]
        if jenis == "teks":
            # tinggi tinta huruf (tanpa ruang kosong untuk aksen di atas font)
            return font.size(s[1])[0], font.get_ascent() * 0.82, -font.get_descent()
        if jenis == "spasi":
            return font.size(" ")[0], 0, 0
        if jenis == "pangkat":
            w, a, d = self.ukur(s[1], ukuran * 0.64)
            angkat = ukuran * 0.38
            return w + 1, a + angkat, max(0, d - angkat)
        if jenis == "pecahan":
            kecil = ukuran * 0.76
            w1, a1, d1 = self.ukur(s[1], kecil)
            w2, a2, d2 = self.ukur(s[2], kecil)
            sumbu, celah = ukuran * 0.3, 2
            return max(w1, w2) + 8, sumbu + celah + d1 + a1, a2 + d2 + celah - sumbu
        if jenis == "akar":
            w, a, d = self.ukur(s[1], ukuran)
            return ukuran * 0.62 + w + 3, a + 5, d + 1
        if jenis == "komposisi":
            return ukuran * 0.5, ukuran * 0.5, 0
        return 0, 0, 0

    # ------------------------------------------------------------ gambar
    def __gambar_simpul(self, surface, simpul, x, dasar, ukuran, warna):
        font = self.__font(ukuran)
        for s in simpul:
            w, _, _ = self.__ukur_satu(s, ukuran, font)
            jenis = s[0]
            if jenis == "teks":
                surface.blit(font.render(s[1], True, warna), (x, dasar - font.get_ascent()))
            elif jenis == "pangkat":
                self.__gambar_simpul(surface, s[1], x + 1, dasar - ukuran * 0.38, ukuran * 0.64, warna)
            elif jenis == "pecahan":
                kecil = ukuran * 0.76
                w1, a1, d1 = self.ukur(s[1], kecil)
                w2, a2, d2 = self.ukur(s[2], kecil)
                sumbu, celah = ukuran * 0.3, 2
                garis_y = int(dasar - sumbu)
                tebal = max(2, int(ukuran / 13))
                gfx.line(surface, warna, (x + 2, garis_y), (x + w - 3, garis_y), tebal)
                self.__gambar_simpul(surface, s[1], x + (w - w1) / 2, garis_y - celah - d1, kecil, warna)
                self.__gambar_simpul(surface, s[2], x + (w - w2) / 2, garis_y + celah + a2 + tebal // 2, kecil, warna)
            elif jenis == "akar":
                wi, a, d = self.ukur(s[1], ukuran)
                kiri = ukuran * 0.62
                atas = dasar - a - 3
                tebal = max(2, int(ukuran / 13))
                titik = [
                    (x + 1, dasar - ukuran * 0.28),
                    (x + kiri * 0.3, dasar - ukuran * 0.36),
                    (x + kiri * 0.55, dasar + d * 0.6),
                    (x + kiri - 2, atas),
                    (x + kiri + wi + 2, atas),
                ]
                gfx.lines(surface, warna, False, titik, tebal)
                self.__gambar_simpul(surface, s[1], x + kiri, dasar, ukuran, warna)
            elif jenis == "komposisi":
                gfx.circle(surface, warna, (int(x + w / 2), int(dasar - ukuran * 0.3)), max(3, int(ukuran * 0.14)), 2)
            x += w

    def bungkus(self, teks, lebar):
        """Memecah teks menjadi baris (daftar simpul) yang muat di lebar."""
        simpul = self.urai(teks)
        kata, sekarang = [], []
        for s in simpul:
            if s[0] == "spasi":
                kata.append(sekarang)
                sekarang = []
            else:
                sekarang.append(s)
        kata.append(sekarang)
        baris, isi = [], []
        for k in kata:
            coba = isi + ([("spasi",)] if isi else []) + k
            if isi and self.ukur(coba)[0] > lebar:
                baris.append(isi)
                isi = list(k)
            else:
                isi = coba
        if isi:
            baris.append(isi)
        return baris

    JARAK_BARIS = 4

    def tinggi_baris(self, baris):
        _, naik, turun = self.ukur(baris)
        return naik + turun + self.JARAK_BARIS

    def __tinggi_blok(self, baris):
        """Tinggi blok teks: jarak baris hanya di antara baris, bukan setelah baris terakhir."""
        if not baris:
            return 0
        return sum(self.tinggi_baris(b) for b in baris) - self.JARAK_BARIS

    def tinggi(self, teks, lebar):
        return self.__tinggi_blok(self.bungkus(teks, lebar))

    def gambar(self, surface, teks, x, y, lebar, warna, maks_baris=3, tengah_y=None):
        """Menggambar teks mulai (x, y) atas; bila tengah_y diberi, blok teks
        diletakkan tegak di tengah titik itu. Mengembalikan tinggi yang dipakai."""
        baris = self.bungkus(teks, lebar)[:maks_baris]
        tinggi = self.__tinggi_blok(baris)
        if tengah_y is not None:
            y = tengah_y - tinggi / 2
        for b in baris:
            _, naik, turun = self.ukur(b)
            self.__gambar_simpul(surface, b, x, y + naik, self.__ukuran, warna)
            y += naik + turun + 4
        return tinggi
