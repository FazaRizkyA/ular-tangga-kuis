"""Class GameManager: pengendali alur permainan (game state, giliran, skor).

Tidak ada kode gambar di sini; tampilan (main.py) hanya membaca state
dan memanggil method sesuai input pemain.
"""
from config import SKOR_BENAR, WAKTU_SOAL, JUMLAH_PETAK

# Daftar state permainan (lihat tabel Game state di PRD).
MENJAWAB = "MENJAWAB"
HASIL_JAWABAN = "HASIL_JAWABAN"
MENUNGGU_DADU = "MENUNGGU_DADU"
BERGERAK = "BERGERAK"
GANTI_GILIRAN = "GANTI_GILIRAN"
SELESAI = "SELESAI"


class GameManager:
    """Mengatur giliran, soal, dadu, gerak bidak, dan pemenang.

    # ENCAPSULATION: semua data permainan private; tombol dan input hanya
    # bisa mengubahnya lewat method yang memeriksa state, sehingga klik
    # ganda tidak bisa merusak giliran.
    """

    def __init__(self, papan, bank_soal, dadu, kategori):
        self.__papan = papan
        self.__bank = bank_soal
        self.__dadu = dadu
        self.__kategori = kategori
        self.__pemain = []
        self.__indeks_giliran = 0
        self.__state = None
        self.__log = []
        self.__nomor_log = 0
        self.__pemenang = None
        self.__soal_aktif = None
        self.__sisa_waktu = WAKTU_SOAL
        self.__jawaban_terakhir = None
        self.__benar_terakhir = False
        self.__catatan = ""
        self.__info_gerak = None

    # ------------------------------------------------------------ getter
    @property
    def state(self):
        return self.__state

    @property
    def kategori(self):
        return self.__kategori

    @property
    def pemain(self):
        return tuple(self.__pemain)

    @property
    def pemain_aktif(self):
        return self.__pemain[self.__indeks_giliran]

    @property
    def soal_aktif(self):
        return self.__soal_aktif

    @property
    def sisa_waktu(self):
        return max(0.0, self.__sisa_waktu)

    @property
    def jawaban_terakhir(self):
        return self.__jawaban_terakhir

    @property
    def benar_terakhir(self):
        return self.__benar_terakhir

    @property
    def log(self):
        """Riwayat aktivitas, terbaru di depan: tuple (nomor, teks)."""
        return tuple(reversed(self.__log))

    @property
    def pemenang(self):
        return self.__pemenang

    @property
    def info_gerak(self):
        """Data animasi gerak terakhir: jalur, efek, dan nilai dadu."""
        return self.__info_gerak

    # ------------------------------------------------------------ alur
    def __catat(self, teks):
        self.__nomor_log += 1
        self.__log.append((self.__nomor_log, teks))

    def mulai_permainan(self, daftar_pemain):
        self.__pemain = list(daftar_pemain)
        self.__indeks_giliran = 0
        self.__pemenang = None
        self.__log = []
        self.__nomor_log = 0
        self.__catat("Permainan dimulai. Semua bidak di petak 1.")
        self.mulai_giliran()

    def mulai_giliran(self):
        """Mengambil soal baru untuk pemain aktif."""
        # soal diambil sesuai tingkat kesulitan papan (Mudah/Sedang/Sulit)
        self.__soal_aktif = self.__bank.ambil_acak(self.__kategori, self.__papan.kesulitan)
        if self.__bank.baru_diacak:
            self.__catat(f"Semua soal {self.__papan.kesulitan} sudah keluar, bank soal diacak ulang.")
        elif self.__bank.dipinjam:
            self.__catat(f"Soal {self.__kategori} habis, soal diambil dari kategori lain.")
        self.__sisa_waktu = WAKTU_SOAL
        self.__jawaban_terakhir = None
        self.__benar_terakhir = False
        self.__info_gerak = None
        self.__state = MENJAWAB

    def kurangi_waktu(self, dt):
        """Dipanggil tiap frame; waktu habis dianggap jawaban salah."""
        if self.__state != MENJAWAB:
            return
        self.__sisa_waktu -= dt
        if self.__sisa_waktu <= 0:
            self.jawab(None)

    def jawab(self, huruf):
        """Memeriksa jawaban. Mengembalikan True/False, atau None bila
        bukan saatnya menjawab."""
        if self.__state != MENJAWAB or self.__soal_aktif is None:
            return None
        pemain = self.pemain_aktif
        soal = self.__soal_aktif
        benar = huruf is not None and soal.cek_jawaban(huruf)
        self.__jawaban_terakhir = huruf
        self.__benar_terakhir = benar
        if benar:
            pemain.tambah_skor(SKOR_BENAR)
            self.__catatan = f"{pemain.nama} benar (+{SKOR_BENAR})"
        elif huruf is None:
            self.__catat(f"{pemain.nama} kehabisan waktu (kunci {soal.kunci}), giliran dilewati")
        else:
            self.__catat(f"{pemain.nama} salah (kunci {soal.kunci}), giliran dilewati")
        self.__state = HASIL_JAWABAN
        return benar

    def lanjut_setelah_hasil(self):
        if self.__state != HASIL_JAWABAN:
            return
        if self.__benar_terakhir:
            self.__state = MENUNGGU_DADU
        else:
            self.giliran_berikut()

    def kocok_dadu(self):
        """Mengocok dadu sekali per giliran, menggerakkan bidak, lalu
        menjalankan efek petak tujuan. Mengembalikan nilai dadu atau None."""
        if self.__state != MENUNGGU_DADU:
            return None
        pemain = self.pemain_aktif
        nilai = self.__dadu.kocok()
        jalur = self.gerak(nilai)
        catatan = f"{self.__catatan}, dadu {nilai}"
        if jalur and max(jalur) == JUMLAH_PETAK and jalur[-1] != JUMLAH_PETAK:
            catatan += f", memantul ke {jalur[-1]}"

        posisi_sebelum = pemain.posisi
        petak = self.__papan.get_petak(pemain.posisi)
        pesan = petak.efek(pemain)  # POLYMORPHISM: efek tergantung jenis petak
        if pesan:
            catatan += f", {pesan}"
        self.__catatan = catatan
        self.__info_gerak = {
            "dadu": nilai,
            "jalur": jalur,
            "efek_dari": posisi_sebelum,
            "efek_ke": pemain.posisi if pemain.posisi != posisi_sebelum else None,
        }
        self.__state = BERGERAK
        return nilai

    def gerak(self, langkah):
        """Menghitung jalur langkah demi langkah; memantul bila lewat 64."""
        pemain = self.pemain_aktif
        posisi = pemain.posisi
        arah = 1
        jalur = []
        for _ in range(langkah):
            if posisi == JUMLAH_PETAK:
                arah = -1
            posisi += arah
            jalur.append(posisi)
        pemain.pindah_ke(posisi)
        return jalur

    def selesai_animasi(self):
        """Dipanggil tampilan setelah animasi bidak selesai."""
        if self.__state != BERGERAK:
            return
        self.__catat(self.__catatan)
        pemain = self.pemain_aktif
        if pemain.sudah_menang:
            self.__pemenang = pemain
            self.__catat(f"{pemain.nama} MENANG!")
            self.__state = SELESAI
        else:
            self.giliran_berikut()

    def giliran_berikut(self):
        self.__state = GANTI_GILIRAN
        self.__indeks_giliran = (self.__indeks_giliran + 1) % len(self.__pemain)
        self.mulai_giliran()

    def reset(self):
        """Main Lagi: pemain, mode, kategori, dan kesulitan sama; posisi,
        skor, dan log kembali dari awal. Soal yang sudah keluar TIDAK
        di-reset, sehingga permainan berikutnya memakai soal yang berbeda."""
        for p in self.__pemain:
            p.reset()
        self.mulai_permainan(self.__pemain)

    def peringkat(self):
        """Urutan pemain: pemenang dulu, lalu posisi tertinggi, lalu skor."""
        return sorted(self.__pemain, key=lambda p: (p.sudah_menang, p.posisi, p.skor), reverse=True)
