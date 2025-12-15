import pandas as pd


FILE_PATH = r'C:\Users\Vandr\Downloads\opendata.jabarprov.go.id_dataset_od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_csv\static\download\dinkes-od_17448_jml_penderita_diabetes_melitus_brdsrkn_kabupatenko_v2_data.csv'

# --- A. Soal Dasar (Pengenalan DataFrame) ---
print("=" * 50)
print("A. SOAL DASAR (PENGENALAN DATAFRAME)")
print("=" * 50)

# 1. Import library pandas, baca file data ke dalam DataFrame bernama df, lalu tampilkan 5 baris pertama.
try:
    df = pd.read_csv(FILE_PATH)
    print("\n1. DataFrame 'df' berhasil dimuat. 5 Baris Pertama:")
    print(df.head())
except FileNotFoundError:
    print(f"\nERROR: File tidak ditemukan di jalur: {FILE_PATH}. Mohon periksa kembali jalur file Anda.")
    exit()

print("-" * 30)

# 2. Tampilkan 5 baris terakhir dari df.
print("\n2. 5 Baris Terakhir (df.tail()):")
print(df.tail())

print("-" * 30)

# 3. Tampilkan informasi struktur DataFrame menggunakan df.info().
print("\n3. Informasi Struktur DataFrame (df.info()):")
df.info()

print("-" * 30)

# 4. Tampilkan statistik deskriptif untuk kolom numerik (jumlah_penderita_dm dan tahun).
print("\n4. Statistik Deskriptif untuk Kolom Numerik (df.describe()):")
print(df[['jumlah_penderita_dm', 'tahun']].describe())

print("-" * 30)

# 5. Tampilkan daftar nilai unik dari kolom tahun.
print("\n5. Nilai Unik Kolom 'tahun':")
print(df['tahun'].unique())

print("-" * 30)

# 6. Tampilkan daftar nilai unik dari kolom nama_kabupaten_kota dan hitung berapa banyak.
unique_kabupaten = df['nama_kabupaten_kota'].unique()
print("\n6. Nilai Unik Kolom 'nama_kabupaten_kota':")
print(unique_kabupaten)
print(f"   Jumlah Kabupaten/Kota yang Tercatat: {len(unique_kabupaten)}")

print("-" * 30)

# 7. Tampilkan hanya kolom: nama_kabupaten_kota, jumlah_penderita_dm, dan tahun.
print("\n7. Tampilkan Hanya Kolom: nama_kabupaten_kota, jumlah_penderita_dm, dan tahun:")
df_selected_cols = df[['nama_kabupaten_kota', 'jumlah_penderita_dm', 'tahun']]
print(df_selected_cols.head())