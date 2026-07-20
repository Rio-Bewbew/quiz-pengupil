"""
db_driver.py — "Driver" untuk pengujian modul Login & Register.

Aplikasi yang diuji (login.php / register.php) tidak menyediakan API atau
halaman admin apa pun untuk menyiapkan data prasyarat (mis. "user X sudah
terdaftar") selain lewat form register itu sendiri — padahal form register
justru salah satu hal yang sedang diuji. Modul ini berfungsi sebagai DRIVER:
ia memanggil/mengendalikan lapisan data (MySQL) secara langsung, di luar UI,
untuk:

  1. Membersihkan (reset) tabel `users` sebelum tiap test case, supaya tiap
     test case berjalan dari kondisi awal yang bersih & independen.
  2. Menyuntikkan (seed) baris user tertentu secara deterministik sebagai
     prasyarat test case (mis. LG-01 butuh user valid yang sudah ada).
  3. Membaca kembali isi tabel `users` untuk verifikasi hasil (mis. RG-10
     yang memeriksa apakah kolom `name` benar-benar tersimpan).

Password di-hash memakai password_hash() PHP asli (bukan library Python)
supaya hash yang dihasilkan dijamin 100% kompatibel dengan password_verify()
yang dipanggil oleh login.php.
"""
import os
import subprocess

import pymysql


def _connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", "root"),
        database=os.environ.get("DB_NAME", "quiz_pengupil"),
        autocommit=True,
        charset="utf8mb4",
    )


def php_password_hash(plain_password: str) -> str:
    """Hasilkan hash bcrypt via PHP password_hash() asli (bukan tiruan),
    supaya kompatibel byte-per-byte dengan password_verify() di login.php."""
    escaped = plain_password.replace("'", "\\'")
    result = subprocess.run(
        ["php", "-r", f"echo password_hash('{escaped}', PASSWORD_DEFAULT);"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def reset_users_table() -> None:
    """Mengosongkan tabel users. Dipanggil sebelum setiap test case."""
    conn = _connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users")
    finally:
        conn.close()


def seed_user(username: str, password: str, name: str = "Test User",
              email: str | None = None) -> None:
    """Menyuntikkan satu user langsung ke DB (bypass form register)."""
    email = email or f"{username}@example.test"
    hashed = php_password_hash(password)
    conn = _connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, username, email, password) "
                "VALUES (%s, %s, %s, %s)",
                (name, username, email, hashed),
            )
    finally:
        conn.close()


def get_user_row(username: str) -> dict | None:
    """Ambil satu baris user untuk keperluan assertion (mis. cek kolom name)."""
    conn = _connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cur.fetchone()
    finally:
        conn.close()


def count_users(username: str) -> int:
    """Hitung berapa baris user dengan username tertentu (cek duplikasi/injeksi)."""
    conn = _connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
            (n,) = cur.fetchone()
            return n
    finally:
        conn.close()


def table_exists(table_name: str = "users") -> bool:
    """Dipakai test SQL-injection (RG-11) untuk memastikan tabel tidak
    hilang akibat payload seperti `'); DROP TABLE users;--`."""
    conn = _connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", (table_name,))
            return cur.fetchone() is not None
    finally:
        conn.close()
