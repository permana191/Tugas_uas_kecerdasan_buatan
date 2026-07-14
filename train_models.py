import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Set style untuk grafik
sns.set_theme(style="whitegrid")
output_dir = "grafik_jurnal"
os.makedirs(output_dir, exist_ok=True)

print("1. Memuat dataset aqi_dataset.csv...")
df = pd.read_csv('aqi_dataset.csv')

# ==========================================
# PENGHAPUSAN OUTLIER
# ==========================================
print("2. Preprocessing: Menghapus Data Outlier (Pencilan) menggunakan metode IQR...")
Q1 = df['AQI'].quantile(0.25)
Q3 = df['AQI'].quantile(0.75)
IQR = Q3 - Q1
batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

# Memfilter dataset
df_clean = df[(df['AQI'] >= batas_bawah) & (df['AQI'] <= batas_atas)].copy()

# ==========================================
# VISUALISASI EDA (DARI DATA BERSIH)
# ==========================================
print("3. Menghasilkan 3 visualisasi Eksplorasi Data (EDA) dari data bersih...")

# Grafik 1: Heatmap Korelasi
plt.figure(figsize=(8, 6))
correlation_matrix = df_clean.corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matriks Korelasi Parameter Kualitas Udara (Data Bersih)", pad=15)
plt.tight_layout()
plt.savefig(f"{output_dir}/1_heatmap_korelasi.png", dpi=300)
plt.close()

# Grafik 2: Histogram Distribusi
plt.figure(figsize=(8, 5))
sns.histplot(df_clean['AQI'], bins=30, kde=True, color="crimson")
plt.title("Distribusi Indeks Kualitas Udara (AQI) - Tanpa Outlier", pad=15)
plt.xlabel("Nilai AQI")
plt.ylabel("Frekuensi (Jumlah Data)")
plt.tight_layout()
plt.savefig(f"{output_dir}/2_distribusi_aqi.png", dpi=300)
plt.close()

# Grafik 3: Scatter Plot Industri vs AQI
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_clean, x='industrial_activity', y='AQI', alpha=0.5, color="darkblue")
plt.title("Korelasi Aktivitas Industri terhadap Nilai AQI", pad=15)
plt.xlabel("Tingkat Aktivitas Industri")
plt.ylabel("Nilai AQI")
plt.tight_layout()
plt.savefig(f"{output_dir}/3_scatter_industri_aqi.png", dpi=300)
plt.close()

# ==========================================
# PREPROCESSING & TRAINING MODEL
# ==========================================
print("4. Preprocessing: Menangani Missing Values...")
X_clean = df_clean[['temperature', 'humidity', 'wind_speed', 'traffic_density', 'industrial_activity']]
y_clean = df_clean['AQI']

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_clean)

print("5. Membagi data latih (80%) dan data uji (20%)...")
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_clean, test_size=0.2, random_state=42)

print("6. Melatih model Random Forest Regressor dengan Tuning Parameter...")
rf_model = RandomForestRegressor(n_estimators=150, max_depth=10, min_samples_split=10, random_state=42)
rf_model.fit(X_train, y_train)

# ==========================================
# EVALUASI & VISUALISASI HASIL (METRIK & GRAFIK 4-5)
# ==========================================
print("7. Mengevaluasi model dan menghasilkan sisa visualisasi...")
y_pred = rf_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n--- HASIL EVALUASI METRIK REGRESI (SETELAH TUNING) ---")
print(f"Mean Absolute Error (MAE) : {mae:.2f}")
print(f"Mean Squared Error (MSE)  : {mse:.2f}")
print(f"R-squared (R2 Score)      : {r2:.2f}\n")

# Grafik 4: Aktual vs Prediksi
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color="teal")
plt.plot([y_clean.min(), y_clean.max()], [y_clean.min(), y_clean.max()], 'r--', lw=2)
plt.title(f"Perbandingan Nilai Aktual vs Prediksi (R2: {r2:.2f})", pad=15)
plt.xlabel("AQI Aktual (Ground Truth)")
plt.ylabel("AQI Hasil Prediksi Model")
plt.tight_layout()
plt.savefig(f"{output_dir}/4_aktual_vs_prediksi.png", dpi=300)
plt.close()

# Grafik 5: Feature Importance (Bebas FutureWarning)
plt.figure(figsize=(8, 5))
importances = rf_model.feature_importances_
fitur = ['Temperature', 'Humidity', 'Wind Speed', 'Traffic Density', 'Industrial Activity']
indices = np.argsort(importances)[::-1]
fitur_terurut = [fitur[i] for i in indices]
importances_terurut = [importances[i] for i in indices]

# Perbaikan parameter warna pada Seaborn versi terbaru
sns.barplot(x=importances_terurut, y=fitur_terurut, hue=fitur_terurut, palette="viridis", legend=False)
plt.title("Tingkat Kepentingan Fitur (Feature Importance)", pad=15)
plt.xlabel("Bobot Pengaruh (Skala 0-1)")
plt.ylabel("Parameter Lingkungan")
plt.tight_layout()
plt.savefig(f"{output_dir}/5_feature_importance.png", dpi=300)
plt.close()

# ==========================================
# MENYIMPAN MODEL
# ==========================================
print("8. Menyimpan model hasil tuning untuk Flask...")
joblib.dump(rf_model, 'random_forest_aqi_model.pkl')
joblib.dump(imputer, 'imputer_aqi.pkl')
print("Selesai! 5 Grafik terbaru dan Model yang lebih akurat siap digunakan.")