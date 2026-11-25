"""Class Petak dan turunannya: PetakTangga, PetakUlar, PetakFinish."""
import pygame

import kanvas as gfx

from config import (
    BONUS_TANGGA, KOLOM, KREM, KUNING_PUCAT, TINTA, TINTA_LEMBUT, HIJAU_CAT, ULAR_BADAN,
    MERAH_CAT, KREM_GELAP,
)
from tampilan import tulis, gelap, segitiga, campur


class Petak:
    """Petak biasa di papan (induk semua petak).

    # ENCAPSULATION: atribut protected (_nomor, _x, _y) dipakai bersama
    # oleh subclass tetapi tidak diubah dari luar class.
    """

    def __init__(self, nomor, x, y, ukuran):
        self._nomor = nomor
        self._x = x
        self._y = y
        self._ukuran = ukuran

    @property
    def nomor(self):
        return self._nomor

    @property
    def rect(self):
        return pygame.Rect(self._x, self._y, self._ukuran, self._ukuran)

    def efek(self, pemain):
        """Efek saat diinjak. Petak biasa tidak punya efek, jadi kosong."""
        return ""

    def _warna_dasar(self):
        baris = (self._nomor - 1) // KOLOM
        kolom = (self._nomor - 1) % KOLOM
        return KREM if (baris + kolom) % 2 == 0 else KUNING_PUCAT

    def gambar(self, surface, huruf):
        """Lapisan bawah: cat dasar petak."""
        rect = self.rect
        warna = self._warna_dasar()
        gfx.rect(surface, warna, rect)
        gfx.rect(surface, gelap(warna, 0.18), rect, 1)

    def gambar_label(self, surface, huruf):
        """Lapisan atas (digambar setelah tangga & ular): nomor petak
        dengan alas warna petak agar selalu terbaca."""
        rect = self.rect
        # petak 1 diberi tulisan MULAI di tempat nomornya agar tidak tertutup bidak
        tulisan = "MULAI" if self._nomor == 1 else str(self._nomor)
        teks = huruf.label.render(tulisan, True, TINTA)
        alas = teks.get_rect(topleft=(rect.x + 8, rect.y + 6)).inflate(8, 2)
        gfx.rect(surface, self._warna_dasar(), alas, border_radius=4)
        surface.blit(teks, (rect.x + 8, rect.y + 6))

    def _gambar_tanda(self, surface, huruf, warna, teks, ke_atas, di_atas):
        """Tanda kecil: arah panah + petak tujuan, di pojok kanan."""
        rect = self.rect
        y = rect.y + 4 if di_atas else rect.bottom - 28
        label = pygame.Rect(rect.right - 53, y, 49, 24)
        gfx.rect(surface, warna, label, border_radius=6)
        gfx.rect(surface, gelap(warna, 0.4), label, 1, border_radius=6)
        segitiga(surface, KREM, (label.x + 11, label.centery), 5, ke_atas)
        tulis(surface, teks, huruf.angka_kecil, KREM, (label.x + 32, label.centery + 1), "center")


class PetakTangga(Petak):
    """Petak di kaki tangga: pemain naik ke ujung tangga dan dapat bonus.

    # INHERITANCE: turunan dari Petak.
    """

    def __init__(self, nomor, x, y, ukuran, tujuan):
        super().__init__(nomor, x, y, ukuran)
        self._tujuan = tujuan

    @property
    def tujuan(self):
        return self._tujuan

    def efek(self, pemain):
        # POLYMORPHISM: override efek() - naik tangga dan +5 poin.
        pemain.pindah_ke(self._tujuan)
        pemain.tambah_skor(BONUS_TANGGA)
        return f"naik tangga {self._nomor}→{self._tujuan} (+{BONUS_TANGGA})"

    def gambar(self, surface, huruf):
        # POLYMORPHISM: override gambar() - cat dasar diberi rona hijau.
        super().gambar(surface, huruf)
        gfx.rect(surface, campur(self._warna_dasar(), HIJAU_CAT, 0.12), self.rect.inflate(-2, -2))

    def gambar_label(self, surface, huruf):
        # POLYMORPHISM: override gambar_label() - nomor + tanda naik.
        super().gambar_label(surface, huruf)
        self._gambar_tanda(surface, huruf, HIJAU_CAT, self._tujuan, True, di_atas=False)


class PetakUlar(Petak):
    """Petak kepala ular: pemain turun ke ekor ular.

    # INHERITANCE: turunan dari Petak.
    """

    def __init__(self, nomor, x, y, ukuran, tujuan):
        super().__init__(nomor, x, y, ukuran)
        self._tujuan = tujuan

    @property
    def tujuan(self):
        return self._tujuan

    def efek(self, pemain):
        # POLYMORPHISM: override efek() - turun ke ekor ular.
        pemain.pindah_ke(self._tujuan)
        return f"turun ular {self._nomor}→{self._tujuan}"

    def gambar(self, surface, huruf):
        # POLYMORPHISM: override gambar() - cat dasar diberi rona ungu.
        super().gambar(surface, huruf)
        gfx.rect(surface, campur(self._warna_dasar(), ULAR_BADAN, 0.12), self.rect.inflate(-2, -2))

    def gambar_label(self, surface, huruf):
        # POLYMORPHISM: override gambar_label() - nomor + tanda turun.
        super().gambar_label(surface, huruf)
        self._gambar_tanda(surface, huruf, ULAR_BADAN, self._tujuan, False, di_atas=False)


class PetakFinish(Petak):
    """Petak terakhir (64), garis finis.

    # INHERITANCE: turunan dari Petak.
    """

    def efek(self, pemain):
        # POLYMORPHISM: override efek() - menandai pemain sebagai pemenang.
        pemain.tandai_menang()
        return "mencapai FINIS!"

    def gambar(self, surface, huruf):
        # POLYMORPHISM: override gambar() - petak merah bertuliskan FINIS.
        rect = self.rect
        gfx.rect(surface, MERAH_CAT, rect)
        petak_bendera = 9
        for i in range(rect.w // petak_bendera):
            for j in range(2):
                if (i + j) % 2 == 0:
                    gfx.rect(surface, KREM, (rect.x + i * petak_bendera, rect.bottom - 22 + j * petak_bendera, petak_bendera, petak_bendera))
        gfx.rect(surface, gelap(MERAH_CAT, 0.3), rect, 1)
        tulis(surface, self._nomor, huruf.label, KREM, (rect.x + 8, rect.y + 6))
        tulis(surface, "FINIS", huruf.label, KREM, (rect.centerx, rect.centery + 2), "center")
        gfx.line(surface, KREM_GELAP, (rect.x, rect.bottom - 23), (rect.right, rect.bottom - 23), 1)

    def gambar_label(self, surface, huruf):
        # POLYMORPHISM: override gambar_label() - nomor sudah digambar di gambar().
        pass
