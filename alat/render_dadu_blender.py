"""Alat pengembang (dijalankan oleh Blender, bukan oleh game):
merender animasi dadu 3D dari model aset_sumber/dadu.glb menjadi gambar PNG.

Untuk tiap angka 1-6 dirender FRAME gambar dadu berguling yang makin
melambat dan berhenti dengan angka itu menghadap ke atas. Latar transparan;
gerak melintas papan, pantulan, dan bayangan tetap diatur oleh game.

Cara pakai (dari folder source_code):
  D:\\Blender\\blender-4.5...\\blender.exe -b -P alat/render_dadu_blender.py -- <folder_keluaran>
"""
import math
import os
import random
import sys

import bpy
from mathutils import Quaternion, Vector

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(AKAR, "aset_sumber", "dadu.glb")
argumen = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
KELUAR = argumen[0] if argumen else os.path.join(AKAR, "aset_sumber", "render_dadu")
FRAME = 40          # gambar per angka
RESOLUSI = 320      # px; nanti diperkecil jadi 160 agar tepinya halus
SAMPEL = 48

# ------------------------------------------------------------------ adegan kosong + model
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=MODEL)
scene = bpy.context.scene

akar_model = next(o for o in scene.objects if o.parent is None)
bpy.context.view_layer.update()

# arah tiap sisi = rata-rata posisi titik (pip) sisi itu, dibulatkan ke sumbu terdekat
pusat = sum((o.matrix_world.translation for o in scene.objects if o.type == "MESH" and o.name.startswith("body")), Vector())
arah_sisi = {}
for n in range(1, 7):
    titik = [o.matrix_world.translation for o in scene.objects if o.name.startswith(f"pip_{n}_")]
    rata = sum(titik, Vector()) / len(titik) - pusat
    sumbu = max(range(3), key=lambda i: abs(rata[i]))
    v = Vector((0, 0, 0))
    v[sumbu] = 1 if rata[sumbu] > 0 else -1
    arah_sisi[n] = v
print("ARAH SISI:", {n: tuple(v) for n, v in arah_sisi.items()})
assert len({tuple(v) for v in arah_sisi.values()}) == 6, "arah sisi tidak unik"

# poros putar di tengah dadu; model diperbesar agar mudah diatur (aslinya 1,6 cm)
poros = bpy.data.objects.new("poros", None)
scene.collection.objects.link(poros)
poros.rotation_mode = "QUATERNION"
akar_model.parent = poros
akar_model.location -= pusat
poros.scale = (100, 100, 100)

# ------------------------------------------------------------------ kamera & cahaya
kamera_data = bpy.data.cameras.new("kamera")
kamera_data.lens = 85
kamera = bpy.data.objects.new("kamera", kamera_data)
scene.collection.objects.link(kamera)
scene.camera = kamera
elevasi, azimut, jarak = math.radians(64), math.radians(-28), 9.0  # tinggi: sisi atas (hasil) paling dominan
kamera.location = Vector((jarak * math.cos(elevasi) * math.sin(azimut), -jarak * math.cos(elevasi) * math.cos(azimut), jarak * math.sin(elevasi)))
kamera.rotation_euler = (Vector((0, 0, 0)) - kamera.location).to_track_quat("-Z", "Y").to_euler()


def lampu(nama, jenis, lokasi, energi, ukuran=3.0):
    data = bpy.data.lights.new(nama, jenis)
    data.energy = energi
    if jenis == "AREA":
        data.size = ukuran
    obj = bpy.data.objects.new(nama, data)
    obj.location = lokasi
    obj.rotation_euler = (Vector((0, 0, 0)) - Vector(lokasi)).to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(obj)


lampu("utama", "AREA", (-3.5, -3.0, 6.0), 900, 4.0)     # cahaya bohlam hangat dari kiri atas
lampu("isi", "AREA", (4.5, -2.0, 3.0), 250, 5.0)
lampu("tepi", "AREA", (0.5, 5.0, 4.0), 350, 3.0)
dunia = bpy.data.worlds.new("dunia")
dunia.use_nodes = True
dunia.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.6, 0.75, 1)
dunia.node_tree.nodes["Background"].inputs[1].default_value = 0.35
scene.world = dunia

# ------------------------------------------------------------------ pengaturan render
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPEL
scene.cycles.use_denoising = True
scene.render.film_transparent = True
scene.render.resolution_x = scene.render.resolution_y = RESOLUSI
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.view_transform = "Standard"

# ------------------------------------------------------------------ animasi berguling
ATAS = Vector((0, 0, 1))
acak = random.Random(26)
os.makedirs(KELUAR, exist_ok=True)
for n in range(1, 7):
    akhir = arah_sisi[n].rotation_difference(ATAS)                  # angka n menghadap ke atas
    akhir = Quaternion(ATAS, math.radians(acak.uniform(-25, 25))) @ akhir
    sumbu_a = Vector((acak.uniform(-0.4, 0.4), 1.0, acak.uniform(-0.2, 0.2))).normalized()  # guling utama
    sumbu_b = Vector((1.0, acak.uniform(-0.3, 0.3), acak.uniform(0.2, 0.6))).normalized()
    putaran_a = math.radians(acak.choice((-1, 1)) * acak.uniform(620, 760))
    putaran_b = math.radians(acak.choice((-1, 1)) * acak.uniform(160, 260))
    for i in range(FRAME):
        sisa = 1 - i / (FRAME - 1)
        poros.rotation_quaternion = Quaternion(sumbu_a, putaran_a * sisa) @ Quaternion(sumbu_b, putaran_b * sisa) @ akhir
        scene.render.filepath = os.path.join(KELUAR, f"dadu_{n}_{i:02d}.png")
        bpy.ops.render.render(write_still=True)
    print(f"ANGKA {n} SELESAI")
print("RENDER SELESAI", KELUAR)
