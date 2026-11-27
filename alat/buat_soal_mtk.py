"""Pembuat 300 soal Matematika (100 per tingkat kesulitan) untuk soal.json.

Materi (sesuai arahan guru): bunga tunggal & majemuk, fungsi komposisi,
fungsi invers, serta mean/median/modus. Tiap tingkat: 25 soal per materi.
Semua kunci jawaban DIHITUNG oleh program, pengecoh dibuat dari kesalahan
yang umum dilakukan siswa. Rumus memakai markup penata rumus:
\\frac{a}{b}, x^{2}, (f ∘ g)(x).

Dipakai oleh alat/buat_soal.py (tidak dijalankan langsung oleh game).
"""
import random
from fractions import Fraction

MATERI = ["Bunga tunggal & majemuk", "Fungsi komposisi", "Fungsi invers", "Mean, median, modus"]
TINGKAT = ["Mudah", "Sedang", "Sulit"]
PER_MATERI = 25

NAMA = ["Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hana", "Irfan", "Joko",
        "Kirana", "Lukman", "Maya", "Nanda", "Oki", "Putri", "Rizky", "Sinta", "Tono", "Wulan"]


# ------------------------------------------------------------------ format angka
def ribuan(n):
    return f"{int(n):,}".replace(",", ".")


def rp(n):
    return "Rp" + ribuan(n)


def desimal(x):
    """Angka Indonesia: koma desimal, tanpa nol berlebih."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def persen(p):
    return f"{desimal(p)}%"


# ------------------------------------------------------------------ format aljabar
def suku(k, var, pertama):
    """Satu suku k*var dengan tanda yang benar."""
    if k == 0:
        return ""
    tanda = "-" if k < 0 else "+"
    nilai = abs(k)
    isi = (var if nilai == 1 else f"{nilai}{var}") if var else str(nilai)
    if pertama:
        return ("-" if k < 0 else "") + isi
    return f" {tanda} {isi}"


def poli(*koef):
    """poli(a, b, c) -> 'ax^{2} + bx + c' (koefisien dari pangkat tertinggi)."""
    n = len(koef) - 1
    teks = ""
    for i, k in enumerate(koef):
        p = n - i
        var = "x^{%d}" % p if p > 1 else ("x" if p == 1 else "")
        bagian = suku(k, var, teks == "")
        teks += bagian
    return teks or "0"


def pecahan(atas, bawah):
    return "\\frac{%s}{%s}" % (atas, bawah)


# ------------------------------------------------------------------ pembantu soal
class Wadah:
    """Mengumpulkan soal unik per (materi, tingkat)."""

    def __init__(self):
        self.isi = {(m, t): [] for m in MATERI for t in TINGKAT}
        self.teks = set()

    def tambah(self, materi, tingkat, pertanyaan, benar, pengecoh):
        if len(self.isi[(materi, tingkat)]) >= PER_MATERI or pertanyaan in self.teks:
            return False
        pilihan = [benar]
        for p in pengecoh:
            if p not in pilihan:
                pilihan.append(p)
        if len(pilihan) < 4:
            return False
        self.teks.add(pertanyaan)
        self.isi[(materi, tingkat)].append({
            "kategori": "Matematika", "materi": materi, "tingkat": tingkat,
            "pertanyaan": pertanyaan, "benar": benar, "salah": pilihan[1:4]})
        return True

    def penuh(self, materi, tingkat):
        return len(self.isi[(materi, tingkat)]) >= PER_MATERI


def isi_sampai_penuh(wadah, materi, tingkat, pembuat, rng):
    percobaan = 0
    while not wadah.penuh(materi, tingkat):
        percobaan += 1
        if percobaan > 20000:
            raise RuntimeError(f"tidak cukup variasi: {materi} {tingkat}")
        fungsi = rng.choice(pembuat)
        hasil = fungsi(rng)
        if hasil:
            wadah.tambah(materi, tingkat, *hasil)


# ================================================================== BUNGA
def bunga_mudah_1(r):
    m = r.choice([500_000, 1_000_000, 1_500_000, 2_000_000, 2_500_000, 3_000_000, 4_000_000, 5_000_000])
    p = r.choice([4, 5, 6, 8, 10, 12])
    nama = r.choice(NAMA)
    b = m * p // 100
    return (f"{nama} menabung {rp(m)} dengan bunga tunggal {persen(p)} per tahun. Besar bunga setelah 1 tahun adalah ...",
            rp(b), [rp(m + b), rp(b * 2), rp(m * p // 1000)])


def bunga_mudah_2(r):
    m = r.choice([1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000, 6_000_000])
    p = r.choice([5, 6, 8, 10])
    n = r.choice([2, 3, 4])
    nama = r.choice(NAMA)
    b = m * p * n // 100
    return (f"{nama} menyimpan {rp(m)} di bank dengan bunga tunggal {persen(p)} per tahun. Jumlah tabungan setelah {n} tahun adalah ...",
            rp(m + b), [rp(b), rp(m + m * p // 100), rp(m + m * p * (n + 1) // 100)])


def bunga_mudah_3(r):
    m = r.choice([1_200_000, 2_400_000, 3_600_000, 4_800_000, 6_000_000])
    p = r.choice([5, 10, 15])
    bulan = r.choice([2, 4, 6, 8, 10])
    b = m * p * bulan // 1200
    return (f"Modal {rp(m)} dibungakan dengan bunga tunggal {persen(p)} per tahun. Besar bunga selama {bulan} bulan adalah ...",
            rp(b), [rp(m * p // 100), rp(m * p * bulan // 100), rp(m + b)])


def bunga_mudah_4(r):
    m = r.choice([1_000_000, 2_000_000, 5_000_000, 10_000_000])
    b = r.choice([50_000, 80_000, 100_000, 120_000, 150_000])
    p = Fraction(b * 100, m)
    if p.denominator != 1 or p > 20:
        return None
    return (f"Tabungan {rp(m)} mendapat bunga {rp(b)} dalam 1 tahun (bunga tunggal). Persentase bunga per tahun adalah ...",
            persen(p), [persen(p * 2), persen(p + 1), persen(p * 10)])


def bunga_sedang_1(r):
    m = r.choice([1_000_000, 2_000_000, 4_000_000, 5_000_000, 8_000_000, 10_000_000])
    p = r.choice([5, 10, 20])
    akhir = m * (100 + p) ** 2 // 10_000
    tunggal = m + m * p * 2 // 100
    return (f"Modal {rp(m)} disimpan dengan bunga majemuk {persen(p)} per tahun. Besar modal setelah 2 tahun adalah ...",
            rp(akhir), [rp(tunggal), rp(m * (100 + p) // 100), rp(akhir - m)])


def bunga_sedang_2(r):
    m = r.choice([1_000_000, 2_000_000, 2_500_000, 4_000_000, 5_000_000])
    p = r.choice([4, 5, 6, 8, 10, 12])
    n = r.choice([2, 3, 4, 5])
    akhir = m + m * p * n // 100
    return (f"Modal {rp(m)} menjadi {rp(akhir)} setelah {n} tahun dengan bunga tunggal. Persentase bunga per tahun adalah ...",
            persen(p), [persen(p * n), persen(p + 2), persen(Fraction(p, 2))])


def bunga_sedang_3(r):
    m = r.choice([1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000, 6_000_000])
    p = r.choice([5, 6, 8, 10])
    n = r.choice([2, 3, 4])
    akhir = m + m * p * n // 100
    return (f"Setelah {n} tahun, tabungan dengan bunga tunggal {persen(p)} per tahun menjadi {rp(akhir)}. Modal awalnya adalah ...",
            rp(m), [rp(akhir - m * p // 100), rp(m * p * n // 100), rp(m + m * p // 100)])


def bunga_sedang_4(r):
    m = r.choice([1_200_000, 2_400_000, 3_000_000, 6_000_000])
    p = r.choice([6, 8, 10, 12])
    b = r.choice([60_000, 90_000, 120_000, 180_000, 240_000])
    bulan = Fraction(b * 1200, m * p)
    if bulan.denominator != 1 or not 1 <= bulan <= 24:
        return None
    bulan = int(bulan)
    return (f"Modal {rp(m)} dengan bunga tunggal {persen(p)} per tahun menghasilkan bunga {rp(b)}. Lama menabung adalah ...",
            f"{bulan} bulan", [f"{bulan + 2} bulan", f"{bulan * 2} bulan", f"{max(1, bulan - 1)} tahun"])


def bunga_sedang_5(r):
    p = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = r.choice([2, 3, 4, 5, 6])
    return (f"Modal M dibungakan dengan bunga majemuk {persen(p)} per tahun selama {n} tahun. Rumus modal akhirnya adalah ...",
            "M(1 + %s)^{%d}" % (desimal(Fraction(p, 100)), n),
            ["M(1 + %s)" % desimal(Fraction(p * n, 100)),
             "M(1 + %s)^{%d}" % (desimal(Fraction(p, 100)), n - 1),
             "M(%s)^{%d}" % (desimal(Fraction(p, 100)), n)])


def bunga_sulit_1(r):
    m = r.choice([1_000_000, 2_000_000, 3_000_000, 5_000_000, 10_000_000])
    akhir = m * 1331 // 1000
    return (f"Modal {rp(m)} disimpan dengan bunga majemuk 10% per tahun. Besar modal setelah 3 tahun adalah ...",
            rp(akhir), [rp(m * 13 // 10), rp(m * 121 // 100), rp(akhir - m)])


def bunga_sulit_2(r):
    m = r.choice([2_000_000, 4_000_000, 5_000_000, 8_000_000, 10_000_000])
    p = r.choice([10, 20])
    i = p // 2
    akhir = m * (100 + i) ** 2 // 10_000
    return (f"Modal {rp(m)} dibungakan dengan bunga majemuk {persen(p)} per tahun yang dihitung tiap semester. Modal setelah 1 tahun adalah ...",
            rp(akhir), [rp(m * (100 + p) // 100), rp(m * (100 + p) ** 2 // 10_000), rp(m * (100 + i) // 100)])


def bunga_sulit_3(r):
    m = r.choice([1_000_000, 2_000_000, 4_000_000, 5_000_000, 10_000_000])
    p = r.choice([5, 10, 20])
    n = r.choice([2, 3])
    akhir = m * (100 + p) ** n // 100 ** n
    if m * (100 + p) ** n % 100 ** n:
        return None
    return (f"Modal {rp(m)} disimpan dengan bunga majemuk {persen(p)} per tahun. Besar bunganya saja setelah {n} tahun adalah ...",
            rp(akhir - m), [rp(akhir), rp(m * p * n // 100), rp(m * p // 100)])


def bunga_sulit_4(r):
    m = r.choice([1_000_000, 2_000_000, 4_000_000, 5_000_000, 8_000_000, 10_000_000])
    p = r.choice([5, 10, 20])
    selisih = m * p * p // 10_000
    return (f"Modal {rp(m)} disimpan 2 tahun dengan bunga {persen(p)} per tahun. Selisih hasil bunga majemuk dan bunga tunggal adalah ...",
            rp(selisih), [rp(m * p // 100), rp(selisih * 2), rp(0)])


def bunga_sulit_5(r):
    akhir_m = r.choice([1_210_000, 2_420_000, 4_840_000, 6_050_000, 12_100_000])
    m = akhir_m * 100 // 121
    return (f"Setelah 2 tahun dengan bunga majemuk 10% per tahun, tabungan menjadi {rp(akhir_m)}. Modal awalnya adalah ...",
            rp(m), [rp(akhir_m * 10 // 12), rp(akhir_m * 9 // 10), rp(akhir_m - akhir_m // 10)])


def bunga_sulit_6(r):
    m = r.choice([2_000_000, 3_000_000, 5_000_000, 6_000_000])
    p = r.choice([6, 8, 10, 12])  # genap, agar p/2 bulat
    a, b = r.sample(NAMA, 2)
    n = r.choice([2, 3])
    beda = m * p * n // 100 - m * (p // 2) * n // 100
    assert beda * 200 == m * p * n
    return (f"{a} dan {b} menabung {rp(m)} selama {n} tahun dengan bunga tunggal {persen(p)} dan {persen(Fraction(p, 2))} per tahun. Selisih bunga mereka ...",
            rp(beda), [rp(beda * 2), rp(m * p // 200), rp(beda + m * p // 100)])


# ================================================================== KOMPOSISI
def lin_acak(r, besar=5):
    a = r.choice([k for k in range(-besar, besar + 1) if k not in (0, 1)] + [1, 2, 3])
    b = r.choice([k for k in range(-9, 10) if k != 0])
    return a, b


def komp_mudah_1(r):
    a, b = lin_acak(r, 4)
    c, d = lin_acak(r, 4)
    k = r.randint(-3, 4)
    benar = a * (c * k + d) + b
    salah = [c * (a * k + b) + d, (a * k + b) + (c * k + d), a * (c * k) + b]
    return (f"Diketahui f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}. Nilai (f ∘ g)({k}) adalah ...",
            str(benar), [str(s) for s in salah] + [str(benar + 2), str(benar - 1)])


def komp_mudah_2(r):
    a, b = lin_acak(r, 4)
    c, d = lin_acak(r, 4)
    k = r.randint(-3, 4)
    benar = c * (a * k + b) + d
    salah = [a * (c * k + d) + b, (a * k + b) * (c * k + d), (a * k + b) + d]
    return (f"Jika f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}, nilai (g ∘ f)({k}) adalah ...",
            str(benar), [str(s) for s in salah] + [str(benar + 3)])


def komp_mudah_3(r):
    a, b = lin_acak(r, 4)
    k = r.randint(-3, 4)
    c = r.choice([1, 2, -1])
    gk = r.randint(-4, 5)
    return (f"Diketahui g({k}) = {gk} dan f(x) = {poli(a, b)}. Nilai (f ∘ g)({k}) adalah ...",
            str(a * gk + b), [str(a * k + b), str(gk), str(a * gk - b), str(a * gk + b + c * 2)])


def komp_sedang_1(r):
    a, b = lin_acak(r, 5)
    c, d = lin_acak(r, 5)
    benar = poli(a * c, a * d + b)
    salah = [poli(a * c, c * b + d), poli(a * c, d + b), poli(a + c, b + d)]
    return (f"Diketahui f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}. Rumus (f ∘ g)(x) adalah ...", benar, salah)


def komp_sedang_2(r):
    a, b = lin_acak(r, 5)
    c, d = lin_acak(r, 5)
    benar = poli(a * c, c * b + d)
    salah = [poli(a * c, a * d + b), poli(a * c, b * d), poli(a + c, b + d)]
    return (f"Jika f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}, maka (g ∘ f)(x) adalah ...", benar, salah)


def komp_sedang_3(r):
    p = r.choice([k for k in range(-6, 7) if k != 0])
    c, d = lin_acak(r, 3)
    k = r.randint(-2, 3)
    g = c * k + d
    benar = g * g + p
    salah = [c * (k * k + p) + d, c * k * k + d + p, g * 2 + p]
    return (f"Diketahui f(x) = {poli(1, 0, p)} dan g(x) = {poli(c, d)}. Nilai (f ∘ g)({k}) adalah ...",
            str(benar), [str(s) for s in salah] + [str(benar + 1)])


def komp_sedang_4(r):
    p = r.choice([k for k in range(-6, 7) if k != 0])
    c, d = lin_acak(r, 3)
    k = r.randint(-2, 3)
    benar = c * (k * k + p) + d
    g = c * k + d
    salah = [g * g + p, c * k * k + d, (k * k + p) + c + d]
    return (f"Jika f(x) = {poli(1, 0, p)} dan g(x) = {poli(c, d)}, nilai (g ∘ f)({k}) adalah ...",
            str(benar), [str(s) for s in salah] + [str(benar - 2)])


def komp_sulit_1(r):
    c, d = lin_acak(r, 3)
    p = r.randint(-4, 4)
    q = r.choice([k for k in range(-6, 7) if k != 0])
    # f(x) = x^2 + px + q ; (f o g)(x) = (cx+d)^2 + p(cx+d) + q
    a2 = c * c
    a1 = 2 * c * d + p * c
    a0 = d * d + p * d + q
    benar = poli(a2, a1, a0)
    salah = [poli(a2, c * d + p * c, a0), poli(c, d * d + p, q), poli(a2, a1, d * d + q)]
    return (f"Diketahui f(x) = {poli(1, p, q)} dan g(x) = {poli(c, d)}. Rumus (f ∘ g)(x) adalah ...", benar, salah)


def komp_sulit_2(r):
    a, b = lin_acak(r, 4)
    c, d = lin_acak(r, 4)
    # f(x) = ax + b, (f o g)(x) = acx + (ad + b); cari g(x)
    fg = poli(a * c, a * d + b)
    benar = poli(c, d)
    salah = [poli(a * c, d), poli(c, a * d), poli(c, a * d + b - b * 2)]
    return (f"Diketahui f(x) = {poli(a, b)} dan (f ∘ g)(x) = {fg}. Rumus g(x) adalah ...", benar, salah + [poli(c, d + b)])


def komp_sulit_3(r):
    c, d = lin_acak(r, 4)
    m, n = lin_acak(r, 4)
    # g(x) = cx + d, (f o g)(x) = m x + n  ->  f(x) = m (x - d)/c + n, pilih agar bulat
    if m % c:
        return None
    a = m // c
    b = n - a * d
    if b == 0:
        return None
    return (f"Diketahui g(x) = {poli(c, d)} dan (f ∘ g)(x) = {poli(m, n)}. Rumus f(x) adalah ...",
            poli(a, b), [poli(a, n + a * d), poli(m, b), poli(a, n)])


def komp_sulit_4(r):
    a, b = lin_acak(r, 3)
    c, d = lin_acak(r, 3)
    e, f = lin_acak(r, 3)
    k = r.randint(-2, 2)
    h = e * k + f
    g = c * h + d
    benar = a * g + b
    salah = [e * (c * (a * k + b) + d) + f, a * (c * k + d) + b, benar + a]
    return (f"Jika f(x) = {poli(a, b)}, g(x) = {poli(c, d)}, dan h(x) = {poli(e, f)}, nilai (f ∘ g ∘ h)({k}) adalah ...",
            str(benar), [str(s) for s in salah] + [str(benar - 2)])


# ================================================================== INVERS
def inv_mudah_1(r):
    a, b = lin_acak(r, 5)
    hasil = r.randint(-5, 6)
    k = a * hasil + b
    return (f"Diketahui f(x) = {poli(a, b)}. Nilai f^{{-1}}({k}) adalah ...",
            str(hasil), [str(a * k + b), str(hasil + 1), str(-hasil if hasil else 2), str(k - b)])


def inv_mudah_2(r):
    a, b = lin_acak(r, 5)
    x = r.randint(-4, 5)
    y = a * x + b
    return (f"Jika f({x}) = {y}, maka nilai f^{{-1}}({y}) adalah ...",
            str(x), [str(y), str(-x if x else 1), str(x + y)])


def inv_mudah_3(r):
    b = r.choice([k for k in range(-12, 13) if k != 0])
    return (f"Invers dari fungsi f(x) = {poli(1, b)} adalah ...",
            "f^{-1}(x) = " + poli(1, -b), ["f^{-1}(x) = " + poli(1, b), "f^{-1}(x) = " + poli(-1, b), "f^{-1}(x) = " + poli(-1, -b)])


def inv_sedang_1(r):
    a = r.choice([2, 3, 4, 5, 6, 7])
    b = r.choice([k for k in range(-9, 10) if k != 0])
    benar = pecahan(poli(1, -b), a)
    salah = [pecahan(poli(1, b), a), pecahan(a, poli(1, -b)), poli(a, -b)]
    return (f"Invers dari f(x) = {poli(a, b)} adalah f^{{-1}}(x) = ...", benar, salah)


def inv_sedang_2(r):
    p = r.choice([k for k in range(-9, 10) if k != 0])
    q = r.choice([2, 3, 4, 5])
    benar = poli(q, -p)
    salah = [poli(q, p), pecahan(poli(1, -p), q), poli(-q, p)]
    return (f"Jika f(x) = {pecahan(poli(1, p), q)}, maka f^{{-1}}(x) adalah ...", benar, salah)


def inv_sedang_3(r):
    a = r.choice([2, 3, 4, 5])
    b = r.choice([k for k in range(-8, 9) if k != 0])
    hasil = r.randint(-4, 5)
    k = a * hasil + b
    return (f"Diketahui f(x) = {poli(a, b)}. Nilai f^{{-1}}({k}) + f({hasil}) adalah ...",
            str(hasil + k), [str(hasil), str(k), str(2 * k), str(hasil + k + a)])


def inv_sedang_4(r):
    a = r.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    b = r.choice([k for k in range(-9, 10) if k != 0])
    benar = pecahan(poli(1, -b), a)  # f^-1(x) = (x - b)/a
    salah = [pecahan(poli(1, b), a), pecahan(poli(1, -b), -a), pecahan(a, poli(1, -b))]
    return (f"Fungsi f(x) = {poli(a, b)}. Rumus f^{{-1}}(x) adalah ...", benar, salah)


def inv_sulit_1(r):
    a, b = r.choice([k for k in range(-5, 6) if k]), r.choice([k for k in range(-6, 7) if k])
    c, d = r.choice([1, 2, 3]), r.choice([k for k in range(-6, 7) if k])
    if a * d - b * c == 0 or a == -d:
        return None
    # f(x) = (ax + b)/(cx + d)  ->  f^-1(x) = (-dx + b)/(cx - a)
    benar = pecahan(poli(-d, b), poli(c, -a))
    salah = [pecahan(poli(d, b), poli(c, -a)), pecahan(poli(-d, b), poli(c, a)), pecahan(poli(-d, -b), poli(c, -a))]
    return (f"Invers dari f(x) = {pecahan(poli(a, b), poli(c, d))} adalah f^{{-1}}(x) = ...", benar, salah)


def inv_sulit_2(r):
    a, b = r.choice([k for k in range(-4, 5) if k]), r.choice([k for k in range(-6, 7) if k])
    c, d = r.choice([1, 2]), r.choice([k for k in range(-6, 7) if k])
    if a * d - b * c == 0:
        return None
    y = r.randint(-3, 4)
    # f^-1(y) = (-dy + b)/(cy - a)
    pembagi = c * y - a
    if pembagi == 0 or (-d * y + b) % pembagi:
        return None
    hasil = (-d * y + b) // pembagi
    salah = [Fraction(a * y + b, c * y + d) if c * y + d else 99, hasil + 1, -hasil if hasil else 3]
    return (f"Diketahui f(x) = {pecahan(poli(a, b), poli(c, d))}. Nilai f^{{-1}}({y}) adalah ...",
            str(hasil), [desimal(s) if isinstance(s, Fraction) else str(s) for s in salah] + [str(hasil - 2)])


def inv_sulit_3(r):
    a, b = r.choice([2, 3]), r.choice([k for k in range(-5, 6) if k])
    c, d = r.choice([2, 3, -2]), r.choice([k for k in range(-5, 6) if k])
    hasil = r.randint(-3, 3)
    # (f o g)(x) = a(cx + d) + b ; cari (f o g)^-1(k)
    k = a * (c * hasil + d) + b
    return (f"Diketahui f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}. Nilai (f ∘ g)^{{-1}}({k}) adalah ...",
            str(hasil), [str(hasil + 1), str(-hasil if hasil else 2), str(a * (c * k + d) + b)])


def inv_sulit_4(r):
    a = r.choice([2, 3, 4])
    b = r.choice([k for k in range(-6, 7) if k])
    c = r.choice([2, 3])
    d = r.choice([k for k in range(-6, 7) if k])
    # f^-1(x) = (x - b)/a ; g(x) = cx + d ; (g o f^-1)(x) = c(x - b)/a + d
    hasil = r.randint(-3, 4)
    x = a * hasil + b
    return (f"Diketahui f(x) = {poli(a, b)} dan g(x) = {poli(c, d)}. Nilai (g ∘ f^{{-1}})({x}) adalah ...",
            str(c * hasil + d), [str(c * x + d), str(hasil), str(a * (c * x + d) + b)])


# ================================================================== STATISTIKA
def data_teks(data):
    return ", ".join(str(x) for x in data)


def median(data):
    s = sorted(data)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def stat_mudah_1(r):
    n = r.choice([5, 6])
    data = [r.randint(4, 10) for _ in range(n)]
    rata = Fraction(sum(data), n)
    if rata.denominator != 1:
        return None
    return (f"Rata-rata (mean) dari data {data_teks(data)} adalah ...",
            desimal(rata), [desimal(median(data)), desimal(rata + 1), str(sum(data))])


def stat_mudah_2(r):
    data = [r.randint(3, 12) for _ in range(r.choice([5, 7]))]
    return (f"Median dari data {data_teks(data)} adalah ...",
            desimal(median(data)), [str(data[len(data) // 2]), desimal(Fraction(sum(data), len(data))), str(max(data)), str(min(data))])


def stat_mudah_3(r):
    nilai = r.sample(range(4, 11), 4)
    modus = nilai[0]
    data = [modus] * 3 + [nilai[1]] * 2 + [nilai[2], nilai[3]]
    r.shuffle(data)
    return (f"Modus dari data {data_teks(data)} adalah ...",
            str(modus), [str(nilai[1]), desimal(median(data)), str(max(data)) if max(data) != modus else str(min(data))])


def stat_mudah_4(r):
    nama = r.choice(NAMA)
    data = [r.randint(60, 95) for _ in range(4)]
    rata = Fraction(sum(data), 4)
    if rata.denominator != 1:
        return None
    return (f"Nilai ulangan {nama}: {data_teks(data)}. Rata-rata nilainya adalah ...",
            desimal(rata), [desimal(rata + 2), desimal(median(data)), str(sum(data))])


def stat_sedang_1(r):
    nilai = sorted(r.sample(range(5, 10), 3))
    frek = [r.randint(2, 6) for _ in range(3)]
    total = sum(v * f for v, f in zip(nilai, frek))
    n = sum(frek)
    rata = Fraction(total, n)
    if (rata * 10).denominator != 1:
        return None
    teks = ", ".join(f"{v} ({f} siswa)" for v, f in zip(nilai, frek))
    return (f"Nilai siswa: {teks}. Rata-rata nilai siswa adalah ...",
            desimal(rata), [desimal(Fraction(sum(nilai), 3)), desimal(rata + Fraction(1, 2)), str(nilai[frek.index(max(frek))])])


def stat_sedang_2(r):
    nilai = sorted(r.sample(range(5, 11), 4))
    frek = [r.randint(1, 6) for _ in range(4)]
    data = [v for v, f in zip(nilai, frek) for _ in range(f)]
    teks = ", ".join(f"{v} ({f} anak)" for v, f in zip(nilai, frek))
    med = median(data)
    return (f"Data nilai: {teks}. Median data tersebut adalah ...",
            desimal(med), [desimal(Fraction(sum(nilai), 4)), str(nilai[frek.index(max(frek))]) if nilai[frek.index(max(frek))] != med else str(nilai[0]),
                           desimal(med + 1), desimal(Fraction(sum(data), len(data)))])


def stat_sedang_3(r):
    nilai = sorted(r.sample(range(4, 11), 4))
    frek = r.sample([2, 3, 5, 7], 4)
    teks = ", ".join(f"{v} ({f} siswa)" for v, f in zip(nilai, frek))
    modus = nilai[frek.index(max(frek))]
    return (f"Tabel nilai: {teks}. Modus data tersebut adalah ...",
            str(modus), [str(max(frek)), str(nilai[frek.index(min(frek))]), str(nilai[-1]) if nilai[-1] != modus else str(nilai[0])])


def stat_sedang_4(r):
    n = r.choice([6, 8])
    data = [r.randint(3, 15) for _ in range(n)]
    med = median(data)
    if med.denominator == 1:
        return None
    return (f"Median dari data {data_teks(data)} adalah ...",
            desimal(med), [desimal(median(data[:n - 1])), str(data[n // 2]), desimal(Fraction(sum(data), n))])


def stat_sedang_5(r):
    n = r.choice([4, 5])
    rata = r.randint(6, 9)
    data = [r.randint(rata - 3, rata + 3) for _ in range(n - 1)]
    terakhir = rata * n - sum(data)
    if not 1 <= terakhir <= 10:
        return None
    return (f"Rata-rata {n} bilangan adalah {rata}. Jika {n - 1} bilangan di antaranya {data_teks(data)}, bilangan yang lain adalah ...",
            str(terakhir), [str(rata), str(terakhir + 1), str(rata * (n - 1) - sum(data) if rata * (n - 1) - sum(data) != terakhir else terakhir + 2)])


def stat_sulit_1(r):
    n1, n2 = r.choice([20, 25, 30]), r.choice([10, 15, 20])
    m1, m2 = r.randint(65, 80), r.randint(70, 90)
    rata = Fraction(n1 * m1 + n2 * m2, n1 + n2)
    if (rata * 10).denominator != 1 or m1 == m2:
        return None
    return (f"Rata-rata nilai {n1} siswa kelas A adalah {m1}, dan {n2} siswa kelas B adalah {m2}. Rata-rata gabungannya adalah ...",
            desimal(rata), [desimal(Fraction(m1 + m2, 2)), desimal(rata + 1), desimal(rata - 1)])


def stat_sulit_2(r):
    n = r.choice([20, 25, 30, 35])
    m = r.randint(70, 80)
    baru = r.randint(m + 5, 99)
    rata = Fraction(n * m + baru, n + 1)
    if (rata * 10).denominator != 1:
        return None
    return (f"Rata-rata nilai {n} siswa adalah {m}. Seorang siswa baru bernilai {baru} bergabung. Rata-rata sekarang adalah ...",
            desimal(rata), [desimal(Fraction(m + baru, 2)), str(m + 1), desimal(rata + Fraction(1, 2))])


def stat_sulit_3(r):
    n = r.choice([10, 20, 25])
    m = r.randint(60, 75)
    keluar = r.randint(m + 5, 95)
    rata = Fraction(n * m - keluar, n - 1)
    if (rata * 10).denominator != 1:
        return None
    return (f"Rata-rata berat {n} anak adalah {m} kg. Jika satu anak dengan berat {keluar} kg keluar, rata-rata berat sisanya adalah ...",
            f"{desimal(rata)} kg", [f"{desimal(Fraction(n * m + keluar, n + 1))} kg", f"{m - 1} kg", f"{desimal(rata + 1)} kg"])


def stat_sulit_4(r):
    n_total = r.choice([30, 40])
    rata_total = r.randint(68, 75)
    n_a = r.choice([10, 15, 20])
    rata_a = r.randint(rata_total + 2, rata_total + 10)
    rata_b = Fraction(n_total * rata_total - n_a * rata_a, n_total - n_a)
    if (rata_b * 10).denominator != 1:
        return None
    return (f"Rata-rata {n_total} siswa adalah {rata_total}. Rata-rata {n_a} siswa putra adalah {rata_a}. Rata-rata siswa putri adalah ...",
            desimal(rata_b), [desimal(Fraction(2 * rata_total - rata_a)), desimal(rata_b + 2), str(rata_a - rata_total)])


def stat_sulit_5(r):
    n = r.choice([5, 6, 7])
    data = sorted(r.sample(range(2, 15), n))
    k = r.choice([2, 3, 5])
    med = median(data)
    rata = Fraction(sum(data), n)
    # setiap data dikali k lalu ditambah 1
    return (f"Data {data_teks(data)} masing-masing dikali {k} lalu ditambah 1. Median data baru adalah ...",
            desimal(med * k + 1), [desimal(med * k), desimal(med + 1), desimal(rata * k + 1) if rata * k + 1 != med * k + 1 else desimal(med * k + k)])


def stat_sulit_6(r):
    a = r.randint(4, 9)
    data = [a, a + 2, r.randint(3, 10), r.randint(3, 10)]
    rata = r.randint(6, 8)
    # data: a, a+2, p, q, x ; rata-rata 5 data = rata ; cari x
    x = rata * 5 - sum(data)
    if not 1 <= x <= 15:
        return None
    return (f"Data 5 nilai: {data_teks(data)}, dan x. Jika rata-ratanya {rata}, nilai x adalah ...",
            str(x), [str(x + 2), str(rata), str(rata * 4 - sum(data)) if rata * 4 - sum(data) != x else str(x - 1)])


PEMBUAT = {
    ("Bunga tunggal & majemuk", "Mudah"): [bunga_mudah_1, bunga_mudah_2, bunga_mudah_3, bunga_mudah_4],
    ("Bunga tunggal & majemuk", "Sedang"): [bunga_sedang_1, bunga_sedang_2, bunga_sedang_3, bunga_sedang_4, bunga_sedang_5],
    ("Bunga tunggal & majemuk", "Sulit"): [bunga_sulit_1, bunga_sulit_2, bunga_sulit_3, bunga_sulit_4, bunga_sulit_5, bunga_sulit_6],
    ("Fungsi komposisi", "Mudah"): [komp_mudah_1, komp_mudah_2, komp_mudah_3],
    ("Fungsi komposisi", "Sedang"): [komp_sedang_1, komp_sedang_2, komp_sedang_3, komp_sedang_4],
    ("Fungsi komposisi", "Sulit"): [komp_sulit_1, komp_sulit_2, komp_sulit_3, komp_sulit_4],
    ("Fungsi invers", "Mudah"): [inv_mudah_1, inv_mudah_2, inv_mudah_3],
    ("Fungsi invers", "Sedang"): [inv_sedang_1, inv_sedang_2, inv_sedang_3, inv_sedang_4],
    ("Fungsi invers", "Sulit"): [inv_sulit_1, inv_sulit_2, inv_sulit_3, inv_sulit_4],
    ("Mean, median, modus", "Mudah"): [stat_mudah_1, stat_mudah_2, stat_mudah_3, stat_mudah_4],
    ("Mean, median, modus", "Sedang"): [stat_sedang_1, stat_sedang_2, stat_sedang_3, stat_sedang_4, stat_sedang_5],
    ("Mean, median, modus", "Sulit"): [stat_sulit_1, stat_sulit_2, stat_sulit_3, stat_sulit_4, stat_sulit_5, stat_sulit_6],
}


def buat(seed=2026):
    """Mengembalikan daftar 300 soal mentah (benar + 3 pengecoh)."""
    rng = random.Random(seed)
    wadah = Wadah()
    for (materi, tingkat), pembuat in PEMBUAT.items():
        isi_sampai_penuh(wadah, materi, tingkat, pembuat, rng)
    hasil = []
    for t in TINGKAT:
        for m in MATERI:
            hasil.extend(wadah.isi[(m, t)])
    return hasil
