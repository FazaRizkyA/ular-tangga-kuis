"""Uji otomatis logika permainan (tanpa layar).

Menjalankan kasus uji dari PRD yang bisa diuji tanpa klik:
T2, T4-T12, T14, aturan kesulitan, soal tidak berulang, serta validasi
skor/posisi. Jalankan dari folder source_code:  python alat/uji_logika.py
"""
import json
import os
import random
import sys
import tempfile
from collections import Counter

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AKAR)
os.chdir(AKAR)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

from config import KESULITAN, SKOR_BENAR, BONUS_TANGGA, JUMLAH_PETAK, KATEGORI  # noqa: E402
from pemain import Pemain, Bot  # noqa: E402
from soal import BankSoal  # noqa: E402
from dadu import Dadu  # noqa: E402
from papan import Papan  # noqa: E402
sys.path.insert(0, os.path.join(AKAR, "alat"))
from cek_tata_letak import masalah as masalah_tata_letak  # noqa: E402
from game import GameManager, MENJAWAB, HASIL_JAWABAN, MENUNGGU_DADU, BERGERAK, SELESAI  # noqa: E402

gagal = 0


def cek(nama, kondisi):
    global gagal
    print(("LULUS " if kondisi else "GAGAL ") + nama)
    if not kondisi:
        gagal += 1


class DaduTetap(Dadu):
    """Dadu palsu untuk pengujian: nilainya bisa diatur."""

    def __init__(self, nilai):
        super().__init__()
        self.atur = nilai

    def kocok(self):
        return self.atur


def buat_game(nilai_dadu=1, jumlah=2, kesulitan="Sedang", kategori="Campuran"):
    bank = BankSoal()
    ok, _ = bank.muat("soal.json")
    assert ok
    dadu = DaduTetap(nilai_dadu)
    gm = GameManager(Papan(kesulitan), bank, dadu, kategori)
    pemain = [Pemain(f"P{i}", (0, 0, 0), i + 1) for i in range(jumlah)]
    gm.mulai_permainan(pemain)
    return gm, dadu, bank


def jawab_benar(gm):
    gm.jawab(gm.soal_aktif.kunci)
    gm.lanjut_setelah_hasil()


def salah_dari(gm):
    return next(h for h in "ABCD" if h != gm.soal_aktif.kunci)


# ================================================================ bank soal
bank = BankSoal()
ok, pesan = bank.muat("soal.json")
cek(f"soal.json dimuat ({pesan})", ok and bank.jumlah() == 300 and bank.jumlah_dilewati == 0)
data = json.load(open("soal.json", encoding="utf-8"))
for kat in KATEGORI:
    isi = [s for s in data if s["kategori"] == kat]
    kunci = Counter(s["kunci"] for s in isi)
    cek(f"{kat}: 100 soal, kunci A-D seimbang {dict(kunci)}", len(isi) == 100 and set(kunci.values()) == {25})
cek("id soal unik", len({s["id"] for s in data}) == len(data))
cek("teks soal tidak ada yang kembar", len({s["pertanyaan"] for s in data}) == len(data))
cek("4 pilihan tiap soal berbeda", all(len(set(s["pilihan"].values())) == 4 for s in data))
mtk_materi = Counter(s.get("materi") for s in data if s["kategori"] == "Matematika")
cek(f"materi Matematika lengkap {dict(mtk_materi)}",
    set(mtk_materi) == {"Aljabar", "Eksponen", "Pangkat", "Akar", "Fungsi komposisi"})
pj_materi = Counter(s.get("materi") for s in data if s["kategori"] == "Penjas Orkes")
cek(f"materi Penjas lengkap {dict(pj_materi)}", set(pj_materi) == {"Renang", "Sepak bola", "Bulu tangkis"})

# muat di layar: diukur dengan penata rumus yang sama dengan main.py
pygame.init()
from rumus import PenataRumus  # noqa: E402
rumus_soal = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 24)
rumus_soal_kecil = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 20)
rumus_jawab = PenataRumus("AtkinsonHyperlegible-Bold.ttf", 18)
lebar_soal = 560 - 36
lebar_jawab = (560 - 28 - 10) // 2 - 56
TINGGI_SOAL, TINGGI_JAWAB = 68, 46
terlalu_panjang = []
for s in data:
    penata = rumus_soal
    if len(penata.bungkus(s["pertanyaan"], lebar_soal)) > 2 or penata.tinggi(s["pertanyaan"], lebar_soal) > TINGGI_SOAL:
        penata = rumus_soal_kecil
    if len(penata.bungkus(s["pertanyaan"], lebar_soal)) > 3 or penata.tinggi(s["pertanyaan"], lebar_soal) > TINGGI_SOAL + 8:
        terlalu_panjang.append((s["id"], "soal"))
    for v in s["pilihan"].values():
        baris = rumus_jawab.bungkus(v, lebar_jawab)
        if len(baris) > 2 or rumus_jawab.tinggi(v, lebar_jawab) > TINGGI_JAWAB or any(rumus_jawab.ukur(b)[0] > lebar_jawab for b in baris):
            terlalu_panjang.append((s["id"], v))
cek(f"semua soal & jawaban (termasuk rumus) muat di kartu {terlalu_panjang[:5]}", not terlalu_panjang)
mtk = [s for s in data if s["kategori"] == "Matematika"]
teks_mtk = " ".join(s["pertanyaan"] + " " + " ".join(s["pilihan"].values()) for s in mtk)
cek("rumus Matematika memakai pecahan/pangkat tulis (tanpa '/' atau pangkat '^angka' polos)",
    "/" not in teks_mtk and "\\frac" in teks_mtk and "^{" in teks_mtk and not any(c in teks_mtk for c in "²³"))
urai = rumus_soal.urai("\\frac{1}{x^{6}} + √{48} + (f ∘ g)(x)")
cek("penata rumus mengenali pecahan, pangkat, akar, komposisi",
    [n[0] for n in urai if n[0] != "spasi"][:1] == ["pecahan"] and any(n[0] == "akar" for n in urai) and any(n[0] == "komposisi" for n in urai))

# ================================================================ dadu 3D hasil Blender
pygame.display.set_mode((1, 1))
from dadu3d import DaduRender  # noqa: E402
dadu_r = DaduRender()
cek("gambar dadu Blender (6 angka) termuat", dadu_r.siap)
dadu_rusak = DaduRender(os.path.join("assets", "folder_tidak_ada"))
cek("file dadu Blender hilang: tidak crash, memakai dadu buatan kode", not dadu_rusak.siap)

# ================================================================ T10, T11, soal rusak
ok, pesan = BankSoal().muat("tidak_ada.json")
cek(f"T10 file hilang -> '{pesan}'", not ok and pesan == "File soal tidak ditemukan")
tmp = os.path.join(tempfile.gettempdir(), "soal_rusak.json")
with open(tmp, "w", encoding="utf-8") as f:
    f.write("{ ini bukan json")
ok, pesan = BankSoal().muat(tmp)
cek(f"T11 file rusak -> '{pesan}'", not ok and pesan == "Format soal.json rusak")
with open(tmp, "w", encoding="utf-8") as f:
    json.dump([data[0], {"id": 999, "kategori": "X", "pertanyaan": "?", "pilihan": {"A": "1"}, "kunci": "E"}], f)
b = BankSoal()
ok, _ = b.muat(tmp)
cek("soal tidak valid dilewati, sisanya dipakai", ok and b.jumlah() == 1 and b.jumlah_dilewati == 1)

# ================================================================ T12: soal tidak berulang
b = BankSoal()
b.muat("soal.json")
dilihat = [b.ambil_acak("Matematika") for _ in range(100)]
cek("100 soal Matematika keluar tanpa berulang", len({s.id for s in dilihat}) == 100 and all(s.kategori == "Matematika" for s in dilihat))
s101 = b.ambil_acak("Matematika")
cek("T12 soal ke-101 dipinjam dari kategori lain (bukan mengulang)", b.dipinjam and s101.kategori != "Matematika")
semua = {s.id for s in dilihat} | {s101.id}
for _ in range(199):
    semua.add(b.ambil_acak("Matematika").id)
cek("300 soal keluar semua tanpa satu pun berulang", len(semua) == 300)
b.ambil_acak("Matematika")
cek("baru setelah 300 soal habis, bank diacak ulang", b.baru_diacak)

gm, _, bank_g = buat_game(kategori="Sejarah Indonesia")
id_game1 = set()
for _ in range(30):
    id_game1.add(gm.soal_aktif.id)
    gm.jawab(salah_dari(gm))
    gm.lanjut_setelah_hasil()
gm.reset()
id_game2 = set()
for _ in range(30):
    id_game2.add(gm.soal_aktif.id)
    gm.jawab(salah_dari(gm))
    gm.lanjut_setelah_hasil()
cek("dalam satu game soal tidak berulang", len(id_game1) == 30)
cek("Main Lagi memakai soal yang berbeda dari game sebelumnya", not (id_game1 & id_game2) and len(id_game2) == 30)

# ================================================================ kesulitan
jumlah_ular = [len(KESULITAN[k]["ular"]) for k in ("Mudah", "Sedang", "Sulit")]
jumlah_tangga = [len(KESULITAN[k]["tangga"]) for k in ("Mudah", "Sedang", "Sulit")]
akurasi = [KESULITAN[k]["akurasi_bot"] for k in ("Mudah", "Sedang", "Sulit")]
cek(f"ular makin banyak: {jumlah_ular}", jumlah_ular[0] < jumlah_ular[1] < jumlah_ular[2])
cek(f"tangga makin sedikit: {jumlah_tangga}", jumlah_tangga[0] > jumlah_tangga[1] > jumlah_tangga[2])
cek(f"bot makin pintar: {akurasi}", akurasi[0] < akurasi[1] < akurasi[2])
for nama, aturan in KESULITAN.items():
    t, u = aturan["tangga"], aturan["ular"]
    awal = set(t) | set(u)
    ujung = set(t.values()) | set(u.values())
    sah = (all(a < b for a, b in t.items()) and all(a > b for a, b in u.items())
           and not (awal & ujung) and len(awal) == len(t) + len(u)
           and all(1 < n < JUMLAH_PETAK for n in awal | ujung))
    cek(f"{nama}: letak ular & tangga sah (tidak saling tumpuk)", sah)
    soal_letak = masalah_tata_letak(t, u)
    cek(f"{nama}: tangga tidak berdekatan/segaris {soal_letak or ''}", not soal_letak)

R = random.Random(1)
soal_uji = buat_game()[0].soal_aktif
for nama in ("Mudah", "Sulit"):
    random.seed(7)
    bot = Bot("B", (0, 0, 0), 2, KESULITAN[nama]["akurasi_bot"])
    benar = sum(bot.pilih_jawaban(soal_uji) == soal_uji.kunci for _ in range(4000)) / 4000
    KESULITAN[nama]["_uji"] = benar
cek(f"bot Sulit lebih sering benar ({KESULITAN['Sulit']['_uji']:.2f}) dari bot Mudah ({KESULITAN['Mudah']['_uji']:.2f})",
    KESULITAN["Sulit"]["_uji"] > KESULITAN["Mudah"]["_uji"] + 0.25)

# ================================================================ T5, T14, T4, waktu habis
gm, dadu, _ = buat_game()
p = gm.pemain_aktif
gm.jawab(gm.soal_aktif.kunci)
cek("T5 jawab benar +10 skor", p.skor == SKOR_BENAR and gm.state == HASIL_JAWABAN)
gm.lanjut_setelah_hasil()
cek("T5 tombol dadu terbuka (MENUNGGU_DADU)", gm.state == MENUNGGU_DADU)
dadu.atur = 1
n1, n2 = gm.kocok_dadu(), gm.kocok_dadu()
cek("T14 kocok kedua diabaikan", n1 == 1 and n2 is None and gm.state == BERGERAK)

gm, _, _ = buat_game()
p0 = gm.pemain_aktif
gm.jawab(salah_dari(gm))
cek("T4 jawab salah tanpa skor", p0.skor == 0 and gm.state == HASIL_JAWABAN)
gm.lanjut_setelah_hasil()
cek("T4 giliran pindah", gm.pemain_aktif is not p0 and gm.state == MENJAWAB and p0.posisi == 1)

gm, _, _ = buat_game()
gm.kurangi_waktu(31)
cek("waktu habis dianggap salah", gm.state == HASIL_JAWABAN and gm.jawaban_terakhir is None)

# ================================================================ T6: tangga & ular semua kesulitan
for nama, aturan in KESULITAN.items():
    semua_ok = True
    for bawah, atas in aturan["tangga"].items():
        gm, dadu, _ = buat_game(kesulitan=nama)
        p = gm.pemain_aktif
        p.pindah_ke(bawah - 1)
        jawab_benar(gm)
        dadu.atur = 1
        gm.kocok_dadu()
        semua_ok &= p.posisi == atas and p.skor == SKOR_BENAR + BONUS_TANGGA
    for kepala, ekor in aturan["ular"].items():
        gm, dadu, _ = buat_game(kesulitan=nama)
        p = gm.pemain_aktif
        p.pindah_ke(kepala - 1)
        jawab_benar(gm)
        dadu.atur = 1
        gm.kocok_dadu()
        gm.selesai_animasi()
        semua_ok &= p.posisi == ekor and "turun ular" in gm.log[0][1]
    cek(f"T6 {nama}: semua tangga naik +{BONUS_TANGGA} dan semua ular turun", semua_ok)

# ================================================================ T7 pantul, T8 finis, T9 main lagi
gm, dadu, _ = buat_game(kesulitan="Sedang")
p = gm.pemain_aktif
p.pindah_ke(60)
jawab_benar(gm)
dadu.atur = 5
gm.kocok_dadu()
cek("T7 60 + 5 memantul (61-64-63) lalu ular 63 ke 45", gm.info_gerak["jalur"] == [61, 62, 63, 64, 63] and p.posisi == 45)

gm, dadu, _ = buat_game()
p = gm.pemain_aktif
p.pindah_ke(61)
jawab_benar(gm)
dadu.atur = 3
gm.kocok_dadu()
gm.selesai_animasi()
cek(f"T8 mendarat tepat di {JUMLAH_PETAK} -> SELESAI", gm.state == SELESAI and gm.pemenang is p)
gm.reset()
cek("T9 Main Lagi: posisi 1, skor 0, pemain sama",
    all(x.posisi == 1 and x.skor == 0 and not x.sudah_menang for x in gm.pemain) and gm.state == MENJAWAB and len(gm.pemain) == 2)

# ================================================================ T2 giliran
gm, _, _ = buat_game(jumlah=4)
urutan = []
for _ in range(8):
    urutan.append(gm.pemain_aktif.nomor)
    gm.jawab(salah_dari(gm))
    gm.lanjut_setelah_hasil()
cek("T2 giliran 4 pemain berputar sesuai urutan", urutan == [1, 2, 3, 4, 1, 2, 3, 4])

# ================================================================ OOP
p = Pemain("X", (0, 0, 0), 1)
try:
    p.skor = -1
    cek("setter skor menolak negatif", False)
except ValueError:
    cek("setter skor menolak negatif", True)
try:
    p.pindah_ke(JUMLAH_PETAK + 1)
    cek(f"pindah_ke menolak petak {JUMLAH_PETAK + 1}", False)
except ValueError:
    cek(f"pindah_ke menolak petak {JUMLAH_PETAK + 1}", True)
gm, _, _ = buat_game()
cek("Bot akurasi 100% selalu benar", Bot("B", (0, 0, 0), 2, akurasi=1.0).pilih_jawaban(gm.soal_aktif) == gm.soal_aktif.kunci)
cek("Pemain manusia tidak memilih sendiri", Pemain("H", (0, 0, 0), 1).pilih_jawaban(gm.soal_aktif) is None)

print()
print("SEMUA LULUS" if gagal == 0 else f"{gagal} UJI GAGAL")
sys.exit(1 if gagal else 0)
