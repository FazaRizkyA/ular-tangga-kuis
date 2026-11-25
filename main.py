"""Ular Tangga Kuis - titik masuk aplikasi.

Class App menjalankan loop Pygame dan menggambar lima layar:
Menu Utama, Cara Bermain, Setup Pemain, Papan Permainan, dan Pemenang.
Semua logika permainan ada di GameManager (game.py); App hanya membaca
state dan meneruskan input pemain.
"""
import math
import os
import random
import sys
import traceback

import pygame

import kanvas as gfx

from config import (
    JUDUL, VERSI, LEBAR, TINGGI, FPS, FILE_SOAL, FILE_IKON_PNG, FOLDER_SUARA,
    IS_ANDROID, resource_path, KATEGORI, KATEGORI_CAMPURAN, HURUF_JAWABAN,
    MIN_PEMAIN, MAKS_PEMAIN, MAKS_NAMA, WARNA_PEMAIN, JEDA_BOT, JUMLAH_PETAK,
    JEDA_HASIL, WAKTU_SOAL, BONUS_TANGGA, SKOR_BENAR, KOLOM_KANAN_X,
    KOLOM_KANAN_LEBAR, BARIS_LOG, KESULITAN, KESULITAN_AWAL,
    TERPAL, TERPAL_GELAP, KREM, KREM_GELAP, KUNING_CAT, KUNING_PUCAT, KUNING_TUA,
    MERAH_CAT, MERAH_TUA, HIJAU_CAT, HIJAU_TUA, TINTA, TINTA_LEMBUT, KAYU, KAYU_GELAP,
    ULAR_BADAN, ULAR_TUA, ULAR_GARIS, BOHLAM_NYALA,
)
from pemain import Pemain, Bot
from rumus import PenataRumus
from dadu3d import Dadu3D, DaduRender, SUDUT_AKHIR
from soal import BankSoal
from dadu import Dadu
from papan import Papan
from game import (
    GameManager, MENJAWAB, HASIL_JAWABAN, MENUNGGU_DADU, BERGERAK, SELESAI,
)
from tampilan import (
    Huruf, Tombol, KolomTeks, tulis, bungkus_teks, papan_cat, latar_terpal,
    tali_bohlam, karcis, gambar_dadu, gambar_bidak, gambar_ular, redupkan,
    terang, gelap,
)

# ------------------------------------------------------------------ tata letak kolom kanan
R_SKOR = pygame.Rect(KOLOM_KANAN_X, 24, KOLOM_KANAN_LEBAR, 140)
R_SOAL = pygame.Rect(KOLOM_KANAN_X, 174, KOLOM_KANAN_LEBAR, 262)
R_DADU = pygame.Rect(KOLOM_KANAN_X, 446, KOLOM_KANAN_LEBAR - 76, 56)
PUSAT_DADU = (KOLOM_KANAN_X + KOLOM_KANAN_LEBAR - 30, 474)
R_LOG = pygame.Rect(KOLOM_KANAN_X, 512, KOLOM_KANAN_LEBAR, 192)
TINGGI_SOAL = 68   # ruang tegak untuk teks soal di antara baris status dan tombol jawaban
DURASI_GULIR = 1.35   # detik dadu 3D berguling
DURASI_DIAM = 0.45    # detik dadu diam menunjukkan angka
DURASI_HILANG = 0.35  # detik dadu memudar saat bidak mulai berjalan
JUMLAH_PANTUL = 3
UKURAN_DADU_RENDER = 160  # px gambar dadu Blender di layar


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


class Suara:
    """Efek suara (dadu, benar, salah, langkah, naik, turun, menang).
    Bila file suara atau perangkat audio tidak ada, game tetap jalan tanpa suara."""

    NAMA = ("dadu", "benar", "salah", "langkah", "naik", "turun", "menang", "klik")

    def __init__(self):
        self.aktif = True
        self.__klip = {}
        try:
            pygame.mixer.init()
            for nama in self.NAMA:
                try:
                    self.__klip[nama] = pygame.mixer.Sound(resource_path(os.path.join(FOLDER_SUARA, f"{nama}.wav")))
                    self.__klip[nama].set_volume(0.5)
                except Exception:
                    pass
        except Exception:
            self.__klip = {}

    def main(self, nama):
        if self.aktif and nama in self.__klip:
            self.__klip[nama].play()


class App:
    """Loop utama Pygame: membaca input, memperbarui animasi, menggambar."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(JUDUL)
        try:
            self.ikon = pygame.image.load(resource_path(FILE_IKON_PNG))
            pygame.display.set_icon(self.ikon)
        except Exception:
            self.ikon = None
        self.mode_gpu = False
        self.layar_penuh = False
        self.skala, self.geser = 1.0, (0, 0)
        self.skala_render = self.__skala_render()
        gfx.atur_skala(self.skala_render)
        # Kanvas: koordinat logis 1280x720, piksel fisik sebesar resolusi layar
        # (mis. 1920x1080), sehingga layar penuh tampil 1:1 dan tajam.
        self.window = self.__buat_jendela()
        if IS_ANDROID:
            # HP/tablet: layar penuh landscape. Kanvas digambar pas di resolusi layar
            # (tanpa diperbesar) di tengah layar; sisa layar menjadi bilah gelap.
            lw, lh = self.window.get_size()
            s = min(lw / LEBAR, lh / TINGGI)
            self.skala_render = s
            gfx.atur_skala(s)
            fisik = (min(lw, round(LEBAR * s)), min(lh, round(TINGGI * s)))
            self.geser = ((lw - fisik[0]) // 2, (lh - fisik[1]) // 2)
            self.skala = s
            self.window.fill((8, 16, 34))
            self.canvas = gfx.Kanvas(permukaan=self.window.subsurface(pygame.Rect(self.geser, fisik)))
        elif self.mode_gpu:
            self.canvas = gfx.Kanvas(permukaan=pygame.Surface(self.ukuran_fisik))
            self.tekstur = self.__Texture.from_surface(self.renderer, self.canvas.p)
        else:
            self.canvas = gfx.Kanvas((LEBAR, TINGGI))
        self.clock = pygame.time.Clock()
        self.huruf = Huruf()
        self.rumus_soal = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 24)
        self.rumus_soal_kecil = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 20)
        self.rumus_jawab = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 18)
        self.dadu3d = Dadu3D(84)            # cadangan: dadu digambar dengan kode
        self.dadu_render = DaduRender()     # utama: hasil render Blender dari dadu.glb
        self.suara = Suara()
        pygame.key.stop_text_input()

        self.bank = BankSoal()
        self.soal_siap, self.pesan_soal = self.bank.muat(FILE_SOAL)
        if self.soal_siap and self.bank.jumlah_dilewati:
            self.pesan_soal += f" ({self.bank.jumlah_dilewati} soal tidak valid dilewati)"
        self.papan = Papan(KESULITAN_AWAL)
        self.dadu = Dadu()
        self.gm = None

        self.layar_aktif = "menu"
        self.konfirmasi = False
        self.pesan_error = ""
        self.waktu = 0.0
        self.berjalan = True

        self.__siapkan_menu()
        self.__siapkan_setup()
        self.__siapkan_game()

    # ============================================================ jendela & skala
    def __skala_render(self):
        """Skala gambar = resolusi layar / 1280x720 (1,5 di layar 1920x1080).
        Game digambar di resolusi itu sehingga layar penuh tidak diperbesar."""
        if os.environ.get("UTK_SKALA"):
            return float(os.environ["UTK_SKALA"])
        if os.environ.get("SDL_VIDEODRIVER") == "dummy":
            return 1.0
        try:
            lebar_layar, tinggi_layar = pygame.display.get_desktop_sizes()[0]
            return max(1.0, min(lebar_layar / LEBAR, tinggi_layar / TINGGI))
        except Exception:
            return 1.0

    def __ukuran_awal(self):
        """Skala jendela awal agar muat di layar laptop (mis. 1366x768)."""
        try:
            lebar_layar, tinggi_layar = pygame.display.get_desktop_sizes()[0]
            return min(1.0, lebar_layar * 0.94 / LEBAR, tinggi_layar * 0.86 / TINGGI)
        except Exception:
            return 1.0

    def __buat_jendela(self):
        """Mode utama (GPU): jendela bebas ukuran + renderer SDL. Kanvas digambar
        di resolusi layar; GPU hanya mengecilkannya di mode jendela, sedangkan
        layar penuh tampil 1:1 (tajam). Bila tidak didukung, pakai cara lama."""
        self.ukuran_fisik = (round(LEBAR * self.skala_render), round(TINGGI * self.skala_render))
        if not IS_ANDROID and os.environ.get("SDL_VIDEODRIVER") != "dummy":
            try:
                from pygame._sdl2 import video
                self.__Texture = video.Texture
                s = self.__ukuran_awal()
                self.win = video.Window(JUDUL, size=(int(LEBAR * s), int(TINGGI * s)), resizable=True,
                                        position=video.WINDOWPOS_CENTERED)
                if self.ikon is not None:
                    self.win.set_icon(self.ikon)
                self.renderer = video.Renderer(self.win, accelerated=1)
                self.mode_gpu = True
                return None
            except Exception:
                self.mode_gpu = False
        self.skala_render = 1.0
        gfx.atur_skala(1.0)
        self.ukuran_fisik = (LEBAR, TINGGI)
        if IS_ANDROID:
            return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        s = self.__ukuran_awal()
        return pygame.display.set_mode((int(LEBAR * s), int(TINGGI * s)), pygame.RESIZABLE)

    def __layar_penuh(self):
        """F11 / Alt+Enter: masuk atau keluar dari layar penuh."""
        if self.mode_gpu:
            if self.layar_penuh:
                self.win.set_windowed()
            else:
                self.win.set_fullscreen(desktop=True)
            self.layar_penuh = not self.layar_penuh
            return
        penuh = bool(self.window.get_flags() & pygame.FULLSCREEN)
        if penuh:
            s = self.__ukuran_awal()
            self.window = pygame.display.set_mode((int(LEBAR * s), int(TINGGI * s)), pygame.RESIZABLE)
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def __ke_kanvas(self, pos):
        """Koordinat jendela -> koordinat logis 1280x720 (memperhitungkan bilah hitam)."""
        return ((pos[0] - self.geser[0]) / self.skala, (pos[1] - self.geser[1]) / self.skala)

    def __tampilkan(self):
        if IS_ANDROID:
            pygame.display.flip()  # kanvas sudah bagian dari layar (subsurface)
            return
        if self.mode_gpu:
            # unggah kanvas ke GPU, lalu tampilkan sesuai ukuran jendela (bilah hitam bila perlu)
            self.tekstur.update(self.canvas.p)
            lw, lh = self.win.size
            self.skala = min(lw / LEBAR, lh / TINGGI)
            w, h = LEBAR * self.skala, TINGGI * self.skala
            self.geser = ((lw - w) / 2, (lh - h) / 2)
            self.renderer.draw_color = (8, 16, 34, 255)
            self.renderer.clear()
            self.tekstur.draw(dstrect=pygame.Rect(round(self.geser[0]), round(self.geser[1]), round(w), round(h)))
            self.renderer.present()
            return
        lw, lh = self.window.get_size()
        self.skala = min(lw / LEBAR, lh / TINGGI)
        w, h = int(LEBAR * self.skala), int(TINGGI * self.skala)
        self.geser = ((lw - w) // 2, (lh - h) // 2)
        self.window.fill((8, 16, 34))
        if (w, h) == (LEBAR, TINGGI):
            self.window.blit(self.canvas.p, self.geser)
        else:
            self.window.blit(pygame.transform.smoothscale(self.canvas.p, (w, h)), self.geser)
        pygame.display.flip()

    # ============================================================ loop
    def run(self):
        while self.berjalan:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.waktu += dt
            try:
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update(dt)
                self.render()
            except Exception as e:
                # Exception umum: tampilkan pesan dan kembali ke Menu Utama.
                traceback.print_exc()
                self.pesan_error = f"Terjadi kesalahan: {e}. Kembali ke menu."
                self.layar_aktif = "menu"
                self.konfirmasi = False
                self.gm = None
            self.__tampilkan()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            if self.layar_aktif == "main" and not self.konfirmasi:
                self.konfirmasi = True
            else:
                self.berjalan = False
            return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            if event.button not in (1, 2, 3):
                return
            pos = self.__ke_kanvas(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__klik(pos)
            return
        if event.type == pygame.MOUSEWHEEL and self.layar_aktif == "main":
            self.gulir_log = max(0, self.gulir_log - event.y)
            return
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT)):
            self.__layar_penuh()
            return
        if event.type == pygame.KEYDOWN:
            self.__tombol_keyboard(event)
        if event.type in (pygame.TEXTINPUT, pygame.KEYDOWN) and self.layar_aktif == "setup":
            for kolom in self.kolom_nama:
                if kolom.handle(event):
                    break

    def __tombol_keyboard(self, event):
        kembali = event.key in (pygame.K_ESCAPE, pygame.K_AC_BACK)
        if self.konfirmasi:
            if kembali:
                self.konfirmasi = False
            return
        if self.layar_aktif == "main":
            if kembali:
                self.konfirmasi = True
            elif event.key == pygame.K_m:
                self.suara.aktif = not self.suara.aktif
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.__coba_kocok()
            else:
                huruf = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D",
                         pygame.K_1: "A", pygame.K_2: "B", pygame.K_3: "C", pygame.K_4: "D"}.get(event.key)
                if huruf:
                    self.__coba_jawab(huruf)
        elif self.layar_aktif == "setup":
            if kembali:
                self.__ke_layar("menu")
            elif event.key == pygame.K_TAB:
                self.__fokus_berikut()
            elif event.key == pygame.K_RETURN:
                self.__mulai_permainan()
        elif self.layar_aktif == "cara" and kembali:
            self.__ke_layar("menu")
        elif self.layar_aktif == "pemenang" and kembali:
            self.__ke_layar("menu")

    def __ke_layar(self, nama):
        self.layar_aktif = nama
        if nama == "setup":
            self.pesan_error = ""
        else:
            self.__fokus_kolom(None)

    def update(self, dt):
        if self.layar_aktif == "main" and self.gm and not self.konfirmasi:
            self.__update_game(dt)

    def render(self):
        layar = {
            "menu": self.__gambar_menu,
            "cara": self.__gambar_cara,
            "setup": self.__gambar_setup,
            "main": self.__gambar_game,
            "pemenang": self.__gambar_pemenang,
        }[self.layar_aktif]
        layar()
        if self.konfirmasi:
            self.__gambar_konfirmasi()

    def __mouse(self):
        return self.__ke_kanvas(pygame.mouse.get_pos())

    # ============================================================ klik
    def __klik(self, pos):
        if self.konfirmasi:
            if self.t_batal.kena(pos):
                self.konfirmasi = False
            elif self.t_ya_keluar.kena(pos):
                self.konfirmasi = False
                if self.layar_aktif == "main":
                    self.gm = None
                    self.__ke_layar("menu")
                else:
                    self.berjalan = False
            return
        if self.layar_aktif == "menu":
            if self.t_mulai.kena(pos):
                self.suara.main("klik")
                self.__ke_layar("setup")
            elif self.t_cara.kena(pos):
                self.suara.main("klik")
                self.__ke_layar("cara")
            elif self.t_keluar.kena(pos):
                self.berjalan = False
        elif self.layar_aktif == "cara":
            if self.t_kembali_cara.kena(pos):
                self.__ke_layar("menu")
        elif self.layar_aktif == "setup":
            self.__klik_setup(pos)
        elif self.layar_aktif == "main":
            self.__klik_game(pos)
        elif self.layar_aktif == "pemenang":
            if self.t_main_lagi.kena(pos):
                self.suara.main("klik")
                self.gm.reset()
                self.__mulai_layar_game()
            elif self.t_menu.kena(pos):
                self.gm = None
                self.__ke_layar("menu")

    # ============================================================ MENU
    def __siapkan_menu(self):
        x = LEBAR // 2 - 170
        self.t_mulai = Tombol((x, 432, 340, 62), "MULAI", KUNING_CAT, TINTA)
        self.t_cara = Tombol((x, 506, 340, 62), "CARA BERMAIN", KREM, TINTA)
        self.t_keluar = Tombol((x, 580, 340, 62), "KELUAR", KREM, TINTA)
        self.t_kembali_cara = Tombol((LEBAR // 2 - 120, 596, 240, 56), "KEMBALI", KUNING_CAT, TINTA)
        self.t_batal = Tombol((462, 392, 160, 52), "BATAL", KREM, TINTA)
        self.t_ya_keluar = Tombol((636, 392, 182, 52), "YA, KELUAR", MERAH_CAT, KREM)

    def __gambar_papan_nama(self, rect, baris_atas, baris_bawah):
        """Papan nama stan: papan merah besar dan plakat kuning di bawahnya."""
        for x in (rect.x + 70, rect.right - 70):
            gfx.line(self.canvas, (14, 22, 40), (x, 92), (x, rect.y + 8), 3)
        papan_cat(self.canvas, rect, MERAH_CAT, radius=16, tebal_tepi=4)
        gfx.rect(self.canvas, terang(MERAH_CAT, 0.35), rect.inflate(-20, -20), 2, border_radius=10)
        tulis(self.canvas, baris_atas, self.huruf.raksasa, KREM, (rect.centerx, rect.centery - 18), "center")
        plakat = pygame.Rect(0, 0, 240, 66)
        plakat.center = (rect.centerx, rect.bottom)
        papan_cat(self.canvas, plakat, KUNING_CAT, radius=10)
        tulis(self.canvas, baris_bawah, self.huruf.judul, TINTA, plakat.center, "center")

    def __gambar_menu(self):
        c = self.canvas
        latar_terpal(c)
        tali_bohlam(c, 30, LEBAR - 30, 56, 46, 27, self.waktu, "kejar")
        self.__gambar_papan_nama(pygame.Rect(240, 128, 800, 196), "ULAR TANGGA", "KUIS")
        tulis(c, f"Jawab soalnya, buka dadunya, capai petak {JUMLAH_PETAK}.", self.huruf.teks_tebal, KREM, (LEBAR // 2, 392), "center")

        self.t_mulai.aktif = self.soal_siap
        mouse = self.__mouse()
        for t in (self.t_mulai, self.t_cara, self.t_keluar):
            t.gambar(c, self.huruf, mouse)

        pesan = self.pesan_error or ("" if self.soal_siap else f"{self.pesan_soal}. Tombol Mulai dinonaktifkan.")
        if pesan:
            r = pygame.Rect(0, 0, 760, 40)
            r.center = (LEBAR // 2, 668)
            papan_cat(c, r, MERAH_CAT, radius=8)
            tulis(c, pesan, self.huruf.kecil_tebal, KREM, r.center, "center")
        else:
            tulis(c, f"SMK Krian 1 Sidoarjo  ·  PBTG 2026/2027  ·  versi {VERSI}", self.huruf.kecil, terang(TERPAL, 0.78), (LEBAR // 2, 684), "center")

        # Hiasan stan: tangga bersandar di kiri, ular melingkar di kanan.
        self.__hiasan_tangga(c, 120, 640, 200)
        self.__hiasan_ular(c, 1130, 600)

    def __hiasan_tangga(self, c, x, y_bawah, tinggi):
        for dx in (-18, 18):
            gfx.line(c, KAYU_GELAP, (x + dx, y_bawah), (x + dx + 30, y_bawah - tinggi), 10)
        for i in range(1, 9):
            yy = y_bawah - i * tinggi / 9
            off = 30 * i / 9
            gfx.line(c, KAYU_GELAP, (x - 18 + off, yy), (x + 18 + off, yy), 8)
            gfx.line(c, KAYU, (x - 18 + off, yy), (x + 18 + off, yy), 4)
        for dx in (-18, 18):
            gfx.line(c, KAYU, (x + dx, y_bawah), (x + dx + 30, y_bawah - tinggi), 5)

    def __hiasan_ular(self, c, cx, cy):
        # Ular cat yang sama dengan ular di papan, dipasang tegak di sisi stan.
        gambar_ular(c, (cx - 10, cy - 150), (cx + 20, cy + 60), tebal=17)

    # ============================================================ CARA BERMAIN
    def __gambar_cara(self):
        c = self.canvas
        latar_terpal(c)
        papan = pygame.Rect(120, 40, 1040, 640)
        papan_cat(c, papan, KREM, radius=16)
        tulis(c, "CARA BERMAIN", self.huruf.judul, TINTA, (papan.x + 48, papan.y + 30))
        aturan = [
            f"Setiap giliran dimulai dengan satu soal pilihan ganda. Waktu menjawab {WAKTU_SOAL} detik.",
            f"Jawaban benar: +{SKOR_BENAR} poin dan tombol Kocok Dadu terbuka.",
            "Jawaban salah atau waktu habis: kunci ditampilkan, giliran pindah.",
            f"Bidak maju sesuai angka dadu. Harus pas di petak {JUMLAH_PETAK}; kelebihan langkah memantul mundur.",
            f"Berhenti di kaki tangga: naik dan +{BONUS_TANGGA} poin. Berhenti di kepala ular: turun ke ekornya.",
            f"Pemain pertama yang mendarat tepat di petak {JUMLAH_PETAK} menang. Pilih kesulitan Mudah, Sedang, atau Sulit: makin sulit, makin banyak ular dan bot makin pintar.",
        ]
        y = papan.y + 104
        for i, teks in enumerate(aturan, 1):
            nomor = pygame.Rect(papan.x + 48, y, 34, 34)
            gfx.circle(c, MERAH_CAT, nomor.center, 17)
            tulis(c, i, self.huruf.label, KREM, (nomor.centerx, nomor.centery + 1), "center")
            for j, baris in enumerate(bungkus_teks(teks, self.huruf.teks, 560)):
                tulis(c, baris, self.huruf.teks, TINTA, (papan.x + 100, y + 5 + j * 26))
            y += 26 * len(bungkus_teks(teks, self.huruf.teks, 560)) + 20

        kanan = papan.x + 730
        tulis(c, "TANDA DI PAPAN", self.huruf.label, TINTA_LEMBUT, (kanan, papan.y + 104))
        # tangga
        for dx in (0, 26):
            gfx.line(c, KAYU_GELAP, (kanan + dx, papan.y + 210), (kanan + dx, papan.y + 140), 9)
            gfx.line(c, KAYU, (kanan + dx, papan.y + 210), (kanan + dx, papan.y + 140), 4)
        for yy in range(papan.y + 150, papan.y + 210, 16):
            gfx.line(c, KAYU_GELAP, (kanan, yy), (kanan + 26, yy), 6)
            gfx.line(c, KAYU, (kanan, yy), (kanan + 26, yy), 3)
        tulis(c, "Tangga", self.huruf.teks_tebal, TINTA, (kanan + 50, papan.y + 148))
        tulis(c, f"Naik ke ujung, +{BONUS_TANGGA} poin", self.huruf.kecil, TINTA_LEMBUT, (kanan + 50, papan.y + 174))
        # ular
        yy = papan.y + 250
        gambar_ular(c, (kanan + 16, yy + 10), (kanan + 18, yy + 92), tebal=9)
        tulis(c, "Ular", self.huruf.teks_tebal, TINTA, (kanan + 50, yy + 26))
        tulis(c, "Turun ke ekornya", self.huruf.kecil, TINTA_LEMBUT, (kanan + 50, yy + 52))
        # bidak
        yy = papan.y + 380
        for i, (_, warna) in enumerate(WARNA_PEMAIN):
            gambar_bidak(c, (kanan + 18 + i * 46, yy + 20), warna, i + 1, self.huruf.angka_kecil, r=17)
        tulis(c, "Bidak: warna dan nomor pemain", self.huruf.kecil, TINTA_LEMBUT, (kanan, yy + 52))
        # kontrol
        yy = papan.y + 470
        tulis(c, "TOMBOL KEYBOARD", self.huruf.label, TINTA_LEMBUT, (kanan, yy))
        for j, baris in enumerate(["A-D atau 1-4 : menjawab", "Spasi : kocok dadu", "M : suara nyala/mati", "F11 : layar penuh", "Esc : keluar"]):
            tulis(c, baris, self.huruf.kecil, TINTA, (kanan, yy + 30 + j * 24))
        self.t_kembali_cara.gambar(c, self.huruf, self.__mouse())

    # ============================================================ SETUP
    def __siapkan_setup(self):
        self.mode = "pass"
        self.jumlah = 2
        self.kategori = KATEGORI_CAMPURAN
        self.kesulitan = KESULITAN_AWAL
        self.kolom_nama = [KolomTeks((470, 282 + i * 52, 320, 42), f"Pemain {i + 1}") for i in range(MAKS_PEMAIN)]
        self.t_mode = {
            "pass": Tombol((420, 118, 230, 44), "PASS & PLAY", KREM, TINTA, "label"),
            "bot": Tombol((662, 118, 170, 44), "VS BOT", KREM, TINTA, "label"),
        }
        self.t_jumlah = {n: Tombol((420 + (n - 2) * 76, 170, 64, 44), str(n), KREM, TINTA, "label") for n in range(MIN_PEMAIN, MAKS_PEMAIN + 1)}
        self.t_kesulitan = {}
        x = 420
        for nama in KESULITAN:
            w = self.huruf.label.size(nama.upper())[0] + 34
            self.t_kesulitan[nama] = Tombol((x, 222, w, 44), nama.upper(), KREM, TINTA, "label")
            x += w + 8
        self.t_kategori = {}
        x = 420
        for nama in [*KATEGORI, KATEGORI_CAMPURAN]:
            w = self.huruf.label.size(nama.upper())[0] + 20
            self.t_kategori[nama] = Tombol((x, 500, w, 44), nama.upper(), KREM, TINTA, "label")
            x += w + 6
        self.t_kembali_setup = Tombol((190, 596, 200, 56), "KEMBALI", KREM, TINTA)
        self.t_mulai_main = Tombol((850, 596, 250, 56), "MULAI MAIN", KUNING_CAT, TINTA)
        self.__terapkan_mode()

    def __terapkan_mode(self):
        for i, kolom in enumerate(self.kolom_nama):
            bot = self.mode == "bot" and i > 0
            kolom.bisa_diubah = not bot
            kolom.error = ""
            if bot:
                kolom.fokus = False
            if bot:
                kolom.teks = f"Bot {i}"
            elif kolom.teks.startswith("Bot "):
                kolom.teks = f"Pemain {i + 1}"

    def __fokus_kolom(self, kolom):
        for k in self.kolom_nama:
            k.fokus = k is kolom
        if kolom is not None:
            pygame.key.start_text_input()
            pygame.key.set_text_input_rect(pygame.Rect(kolom.rect))
        else:
            pygame.key.stop_text_input()

    def __fokus_berikut(self):
        bisa = [k for k in self.kolom_nama[:self.jumlah] if k.bisa_diubah]
        if not bisa:
            return
        sekarang = next((i for i, k in enumerate(bisa) if k.fokus), -1)
        self.__fokus_kolom(bisa[(sekarang + 1) % len(bisa)])

    def __klik_setup(self, pos):
        for mode, t in self.t_mode.items():
            if t.kena(pos) and self.mode != mode:
                self.mode = mode
                self.__terapkan_mode()
                self.suara.main("klik")
        for n, t in self.t_jumlah.items():
            if t.kena(pos):
                self.jumlah = n
                self.suara.main("klik")
        for nama, t in self.t_kesulitan.items():
            if t.kena(pos):
                self.kesulitan = nama
                self.suara.main("klik")
        for nama, t in self.t_kategori.items():
            if t.kena(pos):
                self.kategori = nama
                self.pesan_error = ""
                self.suara.main("klik")
        target = None
        for kolom in self.kolom_nama[:self.jumlah]:
            if kolom.bisa_diubah and kolom.rect.collidepoint(pos):
                target = kolom
        self.__fokus_kolom(target)
        if self.t_kembali_setup.kena(pos):
            self.__ke_layar("menu")
        elif self.t_mulai_main.kena(pos):
            self.__mulai_permainan()

    def __validasi_nama(self):
        """T1: nama tidak boleh kosong, maksimal 12 karakter, tidak boleh sama."""
        aktif = self.kolom_nama[:self.jumlah]
        semua_ok = True
        dipakai = {}
        for kolom in aktif:
            kolom.error = ""
            nama = kolom.teks.strip()
            if not nama:
                kolom.error = "Nama tidak boleh kosong"
            elif len(nama) > MAKS_NAMA:
                kolom.error = f"Maksimal {MAKS_NAMA} karakter"
            elif nama.lower() in dipakai:
                kolom.error = "Nama sudah dipakai"
            dipakai.setdefault(nama.lower(), kolom)
            semua_ok = semua_ok and not kolom.error
        return semua_ok

    def __mulai_permainan(self):
        if not self.__validasi_nama():
            return
        if self.bank.jumlah(self.kategori) == 0:
            self.pesan_error = f"Tidak ada soal untuk kategori {self.kategori}."
            return
        daftar = []
        akurasi = KESULITAN[self.kesulitan]["akurasi_bot"]
        for i, kolom in enumerate(self.kolom_nama[:self.jumlah]):
            nama_warna, warna = WARNA_PEMAIN[i]
            if self.mode == "bot" and i > 0:
                daftar.append(Bot(kolom.teks.strip(), warna, i + 1, akurasi))
            else:
                daftar.append(Pemain(kolom.teks.strip(), warna, i + 1))
        self.papan = Papan(self.kesulitan)  # letak ular & tangga sesuai kesulitan
        self.gm = GameManager(self.papan, self.bank, self.dadu, self.kategori)
        self.gm.mulai_permainan(daftar)
        self.suara.main("klik")
        self.__mulai_layar_game()

    def __gambar_setup(self):
        c = self.canvas
        latar_terpal(c)
        mouse = self.__mouse()
        papan = pygame.Rect(140, 40, 1000, 640)
        papan_cat(c, papan, KREM, radius=16)
        tulis(c, "DAFTAR PEMAIN", self.huruf.judul, TINTA, (papan.x + 50, papan.y + 26))

        def label(teks, y):
            tulis(c, teks, self.huruf.label, TINTA_LEMBUT, (190, y), "midleft")

        label("MODE", 140)
        for mode, t in self.t_mode.items():
            dipilih = self.mode == mode
            t.gambar(c, self.huruf, mouse, MERAH_CAT if dipilih else KREM_GELAP, KREM if dipilih else TINTA)
        label("JUMLAH PEMAIN", 192)
        for n, t in self.t_jumlah.items():
            dipilih = self.jumlah == n
            t.gambar(c, self.huruf, mouse, MERAH_CAT if dipilih else KREM_GELAP, KREM if dipilih else TINTA)
        keterangan = "1 pemain melawan bot" if self.mode == "bot" else "bergantian di satu perangkat"
        tulis(c, keterangan, self.huruf.kecil, TINTA_LEMBUT, (680, 192), "midleft")

        label("KESULITAN", 244)
        for nama, t in self.t_kesulitan.items():
            dipilih = self.kesulitan == nama
            t.gambar(c, self.huruf, mouse, MERAH_CAT if dipilih else KREM_GELAP, KREM if dipilih else TINTA)
        aturan = KESULITAN[self.kesulitan]
        ket = f"{len(aturan['tangga'])} tangga · {len(aturan['ular'])} ular"
        if self.mode == "bot":
            ket += f" · bot benar ±{int(aturan['akurasi_bot'] * 100)}%"
        x_ket = max(t.rect.right for t in self.t_kesulitan.values()) + 18
        tulis(c, ket, self.huruf.kecil, TINTA_LEMBUT, (x_ket, 244), "midleft")

        label("NAMA PEMAIN", 303)
        for i, kolom in enumerate(self.kolom_nama[:self.jumlah]):
            gambar_bidak(c, (440, kolom.rect.centery), WARNA_PEMAIN[i][1], i + 1, self.huruf.angka_kecil, r=17)
            kolom.gambar(c, self.huruf, self.waktu)
            if not kolom.bisa_diubah:
                tulis(c, "BOT", self.huruf.angka_kecil, TINTA_LEMBUT, (kolom.rect.right - 14, kolom.rect.centery), "midright")
            if kolom.error:
                tulis(c, kolom.error, self.huruf.kecil_tebal, MERAH_CAT, (kolom.rect.right + 16, kolom.rect.centery), "midleft")
            elif kolom.bisa_diubah and kolom.fokus:
                tulis(c, f"{len(kolom.teks.strip())}/{MAKS_NAMA}", self.huruf.kecil, TINTA_LEMBUT, (kolom.rect.right + 16, kolom.rect.centery), "midleft")

        label("KATEGORI SOAL", 522)
        for nama, t in self.t_kategori.items():
            dipilih = self.kategori == nama
            t.aktif = self.bank.jumlah(nama) > 0
            t.gambar(c, self.huruf, mouse, MERAH_CAT if dipilih else KREM_GELAP, KREM if dipilih else TINTA)
        jumlah_soal = self.bank.jumlah(self.kategori)
        sisa = self.bank.sisa(self.kategori)
        tulis(c, f"{jumlah_soal} soal, {sisa} belum pernah keluar", self.huruf.kecil, TINTA_LEMBUT, (420, 562), "midleft")

        self.t_kembali_setup.gambar(c, self.huruf, mouse)
        self.t_mulai_main.gambar(c, self.huruf, mouse)
        if self.pesan_error:
            tulis(c, self.pesan_error, self.huruf.kecil_tebal, MERAH_CAT, (640, 624), "center")

    # ============================================================ GAME
    def __siapkan_game(self):
        self.t_jawab = {}
        lebar = (R_SOAL.w - 28 - 10) // 2
        for i, h in enumerate(HURUF_JAWABAN):
            x = R_SOAL.x + 14 + (i % 2) * (lebar + 10)
            y = R_SOAL.bottom - 14 - 2 * 46 - 6 + (i // 2) * 52
            self.t_jawab[h] = pygame.Rect(x, y, lebar, 46)
        self.t_kocok = Tombol(R_DADU, "KOCOK DADU", MERAH_CAT, KREM)
        self.t_suara = pygame.Rect(R_SKOR.right - 162, R_SKOR.y + 5, 150, 24)
        self.__reset_tampilan_game()

    def __reset_tampilan_game(self):
        self.anim = None
        self.t_hasil = 0.0
        self.t_bot = 0.0
        self.t_selesai = 0.0
        self.gulir_log = 0
        self.nilai_dadu_tampil = 1
        self.sudut_dadu = 0.0
        self.skor_tampil = {}
        self.popup = []
        self.soal_tampil = None
        self.t_geser_soal = 1.0

    def __mulai_layar_game(self):
        self.__reset_tampilan_game()
        for p in self.gm.pemain:
            self.skor_tampil[p.nomor] = float(p.skor)
        self.layar_aktif = "main"

    def __coba_jawab(self, huruf):
        gm = self.gm
        if gm and gm.state == MENJAWAB and not gm.pemain_aktif.is_bot():
            self.__jawab(huruf)

    def __jawab(self, huruf):
        benar = self.gm.jawab(huruf)
        if benar is None:
            return
        self.t_hasil = 0.0
        self.suara.main("benar" if benar else "salah")
        if benar:
            self.__popup(self.gm.pemain_aktif, f"+{SKOR_BENAR}")

    def __bisa_kocok(self):
        """Dadu terbuka untuk pemain manusia begitu jawabannya benar."""
        gm = self.gm
        if not gm or gm.pemain_aktif.is_bot() or self.anim is not None:
            return False
        return gm.state == MENUNGGU_DADU or (gm.state == HASIL_JAWABAN and gm.benar_terakhir)

    def __coba_kocok(self):
        if not self.__bisa_kocok():
            return
        if self.gm.state == HASIL_JAWABAN:
            self.gm.lanjut_setelah_hasil()
        self.__kocok()

    def __kocok(self):
        indeks = self.gm.pemain.index(self.gm.pemain_aktif)
        if self.gm.kocok_dadu() is None:
            return  # T14: klik berulang diabaikan karena state sudah berubah
        self.suara.main("dadu")
        info = self.gm.info_gerak
        # Lintasan lempar: dari meja dadu (kolom kanan) berguling ke tengah papan.
        papan = self.papan.rect
        rx_akhir, ry_akhir = SUDUT_AKHIR[info["dadu"]]
        lempar = {
            "awal": (PUSAT_DADU[0] - 40, PUSAT_DADU[1] - 30),
            "akhir": (papan.centerx + random.randint(-90, 90), papan.centery + random.randint(-70, 70)),
            "putar": (random.choice((-1, 1)) * (4 + random.random() * 2) * math.pi,
                      random.choice((-1, 1)) * (3 + random.random() * 2) * math.pi,
                      random.choice((-1, 1)) * (2 + random.random()) * math.pi),
            "target": (rx_akhir, ry_akhir, 0.0),
            "pantul": 0,
        }
        self.anim = {"fase": "dadu", "t": 0.0, "info": info, "indeks": indeks, "langkah": 0, "lempar": lempar}

    def __popup(self, pemain, teks):
        self.popup.append({"nomor": pemain.nomor, "teks": teks, "t": 0.0})

    def __klik_game(self, pos):
        gm = self.gm
        if self.t_suara.collidepoint(pos):
            self.suara.aktif = not self.suara.aktif
            return
        if gm.state == MENJAWAB and not gm.pemain_aktif.is_bot():
            for h, rect in self.t_jawab.items():
                if rect.collidepoint(pos):
                    self.__jawab(h)
                    return
        if self.t_kocok.kena(pos):
            self.__coba_kocok()

    def __update_game(self, dt):
        gm = self.gm
        pemain = gm.pemain_aktif
        # soal baru meluncur masuk seperti karcis disodorkan di loket
        if gm.soal_aktif is not self.soal_tampil:
            self.soal_tampil = gm.soal_aktif
            self.t_geser_soal = 0.0
            self.t_bot = 0.0
        self.t_geser_soal = min(1.0, self.t_geser_soal + dt / 0.35)

        if gm.state == MENJAWAB:
            gm.kurangi_waktu(dt)
            if gm.state == HASIL_JAWABAN:  # waktu habis
                self.t_hasil = 0.0
                self.suara.main("salah")
            elif pemain.is_bot():
                self.t_bot += dt
                if self.t_bot >= JEDA_BOT:
                    self.__jawab(pemain.pilih_jawaban(gm.soal_aktif))  # POLYMORPHISM
        elif gm.state == HASIL_JAWABAN:
            self.t_hasil += dt
            if self.t_hasil >= JEDA_HASIL:
                gm.lanjut_setelah_hasil()
                self.t_bot = 0.0
        elif gm.state == MENUNGGU_DADU and pemain.is_bot() and self.anim is None:
            self.t_bot += dt
            if self.t_bot >= 0.9:
                self.__kocok()
        elif gm.state == SELESAI:
            self.t_selesai += dt
            if self.t_selesai >= 1.4:
                self.layar_aktif = "pemenang"

        if self.anim:
            self.__update_animasi(dt)

        for p in gm.pemain:
            target = p.skor
            if self.anim and gm.pemain[self.anim["indeks"]] is p:
                info = self.anim["info"]
                if info["efek_ke"] and info["efek_ke"] > info["efek_dari"]:
                    target -= BONUS_TANGGA  # bonus tampil setelah naik tangga
            sekarang = self.skor_tampil.get(p.nomor, 0.0)
            self.skor_tampil[p.nomor] = sekarang + (target - sekarang) * min(1.0, dt * 8)
        for pop in self.popup:
            pop["t"] += dt
        self.popup = [p for p in self.popup if p["t"] < 1.2]

    def __update_animasi(self, dt):
        a = self.anim
        a["t"] += dt
        info = a["info"]
        if a["fase"] == "dadu":
            # dadu 3D berguling dan memantul; bunyi ketukan tiap kali menyentuh papan
            pantul = min(JUMLAH_PANTUL, int(a["t"] / DURASI_GULIR * JUMLAH_PANTUL))
            if pantul != a["lempar"]["pantul"]:
                a["lempar"]["pantul"] = pantul
                self.suara.main("klik")
            if a["t"] >= DURASI_GULIR:
                self.nilai_dadu_tampil = info["dadu"]
            if a["t"] >= DURASI_GULIR + DURASI_DIAM:
                a["fase"], a["t"] = "jalan", 0.0
        elif a["fase"] == "jalan":
            durasi = 0.26
            langkah = int(a["t"] / durasi)
            if langkah != a["langkah"] and langkah <= len(info["jalur"]):
                self.suara.main("langkah")
            a["langkah"] = langkah
            if a["t"] >= durasi * len(info["jalur"]):
                if info["efek_ke"]:
                    a["fase"], a["t"] = "efek", 0.0
                    self.suara.main("naik" if info["efek_ke"] > info["efek_dari"] else "turun")
                else:
                    self.__akhiri_animasi()
        elif a["fase"] == "efek":
            if a["t"] >= 0.8:
                if info["efek_ke"] > info["efek_dari"]:
                    self.__popup(self.gm.pemain[a["indeks"]], f"+{BONUS_TANGGA}")
                self.__akhiri_animasi()

    def __akhiri_animasi(self):
        self.anim = None
        self.gm.selesai_animasi()
        self.t_bot = 0.0
        if self.gm.state == SELESAI:
            self.suara.main("menang")
            self.t_selesai = 0.0

    def __posisi_tampil(self):
        """Posisi piksel tiap bidak, termasuk bidak yang sedang dianimasikan."""
        gm = self.gm
        posisi = {}
        angkat = {}
        petak_pemain = {}
        for i, p in enumerate(gm.pemain):
            petak = p.posisi
            if self.anim and self.anim["indeks"] == i:
                continue
            petak_pemain.setdefault(petak, []).append(i)
        for petak, daftar in petak_pemain.items():
            for urut, i in enumerate(daftar):
                posisi[i] = self.papan.posisi_bidak(petak, urut, len(daftar))
                angkat[i] = 0
        if self.anim:
            a = self.anim
            info = a["info"]
            jalur = info["jalur"]
            mulai = jalur[0] - 1
            if a["fase"] == "dadu":
                posisi[a["indeks"]] = self.papan.posisi_bidak(mulai, 0, 1)
                angkat[a["indeks"]] = 0
            elif a["fase"] == "jalan":
                durasi = 0.26
                k = min(int(a["t"] / durasi), len(jalur) - 1)
                f = min(1.0, (a["t"] - k * durasi) / durasi)
                dari = mulai if k == 0 else jalur[k - 1]
                p0 = self.papan.posisi_bidak(dari, 0, 1)
                p1 = self.papan.posisi_bidak(jalur[k], 0, 1)
                e = ease_out(f)
                posisi[a["indeks"]] = (p0[0] + (p1[0] - p0[0]) * e, p0[1] + (p1[1] - p0[1]) * e)
                angkat[a["indeks"]] = math.sin(math.pi * f) * 22
            else:
                f = ease_out(a["t"] / 0.8)
                p0 = self.papan.posisi_bidak(jalur[-1], 0, 1)
                p1 = self.papan.posisi_bidak(info["efek_ke"], 0, 1)
                posisi[a["indeks"]] = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
                angkat[a["indeks"]] = math.sin(math.pi * f) * 30
        return posisi, angkat

    def __sorot_jalur(self):
        """Signature: bohlam jalur menyala petak demi petak di depan bidak."""
        if not self.anim or self.anim["fase"] != "jalan":
            return None
        jalur = self.anim["info"]["jalur"]
        k = self.anim["langkah"]
        sorot = {}
        for j, nomor in enumerate(jalur):
            if j < k:
                sorot[nomor] = max(sorot.get(nomor, 0), 0.25)
            elif j <= k + 2:
                sorot[nomor] = max(sorot.get(nomor, 0), 1.0 - (j - k) * 0.3)
        return sorot

    def __gambar_game(self):
        c = self.canvas
        gm = self.gm
        # Latar terpal + bagian papan yang diam disimpan sebagai satu gambar
        # (dibuat ulang hanya bila papan berganti), agar tiap frame cepat.
        if getattr(self, "_latar_papan", None) is None or self._latar_papan[0] is not self.papan:
            latar = gfx.Kanvas((LEBAR, TINGGI))
            latar_terpal(latar)
            self.papan.gambar_tetap(latar, self.huruf)
            self._latar_papan = (self.papan, latar)
        c.blit(self._latar_papan[1], (0, 0))
        mouse = self.__mouse()

        petak_aktif = None
        if not self.anim and gm.state != SELESAI:
            petak_aktif = gm.pemain_aktif.posisi
        self.papan.gambar(c, self.huruf, self.waktu, self.__sorot_jalur(), petak_aktif, tetap=False)

        posisi, angkat = self.__posisi_tampil()
        urutan = sorted(posisi, key=lambda i: posisi[i][1])
        for i in urutan:
            p = gm.pemain[i]
            gambar_bidak(c, posisi[i], p.warna, p.nomor, self.huruf.angka_kecil, angkat[i], r=15)

        self.__gambar_skor(c, mouse)
        self.__gambar_soal(c, mouse)
        self.__gambar_dadu(c, mouse)
        self.__gambar_log(c)
        self.__gambar_dadu_lempar(c)

    def __gambar_dadu_lempar(self, c):
        """Dadu 3D dilempar dari meja dadu, berguling dan memantul di atas papan,
        lalu berhenti dengan angka hasil kocokan menghadap pemain."""
        a = self.anim
        if not a or "lempar" not in a:
            return
        L = a["lempar"]
        if a["fase"] == "dadu":
            t = min(1.0, a["t"] / DURASI_GULIR)
            alfa = 255
        elif a["fase"] == "jalan" and a["t"] < DURASI_HILANG:
            t = 1.0
            alfa = int(255 * (1 - a["t"] / DURASI_HILANG))
        else:
            return
        e = ease_out(t)
        x = L["awal"][0] + (L["akhir"][0] - L["awal"][0]) * e
        lantai = L["awal"][1] + (L["akhir"][1] - L["awal"][1]) * e
        tinggi = abs(math.sin(math.pi * JUMLAH_PANTUL * t)) * 120 * (1 - t) ** 1.6
        sisa = 1 - e
        rx = L["target"][0] + L["putar"][0] * sisa
        ry = L["target"][1] + L["putar"][1] * sisa
        rz = L["putar"][2] * sisa

        ukuran = self.dadu3d.ukuran
        sisi = int(ukuran * 2.4)
        lapis = gfx.Kanvas((sisi, sisi + 130), pygame.SRCALPHA)
        tengah = (sisi // 2, sisi // 2 + 120 - tinggi)
        # bayangan di papan: mengecil dan memudar saat dadu melambung
        lebar_bayang = int(ukuran * (1.25 - 0.4 * tinggi / 120))
        bayang = gfx.Kanvas((lebar_bayang, max(8, lebar_bayang // 3)), pygame.SRCALPHA)
        gfx.ellipse(bayang, (0, 0, 0, int(90 - 40 * tinggi / 120)), bayang.get_rect())
        lapis.blit(bayang, bayang.get_rect(center=(sisi // 2, sisi // 2 + 120 + ukuran * 0.55)))
        if a["fase"] != "dadu" or a["t"] >= DURASI_GULIR:
            # dadu sudah diam: cahaya hangat di belakangnya menandai hasil
            for r in range(int(ukuran * 0.95), 0, -6):
                gfx.circle(lapis, (*BOHLAM_NYALA, int(40 * (1 - r / (ukuran * 0.95)))), tengah, r)
        if self.dadu_render.siap:
            self.dadu_render.gambar(lapis, tengah, a["info"]["dadu"], e, UKURAN_DADU_RENDER)
        else:
            self.dadu3d.gambar(lapis, tengah, rx, ry, rz)
        lapis.set_alpha(alfa)
        c.blit(lapis, (x - sisi // 2, lantai - sisi // 2 - 120))

    def __gambar_skor(self, c, mouse):
        gm = self.gm
        papan_cat(c, R_SKOR, MERAH_CAT, radius=12)
        tulis(c, f"PAPAN SKOR · {self.papan.kesulitan.upper()}", self.huruf.label, KREM, (R_SKOR.x + 16, R_SKOR.y + 17), "midleft")
        teks_suara = "SUARA: NYALA" if self.suara.aktif else "SUARA: MATI"
        hover = self.t_suara.collidepoint(mouse)
        gfx.rect(c, terang(MERAH_CAT, 0.2) if hover else gelap(MERAH_CAT, 0.2), self.t_suara, border_radius=6)
        tulis(c, teks_suara, self.huruf.angka_kecil, KREM, self.t_suara.center, "center")

        lebar = (R_SKOR.w - 24 - 8) // 2
        for i, p in enumerate(gm.pemain):
            aktif = p is gm.pemain_aktif and gm.state != SELESAI
            x = R_SKOR.x + 12 + (i % 2) * (lebar + 8)
            y = R_SKOR.y + 34 + (i // 2) * 52
            sel = pygame.Rect(x, y - (3 if aktif else 0), lebar, 48)
            warna = KUNING_CAT if aktif else KREM_GELAP
            gfx.rect(c, warna, sel, border_radius=8)
            if aktif:
                gfx.rect(c, gelap(KUNING_CAT, 0.4), sel, 2, border_radius=8)
            tinta = TINTA if aktif else TINTA_LEMBUT
            gambar_bidak(c, (sel.x + 24, sel.centery - 2), p.warna, p.nomor, self.huruf.angka_kecil, r=17)
            nama = p.nama + (" (bot)" if p.is_bot() else "")
            batas = sel.w - 56
            while self.huruf.kecil_tebal.size(nama)[0] > batas and len(nama) > 1:
                nama = nama[:-1]
            tulis(c, nama, self.huruf.kecil_tebal, tinta, (sel.x + 48, sel.y + 13), "midleft")
            skor = int(round(self.skor_tampil.get(p.nomor, p.skor)))
            r_skor = tulis(c, f"Petak {p.posisi}  ·  {skor} poin", self.huruf.kecil, tinta, (sel.x + 48, sel.y + 34), "midleft")
            for pop in self.popup:
                if pop["nomor"] == p.nomor:
                    naik = pop["t"] * 24
                    alfa = max(0, 255 - int(pop["t"] * 210))
                    gambar = self.huruf.label.render(pop["teks"], True, HIJAU_CAT)
                    gambar.set_alpha(alfa)
                    c.blit(gambar, gambar.get_rect(midleft=(r_skor.right + 10, r_skor.centery - naik)))

    def __gambar_soal(self, c, mouse):
        gm = self.gm
        pemain = gm.pemain_aktif
        soal = gm.soal_aktif
        papan_cat(c, R_SOAL, KREM, radius=12)
        kepala = pygame.Rect(R_SOAL.x, R_SOAL.y, R_SOAL.w, 44)
        gfx.rect(c, KUNING_CAT, kepala, border_top_left_radius=12, border_top_right_radius=12)
        gfx.line(c, gelap(KUNING_CAT, 0.35), kepala.bottomleft, kepala.bottomright, 2)
        gfx.rect(c, gelap(KREM, 0.35), R_SOAL, 3, border_radius=12)
        gambar_bidak(c, (kepala.x + 26, kepala.centery), pemain.warna, pemain.nomor, self.huruf.angka_kecil, r=14)
        tulis(c, f"GILIRAN {pemain.nama.upper()}", self.huruf.label, TINTA, (kepala.x + 50, kepala.centery + 1), "midleft")

        # timer
        sisa = gm.sisa_waktu if gm.state == MENJAWAB else (0 if gm.jawaban_terakhir is None and gm.state == HASIL_JAWABAN else gm.sisa_waktu)
        pusat = (kepala.right - 30, kepala.centery)
        kritis = gm.state == MENJAWAB and sisa <= 10
        gfx.circle(c, MERAH_CAT if kritis else TINTA, pusat, 18)
        if gm.state == MENJAWAB:
            sudut = 2 * math.pi * (sisa / WAKTU_SOAL)
            if sudut > 0.05:
                gfx.arc(c, KUNING_PUCAT, (pusat[0] - 17, pusat[1] - 17, 34, 34), math.pi / 2, math.pi / 2 + sudut, 3)
        tulis(c, int(math.ceil(sisa)), self.huruf.angka_kecil, KREM, (pusat[0], pusat[1] + 1), "center")
        tulis(c, "DETIK", self.huruf.angka_kecil, TINTA, (pusat[0] - 26, kepala.centery + 1), "midright")

        if soal is None:
            tulis(c, "Soal tidak tersedia.", self.huruf.teks_tebal, MERAH_CAT, (R_SOAL.x + 18, R_SOAL.y + 70))
            return

        geser = int((1 - ease_out(self.t_geser_soal)) * 40)
        x0 = R_SOAL.x + 18 + geser
        # baris status: kategori, atau hasil jawaban
        if gm.state in (MENJAWAB,):
            status = soal.kategori + (f" · {soal.materi}" if soal.materi else "")
            if pemain.is_bot():
                status += f"  ·  {pemain.nama} sedang berpikir..."
            tulis(c, status, self.huruf.kecil_tebal, TINTA_LEMBUT, (x0, R_SOAL.y + 54))
        elif gm.state == HASIL_JAWABAN or (gm.benar_terakhir and gm.state in (MENUNGGU_DADU, BERGERAK)):
            if gm.benar_terakhir:
                teks, warna = f"BENAR!  +{SKOR_BENAR} poin. Silakan kocok dadu.", HIJAU_TUA
            elif gm.jawaban_terakhir is None:
                teks, warna = f"WAKTU HABIS. Kunci: {soal.kunci}. Giliran pindah.", MERAH_CAT
            else:
                teks, warna = f"SALAH. Kunci: {soal.kunci}. Giliran pindah.", MERAH_CAT
            tulis(c, teks, self.huruf.kecil_tebal, warna, (x0, R_SOAL.y + 54))

        # Soal digambar oleh penata rumus: pecahan bersusun, pangkat di atas, akar bergaris.
        lebar_soal = R_SOAL.w - 36
        penata = self.rumus_soal
        if len(penata.bungkus(soal.pertanyaan, lebar_soal)) > 2 or penata.tinggi(soal.pertanyaan, lebar_soal) > TINGGI_SOAL:
            penata = self.rumus_soal_kecil  # soal panjang: huruf sedikit lebih kecil agar tetap muat
        penata.gambar(c, soal.pertanyaan, x0, R_SOAL.y + 78, lebar_soal, TINTA, maks_baris=3)

        bisa_klik = gm.state == MENJAWAB and not pemain.is_bot()
        sudah = gm.state != MENJAWAB
        for h, rect in self.t_jawab.items():
            rect = rect.move(geser, 0)
            hover = bisa_klik and rect.collidepoint(mouse) and not IS_ANDROID
            if sudah and h == soal.kunci:
                warna, tinta = HIJAU_CAT, KREM
            elif sudah and h == gm.jawaban_terakhir:
                warna, tinta = MERAH_CAT, KREM
            elif sudah:
                warna, tinta = KREM_GELAP, TINTA_LEMBUT
            elif bisa_klik:
                warna, tinta = (terang(KUNING_CAT, 0.25) if hover else KUNING_CAT), TINTA
            else:
                warna, tinta = KUNING_PUCAT, TINTA_LEMBUT
            r = rect.move(0, -2 if hover else 0)
            papan_cat(c, r, warna, radius=9, bayang=not sudah)
            lencana = (r.x + 22, r.centery)
            gfx.circle(c, tinta, lencana, 14)
            tulis(c, h, self.huruf.label, warna, (lencana[0], lencana[1] + 1), "center")
            self.rumus_jawab.gambar(c, soal.pilihan[h], r.x + 44, 0, r.w - 56, tinta, maks_baris=2, tengah_y=r.centery)

    def __gambar_dadu(self, c, mouse):
        gm = self.gm
        pemain = gm.pemain_aktif
        bisa = self.__bisa_kocok()
        self.t_kocok.aktif = bisa
        if bisa:
            label = "KOCOK DADU"
        elif self.anim:
            label = "BIDAK BERJALAN..."
        elif gm.state == MENUNGGU_DADU or (gm.state == HASIL_JAWABAN and gm.benar_terakhir):
            label = f"{pemain.nama.upper()} MENGOCOK..."
        elif gm.state == HASIL_JAWABAN:
            label = "GILIRAN PINDAH..."
        elif gm.state == SELESAI:
            label = "PERMAINAN SELESAI"
        else:
            label = "JAWAB SOAL DULU"
        self.t_kocok.gambar(c, self.huruf, mouse, label=label)
        gambar_dadu(c, PUSAT_DADU, 52, self.nilai_dadu_tampil, self.sudut_dadu)

    def __gambar_log(self, c):
        gm = self.gm
        karcis(c, R_LOG, KREM, TERPAL, 64)
        tulis(c, "NO.", self.huruf.angka_kecil, TINTA_LEMBUT, (R_LOG.x + 32, R_LOG.y + 15), "center")
        tulis(c, "RIWAYAT PERMAINAN", self.huruf.label, TINTA, (R_LOG.x + 80, R_LOG.y + 15), "midleft")
        log = gm.log
        maks_gulir = max(0, len(log) - BARIS_LOG)
        self.gulir_log = min(self.gulir_log, maks_gulir)
        tampil = log[self.gulir_log:self.gulir_log + BARIS_LOG]
        y = R_LOG.y + 29
        for j, (nomor, teks) in enumerate(tampil):
            terbaru = self.gulir_log == 0 and j == 0
            tulis(c, f"{nomor:03d}", self.huruf.angka_kecil, TINTA_LEMBUT, (R_LOG.x + 32, y + 11), "center")
            font = self.huruf.kecil_tebal if terbaru else self.huruf.kecil
            batas = R_LOG.w - 96
            if font.size(teks)[0] > batas:
                while font.size(teks + "...")[0] > batas and teks:
                    teks = teks[:-1]
                teks += "..."
            tulis(c, teks, font, TINTA if terbaru else TINTA_LEMBUT, (R_LOG.x + 80, y + 11), "midleft")
            if j < len(tampil) - 1:
                for xx in range(R_LOG.x + 80, R_LOG.right - 14, 8):
                    gfx.line(c, KREM_GELAP, (xx, y + 22), (xx + 3, y + 22))
            y += 23
        if maks_gulir:
            tulis(c, f"GULIR {self.gulir_log}/{maks_gulir}", self.huruf.angka_kecil, TINTA_LEMBUT, (R_LOG.right - 14, R_LOG.y + 15), "midright")

    # ============================================================ PEMENANG
    def __gambar_pemenang(self):
        c = self.canvas
        gm = self.gm
        latar_terpal(c)
        tali_bohlam(c, 30, LEBAR - 30, 40, 40, 27, self.waktu, "semua")
        pemenang = gm.pemenang
        papan = pygame.Rect(290, 100, 700, 170)
        for x in (papan.x + 70, papan.right - 70):
            gfx.line(c, (14, 22, 40), (x, 74), (x, papan.y + 8), 3)
        papan_cat(c, papan, MERAH_CAT, radius=16, tebal_tepi=4)
        gfx.rect(c, terang(MERAH_CAT, 0.35), papan.inflate(-20, -20), 2, border_radius=10)
        judul = f"{pemenang.nama.upper()} MENANG!"
        font = self.huruf.raksasa
        for kandidat in (self.huruf.raksasa, self.huruf.judul, self.huruf.sub):
            font = kandidat
            if kandidat.size(judul)[0] <= papan.w - 150:
                break
        lebar = font.size(judul)[0]
        tulis(c, judul, font, KREM, (papan.centerx + 30, papan.centery + 2), "center")
        gambar_bidak(c, (papan.centerx + 30 - lebar // 2 - 38, papan.centery), pemenang.warna, pemenang.nomor, self.huruf.label, r=26)
        self.__pita_juara(c, papan.right - 4, papan.y + 4)

        tabel = pygame.Rect(390, 300, 500, 60 + 52 * len(gm.pemain))
        papan_cat(c, tabel, KREM, radius=14)
        tulis(c, "PERINGKAT", self.huruf.label, TINTA_LEMBUT, (tabel.x + 24, tabel.y + 28), "midleft")
        tulis(c, "PETAK", self.huruf.angka_kecil, TINTA_LEMBUT, (tabel.right - 150, tabel.y + 28), "center")
        tulis(c, "SKOR", self.huruf.angka_kecil, TINTA_LEMBUT, (tabel.right - 60, tabel.y + 28), "center")
        for i, p in enumerate(gm.peringkat()):
            y = tabel.y + 74 + i * 52
            if i == 0:
                gfx.rect(c, KUNING_CAT, (tabel.x + 12, y - 22, tabel.w - 24, 44), border_radius=8)
            tulis(c, i + 1, self.huruf.angka, TINTA, (tabel.x + 36, y), "center")
            gambar_bidak(c, (tabel.x + 84, y - 2), p.warna, p.nomor, self.huruf.angka_kecil, r=15)
            tulis(c, p.nama, self.huruf.teks_tebal, TINTA, (tabel.x + 112, y), "midleft")
            tulis(c, p.posisi, self.huruf.label, TINTA, (tabel.right - 150, y), "center")
            tulis(c, p.skor, self.huruf.label, TINTA, (tabel.right - 60, y), "center")

        y_tombol = tabel.bottom + 30
        self.t_main_lagi = Tombol((390, y_tombol, 290, 60), "MAIN LAGI (RESTART)", KUNING_CAT, TINTA)
        self.t_menu = Tombol((694, y_tombol, 196, 60), "MENU UTAMA", KREM, TINTA)
        mouse = self.__mouse()
        self.t_main_lagi.gambar(c, self.huruf, mouse)
        self.t_menu.gambar(c, self.huruf, mouse)

    def __pita_juara(self, c, x, y):
        """Hadiah stan: rosette pita juara yang digantung di pojok papan."""
        for dx, warna in ((-14, MERAH_TUA), (14, MERAH_CAT)):
            ekor = [(x + dx - 12, y + 30), (x + dx + 12, y + 30), (x + dx + 10, y + 96), (x + dx, y + 84), (x + dx - 10, y + 96)]
            gfx.polygon(c, warna, ekor)
            gfx.polygon(c, gelap(warna, 0.4), ekor, 2)
        for i in range(16):
            sudut = i / 16 * 2 * math.pi
            gfx.circle(c, KUNING_TUA, (int(x + math.cos(sudut) * 34), int(y + math.sin(sudut) * 34)), 12)
        gfx.circle(c, KUNING_CAT, (x, y), 36)
        gfx.circle(c, KREM, (x, y), 26)
        gfx.circle(c, KUNING_TUA, (x, y), 26, 2)
        tulis(c, "1", self.huruf.judul, MERAH_CAT, (x, y + 2), "center")

    # ============================================================ KONFIRMASI
    def __gambar_konfirmasi(self):
        c = self.canvas
        redupkan(c, 160)
        kotak = pygame.Rect(440, 250, 400, 214)
        papan_cat(c, kotak, KREM, radius=14)
        dalam_game = self.layar_aktif == "main"
        judul = "KELUAR DARI PERMAINAN?" if dalam_game else "TUTUP APLIKASI?"
        tulis(c, judul, self.huruf.label, TINTA, (kotak.centerx, kotak.y + 42), "center")
        ket = "Permainan yang sedang berjalan akan hilang." if dalam_game else "Sampai jumpa lagi."
        for j, b in enumerate(bungkus_teks(ket, self.huruf.kecil, 340)):
            tulis(c, b, self.huruf.kecil, TINTA_LEMBUT, (kotak.centerx, kotak.y + 84 + j * 22), "center")
        mouse = self.__mouse()
        self.t_batal.gambar(c, self.huruf, mouse)
        self.t_ya_keluar.gambar(c, self.huruf, mouse)


def siapkan_layar():
    """Dipanggil sebelum pygame.init():
    - aplikasi ditandai DPI-aware agar Windows tidak meregangkan (memburamkan)
      jendela di laptop dengan skala tampilan 125%/150%;
    - penskalaan GPU memakai filter halus (linear)."""
    os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "1")
    if sys.platform == "win32":
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main():
    siapkan_layar()
    App().run()
    sys.exit()


if __name__ == "__main__":
    main()
