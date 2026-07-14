from flask import Flask, render_template, request, jsonify, session, send_file
import joblib
import pandas as pd
import numpy as np
import os
import io

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Secret Key wajib ada untuk menggunakan fitur Session (Ekspor Data)
app.secret_key = "nexus_ai_secure_key_2026"

MODEL_PATH = 'models/random_forest_aqi_model.pkl'
IMPUTER_PATH = 'imputer_aqi.pkl'

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)

@app.route('/')
def home():
    return render_template('index.html', title="Beranda | AirGuard AI")

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    hasil_prediksi = None
    kategori = None
    warna = None
    warna_hex = None
    saran = None
    
    if request.method == 'POST':
        try:
            suhu = float(request.form['suhu'])
            kelembapan = float(request.form['kelembapan'])
            angin = float(request.form['angin'])
            lalu_lintas = float(request.form['lalu_lintas'])
            industri = float(request.form['industri'])
            
            input_data = pd.DataFrame([[suhu, kelembapan, angin, lalu_lintas, industri]], 
                                      columns=['temperature', 'humidity', 'wind_speed', 'traffic_density', 'industrial_activity'])
            
            input_imputed = imputer.transform(input_data)
            prediksi_aqi = model.predict(input_imputed)[0]
            hasil_prediksi = round(prediksi_aqi, 2)
            
            if hasil_prediksi <= 50:
                kategori = "Baik (Sehat)"
                warna = "success"
                warna_hex = "#10b981"
                saran = "Udara bersih. Ideal untuk aktivitas luar ruangan."
            elif hasil_prediksi <= 100:
                kategori = "Sedang"
                warna = "warning"
                warna_hex = "#f59e0b"
                saran = "Kualitas udara dapat diterima. Kelompok sensitif harap waspada."
            elif hasil_prediksi <= 150:
                kategori = "Tidak Sehat"
                warna = "orange"
                warna_hex = "#f97316"
                saran = "Peringatan: Udara kurang sehat! Gunakan masker medis di luar ruangan."
            else:
                kategori = "Berbahaya"
                warna = "danger"
                warna_hex = "#ef4444"
                saran = "BAHAYA! Polusi tinggi. Wajib gunakan masker N95."
            
            # Simpan data ke session untuk diekspor menjadi laporan
            session['laporan_terakhir'] = {
                'Suhu Udara (C)': suhu,
                'Kelembapan (%)': kelembapan,
                'Kecepatan Angin (km/h)': angin,
                'Kepadatan Lalu Lintas (1-10)': lalu_lintas,
                'Aktivitas Industri (1-100)': industri,
                'Skor AQI Prediksi': hasil_prediksi,
                'Status Kualitas Udara': kategori
            }
                
        except Exception as e:
            hasil_prediksi = f"Error: Masukkan data yang valid. Detail: {str(e)}"
            
    return render_template('prediksi.html', 
                           title="Dashboard Prediksi | AirGuard AI", 
                           hasil=hasil_prediksi, kategori=kategori, warna=warna, warna_hex=warna_hex, saran=saran)

# Rute Baru: Ekspor Laporan Prediksi (Download File Excel/CSV)
@app.route('/ekspor_laporan')
def ekspor_laporan():
    if 'laporan_terakhir' not in session:
        return "Tidak ada data untuk diekspor. Lakukan prediksi terlebih dahulu.", 400
    
    data = session['laporan_terakhir']
    df_export = pd.DataFrame([data])
    
    # Konversi ke format CSV dalam memori
    output = io.StringIO()
    df_export.to_csv(output, index=False)
    output.seek(0)
    
    # Mengirim file ke browser pengguna
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='Laporan_Prediksi_AQI.csv'
    )

@app.route('/radar')
def radar():
    return render_template('radar.html', title="Radar Atmosfer | AirGuard AI")

@app.route('/analisis')
def analisis():
    return render_template('analisis.html', title="Analisis Data | AirGuard AI")

@app.route('/metodologi')
def metodologi():
    return render_template('model.html', title="Metodologi Model | AirGuard AI")

if __name__ == '__main__':
    app.run(debug=True, port=5000)