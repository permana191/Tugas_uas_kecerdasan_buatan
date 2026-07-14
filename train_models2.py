import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib
import os
import sys

print("Membaca dataset CSV...")
DATASET_PATH = 'data/aqi_dataset.csv'

try:
    df = pd.read_csv(DATASET_PATH)
    print("Dataset berhasil dimuat!")
    print("\n" + "="*50)
    print("DAFTAR NAMA KOLOM DI FILE CSV ANDA:")
    print(df.columns.tolist())
    print("="*50 + "\n")
except FileNotFoundError:
    print(f"ERROR: File tidak ditemukan di {DATASET_PATH}")
    sys.exit()

# Mengubah semua nama kolom di CSV menjadi huruf kecil dan menghapus spasi awal/akhir 
# agar kita tidak pusing memikirkan huruf besar/kecil (Case-Insensitive)
df.columns = df.columns.str.strip().str.lower()

# Karena semua sudah diubah ke huruf kecil, kita definisikan fiturnya dengan huruf kecil
# PERHATIAN: Jika nama kolom di CSV Anda bahasa Indonesia (misal: 'suhu', 'angin'), 
# ubah daftar di bawah ini agar sesuai.
fitur_kolom = ['temperature', 'humidity', 'wind_speed', 'traffic_density', 'industrial_activity']
target_kolom = 'aqi'

# Mengecek apakah kolom-kolom yang kita butuhkan benar-benar ada
missing_cols = [col for col in fitur_kolom + [target_kolom] if col not in df.columns]

if missing_cols:
    print(f"❌ ERROR: Kolom berikut tidak ditemukan di CSV Anda: {missing_cols}")
    print(f"💡 SOLUSI: Coba periksa daftar nama kolom di atas, lalu ubah variabel 'fitur_kolom' atau 'target_kolom' di baris 26-27 pada kodingan ini agar namanya sama persis (gunakan huruf kecil).")
    sys.exit()

X = df[fitur_kolom]
y = df[target_kolom]

print("Memulai pelatihan model Machine Learning...")

# Membuat dan melatih Imputer
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Membuat dan melatih Model Random Forest
model = RandomForestRegressor(n_estimators=150, max_depth=10, random_state=42)
model.fit(X_imputed, y)

# Memastikan folder 'models' tersedia
if not os.path.exists('models'):
    os.makedirs('models')

# MEN-GENERATE FILE
joblib.dump(imputer, 'models/imputer_aqi.pkl')
joblib.dump(model, 'models/random_forest_aqi_model.pkl')

print("=========================================================")
print("✅ SUKSES!")
print("File 'imputer_aqi.pkl' dan 'random_forest_aqi_model.pkl'")
print("telah berhasil diciptakan di dalam folder 'models/'.")
print("=========================================================")