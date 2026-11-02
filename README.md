# Awasin — Pesan mencurigakan? Awasin yang cek duluan.

Prototipe web (PWA) pemindai pesan penipuan berbahasa Indonesia untuk tugas kuliah. Seluruh analisis berjalan di browser; tidak ada pesan yang dikirim ke server.

## Sistem (3 lapis, hibrida)
1. **Aturan berbobot** — PIN/OTP, link mencurigakan, urgensi, hadiah, bayar di muka, ancaman data, nomor rekening, dll. (juga memahami bahasa santai lewat normalisasi: "dapet", "norek", "tf", "dp").
2. **Model teks** — TF-IDF n-gram karakter (2-4) + Regresi Logistik, dilatih dari `data/dataset_awasin_v3.csv`. N-gram karakter tahan terhadap typo dan singkatan. Model diekspor ke JSON dan dijalankan langsung di JavaScript.
3. **Cross-check** — mencocokkan ke daftar contoh kecil (bukan data CekRekening.id asli).

Skor akhir = rata-rata skor aturan dan probabilitas "bukan aman" dari model → BERBAHAYA / WASPADA / TIDAK TERDETEKSI. Tombol "Simulasikan pesan masuk" hanya simulasi; membaca notifikasi asli butuh aplikasi Android native.

## Struktur
- `index.html`, `manifest.webmanifest`, `sw.js`, `icon-*.png` — aplikasi (model sudah tertanam di `index.html`)
- `data/dataset_awasin_v3.csv` — 700 sampel, 7 kelas seimbang; kolom `sumber` menandai data sintetis
- `data/test_realistic.csv` — 28 pesan uji terpisah (tidak dipakai training)
- `ml/build_dataset.py`, `ml/train_model.py`, `ml/awasin_training.ipynb` (Colab), `ml/model.json`

## Melatih ulang
```
pip install scikit-learn pandas
python ml/build_dataset.py   # opsional, membuat ulang dataset sintetis
python ml/train_model.py     # evaluasi + ekspor ml/model.json
```
Setelah melatih ulang, tanam isi `ml/model.json` ke variabel `MODEL` di `index.html`.

## Keterbatasan (jujur)
- Dataset sebagian besar **sintetis** (template). Data uji hanya 28 pesan yang ditulis sendiri dengan gaya mirip template, jadi angka akurasinya **optimistis**. Uji dengan pesan asli (nomor/nama disamarkan) sebelum mengklaim akurasi.
- Bukan pengganti pengecekan resmi (CekRekening.id, IASC OJK 157, Lapor.go.id).

## Deploy ke GitHub Pages
Unggah semua file → Settings → Pages → branch `main`, folder root. Buka link di Chrome HP → ⋮ → Tambahkan ke layar utama.
