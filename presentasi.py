from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# Menggunakan path lengkap sesuai yang kamu berikan
FILE_PATH = r"C:\Users\Vandr\Downloads\opendata.jabarprov.go.id_dataset_od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_csv\static\download\dinkes-od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_data.csv"

def get_plot_url():
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route('/')
def index():
    # Cek apakah file ada di lokasi tersebut
    if not os.path.exists(FILE_PATH):
        return f"Error: File tidak ditemukan di lokasi: {FILE_PATH}. Pastikan path sudah benar."

    # --- PROSES DATA (Logika dari Soal_Pandas_Kelompok) ---
    df = pd.read_csv(FILE_PATH)
    
    # [cite_start]Mengubah nama kolom agar mudah digunakan [cite: 10]
    df.rename(columns={
        'nama_kabupaten_kota': 'kab_kota', 
        'jumlah_penderita_dm': 'jumlah_dm'
    }, inplace=True)

    # [cite_start]C.17: Membuat kolom kategori_dm [cite: 22, 23, 24, 25]
    def get_kategori(jumlah):
        if jumlah >= 100000: return "Tinggi"
        elif jumlah >= 50000: return "Sedang"
        else: return "Rendah"
    df['kategori_dm'] = df['jumlah_dm'].apply(get_kategori)

    # --- PENYIAPAN VISUALISASI (Matplotlib) ---
    
    # [cite_start]D.21: Grafik Garis Tren Tahunan [cite: 33, 34, 35, 36]
    total_per_tahun = df.groupby('tahun')['jumlah_dm'].sum().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(total_per_tahun['tahun'], total_per_tahun['jumlah_dm'], marker='o', color='red')
    plt.title('Tren Total Penderita DM Jawa Barat Per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Total Jumlah Penderita')
    plot_tren = get_plot_url()

    # [cite_start]D.22: Grafik Bar Horizontal Top 10 Kab/Kota 2019 [cite: 37, 38]
    df_2019 = df[df['tahun'] == 2019].copy()
    top_10_2019 = df_2019.sort_values(by='jumlah_dm', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_2019['kab_kota'], top_10_2019['jumlah_dm'], color='teal')
    plt.gca().invert_yaxis()
    plt.title('Top 10 Kabupaten/Kota dengan Penderita DM Tertinggi (2019)')
    plot_top10 = get_plot_url()

    # [cite_start]D.23: Pie Chart Proporsi Kategori DM 2019 [cite: 39]
    proporsi_dm = df_2019.groupby('kategori_dm')['jumlah_dm'].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(proporsi_dm, labels=proporsi_dm.index, autopct='%1.1f%%', startangle=90)
    plt.title('Proporsi Jumlah Penderita DM Berdasarkan Kategori (2019)')
    plot_pie = get_plot_url()

    # [cite_start]A.1: Menampilkan 5 baris pertama data [cite: 4]
    tabel_html = df.head(5).to_html(classes='table table-bordered table-striped')

    return render_template('index.html', 
                           tabel=tabel_html, 
                           plot_tren=plot_tren, 
                           plot_top10=plot_top10, 
                           plot_pie=plot_pie)

if __name__ == '__main__':
    app.run(debug=True)