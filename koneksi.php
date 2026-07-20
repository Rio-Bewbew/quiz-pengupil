<?php
// NOTE: Satu-satunya perubahan dari koneksi.php asli adalah sumber konfigurasi
// (env var, dengan fallback ke nilai default yang sama seperti aslinya) agar
// bisa diarahkan ke database MySQL sementara (ephemeral) di GitHub Actions.
// Tidak ada logic aplikasi yang diubah.
$host     = getenv('DB_HOST') ?: 'localhost';
$user     = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASS') !== false ? getenv('DB_PASS') : '';
$db       = getenv('DB_NAME') ?: 'quiz_pengupil';

$con = mysqli_connect($host, $user, $password, $db);
if (!$con) {
    die("Connection failed: " . mysqli_connect_error());
}
?>
