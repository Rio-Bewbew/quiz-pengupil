# Test Case Design — Modul Login & Register
Repo yang diuji: `login.php` & `register.php` dari [hermanka/quiz-pengupil](https://github.com/hermanka/quiz-pengupil)

Metode: kombinasi **black-box** (equivalence partitioning, boundary/empty-value,
negative testing, security testing sederhana) dan **white-box** (hasil code
review terhadap source `login.php` / `register.php` untuk menemukan defect
yang tidak terlihat murni dari UI).

Legenda kolom **Otomatis**: ✅ = ada di `tests/test_login.py` /
`tests/test_register.py`. **Temuan Bug** menandai test case yang justru
dirancang untuk mendokumentasikan perilaku SUT yang salah (regression-capture).

---

## A. Modul Login (`login.php`)

| ID | Tujuan | Precondition | Data Uji | Langkah | Expected Result | Otomatis | Temuan Bug |
|----|--------|-------------|----------|---------|------------------|:---:|:---:|
| LG-01 | Login sukses dengan kredensial valid | User `budi01` / `Password123` sudah ada di DB (via driver) | username=budi01, password=Password123 | Isi form, klik Sign In | Redirect ke `index.php` (stub), session `username` ter-set, tampil "Selamat datang, budi01" | ✅ | |
| LG-02 | Login dengan password salah | User `budi01` ada di DB | username=budi01, password=SALAH | Isi form, klik Sign In | **Bug**: tetap di `login.php`, **tidak ada pesan error sama sekali** ditampilkan, session tidak ter-set | ✅ | ✅ BUG-01 |
| LG-03 | Login dengan username tidak terdaftar | DB kosong / username tidak ada | username=tidakada, password=bebas | Isi form, klik Sign In | Muncul alert error, tapi **teksnya "Register User Gagal !!"** (pesan salah, seharusnya pesan login gagal) | ✅ | ✅ BUG-02 |
| LG-04 | Username kosong | - | username="", password=Password123 | Kosongkan username, isi password, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| LG-05 | Password kosong | - | username=budi01, password="" | Isi username, kosongkan password, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| LG-06 | Username & password kosong | - | keduanya "" | Langsung klik Sign In tanpa isi apa pun | Alert "Data tidak boleh kosong !!" | ✅ | |
| LG-07 | Input hanya berupa whitespace | - | username="   ", password="   " | Isi spasi saja di kedua field, submit | Alert "Data tidak boleh kosong !!" (karena server pakai `trim()`) | ✅ | |
| LG-08 | SQL Injection pada field username | - | username=`' OR '1'='1`, password=bebas | Isi username dengan payload injeksi, submit | Login **tidak boleh** berhasil / tidak bypass autentikasi (query sudah di-escape via `mysqli_real_escape_string`) | ✅ | |
| LG-09 | Redirect otomatis bila sudah login | Sudah login sukses (session aktif) | - | Akses ulang `login.php` langsung via URL | Redirect otomatis ke `index.php`, tidak menampilkan form login lagi | ✅ | |
| LG-10 | Verifikasi session benar-benar tidak terbentuk setelah gagal login | Sama seperti LG-02 | Sama seperti LG-02 | Setelah gagal login, akses `index.php` langsung | Redirect ke `login.php` (membuktikan session memang tidak ter-set) | ✅ | |

**BUG-01**: Pada `login.php`, blok `if ($rows != 0) { if(password_verify(...)) {...} }` **tidak memiliki `else`** untuk kasus password salah. Akibatnya user tidak mendapat feedback apa pun ketika password salah — dari sisi UX ini membingungkan dan berpotensi disalahartikan sebagai bug availability.

**BUG-02**: Pesan error untuk "username tidak ditemukan" pada `login.php` adalah `'Register User Gagal !!'` — jelas hasil copy-paste dari modul register, salah konteks.

---

## B. Modul Register (`register.php`)

| ID | Tujuan | Precondition | Data Uji | Langkah | Expected Result | Otomatis | Temuan Bug |
|----|--------|-------------|----------|---------|------------------|:---:|:---:|
| RG-01 | Registrasi sukses dengan data valid & unik | Username belum terdaftar | name=Dewi Lestari, email=dewi@test.com, username=dewi01, password=Password123, repassword=Password123 | Isi semua field, submit | Redirect ke `index.php`, row baru masuk ke tabel `users`, session `username` ter-set | ✅ | |
| RG-02 | Registrasi dengan username yang sudah ada | Username `budi01` sudah ada (via driver) | username=budi01 (data lain valid) | Isi form pakai username duplikat, submit | Alert "Username sudah terdaftar !!", **tidak ada** row baru ditambahkan | ✅ | |
| RG-03 | Password & Re-Password tidak sama | - | password=Password123, repassword=Lain123 | Isi form dgn password berbeda, submit | Pesan "Password tidak sama !!" di bawah field password, tidak ada row baru | ✅ | |
| RG-04 | Field nama kosong | - | name="" (lain valid) | Kosongkan Nama, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| RG-05 | Field email kosong | - | email="" (lain valid) | Kosongkan Email, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| RG-06 | Field username kosong | - | username="" (lain valid) | Kosongkan Username, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| RG-07 | Field password/repassword kosong | - | password="" & repassword="" | Kosongkan keduanya, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| RG-08 | Semua field whitespace saja | - | semua field "   " | Isi spasi di semua field, submit | Alert "Data tidak boleh kosong !!" | ✅ | |
| RG-09 | Format email tidak valid berhasil lolos ke server | Bypass validasi HTML5 (`type="email"`) via JS `form.submit()` | email="bukan-email-valid" | Submit via JS (bypass constraint validation browser) | **Bug**: data tetap diterima & disimpan — server tidak melakukan validasi format email sama sekali | ✅ | ✅ BUG-03 |
| RG-10 | Kolom `name` selalu kosong di database setelah registrasi sukses | - | name=Dewi Lestari (lain valid & unik) | Registrasi sukses, lalu cek langsung ke DB | **Bug**: kolom `name` di DB tersimpan **kosong**, bukan "Dewi Lestari", karena query INSERT memakai variabel `$nama` (undefined) alih-alih `$name` | ✅ | ✅ BUG-04 |
| RG-11 | SQL Injection pada field nama/username | - | name=`Robert'); DROP TABLE users;--` | Isi field nama dengan payload injeksi, submit | Query tidak rusak / tabel `users` tetap ada (escaping berhasil) | ✅ | |
| RG-12 | Guard "sudah login" pada register.php tidak berfungsi | Sudah login sukses via `login.php` (session `username` ter-set) | - | Setelah login, akses `register.php` langsung via URL | **Bug**: seharusnya redirect ke `index.php`, tapi form register tetap tampil — karena `register.php` mengecek `$_SESSION['user']` (typo), padahal `login.php` men-set `$_SESSION['username']` | ✅ | ✅ BUG-05 |

**BUG-03**: Tidak ada validasi format email di sisi server (`filter_var($email, FILTER_VALIDATE_EMAIL)` tidak pernah dipanggil). Validasi HTML5 `type="email"` di client bisa dilewati (mis. lewat DevTools/JS), sehingga data kotor bisa masuk ke DB.

**BUG-04**: Baris `$query = "INSERT INTO users (...) VALUES ('$username','$nama','$email','$pass')"` memakai variabel **`$nama`** yang tidak pernah didefinisikan (yang ada adalah `$name`), sehingga PHP menganggapnya string kosong. Ini terbukti juga dari data seed asli di `db/quiz_pengupil.sql` — kedua baris user (`irul`, `ahmad`) kolom `name`-nya kosong.

**BUG-05**: `login.php` menyimpan sesi di `$_SESSION['username']`, sedangkan guard "sudah login" di `register.php` mengecek `$_SESSION['user']` — nama key session tidak konsisten antar modul, sehingga guard tersebut tidak pernah aktif untuk user yang login lewat `login.php`.

---

## C. Kebutuhan Stub & Driver

Readme repo asli menyebutkan eksplisit: *"Diperlukan Stub untuk menguji modul"*.

- **Stub** → `index.php` (+ `logout.php`) di root repo. Repo asli **tidak menyediakan**
  `index.php` sama sekali, padahal `login.php` & `register.php` sama-sama
  memanggil `header('Location: index.php')` dan mengecek session untuk
  redirect ke sana. `index.php` adalah modul "bawahan" yang dipanggil tapi
  belum diimplementasikan — persis definisi **stub** pada integration testing
  top-down: pengganti sederhana dari modul yang dipanggil, agar modul yang
  sedang diuji (login/register) bisa dieksekusi dan diverifikasi secara utuh
  tanpa berhenti di halaman 404.

- **Driver** → `tests/db_driver.py`. Tidak ada modul/API lain di aplikasi
  ini yang bisa dipakai untuk menyiapkan prasyarat data secara deterministik
  (mis. "sudah ada user bernama budi01" untuk kasus login/duplikasi
  registrasi) selain lewat form register itu sendiri — yang justru salah
  satu hal yang sedang diuji. `db_driver.py` bertindak sebagai **driver**:
  modul kecil yang "memanggil" lapisan data secara langsung (bypass UI) untuk
  menyuntikkan/reset data uji sebelum tiap test case dijalankan, dan
  memverifikasi isi tabel `users` setelah test case berjalan (dipakai pada
  RG-10). Password di-hash memakai `password_hash()` PHP asli (dipanggil via
  `php -r`) supaya 100% kompatibel dengan `password_verify()` di `login.php`.
