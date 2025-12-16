import pandas as pd
import matplotlib.pyplot as plt


FILE_PATH = r"C:\Users\Vandr\Downloads\opendata.jabarprov.go.id_dataset_od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_csv\static\download\dinkes-od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_data.csv"

try:
    data_dm = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print("Error: File data tidak ditemukan. Pastikan path sudah benar.")
    exit()

# Mengubah nama kolom yang panjang menjadi lebih ringkas agar mudah diketik
data_dm.rename(columns={'nama_kabupaten_kota': 'kab_kota', 
                        'jumlah_penderita_dm': 'jumlah_dm'}, inplace=True)



# =============== A. SOAL DASAR (Pengenalan DataFrame) =================


print("--- A. Soal Dasar ---")

# 1 Import library pandas, baca file data_dm_jabar.csv ke dalam DataFrame bernama df, lalu tampilkan 5 baris pertama.
print("\n1. 5 Baris Pertama:")
print(data_dm.head())

# 2	Tampilkan 5 baris terakhir dari df.
print("\n2. 5 Baris Terakhir:")
print(data_dm.tail())

# 3.Tampilkan informasi struktur DataFrame menggunakan df.info().
print("\n3. Struktur Data (df.info()):")
data_dm.info()

# 4.Tampilkan statistik deskriptif untuk kolom numerik (misalnya jumlah_penderita_dm dan tahun) menggunakan df.describe().
print("\n4. Statistik Deskriptif (jumlah_dm dan tahun):")
print(data_dm[['jumlah_dm', 'tahun']].describe())

# 5.Tampilkan daftar nilai unik dari kolom tahun.
print("\n5. Tahun yang Tersedia:")
print(data_dm['tahun'].unique())

# 6.Tampilkan daftar nilai unik dari kolom nama_kabupaten_kota dan hitung berapa banyak kabupaten/kota yang tercatat.
unique_kab = data_dm['kab_kota'].unique()
print("\n6. Daftar Kabupaten/Kota Unik (dan jumlahnya):")
print(unique_kab)
print(f"   Total Kab/Kota: {len(unique_kab)}")

# 7. kolom
print("\n7. Subset Kolom (kab_kota, jumlah_dm, tahun):")
print(data_dm[['kab_kota', 'jumlah_dm', 'tahun']].head())



# =============== B. SOAL PENGOLAHAN DATA (Filtering & Sorting) ==============


print("\n--- B. Soal Pengolahan Data ---")

# 8.Tampilkan semua baris data untuk tahun 2019 saja.
df_2019 = data_dm[data_dm['tahun'] == 2019].copy()
print("\n8. Data Tahun 2019 (5 baris pertama):")
print(df_2019.head())

# 9.Tampilkan semua kabupaten/kota yang memiliki jumlah_penderita_dm lebih dari 100.000 orang (tahun berapa pun).
df_diatas_100k = data_dm[data_dm['jumlah_dm'] > 100000]
print("\n9. Data Jumlah DM > 100.000:")
print(df_diatas_100k)

# 10.Urutkan DataFrame berdasarkan jumlah_penderita_dm dari terbesar ke terkecil.
df_sort_dm = data_dm.sort_values(by='jumlah_dm', ascending=False)
print("\n10. Diurutkan berdasarkan jumlah DM (Desc):")
print(df_sort_dm.head())

# 11.Urutkan DataFrame berdasarkan tahun terlebih dahulu, lalu jumlah_penderita_dm dari yang terbesar.
df_sort_multi = data_dm.sort_values(by=['tahun', 'jumlah_dm'], ascending=[True, False])
print("\n11. Diurutkan berdasarkan Tahun dan Jumlah DM:")
print(df_sort_multi.head(10))

# 12.Tampilkan 10 kabupaten/kota dengan jumlah penderita DM tertinggi pada tahun 2019.
top_10_2019 = df_2019.sort_values(by='jumlah_dm', ascending=False).head(10)
print("\n12. Top 10 Kab/Kota DM Tahun 2019:")
print(top_10_2019[['kab_kota', 'jumlah_dm']])

# 13.Tampilkan semua baris data untuk satu kabupaten pilihanmu (misal: KABUPATEN BOGOR) di semua tahun yang tersedia.
kab_target = 'KABUPATEN BOGOR'
df_bogor = data_dm[data_dm['kab_kota'] == kab_target]
print(f"\n13. Data untuk {kab_target} di Semua Tahun:")
print(df_bogor)



#================== C. SOAL AGREGASI & TRANSFORMASI ==================


print("\n--- C. Soal Agregasi & Transformasi ---")

# 14.Kelompokkan data berdasarkan tahun dan hitung total jumlah_penderita_dm per tahun di Jawa Barat.
total_per_tahun = data_dm.groupby('tahun')['jumlah_dm'].sum().reset_index()
total_per_tahun.rename(columns={'jumlah_dm': 'total_dm_jabar'}, inplace=True)
print("\n14. Total DM Jawa Barat Per Tahun:")
print(total_per_tahun)

# 15.Kelompokkan data berdasarkan nama_kabupaten_kota dan hitung rata-rata jumlah_penderita_dm tiap kabupaten/kota (jika terdapat lebih dari satu tahun).
avg_per_kab = data_dm.groupby('kab_kota')['jumlah_dm'].mean().sort_values(ascending=False).round(0).astype(int)
print("\n15. Rata-rata Jumlah DM per Kab/Kota (Top 5):")
print(avg_per_kab.head())

# 16.Tentukan kabupaten/kota dengan total jumlah_penderita_dm tertinggi dan terendah di seluruh tahun.
total_kumulatif = data_dm.groupby('kab_kota')['jumlah_dm'].sum()
kab_max = total_kumulatif.idxmax()
val_max = total_kumulatif.max()
kab_min = total_kumulatif.idxmin()
val_min = total_kumulatif.min()

print("\n16. Kab/Kota Total DM Kumulatif (Seluruh Tahun):")
print(f"   Tertinggi: {kab_max} ({val_max:,} orang)")
print(f"   Terendah: {kab_min} ({val_min:,} orang)")


# 17.Buat kolom baru bernama kategori_dm dengan aturan berbasis jumlah_penderita_dm:
def get_kategori(jumlah):
    if jumlah >= 100000:
        return "Tinggi"
    elif jumlah >= 50000:
        return "Sedang"
    else:
        return "Rendah"

data_dm['kategori_dm'] = data_dm['jumlah_dm'].apply(get_kategori)
print("\n17. Kolom 'kategori_dm' berhasil dibuat (5 baris pertama):")
print(data_dm[['kab_kota', 'tahun', 'jumlah_dm', 'kategori_dm']].head())


# 18.Untuk setiap tahun, hitung persentase jumlah penderita DM per kabupaten/kota terhadap total jumlah penderita DM di tahun tersebut, lalu simpan dalam kolom baru bernama persentase_tahun
data_dm = pd.merge(data_dm, total_per_tahun, on='tahun', how='left')

data_dm['persentase_tahun'] = (data_dm['jumlah_dm'] / data_dm['total_dm_jabar']) * 100

print("\n18. Kolom 'persentase_tahun' (Top 5 kontributor):")
print(data_dm[['kab_kota', 'tahun', 'jumlah_dm', 'persentase_tahun']].sort_values(by='persentase_tahun', ascending=False).head())


# 19. Tabel Ringkas (Tahun, Total DM, Jumlah Kab/Kota)
tabel_ringkas = data_dm.groupby('tahun').agg(
    total_dm=('jumlah_dm', 'sum'),
    jumlah_kab=('kab_kota', 'nunique')
).reset_index()
print("\n19. Tabel Ringkas Tren Data:")
print(tabel_ringkas)



# ====================== D. SOAL ANALISIS & VISUALISASI (Matplotlib) ===================

print("\n--- D. Soal Visualisasi ---")

# 20.Buat grafik bar yang menampilkan jumlah_penderita_dm untuk setiap kabupaten/kota pada tahun 2019.
plt.figure(figsize=(14, 6))
plt.bar(df_2019['kab_kota'], df_2019['jumlah_dm'])
plt.xlabel('Kabupaten/Kota')
plt.ylabel('Jumlah Penderita DM')
plt.title('Jumlah Penderita DM di Jawa Barat (2019)')
plt.xticks(rotation=90, fontsize=8) 
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()

# 21.Buat grafik garis (line chart) yang menampilkan total jumlah penderita DM Jawa Barat per tahun.
plt.figure(figsize=(10, 5))
plt.plot(total_per_tahun['tahun'], total_per_tahun['total_dm_jabar'], 
         marker='o', linestyle='-', color='red', label='Total DM Jabar')
plt.xlabel('Tahun')
plt.ylabel('Total Jumlah Penderita DM')
plt.title('Tren Total Penderita DM Jawa Barat')
plt.xticks(total_per_tahun['tahun']) 
plt.grid(True, linestyle='--')
plt.legend()
plt.tight_layout()
plt.show()


# 22.Buat grafik bar horizontal untuk menampilkan 10 kabupaten/kota dengan jumlah_penderita_dm tertinggi pada tahun 2019.
plt.figure(figsize=(10, 7))
plt.barh(top_10_2019['kab_kota'], top_10_2019['jumlah_dm'], color='teal')
plt.xlabel('Jumlah Penderita DM')
plt.ylabel('Kabupaten/Kota')
plt.title('Top 10 Kab/Kota dengan Penderita DM Tertinggi (2019)')
plt.gca().invert_yaxis() # Tertinggi di atas
plt.grid(axis='x', alpha=0.5)
plt.tight_layout()
plt.show()


# 23.Buat pie chart yang menunjukkan proporsi jumlah_penderita_dm berdasarkan kategori_dm ("Rendah", "Sedang", "Tinggi") pada tahun 2019.
proporsi_dm_2019 = df_2019.groupby('kategori_dm')['jumlah_dm'].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 8))
plt.pie(proporsi_dm_2019, labels=proporsi_dm_2019.index, autopct='%1.1f%%', 
        startangle=90, colors=['lightcoral', 'gold', 'lightskyblue'])
plt.title('Proporsi Jumlah Penderita DM Berdasarkan Kategori (2019)')
plt.axis('equal')
plt.show()


#24.Buat grafik bar yang membandingkan total jumlah_penderita_dm di tiga tahun terakhir yang tersedia (misal: 2017, 2018, 2019 jika ada di dataset).
last_3_years = total_per_tahun.tail(3)
plt.figure(figsize=(8, 5))
plt.bar(last_3_years['tahun'].astype(str), last_3_years['total_dm_jabar'], color='green')
plt.xlabel('Tahun')
plt.ylabel('Total Jumlah Penderita DM')
plt.title('Perbandingan Total DM Jawa Barat (3 Tahun Terakhir)')
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()


# 25. Tuliskan Analisis (Visualisasi di atas adalah buktinya)
print("\n--- 25. ANALISIS TERTULIS ---")
print("a. Kab/Kota dengan DM Tertinggi:")
print(f"   {kab_max} adalah Kab/Kota dengan total kumulatif penderita DM tertinggi di seluruh tahun yang tercatat.")
print("   Di tahun 2019, data dari Soal 22 menunjukkan Kab. Bogor tetap memegang posisi teratas.")

print("\nb. Tren Jumlah Penderita DM di Jawa Barat:")
print("   Secara umum, grafik garis (Soal 21) menunjukkan adanya kecenderungan kenaikan jumlah penderita DM dari tahun ke tahun di Jawa Barat.")

print("\nc. Sebaran Kategori Rendah/Sedang/Tinggi (2019):")
print("   Berdasarkan Pie Chart (Soal 23), sebagian besar kasus DM (persentase jumlah penderita) terkonsentrasi di kategori 'Tinggi'.")
print("   Namun, jika dilihat dari jumlah kabupaten/kota yang masuk kategori tersebut:")
print(df_2019['kategori_dm'].value_counts())
print("   (Kebanyakan kabupaten/kota mungkin masuk kategori 'Rendah' atau 'Sedang', tapi jumlah penderitanya kecil, sementara kab/kota di kategori 'Tinggi' memiliki penderita sangat banyak.)")