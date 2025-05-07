
# 📦 Tokopedia Review Scraper & Sentiment Analysis

Aplikasi berbasis Streamlit untuk melakukan *web scraping*, analisis sentimen, dan analisis topik (LDA) dari ulasan produk di [Tokopedia](https://www.tokopedia.com).

---

## 🚀 Fitur Utama

- Scraping komentar pelanggan dari halaman produk Tokopedia.
- Analisis sentimen menggunakan model NLP Bahasa Indonesia.
- Visualisasi hasil dalam bentuk:
  - Tabel ulasan dan sentimen
  - Pie chart distribusi sentimen
  - Bar chart distribusi rating
  - Word cloud untuk komentar positif, negatif, dan netral
  - Topik utama dari komentar dengan LDA (Latent Dirichlet Allocation)
- Export hasil analisis ke format CSV.

---

## 🛠 Teknologi yang Digunakan

- `Streamlit` — untuk antarmuka pengguna web.
- `Selenium` — untuk scraping ulasan dari Tokopedia.
- `Pandas` & `Matplotlib` & `Seaborn` — untuk manipulasi dan visualisasi data.
- `Hugging Face Transformers` — untuk analisis sentimen.
- `Gensim` — untuk pemodelan topik LDA.
- `WordCloud` — untuk visualisasi kata dominan.

---

## ⚙️ Cara Instalasi dan Menjalankan Aplikasi

1. **Clone repositori:**

```bash
git clone https://github.com/Yud1Pp/tokopedia-review-sentiment.git
cd tokopedia-review-sentiment
````

2. **Buat dan aktifkan environment:**

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Jalankan aplikasi:**

```bash
streamlit run app.py
```

5. **Akses aplikasi:**
   Buka browser dan akses `http://localhost:8501`

Berikut adalah tambahan bagian untuk dokumentasi di README Anda terkait instalasi **ChromeDriver** agar scraping dengan Selenium dapat berjalan dengan baik:

---

## 🔧 Instalasi ChromeDriver

Untuk menjalankan Selenium, Anda perlu menginstal **ChromeDriver** yang sesuai dengan versi Google Chrome yang terpasang di komputer Anda. Berikut langkah-langkahnya:

1. **Periksa versi Chrome Anda:**

   Buka Google Chrome dan akses alamat berikut di browser:

   ```
   chrome://settings/help
   ```

   Catat versi Chrome Anda, misalnya: `114.0.5735.90`.

2. **Download ChromeDriver yang sesuai:**

   Kunjungi situs resmi berikut:
   [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

   Pilih versi yang sesuai dengan Chrome Anda, lalu unduh file untuk sistem operasi yang Anda gunakan (Windows, Linux, atau macOS).

3. **Ekstrak dan simpan ChromeDriver:**

   Setelah diunduh, ekstrak file dan simpan di folder yang mudah diakses, misalnya:

   * `C:\chromedriver\chromedriver.exe` (Windows)
   * `/usr/local/bin/chromedriver` (Linux/macOS)

4. **Ubah variabel `servicePath` di `app.py`:**

   Buka file `app.py` dan cari baris yang memuat `Service(...)` dari Selenium. Ganti path dengan lokasi ChromeDriver Anda.

   Contoh di Windows:

   ```python
   servicePath = Service('C:/chromedriver/chromedriver.exe')
   ```

   Contoh di Linux/macOS:

   ```python
   servicePath = Service('/usr/local/bin/chromedriver')
   ```

5. **Pastikan ChromeDriver dapat dijalankan:**

   Coba jalankan perintah berikut di terminal untuk memastikan ChromeDriver bisa diakses:

   ```bash
   chromedriver --version
   ```
---

## 📥 Cara Menggunakan

1. Buka aplikasi di browser.
2. Masukkan URL produk Tokopedia, misalnya:
(https://www.tokopedia.com/tokokingonline/1-ball-mamypoko-pants-s38-m32-l28-xl26-xxl24-king-online-1729623896722213308?t_id=1746606199417&t_st=1&t_pp=homepage&t_efo=pure_goods_card&t_ef=homepage&t_sm=rec_homepage_outer_flow&t_spt=homepage)
3. Klik tombol **"Mulai Scraping & Analisis"**.
4. Tunggu proses scraping dan analisis selesai.
5. Lihat hasil pada tabel dan visualisasi.
6. Unduh hasil dalam format `.csv` jika dibutuhkan.

---

## 📝 Struktur Folder

```
├── app.py                  # Main Streamlit app
├── scraper/                # Modul scraping Tokopedia
│   └── scraper.py
├── sentiment/              # Analisis sentimen
│   └── sentiment.py
├── lda/                    # Preprocessing dan LDA
│   └── lda.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Catatan

* Untuk scraping, pastikan koneksi internet stabil.
* Scraper dirancang untuk halaman ulasan Tokopedia versi terbaru.
* Model sentimen menggunakan pre-trained model Bahasa Indonesia dari Hugging Face.

---

## 📄 Lisensi

MIT License – Silakan gunakan dan modifikasi sesuai kebutuhan.
Silakan beri kredit jika Anda mengembangkan proyek ini lebih lanjut. 🙌
