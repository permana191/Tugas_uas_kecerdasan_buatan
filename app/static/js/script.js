document.addEventListener('DOMContentLoaded', () => {

    // 0. JAM DIGITAL LIVE (TOP HEADER)
    const timeDisplay = document.getElementById('time');
    const dateDisplay = document.getElementById('date');
    
    if (timeDisplay && dateDisplay) {
        function updateClock() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('id-ID', { hour12: false });
            timeDisplay.textContent = timeString;
            
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            const dateString = now.toLocaleDateString('id-ID', options);
            dateDisplay.textContent = dateString;
        }
        setInterval(updateClock, 1000);
        updateClock(); 
    }

    // 1. FITUR GEOLOKASI (API CUACA)
    const btnGeo = document.getElementById('btn-geo');
    if (btnGeo) {
        btnGeo.addEventListener('click', () => {
            btnGeo.innerHTML = '⏳ Menghubungkan ke satelit koordinat...';
            
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    
                    fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m`)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('suhu').value = data.current.temperature_2m;
                        document.getElementById('kelembapan').value = data.current.relative_humidity_2m;
                        document.getElementById('angin').value = data.current.wind_speed_10m;
                        
                        btnGeo.innerHTML = '✅ Sukses! Injeksi data iklim selesai.';
                        btnGeo.style.color = '#10b981';
                        btnGeo.style.borderColor = '#10b981';
                        
                        setTimeout(() => {
                            btnGeo.innerHTML = '📍 Gunakan Kondisi Cuaca Saat Ini (GPS)';
                            btnGeo.style.color = ''; btnGeo.style.borderColor = '';
                        }, 3000);
                    }).catch(() => { btnGeo.innerHTML = '❌ Gagal akses server data'; });
                }, () => { btnGeo.innerHTML = '❌ Izin lokasi ditolak'; });
            }
        });
    }

    // 2. FITUR VISUALISASI SPEEDOMETER
    const gaugeContainer = document.getElementById('gauge-chart');
    if (gaugeContainer && window.aqiResult) {
        const chart = echarts.init(gaugeContainer);
        const aqiValue = window.aqiResult;
        const mainColor = window.aqiColor;

        const option = {
            series: [{
                type: 'gauge',
                startAngle: 180, endAngle: 0,
                min: 0, max: 300, splitNumber: 6,
                itemStyle: { color: mainColor, shadowColor: mainColor, shadowBlur: 10 },
                progress: { show: true, width: 25 },
                pointer: { show: false }, 
                axisLine: { lineStyle: { width: 25, color: [[1, 'rgba(255,255,255,0.05)']] } },
                axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false },
                detail: {
                    valueAnimation: true, fontSize: 45, fontWeight: 'bold',
                    color: mainColor, offsetCenter: [0, '-10%'], formatter: '{value}'
                },
                data: [{ value: aqiValue }]
            }]
        };
        chart.setOption(option);
    }

    // 3. EFEK TERMINAL LOG (MENGGANTIKAN SUBMIT BIASA)
    const form = document.getElementById('prediksi-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Mencegah form langsung tersubmit jika terminal belum selesai
            if (!form.dataset.terminalDone) {
                e.preventDefault(); 
                
                const btn = document.getElementById('btn-ai');
                btn.innerHTML = '⚙️ Executing AI Protocol...';
                btn.disabled = true;

                // Tampilkan Kotak Terminal
                const terminalBox = document.getElementById('terminal-log');
                const terminalContent = document.getElementById('terminal-content');
                terminalBox.style.display = 'block';
                terminalContent.innerHTML = '';

                // Skrip Logika Teks Terminal
                const lines = [
                    "> Menginisialisasi koneksi server...",
                    "> Validasi matriks data input... [OK]",
                    "> Memuat model Random Forest Regressor... [OK]",
                    "> Menjalankan fungsi predict()...",
                    "> Kalkulasi metrik selesai. Mengalihkan..."
                ];

                let lineIndex = 0;
                function typeLine() {
                    if (lineIndex < lines.length) {
                        terminalContent.innerHTML += lines[lineIndex] + '<br>';
                        lineIndex++;
                        setTimeout(typeLine, 600); // 0.6 detik per baris
                    } else {
                        // Setelah animasi selesai, submit form sesungguhnya
                        form.dataset.terminalDone = 'true';
                        form.submit();
                    }
                }
                
                // Mulai Animasi Ketik Terminal
                typeLine();
            }
        });
    }
});