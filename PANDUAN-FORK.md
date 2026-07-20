# Panduan Menggabungkan Paket Ini ke Hasil Fork Kamu

Paket ini **BUKAN salinan aplikasi**, isinya cuma file TAMBAHAN yang perlu
kamu taruh langsung di root repo hasil fork (menimpa `koneksi.php` yang lama).
Struktur akhir repo kamu nanti akan jadi:

```
quiz-pengupil/                 (repo hasil fork kamu)
├── login.php                  ← sudah ada dari fork, JANGAN diubah
├── register.php                ← sudah ada dari fork, JANGAN diubah
├── koneksi.php                ← TIMPA dengan versi dari paket ini
├── style.css                  ← sudah ada dari fork
├── readme.md                  ← sudah ada dari fork
├── db/
│   └── quiz_pengupil.sql      ← sudah ada dari fork, JANGAN diubah
├── index.php                  ← BARU (dari paket ini) — STUB
├── logout.php                 ← BARU (dari paket ini) — STUB
├── requirements.txt            ← BARU
├── pytest.ini                  ← BARU
├── TESTCASES.md                ← BARU
├── .github/workflows/selenium-ci.yml   ← BARU
└── tests/                      ← BARU (seluruh isi folder)
    ├── conftest.py
    ├── db_driver.py
    ├── pages.py
    ├── test_login.py
    └── test_register.py
```

## Langkah-langkah

### 1. Fork repo aslinya
Buka https://github.com/hermanka/quiz-pengupil → klik tombol **Fork**
(kanan atas) → pilih akun GitHub kamu. Nanti kamu punya
`https://github.com/<username-kamu>/quiz-pengupil`.

### 2. Clone ke laptop kamu
Buka terminal di VS Code:
```bash
git clone https://github.com/<username-kamu>/quiz-pengupil.git
cd quiz-pengupil
```

### 3. Extract paket ini
Extract `fork-addon.zip` yang aku kasih, lalu **copy semua isinya** ke dalam
folder `quiz-pengupil` hasil clone tadi (timpa `koneksi.php` yang lama —
klik "Replace" kalau file explorer nanya).

### 4. Cek ulang koneksi.php
Buka `koneksi.php` hasil timpa tadi, pastikan isinya begini (baca env var,
fallback ke default lokal):
```php
$host     = getenv('DB_HOST') ?: 'localhost';
$user     = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASS') !== false ? getenv('DB_PASS') : '';
$db       = getenv('DB_NAME') ?: 'quiz_pengupil';
```
Kalau mau jalanin manual di XAMPP lokal (bukan CI), ini otomatis fallback ke
`root` / password kosong / `quiz_pengupil` — persis kayak koneksi.php aslinya.

### 5. Commit & push
```bash
git add .
git commit -m "Add Selenium test suite, stub, driver, and CI pipeline"
git push origin main
```

### 6. Cek pipeline-nya
Buka `https://github.com/<username-kamu>/quiz-pengupil/actions` — workflow
**"Selenium Test - Login & Register"** bakal otomatis jalan. Klik run yang
lagi jalan buat lihat log-nya real-time.

Kalau ada langkah yang gagal (merah), scroll ke log step yang error, terus
kirim ke aku — nanti kita debug bareng.

### 7. Simpan link repo-nya
Link `https://github.com/<username-kamu>/quiz-pengupil` itu yang kamu
lampirkan di laporan tugas.

---

## Catatan kalau mau jalanin di laptop dulu (opsional, sebelum push)

Kalau kamu punya XAMPP + MySQL lokal:
```bash
# 1. Buat database & import schema (kalau belum ada)
mysql -u root -e "CREATE DATABASE IF NOT EXISTS quiz_pengupil;"
mysql -u root quiz_pengupil < db/quiz_pengupil.sql

# 2. Install dependency python
pip install -r requirements.txt

# 3. Jalankan test
pytest
```
Pastikan PHP CLI ada di PATH (`php -v` harus jalan) dan Google Chrome
ter-install, karena `pytest` otomatis menyalakan PHP built-in server sendiri
(gak perlu Apache/XAMPP running, cukup MySQL-nya saja yang aktif).
