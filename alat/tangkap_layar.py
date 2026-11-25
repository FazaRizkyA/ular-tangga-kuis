"""Alat pengembang: merender setiap layar dan state ke PNG untuk ditinjau.
Jalankan dari folder source_code:  python alat/tangkap_layar.py <folder_keluaran>
"""
import os
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AKAR)
os.chdir(AKAR)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame  # noqa: E402

import main as aplikasi  # noqa: E402
from game import MENUNGGU_DADU  # noqa: E402

keluar = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AKAR, ".impeccable", "review")
os.makedirs(keluar, exist_ok=True)


def simpan(app, nama, langkah_waktu=0.0):
    if langkah_waktu:
        app.waktu += langkah_waktu
    app.render()
    pygame.image.save(app.canvas.p, os.path.join(keluar, f"{nama}.png"))
    print("tersimpan", nama)


app = aplikasi.App()
app.waktu = 1.3
simpan(app, "01_menu")
app.layar_aktif = "cara"
simpan(app, "02_cara_bermain")

app.layar_aktif = "setup"
app.jumlah = 4
app.kolom_nama[0].teks = "Andi"
app.kolom_nama[1].teks = "Sekar Ayu"
app.kolom_nama[2].teks = ""
app.kolom_nama[3].teks = "andi"
app._App__validasi_nama()
app._App__fokus_kolom(app.kolom_nama[1])
app.kategori = "Sejarah Indonesia"
app.kesulitan = "Sulit"
simpan(app, "03_setup_error")

app.kolom_nama[2].teks = "Bagus"
app.kolom_nama[3].teks = "Rina"
app._App__mulai_permainan()
gm = app.gm
for p, pos in zip(gm.pemain, (37, 19, 19, 50)):
    p.pindah_ke(pos)
    p.skor = {37: 45, 19: 20, 50: 30}[pos]
app.skor_tampil = {p.nomor: p.skor for p in gm.pemain}
for _ in range(9):
    salah = next(h for h in "ABCD" if h != gm.soal_aktif.kunci)
    gm.jawab(salah)
    gm.lanjut_setelah_hasil()
app._App__update_game(0.6)
gm.kurangi_waktu(12)
simpan(app, "04_game_menjawab")

benar = gm.soal_aktif.kunci
app._App__jawab(benar)
app._App__update_game(0.2)
simpan(app, "05_game_benar")

app._App__update_game(1.6)
assert gm.state == MENUNGGU_DADU
simpan(app, "06_game_menunggu_dadu")

app._App__kocok()
for _ in range(60):
    app._App__update_game(1 / 60)
simpan(app, "07_game_jalan")
while app.anim:
    app._App__update_game(1 / 60)

salah = next(h for h in "ABCD" if h != gm.soal_aktif.kunci)
app._App__update_game(0.5)
app._App__jawab(salah)
simpan(app, "08_game_salah")

app.konfirmasi = True
simpan(app, "09_konfirmasi")
app.konfirmasi = False

# pemenang
p = gm.pemain_aktif
gm.lanjut_setelah_hasil()
p = gm.pemain_aktif
p.pindah_ke(61)
gm.jawab(gm.soal_aktif.kunci)
gm.lanjut_setelah_hasil()
app.dadu.kocok = lambda: 3
app._App__kocok()
while app.anim:
    app._App__update_game(1 / 30)
app.layar_aktif = "pemenang"
simpan(app, "10_pemenang")

# papan tingkat Mudah dan Sedang (untuk membandingkan jumlah ular)
for tingkat in ("Mudah", "Sedang"):
    app.layar_aktif = "setup"
    app.kesulitan = tingkat
    app.mode = "bot"
    app._App__terapkan_mode()
    app.jumlah = 3
    app.kolom_nama[0].teks = "Andi"
    app._App__mulai_permainan()
    app._App__update_game(0.6)
    simpan(app, f"12_game_{tingkat.lower()}")
app.layar_aktif = "setup"
app.pesan_error = ""
simpan(app, "13_setup_bot")

# rumus Matematika (pecahan, pangkat, akar, komposisi) dan dadu 3D
app.layar_aktif = "setup"
app.mode = "pass"
app._App__terapkan_mode()
app.jumlah = 2
app.kolom_nama[0].teks, app.kolom_nama[1].teks = "Andi", "Sekar"
app.kategori = "Matematika"
app.kesulitan = "Sedang"
app._App__mulai_permainan()
gm = app.gm
dicari = {"14_rumus_pecahan": "\\frac", "15_rumus_akar": "âˆš", "16_rumus_komposisi": "âˆ˜"}
for _ in range(100):
    teks = gm.soal_aktif.pertanyaan + " ".join(gm.soal_aktif.pilihan.values())
    for nama, tanda in list(dicari.items()):
        if tanda in teks:
            app._App__update_game(0.6)
            simpan(app, nama)
            del dicari[nama]
            break
    if not dicari:
        break
    gm.jawab(next(h for h in "ABCD" if h != gm.soal_aktif.kunci))
    gm.lanjut_setelah_hasil()
app._App__jawab(gm.soal_aktif.kunci)
app._App__coba_kocok()
for _ in range(27):
    app._App__update_game(1 / 60)
simpan(app, "17_dadu_dilempar")
for _ in range(30):
    app._App__update_game(1 / 60)
simpan(app, "18_dadu_berguling")
for _ in range(40):
    app._App__update_game(1 / 60)
simpan(app, "19_dadu_mendarat")

# menu dengan file soal hilang
app2 = aplikasi.App()
app2.soal_siap, app2.pesan_soal = app2.bank.muat("tidak_ada.json")
app2.waktu = 2.0
simpan(app2, "11_menu_soal_hilang")

