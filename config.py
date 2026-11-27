"""Konstanta permainan, palet warna, dan utilitas path.

Semua angka "ajaib" (ukuran, warna, posisi ular/tangga, aturan skor)
dikumpulkan di sini agar mudah diubah tanpa menyentuh logika.
"""
import os
import sys


def resource_path(rel):
    """Mengembalikan path absolut untuk file aset.

    Saat berjalan sebagai .exe (PyInstaller), file ada di folder sementara
    `sys._MEIPASS`; saat berjalan sebagai skrip, file ada di samping main.py.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


# Berjalan di Android (APK buatan Buildozer / python-for-android)?
IS_ANDROID = hasattr(sys, "getandroidapilevel") or "ANDROID_ARGUMENT" in os.environ

# ---------------------------------------------------------------- layar
JUDUL = "Ular Tangga Kuis"
VERSI = "1.4"   # satu-satunya tempat nomor versi; installer & menu mengikuti
LEBAR, TINGGI = 1280, 720
FPS = 60

# ---------------------------------------------------------------- file
FILE_SOAL = "soal.json"
FILE_IKON_PNG = os.path.join("assets", "icon.png")
FOLDER_FONT = os.path.join("assets", "fonts")
FOLDER_SUARA = os.path.join("assets", "sounds")

# ---------------------------------------------------------------- aturan
JUMLAH_PETAK = 64
KOLOM = 8

# Tingkat kesulitan: makin sulit, makin banyak ular, makin sedikit tangga,
# dan bot makin pintar (peluang menjawab benar lebih tinggi).
# tangga: bawah -> atas, ular: kepala -> ekor
# Letak tangga diperiksa alat/cek_tata_letak.py: antar-tangga berjarak >= 1,5 petak,
# tidak segaris (tampak seperti satu tangga panjang), dan tidak ditindih ular.
KESULITAN = {
    "Mudah": {
        "tangga": {7: 24, 16: 32, 22: 36, 40: 56, 43: 60, 47: 63},
        "ular": {30: 12, 49: 33, 62: 45},
        "akurasi_bot": 0.45,
    },
    "Sedang": {
        "tangga": {6: 21, 9: 25, 19: 35, 33: 49, 44: 61},
        "ular": {18: 3, 34: 16, 47: 31, 56: 38, 63: 45},
        "akurasi_bot": 0.65,
    },
    "Sulit": {
        "tangga": {4: 19, 11: 28, 24: 40, 33: 49},
        "ular": {16: 3, 27: 10, 32: 15, 46: 29, 53: 34, 60: 41, 62: 44, 63: 47},
        "akurasi_bot": 0.85,
    },
}
KESULITAN_AWAL = "Sedang"

SKOR_BENAR = 10
BONUS_TANGGA = 5
WAKTU_SOAL = 30          # detik
JEDA_HASIL = 1.5         # detik, lama hasil jawaban tampil
JEDA_BOT = 1.5           # detik, bot "berpikir"
MIN_PEMAIN, MAKS_PEMAIN = 2, 4
MAKS_NAMA = 12

KATEGORI = ["Matematika", "Penjas Orkes", "Sejarah Indonesia"]
KATEGORI_CAMPURAN = "Campuran"
HURUF_JAWABAN = ("A", "B", "C", "D")

# ---------------------------------------------------------------- tata letak
UKURAN_PETAK = 78
PAPAN_X, PAPAN_Y = 30, 48
KOLOM_KANAN_X = 696
KOLOM_KANAN_LEBAR = 560
BARIS_LOG = 7

# ---------------------------------------------------------------- palet pasar malam
TERPAL = (28, 74, 152)
TERPAL_GELAP = (18, 50, 108)
TERPAL_TERANG = (40, 90, 172)
TERPAL_JAHIT = (92, 136, 206)
KREM = (247, 241, 226)
KREM_GELAP = (222, 210, 184)
KUNING_PUCAT = (252, 226, 158)
KUNING_CAT = (255, 204, 72)
KUNING_TUA = (196, 146, 20)
MERAH_CAT = (204, 36, 52)
MERAH_TUA = (130, 18, 32)
HIJAU_CAT = (24, 132, 78)
HIJAU_TUA = (12, 84, 48)
TINTA = (26, 30, 46)
TINTA_LEMBUT = (84, 80, 92)
BOHLAM_NYALA = (255, 222, 130)
BOHLAM_INTI = (255, 248, 220)
BOHLAM_MATI = (92, 70, 40)
OREN_JALUR = (255, 132, 28)
KAYU = (186, 120, 60)
KAYU_GELAP = (96, 56, 24)
ULAR_BADAN = (142, 52, 150)
ULAR_TUA = (70, 20, 78)
ULAR_GARIS = (255, 206, 84)

WARNA_PEMAIN = [
    ("Merah", (214, 40, 56)),
    ("Biru", (36, 102, 220)),
    ("Hijau", (22, 150, 84)),
    ("Kuning", (240, 178, 16)),
]
