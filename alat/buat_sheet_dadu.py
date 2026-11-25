"""Alat pengembang: menyusun gambar hasil render Blender (aset_sumber/render_dadu)
menjadi 6 lembar sprite (assets/dadu3d/dadu_1.png ... dadu_6.png) + info.json.
Gambar diperkecil dari 320 ke 240 px dengan alpha premultiplied agar tepinya halus.

Jalankan dari folder source_code:  python alat/buat_sheet_dadu.py
"""
import json
import os

from PIL import Image

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(AKAR, "aset_sumber", "render_dadu")
KELUAR = os.path.join(AKAR, "assets", "dadu3d")
UKURAN, KOLOM = 240, 8  # 240 px = 160 logis x skala 1,5 (layar 1920x1080)

os.makedirs(KELUAR, exist_ok=True)
jumlah_frame = len([f for f in os.listdir(SUMBER) if f.startswith("dadu_1_")])
baris = (jumlah_frame + KOLOM - 1) // KOLOM
for n in range(1, 7):
    lembar = Image.new("RGBA", (KOLOM * UKURAN, baris * UKURAN), (0, 0, 0, 0))
    for i in range(jumlah_frame):
        gambar = Image.open(os.path.join(SUMBER, f"dadu_{n}_{i:02d}.png")).convert("RGBA")
        kecil = gambar.convert("RGBa").resize((UKURAN, UKURAN), Image.LANCZOS).convert("RGBA")
        lembar.paste(kecil, ((i % KOLOM) * UKURAN, (i // KOLOM) * UKURAN))
    lembar.save(os.path.join(KELUAR, f"dadu_{n}.png"), optimize=True)
info = {"frame": jumlah_frame, "kolom": KOLOM, "ukuran": UKURAN,
        "sumber": "Model aset_sumber/dadu.glb, dirender dengan Blender 4.5 (alat/render_dadu_blender.py)"}
json.dump(info, open(os.path.join(KELUAR, "info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total = sum(os.path.getsize(os.path.join(KELUAR, f)) for f in os.listdir(KELUAR))
print(f"{jumlah_frame} frame x 6 angka -> {KELUAR} ({total / 1e6:.1f} MB)")

