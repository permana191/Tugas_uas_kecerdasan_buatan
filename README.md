# 🌍 AirGuard.AI - Sistem Peringatan Dini Polusi Udara

AirGuard.AI adalah sebuah aplikasi web *dashboard* cerdas yang dikembangkan untuk memprediksi Indeks Kualitas Udara (AQI) berdasarkan parameter iklim dan lingkungan. Proyek ini dibangun menggunakan algoritma **Random Forest Regressor** sebagai bentuk pemenuhan tugas *Project-Based Take Home Exam* Mata Kuliah Kecerdasan Buatan.

Sistem ini dirancang dengan antarmuka bertema *Cyberpunk / Terminal Dark Mode*, memberikan pengalaman pengguna tingkat lanjut layaknya perangkat lunak pemantauan (monitoring) sekelas industri.

## ✨ Fitur Utama
1. **Prediksi AQI Real-Time**: Menggunakan model Machine Learning (Random Forest) untuk memprediksi tingkat bahaya polusi udara.
2. **Geolokasi & Integrasi API Cuaca**: Mengambil data suhu, kelembapan, dan kecepatan angin aktual sesuai lokasi pengguna menggunakan *Open-Meteo API*.
3. **Radar Atmosfer Global**: Pemantauan pergerakan angin dan cuaca di seluruh belahan dunia secara interaktif melalui integrasi satelit *Windy.com*.
4. **Visualisasi Data (EDA)**: Menampilkan grafik korelasi, distribusi dataset, dan *Feature Importance* hasil *training* model.
5. **Ekspor Laporan**: Mengunduh hasil prediksi dan parameter cuaca ke dalam format `.csv` (Excel).
6. **Animasi Terminal Log**: Efek visual *Command Line Interface (CLI)* saat mengeksekusi model AI.

## 📁 Struktur Folder Proyek
```text
TUGAS_UAS_KECERDASAN_BUATAN/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Desain UI/UX Cyberpunk (Dark Mode)
│   │   ├── images/                # Menyimpan gambar grafik (1_heatmap, dsb)
│   │   └── js/
│   │       └── script.js          # Logika Jam Digital, ECharts, Animasi Terminal
│   └── templates/
│       ├── base.html              # Struktur Layout Induk (Sidebar & Header)
│       ├── index.html             # Halaman Beranda
│       ├── prediksi.html          # Halaman Form AI & Speedometer
│       ├── radar.html             # Halaman Radar Atmosfer
│       ├── analisis.html          # Halaman Visualisasi EDA
│       └── model.html             # Halaman Metodologi & Evaluasi AI
│
├── data/
│   └── aqi_dataset.csv            # Dataset tabular publik (sumber: Kaggle)
│
├── grafik_jurnal/                 # Folder output hasil render visualisasi matplotlib
│
├── models/
│   └── random_forest_aqi_model.pkl # Model AI yang telah dilatih (Tuned)
│
├── .gitignore
├── app.py                         # File Utama Backend (Flask & Routing)
├── imputer_aqi.pkl                # File model imputer (penanganan missing values)
├── Procfile                       # Konfigurasi deployment server
├── README.md                      # Dokumentasi proyek
├── requirements.txt               # Daftar pustaka (library) Python
└── train_models.py                # Script pelatihan ML, evaluasi metrik, & EDA

## 🛠️ Persyaratan Sistem & Instalasi
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal Python 3.8+ di komputer Anda.

Clone repositori ini (atau unduh zip folder proyek):

Bash
git clone [https://github.com/username-anda/airguard-ai.git](https://github.com/username-anda/airguard-ai.git)
cd airguard-ai
Buat dan aktifkan Virtual Environment (Sangat Direkomendasikan):

Bash
python -m venv .venv

# Untuk Windows:
.venv\Scripts\activate

# Untuk Mac/Linux:
source .venv/bin/activate
Instal seluruh pustaka yang dibutuhkan:

Bash
pip install -r requirements.txt
🚀 Cara Menjalankan Aplikasi
Terdapat dua skrip utama dalam proyek ini yang dapat Anda eksekusi.

A. Melatih Ulang Model AI (Opsional)
Jika Anda ingin melatih ulang algoritma Random Forest, membersihkan data outlier, atau merender ulang grafik visualisasi untuk laporan jurnal, jalankan perintah berikut di terminal:

Bash
python train_models.py
(Skrip ini akan memperbarui file random_forest_aqi_model.pkl, file imputer_aqi.pkl, dan meng-generate ulang 5 gambar PNG di dalam folder grafik_jurnal/).

B. Menjalankan Web Dashboard Utama
Untuk menghidupkan server Flask dan menggunakan aplikasi antarmuka prediksi:

Bash
python app.py
Setelah server berjalan dan terminal menampilkan pesan Running on http://127.0.0.1:5000, buka browser web Anda (Chrome/Edge/Firefox) dan akses URL tersebut.

📊 Metrik Evaluasi Model AI
Model Random Forest pada aplikasi ini telah melalui proses pembersihan data outlier dan Hyperparameter Tuning (max_depth=10, n_estimators=150). Evaluasi menggunakan data uji (20%) menghasilkan:

Mean Absolute Error (MAE): 37.03

Mean Squared Error (MSE): 1994.54

R-Squared (R² Score): 0.29 (29%)

🔗 Tautan Deployment
Aplikasi ini telah berhasil di-deploy dan dapat diakses secara publik menggunakan domain mandiri melalui tautan berikut:
https://www.nama-domain-anda.my.id

Dikembangkan oleh Sigit Miraj Permana - Mahasiswa Teknik Informatika, Universitas Bale Bandung (UNIBBA).