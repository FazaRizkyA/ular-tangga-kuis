"""Uji ketahanan: memainkan banyak permainan penuh lewat App (update + render
setiap frame) tanpa layar, untuk memastikan tidak ada crash (mode Pass & Play
dan vs Bot, 2-4 pemain, semua kategori).
Jalankan dari folder source_code:  python alat/uji_simulasi.py
"""
import os
import random
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AKAR)
os.chdir(AKAR)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import main as aplikasi  # noqa: E402
from game import MENJAWAB, MENUNGGU_DADU  # noqa: E402

random.seed(42)
app = aplikasi.App()
dt = 1 / 30
hasil = []
for ronde in range(12):
    mode = "bot" if ronde % 2 else "pass"
    app.layar_aktif = "setup"
    app.mode = mode
    app._App__terapkan_mode()
    app.jumlah = 2 + ronde % 3
    app.kategori = ["Matematika", "Penjas Orkes", "Sejarah Indonesia", "Campuran"][ronde % 4]
    app.kesulitan = ["Mudah", "Sedang", "Sulit"][ronde % 3]
    for i, k in enumerate(app.kolom_nama[:app.jumlah]):
        if k.bisa_diubah:
            k.teks = f"Siswa {i + 1}"
    app._App__mulai_permainan()
    assert app.layar_aktif == "main", app.pesan_error
    frame = 0
    while app.layar_aktif == "main" and frame < 200000:
        gm = app.gm
        p = gm.pemain_aktif
        if not p.is_bot():
            if gm.state == MENJAWAB and random.random() < 0.05:
                app._App__jawab(random.choice("ABCD") if random.random() < 0.4 else gm.soal_aktif.kunci)
            elif gm.state == MENUNGGU_DADU and app.anim is None:
                app._App__coba_kocok()
        app.update(dt)
        if frame % 5 == 0:
            app.render()
        frame += 1
    assert not app.pesan_error, app.pesan_error
    assert app.layar_aktif == "pemenang", f"ronde {ronde} tidak selesai"
    app.render()
    hasil.append((mode, app.kesulitan, app.jumlah, app.kategori, app.gm.pemenang.nama, frame, len(app.gm.log)))

for h in hasil:
    print("SELESAI mode=%s kesulitan=%-6s pemain=%d kategori=%-17s pemenang=%-8s frame=%d log=%d" % h)
print("SEMUA SIMULASI SELESAI TANPA CRASH")
