"""Class Soal (satu pertanyaan) dan BankSoal (memuat soal dari soal.json)."""
import json
import random

from config import resource_path, KATEGORI_CAMPURAN, HURUF_JAWABAN


class Soal:
    """Satu soal pilihan ganda A-D.

    # ENCAPSULATION: isi soal private dan hanya bisa dibaca lewat @property,
    # sehingga kunci jawaban tidak bisa diubah dari luar.
    """

    def __init__(self, id, kategori, pertanyaan, pilihan, kunci, materi=""):
        self.__id = id
        self.__kategori = kategori
        self.__pertanyaan = pertanyaan
        self.__pilihan = dict(pilihan)
        self.__kunci = kunci
        self.__materi = materi

    @property
    def id(self):
        return self.__id

    @property
    def kategori(self):
        return self.__kategori

    @property
    def materi(self):
        return self.__materi

    @property
    def pertanyaan(self):
        return self.__pertanyaan

    @property
    def pilihan(self):
        return dict(self.__pilihan)  # salinan, agar data asli aman

    @property
    def kunci(self):
        return self.__kunci

    def cek_jawaban(self, huruf):
        return huruf == self.__kunci


class BankSoal:
    """Memuat soal dari file lokal dan membagikannya tanpa pengulangan."""

    KOLOM_WAJIB = ("id", "kategori", "pertanyaan", "pilihan", "kunci")

    def __init__(self):
        self.__daftar = []
        self.__terpakai = set()
        self.__baru_diacak = False
        self.__dipinjam = False
        self.__jumlah_dilewati = 0

    @property
    def baru_diacak(self):
        """True bila semua 300 soal sudah terpakai sehingga diacak ulang."""
        return self.__baru_diacak

    @property
    def dipinjam(self):
        """True bila soal kategori terpilih habis dan diambil dari kategori lain."""
        return self.__dipinjam

    def sisa(self, kategori=KATEGORI_CAMPURAN):
        """Banyak soal kategori ini yang belum pernah keluar."""
        return sum(1 for s in self.__kumpulan(kategori) if s.id not in self.__terpakai)

    @property
    def jumlah_dilewati(self):
        """Banyak soal di file yang tidak valid dan dilewati."""
        return self.__jumlah_dilewati

    def muat(self, path):
        """Memuat soal.json. Mengembalikan (berhasil, pesan)."""
        try:
            with open(resource_path(path), encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("isi file harus berupa daftar soal")
            valid = [s for s in data if self.__valid(s)]
            self.__jumlah_dilewati = len(data) - len(valid)
            self.__daftar = [Soal(**{k: s[k] for k in self.KOLOM_WAJIB}, materi=str(s.get("materi", ""))) for s in valid]
            self.__terpakai.clear()
            if not self.__daftar:
                return False, "File soal tidak berisi soal yang valid"
            return True, f"{len(self.__daftar)} soal dimuat"
        except FileNotFoundError:
            return False, "File soal tidak ditemukan"
        except json.JSONDecodeError:
            return False, "Format soal.json rusak"
        except Exception as e:
            return False, f"Gagal memuat soal: {e}"

    def __valid(self, s):
        """Soal valid: kolom lengkap, tepat 4 pilihan A-D, kunci A-D."""
        if not isinstance(s, dict) or any(k not in s for k in self.KOLOM_WAJIB):
            return False
        pilihan = s["pilihan"]
        if not isinstance(pilihan, dict) or sorted(pilihan) != list(HURUF_JAWABAN):
            return False
        if not all(isinstance(v, str) and v.strip() for v in pilihan.values()):
            return False
        return s["kunci"] in HURUF_JAWABAN and bool(str(s["pertanyaan"]).strip())

    def __kumpulan(self, kategori):
        if kategori == KATEGORI_CAMPURAN:
            return list(self.__daftar)
        return [s for s in self.__daftar if s.kategori == kategori]

    def jumlah(self, kategori=KATEGORI_CAMPURAN):
        return len(self.__kumpulan(kategori))

    def ambil_acak(self, kategori):
        """Mengambil satu soal acak yang BELUM PERNAH keluar.

        Soal yang sudah keluar tidak muncul lagi, termasuk pada permainan
        berikutnya (Main Lagi). Bila soal kategori terpilih habis, soal
        diambil dari kategori lain (dipinjam = True). Hanya jika seluruh
        bank soal sudah keluar, daftar di-reset (baru_diacak = True).
        """
        self.__baru_diacak = False
        self.__dipinjam = False
        if not self.__kumpulan(kategori):
            return None
        sisa = [s for s in self.__kumpulan(kategori) if s.id not in self.__terpakai]
        if not sisa:
            sisa = [s for s in self.__daftar if s.id not in self.__terpakai]
            self.__dipinjam = bool(sisa)
        if not sisa:
            self.__terpakai.clear()
            sisa = self.__kumpulan(kategori)
            self.__baru_diacak = True
        soal = random.choice(sisa)
        self.__terpakai.add(soal.id)
        return soal

    def reset_terpakai(self):
        self.__terpakai.clear()
