"""Class Pemain (manusia) dan Bot (pemain otomatis)."""
import random

from config import JUMLAH_PETAK, HURUF_JAWABAN


class Pemain:
    """Data satu pemain: nama, warna bidak, nomor, posisi petak, dan skor.

    # ENCAPSULATION: semua atribut bersifat private (awalan __) dan hanya
    # bisa dibaca lewat @property atau diubah lewat method yang memeriksa
    # nilainya (setter skor menolak angka negatif, pindah_ke() membatasi 1-36).
    """

    def __init__(self, nama, warna, nomor):
        self.__nama = nama
        self.__warna = warna
        self.__nomor = nomor
        self.__posisi = 1
        self.__skor = 0
        self.__menang = False

    # ------------------------------------------------------------ getter
    @property
    def nama(self):
        return self.__nama

    @property
    def warna(self):
        return self.__warna

    @property
    def nomor(self):
        return self.__nomor

    @property
    def posisi(self):
        return self.__posisi

    @property
    def sudah_menang(self):
        return self.__menang

    @property
    def skor(self):
        return self.__skor

    @skor.setter
    def skor(self, nilai):
        # ENCAPSULATION: validasi di setter, skor tidak boleh negatif.
        if nilai < 0:
            raise ValueError("Skor tidak boleh negatif")
        self.__skor = nilai

    # ------------------------------------------------------------ aksi
    def tambah_skor(self, n):
        """Menambah skor lewat setter agar validasi tetap berjalan."""
        self.skor = self.__skor + n

    def pindah_ke(self, nomor_petak):
        """Memindahkan bidak; posisi di luar 1-36 ditolak."""
        if not 1 <= nomor_petak <= JUMLAH_PETAK:
            raise ValueError(f"Petak {nomor_petak} tidak ada di papan")
        self.__posisi = nomor_petak

    def tandai_menang(self):
        self.__menang = True

    def reset(self):
        """Mengembalikan pemain ke kondisi awal untuk Main Lagi."""
        self.__posisi = 1
        self.__skor = 0
        self.__menang = False

    def is_bot(self):
        return False

    def pilih_jawaban(self, soal):
        """Pemain manusia memilih jawaban lewat klik, jadi method ini
        mengembalikan None (tidak memilih sendiri)."""
        return None


class Bot(Pemain):
    """Pemain otomatis yang menjawab soal dengan peluang benar tertentu.

    # INHERITANCE: Bot mewarisi semua data dan method Pemain.
    """

    def __init__(self, nama, warna, nomor, akurasi=0.6):
        super().__init__(nama, warna, nomor)
        self._akurasi = akurasi  # protected: dipakai juga oleh subclass Bot lain

    def is_bot(self):
        # POLYMORPHISM: override is_bot() milik Pemain.
        return True

    def pilih_jawaban(self, soal):
        # POLYMORPHISM: override pilih_jawaban(); manusia menunggu klik,
        # Bot langsung memilih huruf sendiri.
        if random.random() < self._akurasi:
            return soal.kunci
        salah = [h for h in HURUF_JAWABAN if h != soal.kunci]
        return random.choice(salah)
