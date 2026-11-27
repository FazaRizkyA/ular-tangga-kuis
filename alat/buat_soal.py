"""Menyusun soal.json: 900 soal = 3 kesulitan x 3 mapel x 100 soal.

- Matematika (semua tingkat): dibuat alat/buat_soal_mtk.py (kunci dihitung program).
- Penjas Orkes & Sejarah Indonesia:
    Mudah  -> aset_sumber/soal/<mapel>_mudah.txt
    Sedang -> 100 soal lama (v1.1 - v1.3) dari soal.json
    Sulit  -> aset_sumber/soal/<mapel>_sulit.txt
- Nomor id: Mudah 1-300, Sedang 301-600, Sulit 601-900
  (tiap tingkat: Matematika +1..100, Penjas +101..200, Sejarah +201..300).
- Letak kunci A-D diseimbangkan: tiap (mapel, tingkat) tepat 25 per huruf.

Jalankan dari folder source_code:  python alat/buat_soal.py
"""
import json
import os
import random
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "alat"))
from buat_soal_mtk import buat as buat_mtk  # noqa: E402

TINGKAT = ["Mudah", "Sedang", "Sulit"]
MAPEL = ["Matematika", "Penjas Orkes", "Sejarah Indonesia"]
FILE_TXT = {"Penjas Orkes": "penjas", "Sejarah Indonesia": "sejarah"}
HURUF = "ABCD"


def baca_txt(mapel, tingkat):
    path = os.path.join(AKAR, "aset_sumber", "soal", f"{FILE_TXT[mapel]}_{tingkat.lower()}.txt")
    hasil = []
    with open(path, encoding="utf-8") as f:
        for no, baris in enumerate(f, 1):
            baris = baris.strip()
            if not baris or baris.startswith("#"):
                continue
            bagian = [b.strip() for b in baris.split("|")]
            if len(bagian) != 6:
                raise ValueError(f"{path}:{no} harus 6 kolom, ada {len(bagian)}")
            materi, tanya, benar, *salah = bagian
            hasil.append({"kategori": mapel, "materi": materi, "tingkat": tingkat,
                          "pertanyaan": tanya, "benar": benar, "salah": salah})
    return hasil


def soal_lama(data_lama, mapel):
    hasil = []
    for s in data_lama:
        if s["kategori"] != mapel:
            continue
        benar = s["pilihan"][s["kunci"]]
        salah = [v for h, v in sorted(s["pilihan"].items()) if h != s["kunci"]]
        hasil.append({"kategori": mapel, "materi": s.get("materi", ""), "tingkat": "Sedang",
                      "pertanyaan": s["pertanyaan"], "benar": benar, "salah": salah,
                      "kunci_lama": s["kunci"], "pilihan_lama": s["pilihan"]})
    return hasil


def susun(kelompok, id_awal, rng):
    """Memberi id dan meletakkan jawaban benar di A-D (25 per huruf)."""
    if len(kelompok) != 100:
        raise ValueError(f"{kelompok[0]['kategori']} {kelompok[0]['tingkat']}: {len(kelompok)} soal, harus 100")
    kunci = list(HURUF * 25)
    rng.shuffle(kunci)
    hasil = []
    for i, s in enumerate(kelompok):
        if "pilihan_lama" in s:           # soal lama: susunan pilihan dipertahankan
            pilihan, k = s["pilihan_lama"], s["kunci_lama"]
        else:
            k = kunci[i]
            salah = list(s["salah"])
            rng.shuffle(salah)
            pilihan = {}
            for h in HURUF:
                pilihan[h] = s["benar"] if h == k else salah.pop()
        hasil.append({"id": id_awal + i, "kategori": s["kategori"], "materi": s["materi"],
                      "tingkat": s["tingkat"], "pertanyaan": s["pertanyaan"],
                      "pilihan": pilihan, "kunci": k})
    return hasil


def main():
    path_json = os.path.join(AKAR, "soal.json")
    with open(path_json, encoding="utf-8") as f:
        data_lama = json.load(f)
    if any("tingkat" in s for s in data_lama):
        # sudah format baru: soal lama = yang bertingkat Sedang
        data_lama = [s for s in data_lama if s.get("tingkat") == "Sedang"]
    rng = random.Random(2026)
    mtk = buat_mtk()
    semua = []
    for ti, tingkat in enumerate(TINGKAT):
        for mi, mapel in enumerate(MAPEL):
            if mapel == "Matematika":
                kelompok = [s for s in mtk if s["tingkat"] == tingkat]
            elif tingkat == "Sedang":
                kelompok = soal_lama(data_lama, mapel)
            else:
                kelompok = baca_txt(mapel, tingkat)
            semua += susun(kelompok, ti * 300 + mi * 100 + 1, rng)
    teks = [s["pertanyaan"] for s in semua]
    kembar = {t for t in teks if teks.count(t) > 1}
    if kembar:
        raise ValueError(f"soal kembar: {sorted(kembar)[:3]}")
    with open(path_json, "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(s, ensure_ascii=False) for s in semua) + "\n]\n")
    print(f"soal.json: {len(semua)} soal")


if __name__ == "__main__":
    main()
