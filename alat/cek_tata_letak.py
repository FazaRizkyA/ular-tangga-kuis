"""Pemeriksa tata letak tangga & ular agar mudah dibaca di papan.

Dipakai oleh alat/uji_logika.py. Koordinat dalam satuan petak (titik tengah).
Aturan:
- dua tangga tidak boleh berdekatan (jarak garis < 1,5 petak), dan
- dua tangga yang sejajar tidak boleh segaris (kelihatan seperti satu tangga panjang),
- tangga tidak boleh disilang atau ditindih ular (jarak ke garis ular < 0,85 petak).
"""
import math

KOLOM = 8


def titik(n):
    """Nomor petak -> (kolom, baris) dengan penomoran zig-zag."""
    baris = (n - 1) // KOLOM
    kolom = (n - 1) % KOLOM
    if baris % 2 == 1:
        kolom = KOLOM - 1 - kolom
    return kolom, baris


def _jarak_titik_garis(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def _bersilang(a, b, c, d):
    def sisi(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return sisi(a, b, c) * sisi(a, b, d) < 0 and sisi(c, d, a) * sisi(c, d, b) < 0


def jarak_ruas(a, b, c, d):
    if _bersilang(a, b, c, d):
        return 0.0
    return min(_jarak_titik_garis(a, c, d), _jarak_titik_garis(b, c, d),
               _jarak_titik_garis(c, a, b), _jarak_titik_garis(d, a, b))


def _sudut(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


def sejajar(a, b, c, d, batas=25):
    s = abs(math.degrees(_sudut(a, b) - _sudut(c, d))) % 180
    return min(s, 180 - s) < batas


def _jarak_ke_garis_tak_hingga(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return abs((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / math.hypot(dx, dy)


def masalah(tangga, ular, jarak_ular=0.85):
    """Daftar masalah tata letak (kosong = rapi)."""
    hasil = []
    ruas_t = [(b, a, titik(b), titik(a)) for b, a in tangga.items()]
    ruas_u = [(k, e, titik(k), titik(e)) for k, e in ular.items()]
    for i, (b1, a1, p, q) in enumerate(ruas_t):
        for b2, a2, r, s in ruas_t[i + 1:]:
            if jarak_ruas(p, q, r, s) < 1.5:
                hasil.append(f"tangga {b1}-{a1} terlalu dekat tangga {b2}-{a2}")
            elif sejajar(p, q, r, s) and max(_jarak_ke_garis_tak_hingga(r, p, q),
                                             _jarak_ke_garis_tak_hingga(s, p, q)) < 0.6:
                hasil.append(f"tangga {b1}-{a1} segaris dengan tangga {b2}-{a2}")
        for k, e, r, s in ruas_u:
            if jarak_ruas(p, q, r, s) < jarak_ular:
                hasil.append(f"tangga {b1}-{a1} tertindih ular {k}-{e}")
    return hasil
