# Ular Tangga Kuis

Game papan edukasi ular tangga berbasis kuis, 100% offline, dibuat dengan Python 3.12 + Pygame.
Project Sumatif Akhir Semester Ganjil, SMK Krian 1 Sidoarjo 2026/2027 (XI PBTG).

Setiap giliran dimulai dengan satu soal pilihan ganda (waktu 30 detik). Jawaban benar memberi +10 poin
dan membuka tombol **Kocok Dadu**; jawaban salah membuat giliran dilewati. Tangga: naik +5 poin.
Ular: turun. Pemain pertama yang mendarat **tepat** di petak 64 menang (kelebihan langkah memantul).

Papan 8 x 8 = 64 petak dengan tiga tingkat kesulitan:

| Kesulitan | Tangga | Ular | Bot menjawab benar |
| --- | --- | --- | --- |
| Mudah | 6 | 3 | sekitar 45% |
| Sedang | 5 | 5 | sekitar 65% |
| Sulit | 4 | 8 | sekitar 85% |

Soal yang sudah keluar tidak akan muncul lagi, termasuk saat **Main Lagi**. Bila soal kategori terpilih habis,
soal diambil dari kategori lain; baru setelah ke-300 soal keluar semua, bank soal diacak ulang.

## Anggota & peran

| Peran | Nama | Kontribusi |
| --- | --- | --- |
| Perancang Logika/OOP | (isi nama) | pemain.py, petak.py, papan.py, game.py |
| Desainer GUI & Aset | (isi nama) | main.py, tampilan.py, alat/buat_aset.py |
| Penyusun Bank Soal | (isi nama) | soal.json, soal.py |
| Packager/Tester | (isi nama) | installer.iss, build.bat, alat/uji_logika.py |

## Cara menjalankan (dari kode sumber)

```bat
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python main.py
```

Kontrol: klik mouse, atau keyboard **A-D / 1-4** untuk menjawab, **Spasi** untuk kocok dadu,
**M** suara nyala/mati, **F11** atau **Alt+Enter** layar penuh, **Esc** keluar (dengan konfirmasi).

Rumus di `soal.json` memakai tanda sederhana yang digambar oleh `rumus.py`: `\frac{a}{b}` untuk pecahan,
`x^{2}` untuk pangkat, `√{48}` untuk akar, dan `∘` untuk komposisi fungsi.

## Cara build installer

Butuh Inno Setup 6. Dari folder `source_code` jalankan:

```bat
build.bat
```

Skrip ini menjalankan uji logika, lalu PyInstaller (`dist\UlarTanggaKuis\`), lalu Inno Setup.
Hasilnya: `..\installer\Setup_UlarTanggaKuis_v<VERSI>.exe`. Nomor versi cukup diubah di `config.py` (`VERSI`);
menu dan installer mengikuti otomatis.

## Riwayat versi

| Versi | Perubahan |
| --- | --- |
| 1.1 | Papan 8 x 8 (64 petak); tingkat kesulitan Mudah/Sedang/Sulit; 300 soal tanpa pengulangan; rumus Matematika ditulis bersusun (pecahan, pangkat, akar); dadu 3D hasil render Blender; tampilan digambar di resolusi layar sehingga tajam saat layar penuh (F11) |
| 1.0 | Rilis pertama: papan 6 x 6, 45 soal, mode Pass & Play dan vs Bot |

## Struktur

| File | Isi |
| --- | --- |
| `main.py` | Class `App`: loop Pygame, 5 layar (menu, cara bermain, setup, papan, pemenang) |
| `game.py` | Class `GameManager`: game state, giliran, skor, timer, log |
| `pemain.py` | Class `Pemain` dan turunannya `Bot` |
| `petak.py` | Class `Petak` dan turunannya `PetakTangga`, `PetakUlar`, `PetakFinish` |
| `papan.py` | Class `Papan`: 64 petak, letak tangga & ular sesuai kesulitan, gambar papan |
| `soal.py` | Class `Soal` dan `BankSoal` (membaca `soal.json`) |
| `dadu.py` | Class `Dadu` |
| `tampilan.py` | Komponen gambar: papan cat, bohlam, karcis, tombol, kolom teks |
| `rumus.py` | Class `PenataRumus`: menggambar rumus seperti tulisan (pecahan bersusun bergaris, pangkat di atas, akar bergaris atas) |
| `dadu3d.py` | Class `DaduRender`: animasi dadu 3D hasil render Blender dari `aset_sumber/dadu.glb`; class `Dadu3D`: dadu kubus buatan kode sebagai cadangan |
| `aset_sumber/` | Model `dadu.glb` (tidak ikut installer). Render ulang: `D:\Blender\...\blender.exe -b -P alat\render_dadu_blender.py`, lalu `python alat\buat_sheet_dadu.py` |
| `config.py` | Konstanta, palet warna, `resource_path()` |
| `soal.json` | 300 soal: 100 Matematika (aljabar dasar, eksponen, pangkat, akar, fungsi komposisi), 100 Penjas Orkes (renang, sepak bola, bulu tangkis), 100 Sejarah Indonesia |
| `icon.ico`, `assets/` | Ikon, font (.ttf), efek suara (.wav) |
| `alat/` | Alat pengembang: uji logika, pembuat aset, penangkap layar (tidak ikut installer) |

## Di mana prinsip OOP berada (untuk tanya-jawab)

Cari komentar penanda `# ENCAPSULATION`, `# INHERITANCE`, `# POLYMORPHISM` di kode.

- **Encapsulation**: `Pemain` (atribut `__skor`, `__posisi`; setter `skor` menolak nilai negatif;
  `pindah_ke()` menolak petak di luar 1-64), juga `Soal`, `BankSoal`, `Dadu`, `Papan`, `GameManager`.
- **Inheritance**: `Petak` → `PetakTangga`, `PetakUlar`, `PetakFinish`; `Pemain` → `Bot`
  (semua memanggil `super().__init__()`).
- **Polymorphism**: `GameManager.kocok_dadu()` cukup memanggil `petak.efek(pemain)`; tiap jenis
  petak punya efek sendiri. `Papan.gambar()` memanggil `petak.gambar()` dan `petak.gambar_label()`.
  `pemain.pilih_jawaban(soal)`: manusia mengembalikan `None` (menunggu klik), `Bot` memilih sendiri.

## Exception handling

`BankSoal.muat()` membungkus pembacaan `soal.json` dengan `try ... except FileNotFoundError`,
`except json.JSONDecodeError`, dan `except Exception`. Bila file hilang atau rusak, menu menampilkan
pesan dan tombol Mulai dinonaktifkan; program tidak crash. Soal yang formatnya salah dilewati.
Font dan suara yang gagal dimuat juga ditangani (font bawaan / tanpa suara). Kesalahan tak terduga
saat bermain ditangkap di loop utama dan aplikasi kembali ke Menu Utama dengan pesan.

## Pengujian

`venv\Scripts\python alat\uji_logika.py` menguji otomatis kasus T2, T4-T12, T14 dari PRD, aturan kesulitan, soal tidak berulang,
dan apakah semua soal muat di layar (44 pemeriksaan). `alat\uji_simulasi.py` memainkan 12 permainan penuh
tanpa layar di semua mode dan kesulitan. T1, T3, T13 diuji manual lewat aplikasi dan installer.

## Sumber aset

Lihat `assets/SUMBER_ASET.txt`.

## Unduh

Installer Windows siap pakai (offline) ada di halaman **Releases** repo ini:
`Setup_UlarTanggaKuis_v1.1.exe`.

## Lisensi

Kode program dirilis dengan lisensi [MIT](LICENSE). Font Bungee dan Atkinson Hyperlegible memakai
SIL Open Font License 1.1 (file lisensinya ada di `assets/fonts/`).
