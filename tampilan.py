"""Komponen tampilan bertema pasar malam: papan cat kayu, bohlam, karcis,
tombol, kolom teks, dadu, dan bidak. Semua digambar dengan pygame.draw,
tanpa gambar dari internet."""
import math
import os

import pygame

import kanvas as gfx

from config import (
    resource_path, FOLDER_FONT, IS_ANDROID, LEBAR, TINGGI,
    TERPAL, TERPAL_GELAP, TERPAL_TERANG, TERPAL_JAHIT, KREM, KREM_GELAP,
    TINTA, TINTA_LEMBUT, BOHLAM_NYALA, BOHLAM_INTI, BOHLAM_MATI, KUNING_CAT,
)


# ------------------------------------------------------------------ warna
def campur(a, b, t):
    """Interpolasi linear dua warna RGB."""
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def terang(warna, f):
    return campur(warna, (255, 255, 255), f)


def gelap(warna, f):
    return campur(warna, (0, 0, 0), f)


# ------------------------------------------------------------------ font
def _muat_font(nama_file, ukuran):
    # Font dibuat di ukuran fisik layar (ukuran x skala) agar huruf tajam;
    # bila file hilang, HurufSkala memakai font bawaan pygame.
    return gfx.HurufSkala(resource_path(os.path.join(FOLDER_FONT, nama_file)), ukuran)


class Huruf:
    """Kumpulan font: Bungee untuk tulisan papan stan, Atkinson Hyperlegible
    untuk soal dan data agar mudah dibaca."""

    def __init__(self):
        b, r, t = "Bungee-Regular.ttf", "AtkinsonHyperlegible-Regular.ttf", "AtkinsonHyperlegible-Bold.ttf"
        self.raksasa = _muat_font(b, 68)
        self.judul = _muat_font(b, 40)
        self.sub = _muat_font(b, 28)
        self.tombol = _muat_font(b, 22)
        self.label = _muat_font(b, 18)
        self.angka = _muat_font(b, 26)
        self.angka_kecil = _muat_font(b, 18)
        self.teks = _muat_font(r, 20)
        self.teks_tebal = _muat_font(t, 20)
        self.soal = _muat_font(t, 24)
        self.kecil = _muat_font(r, 18)
        self.kecil_tebal = _muat_font(t, 18)


# ------------------------------------------------------------------ teks
_cache_teks = {}


def _render_teks(font, teks, warna):
    """Teks yang sama tidak dirender ulang tiap frame (hemat waktu di resolusi tinggi)."""
    kunci = (id(font), teks, tuple(warna))
    gambar = _cache_teks.get(kunci)
    if gambar is None:
        if len(_cache_teks) > 1500:
            _cache_teks.clear()
        gambar = font.render(teks, True, warna)
        _cache_teks[kunci] = gambar
    return gambar


def tulis(surface, teks, font, warna, pos, anchor="topleft"):
    """Menulis teks di posisi logis; perataan dihitung di piksel fisik agar presisi."""
    gambar = _render_teks(font, str(teks), warna)
    s = gfx.skala()
    fisik = gambar.p.get_rect(**{anchor: (round(pos[0] * s), round(pos[1] * s))})
    (surface.p if isinstance(surface, gfx.Kanvas) else surface).blit(gambar.p, fisik)
    return pygame.Rect(round(fisik.x / s), round(fisik.y / s), round(fisik.w / s), round(fisik.h / s))


def bungkus_teks(teks, font, lebar):
    """Memecah teks menjadi beberapa baris yang muat di lebar tertentu."""
    baris, sekarang = [], ""
    for kata in str(teks).split():
        coba = f"{sekarang} {kata}".strip()
        if font.size(coba)[0] <= lebar or not sekarang:
            sekarang = coba
        else:
            baris.append(sekarang)
            sekarang = kata
    if sekarang:
        baris.append(sekarang)
    return baris


# ------------------------------------------------------------------ bayangan & papan cat
_cache_bayangan = {}


def bayangan(surface, rect, radius=12, offset=(0, 6), blur=10, alpha=90):
    """Bayangan lembut (berbayang kabur, bukan blok keras)."""
    kunci = (rect.w, rect.h, radius, blur, alpha)
    gambar = _cache_bayangan.get(kunci)
    if gambar is None:
        pad = blur * 2
        w, h = rect.w + pad * 2, rect.h + pad * 2
        s = gfx.Kanvas((w, h), pygame.SRCALPHA)
        gfx.rect(s, (6, 14, 36, alpha), (pad, pad, rect.w, rect.h), border_radius=radius)
        kecil = gfx.smoothscale(s, (max(1, w // 5), max(1, h // 5)))
        gambar = gfx.smoothscale(kecil, (w, h))
        _cache_bayangan[kunci] = gambar
    pad = blur * 2
    surface.blit(gambar, (rect.x - pad + offset[0], rect.y - pad + offset[1]))


def papan_cat(surface, rect, warna, radius=12, tepi=None, bayang=True, tebal_tepi=3):
    """Papan triplek dicat: bayangan lembut, isi warna, kilap tipis di atas,
    dan garis tepi lebih gelap seperti cat tangan."""
    if bayang:
        bayangan(surface, rect, radius)
    gfx.rect(surface, warna, rect, border_radius=radius)
    kilap = pygame.Rect(rect.x + radius // 2, rect.y + 3, rect.w - radius, 3)
    gfx.rect(surface, terang(warna, 0.22), kilap, border_radius=2)
    gfx.rect(surface, tepi or gelap(warna, 0.35), rect, tebal_tepi, border_radius=radius)


# ------------------------------------------------------------------ latar terpal
_cache_latar = {}


def latar_terpal(surface):
    """Latar tenda terpal biru dengan panel dan jahitan putus-putus."""
    latar = _cache_latar.get("terpal")
    if latar is None:
        latar = gfx.Kanvas((LEBAR, TINGGI))
        latar.fill(TERPAL)
        lebar_panel = 214
        for i, x in enumerate(range(0, LEBAR, lebar_panel)):
            if i % 2:
                gfx.rect(latar, TERPAL_TERANG, (x, 0, lebar_panel, TINGGI))
            # lipatan lembut di tengah panel
            for d in range(18):
                a = campur(TERPAL_TERANG if i % 2 else TERPAL, TERPAL_GELAP, 0.25 * (1 - d / 18))
                gfx.line(latar, a, (x + lebar_panel // 2 + d, 0), (x + lebar_panel // 2 + d, TINGGI))
            for y in range(4, TINGGI, 14):
                gfx.line(latar, TERPAL_JAHIT, (x + 3, y), (x + 3, y + 7), 2)
        # tepi bawah lebih gelap (bayangan tanah)
        for d in range(60):
            gfx.line(latar, campur(TERPAL, TERPAL_GELAP, d / 60), (0, TINGGI - 60 + d), (LEBAR, TINGGI - 60 + d))
        _cache_latar["terpal"] = latar
    surface.blit(latar, (0, 0))


def redupkan(surface, alpha=150):
    gelapan = gfx.Kanvas((LEBAR, TINGGI), pygame.SRCALPHA)
    gelapan.fill((6, 14, 36, alpha))
    surface.blit(gelapan, (0, 0))


# ------------------------------------------------------------------ bohlam
_cache_cahaya = {}


def bohlam(surface, pos, nyala, r=6):
    """Satu bohlam; nyala 0 (mati) sampai 1 (menyala penuh)."""
    x, y = int(pos[0]), int(pos[1])
    if nyala > 0.05:
        tingkat = round(nyala * 8)
        kunci = (r, tingkat)
        cahaya = _cache_cahaya.get(kunci)
        if cahaya is None:
            rr = r * 4
            cahaya = gfx.Kanvas((rr * 2, rr * 2), pygame.SRCALPHA)
            for k in range(rr, 0, -2):
                a = int(70 * (tingkat / 8) * (1 - k / rr) ** 1.6)
                gfx.circle(cahaya, (*BOHLAM_NYALA, a), (rr, rr), k)
            _cache_cahaya[kunci] = cahaya
        surface.blit(cahaya, (x - r * 4, y - r * 4))
    # fiting lampu, lalu kaca: gelap kecokelatan saat mati, kuning hangat saat menyala
    gfx.rect(surface, (30, 30, 36), (x - r // 2, y - r - 3, r, 4))
    gfx.circle(surface, (24, 20, 16), (x, y), r + 1)
    gfx.circle(surface, campur(BOHLAM_MATI, BOHLAM_NYALA, nyala), (x, y), r)
    if nyala > 0.3:
        gfx.circle(surface, BOHLAM_INTI, (x - r // 3, y - r // 3), max(1, r // 2))
    else:
        gfx.circle(surface, terang(BOHLAM_MATI, 0.35), (x - r // 3, y - r // 3), max(1, r // 3))


def tali_bohlam(surface, x0, x1, y, kendur, jumlah, waktu, pola="kejar", r=6):
    """Untaian bohlam yang melengkung di antara dua tiang."""
    titik = []
    for i in range(jumlah):
        t = i / (jumlah - 1)
        titik.append((x0 + (x1 - x0) * t, y + kendur * 4 * t * (1 - t)))
    gfx.lines(surface, (14, 22, 40), False, titik, 2)
    for i, p in enumerate(titik):
        if pola == "semua":
            n = 0.85 + 0.15 * math.sin(waktu * 9 + i * 1.7)
        elif pola == "redup":
            n = 0.25
        else:
            n = 0.3 + 0.7 * max(0.0, math.sin(waktu * 3 - i * 0.55)) ** 2
        gfx.line(surface, (14, 22, 40), p, (p[0], p[1] + r), 2)
        bohlam(surface, (p[0], p[1] + r + 4), n, r)


# ------------------------------------------------------------------ karcis
def karcis(surface, rect, warna, warna_sobek, lebar_potongan=56):
    """Karcis kertas: potongan nomor seri di kiri, garis lubang sobekan."""
    bayangan(surface, rect, 6, offset=(0, 3), blur=5, alpha=70)
    gfx.rect(surface, warna, rect, border_radius=6)
    potongan = pygame.Rect(rect.x, rect.y, lebar_potongan, rect.h)
    gfx.rect(surface, gelap(warna, 0.08), potongan, border_top_left_radius=6, border_bottom_left_radius=6)
    x = rect.x + lebar_potongan
    for y in range(rect.y + 5, rect.bottom - 3, 7):
        gfx.circle(surface, warna_sobek, (x, y), 2)
    gfx.rect(surface, gelap(warna, 0.3), rect, 1, border_radius=6)


# ------------------------------------------------------------------ tombol
class Tombol:
    """Tombol berupa papan harga stan yang dicat."""

    def __init__(self, rect, label, warna=KUNING_CAT, warna_teks=TINTA, font="tombol"):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.warna = warna
        self.warna_teks = warna_teks
        self.font = font
        self.aktif = True

    def kena(self, pos):
        return self.aktif and self.rect.collidepoint(pos)

    def gambar(self, surface, huruf, mouse, warna=None, warna_teks=None, label=None):
        warna = warna or self.warna
        warna_teks = warna_teks or self.warna_teks
        hover = self.aktif and not IS_ANDROID and self.rect.collidepoint(mouse)
        if not self.aktif:
            # Nonaktif tetap terbaca (kontras > 4.5:1): teks krem di atas terpal gelap.
            warna, warna_teks = (40, 60, 104), (222, 210, 184)
        elif hover:
            warna = terang(warna, 0.14)
        rect = self.rect.move(0, -2 if hover else 0)
        papan_cat(surface, rect, warna, radius=10)
        font = getattr(huruf, self.font)
        teks = label or self.label
        baris = bungkus_teks(teks, font, rect.w - 20)
        tinggi = font.get_linesize()
        y = rect.centery - (len(baris) * tinggi) // 2 + tinggi // 2
        for b in baris:
            tulis(surface, b, font, warna_teks, (rect.centerx, y), "center")
            y += tinggi


# ------------------------------------------------------------------ kolom teks
class KolomTeks:
    """Kolom isian nama yang digambar sendiri (pygame tidak punya widget)."""

    MAKS_KETIK = 20  # boleh lebih dari 12 agar pesan error bisa muncul

    def __init__(self, rect, teks=""):
        self.rect = pygame.Rect(rect)
        self.teks = teks
        self.fokus = False
        self.error = ""
        self.bisa_diubah = True

    def handle(self, event):
        if not (self.fokus and self.bisa_diubah):
            return False
        if event.type == pygame.TEXTINPUT:
            if len(self.teks) < self.MAKS_KETIK:
                self.teks += event.text
            self.error = ""
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.teks = self.teks[:-1]
            self.error = ""
            return True
        return False

    def gambar(self, surface, huruf, waktu):
        warna = KREM if self.bisa_diubah else KREM_GELAP
        gfx.rect(surface, warna, self.rect, border_radius=8)
        if self.error:
            tepi = (204, 36, 52)
        elif self.fokus:
            tepi = TINTA
        else:
            tepi = (150, 140, 120)
        gfx.rect(surface, tepi, self.rect, 3 if (self.fokus or self.error) else 2, border_radius=8)
        r = tulis(surface, self.teks, huruf.teks_tebal, TINTA, (self.rect.x + 14, self.rect.centery), "midleft")
        if self.fokus and self.bisa_diubah and int(waktu * 2) % 2 == 0:
            x = r.right + 3
            gfx.line(surface, TINTA, (x, self.rect.y + 9), (x, self.rect.bottom - 9), 2)


# ------------------------------------------------------------------ dadu & bidak
_TITIK_DADU = {
    1: [(0, 0)],
    2: [(-1, -1), (1, 1)],
    3: [(-1, -1), (0, 0), (1, 1)],
    4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
    6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
}


def gambar_dadu(surface, pusat, ukuran, nilai, sudut=0.0, warna=KREM):
    s = gfx.Kanvas((ukuran, ukuran), pygame.SRCALPHA)
    gfx.rect(s, warna, (0, 0, ukuran, ukuran), border_radius=ukuran // 6)
    gfx.rect(s, TINTA, (0, 0, ukuran, ukuran), 3, border_radius=ukuran // 6)
    jarak = ukuran * 0.27
    for dx, dy in _TITIK_DADU[nilai]:
        warna_titik = (204, 36, 52) if nilai == 1 else TINTA
        gfx.circle(s, warna_titik, (int(ukuran / 2 + dx * jarak), int(ukuran / 2 + dy * jarak)), max(3, ukuran // 11))
    if sudut:
        s = gfx.rotozoom(s, sudut, 1.0)
    rect = s.get_rect(center=(int(pusat[0]), int(pusat[1])))
    bayangan(surface, pygame.Rect(rect.x + 6, rect.y + 6, rect.w - 12, rect.h - 12), 8, offset=(0, 5), blur=6, alpha=80)
    surface.blit(s, rect)


def gambar_bidak(surface, pos, warna, nomor, font, angkat=0.0, r=19):
    """Bidak pemain: bayangan di lantai, badan berwarna, cincin krem,
    nomor pemain di tengah agar tidak hanya dibedakan warna."""
    x, y = pos
    lebar_bayang = int(r * 2 * (1 - angkat / 80))
    bayang = gfx.Kanvas((lebar_bayang, 10), pygame.SRCALPHA)
    gfx.ellipse(bayang, (0, 0, 0, 70), bayang.get_rect())
    surface.blit(bayang, (x - lebar_bayang // 2, y + r - 6))
    y -= angkat
    gfx.circle(surface, TINTA, (int(x), int(y)), r + 2)
    gfx.circle(surface, KREM, (int(x), int(y)), r)
    gfx.circle(surface, warna, (int(x), int(y)), r - 4)
    gfx.circle(surface, terang(warna, 0.35), (int(x - r * 0.35), int(y - r * 0.35)), r // 4)
    warna_angka = TINTA if sum(warna) > 420 else KREM
    tulis(surface, nomor, font, warna_angka, (int(x), int(y) + 1), "center")


def gambar_ular(surface, kepala, ekor, tebal=13, warna=None):
    """Ular dicat: badan meruncing dari kepala ke ekor, belang kuning bergaris,
    kepala dengan mata dan lidah bercabang. Dipakai di papan, menu, dan panduan."""
    from config import ULAR_BADAN, ULAR_TUA, ULAR_GARIS, MERAH_CAT
    badan = warna or ULAR_BADAN
    x1, y1 = kepala
    x2, y2 = ekor
    dx, dy = x2 - x1, y2 - y1
    panjang = math.hypot(dx, dy)
    px, py = -dy / panjang, dx / panjang
    gelombang = max(1.5, panjang / 120)
    jumlah = max(12, int(panjang / 5))
    titik = []
    for i in range(jumlah + 1):
        t = i / jumlah
        amp = tebal * 1.55 * math.sin(math.pi * min(1.0, t * 1.25))
        o = amp * math.sin(t * gelombang * 2 * math.pi)
        titik.append((x1 + dx * t + px * o, y1 + dy * t + py * o, t))
    for x, y, t in titik:
        gfx.circle(surface, ULAR_TUA, (int(x), int(y)), int(tebal * (1 - 0.62 * t)) + 3)
    for x, y, t in titik:
        gfx.circle(surface, badan, (int(x), int(y)), int(tebal * (1 - 0.62 * t)))
    # belang digambar setelah seluruh badan agar tidak tertutup ruas berikutnya
    for i, (x, y, t) in enumerate(titik):
        r = int(tebal * (1 - 0.62 * t))
        if i % 5 == 2 and 0.05 < t < 0.9:
            rb = max(3, int(r * 0.6))
            gfx.circle(surface, ULAR_GARIS, (int(x), int(y)), rb)
            gfx.circle(surface, ULAR_TUA, (int(x), int(y)), rb, 1)
    hx, hy, _ = titik[0]
    nx, ny, _ = titik[min(3, len(titik) - 1)]
    arah = math.atan2(hy - ny, hx - nx)
    k = tebal / 13
    gfx.ellipse(surface, ULAR_TUA, (hx - 19 * k, hy - 16 * k, 38 * k, 32 * k))
    gfx.ellipse(surface, badan, (hx - 16 * k, hy - 13 * k, 32 * k, 26 * k))
    for s in (-1, 1):
        ex = hx + math.cos(arah + s * 0.7) * 8 * k
        ey = hy + math.sin(arah + s * 0.7) * 8 * k
        gfx.circle(surface, KREM, (int(ex), int(ey)), int(5 * k))
        gfx.circle(surface, TINTA, (int(ex + math.cos(arah) * 1.5), int(ey + math.sin(arah) * 1.5)), max(2, int(2 * k)))
    lx, ly = hx + math.cos(arah) * 16 * k, hy + math.sin(arah) * 16 * k
    ujung = (lx + math.cos(arah) * 10 * k, ly + math.sin(arah) * 10 * k)
    gfx.line(surface, MERAH_CAT, (lx, ly), ujung, 3)
    for s in (-1, 1):
        gfx.line(surface, MERAH_CAT, ujung, (ujung[0] + math.cos(arah + s * 0.6) * 5 * k, ujung[1] + math.sin(arah + s * 0.6) * 5 * k), 2)


def segitiga(surface, warna, pusat, ukuran, ke_atas=True):
    x, y = pusat
    if ke_atas:
        titik = [(x, y - ukuran), (x - ukuran, y + ukuran * 0.7), (x + ukuran, y + ukuran * 0.7)]
    else:
        titik = [(x, y + ukuran), (x - ukuran, y - ukuran * 0.7), (x + ukuran, y - ukuran * 0.7)]
    gfx.polygon(surface, warna, titik)
