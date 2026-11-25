"""Lapisan gambar yang tidak bergantung resolusi.

Semua kode game memakai koordinat LOGIS 1280x720. Kanvas menggambar di
resolusi FISIK layar (misalnya 1920x1080 = skala 1,5), sehingga huruf, garis,
dan lingkaran digambar langsung di ukuran aslinya dan tetap tajam saat layar
penuh, tidak diperbesar dari gambar kecil.

Pemakaian di kode game:
    import kanvas as gfx
    gfx.rect(kanvas, warna, (x, y, w, h), border_radius=8)   # seperti pygame.draw.rect
    lapis = gfx.Kanvas((200, 100), pygame.SRCALPHA)            # seperti pygame.Surface
    font = gfx.HurufSkala("file.ttf", 20)                      # seperti pygame.font.Font
"""
import math

import pygame

_SKALA = [1.0]


def atur_skala(s):
    """Dipanggil sekali saat jendela dibuat, sebelum font dan gambar dibuat."""
    _SKALA[0] = float(s)


def skala():
    return _SKALA[0]


def _n(v):
    return v * _SKALA[0]


def _titik(p):
    return (p[0] * _SKALA[0], p[1] * _SKALA[0])


def _kotak(r):
    """Rect logis -> Rect fisik; tepi dibulatkan agar petak bersebelahan tidak bercelah."""
    x, y, w, h = r if not isinstance(r, pygame.Rect) else (r.x, r.y, r.w, r.h)
    s = _SKALA[0]
    x0, y0 = round(x * s), round(y * s)
    return pygame.Rect(x0, y0, round((x + w) * s) - x0, round((y + h) * s) - y0)


def _tebal(w):
    return 0 if w <= 0 else max(1, round(w * _SKALA[0]))


class Kanvas:
    """Permukaan gambar dengan satuan logis; isinya pygame.Surface fisik (atribut p)."""

    def __init__(self, ukuran=None, flags=0, permukaan=None):
        if permukaan is not None:
            self.p = permukaan
        else:
            w, h = ukuran
            self.p = pygame.Surface((max(1, math.ceil(w * _SKALA[0])), max(1, math.ceil(h * _SKALA[0]))), flags)

    # ---------------------------------------------------- ukuran (logis)
    def get_width(self):
        return self.p.get_width() / _SKALA[0]

    def get_height(self):
        return self.p.get_height() / _SKALA[0]

    def get_size(self):
        return self.get_width(), self.get_height()

    def get_rect(self, **posisi):
        r = pygame.Rect(0, 0, round(self.get_width()), round(self.get_height()))
        for k, v in posisi.items():
            setattr(r, k, v)
        return r

    # ---------------------------------------------------- isi
    def fill(self, warna, rect=None):
        if rect is None:
            self.p.fill(warna)
        else:
            self.p.fill(warna, _kotak(rect))

    def set_alpha(self, a):
        self.p.set_alpha(a)

    def blit(self, sumber, tujuan, area=None):
        """Tempel Kanvas lain (atau Surface fisik) di posisi logis."""
        src = sumber.p if isinstance(sumber, Kanvas) else sumber
        if isinstance(tujuan, pygame.Rect):
            tujuan = tujuan.topleft
        pos = (round(tujuan[0] * _SKALA[0]), round(tujuan[1] * _SKALA[0]))
        self.p.blit(src, pos, _kotak(area) if area is not None else None)

    def subsurface(self, rect):
        return Kanvas(permukaan=self.p.subsurface(_kotak(rect)))

    def copy(self):
        return Kanvas(permukaan=self.p.copy())


class HurufSkala:
    """Font yang dibuat di ukuran fisik (ukuran x skala); ukurannya dilaporkan logis."""

    def __init__(self, path, ukuran):
        try:
            self.f = pygame.font.Font(path, max(6, round(ukuran * _SKALA[0])))
        except Exception:
            # File font hilang: tetap jalan dengan font bawaan pygame.
            self.f = pygame.font.Font(None, max(8, round(ukuran * 1.3 * _SKALA[0])))

    def render(self, teks, aa, warna):
        return Kanvas(permukaan=self.f.render(str(teks), aa, warna))

    def size(self, teks):
        w, h = self.f.size(str(teks))
        return w / _SKALA[0], h / _SKALA[0]

    def get_linesize(self):
        return self.f.get_linesize() / _SKALA[0]

    def get_ascent(self):
        return self.f.get_ascent() / _SKALA[0]

    def get_descent(self):
        return self.f.get_descent() / _SKALA[0]


# -------------------------------------------------------- fungsi gambar (seperti pygame.draw)
def _p(surface):
    return surface.p if isinstance(surface, Kanvas) else surface


def rect(surface, warna, r, width=0, border_radius=0, **sudut):
    sudut = {k: round(_n(v)) for k, v in sudut.items()}
    return pygame.draw.rect(_p(surface), warna, _kotak(r), _tebal(width), border_radius=round(_n(border_radius)), **sudut)


def line(surface, warna, a, b, width=1):
    return pygame.draw.line(_p(surface), warna, _titik(a), _titik(b), _tebal(width))


def lines(surface, warna, tertutup, titik, width=1):
    return pygame.draw.lines(_p(surface), warna, tertutup, [_titik(t) for t in titik], _tebal(width))


def circle(surface, warna, pusat, jari, width=0):
    return pygame.draw.circle(_p(surface), warna, _titik(pusat), max(0.5, _n(jari)), _tebal(width))


def polygon(surface, warna, titik, width=0):
    return pygame.draw.polygon(_p(surface), warna, [_titik(t) for t in titik], _tebal(width))


def ellipse(surface, warna, r, width=0):
    return pygame.draw.ellipse(_p(surface), warna, _kotak(r), _tebal(width))


def arc(surface, warna, r, mulai, akhir, width=1):
    return pygame.draw.arc(_p(surface), warna, _kotak(r), mulai, akhir, _tebal(width))


# -------------------------------------------------------- transformasi
def smoothscale(kanvas, ukuran_logis):
    w, h = ukuran_logis
    return Kanvas(permukaan=pygame.transform.smoothscale(_p(kanvas), (max(1, round(_n(w))), max(1, round(_n(h))))))


def rotozoom(kanvas, sudut, zoom):
    return Kanvas(permukaan=pygame.transform.rotozoom(_p(kanvas), sudut, zoom))
