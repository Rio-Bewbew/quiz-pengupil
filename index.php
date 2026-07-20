<?php
session_start();

// Fitur Logout Praktis: Jika ada request ?action=logout, hapus sesi dan kembalikan ke login
if (isset($_GET['action']) && $_GET['action'] == 'logout') {
    session_destroy();
    header("Location: login.php");
    exit;
}

// Proteksi Halaman: Jika belum login (session kosong), lempar kembali ke halaman login
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Dashboard - Quiz Pengupil</title>
    <!-- Memanggil file Bootstrap dan CSS bawaan aplikasi -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="style.css">
    <style>
        /* Tambahan styling sedikit agar container dashboard lebih lebar dan rapi */
        .dashboard-container {
            background: #fff;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <section class="container-fluid mb-4">
        <section class="row justify-content-center">
            <section class="col-12 col-md-8 col-lg-6">
                
                <div class="dashboard-container">
                    <h2 class="text-center font-weight-bold mb-4">🏠 Dashboard Quiz Pengupil</h2>
                    
                    <div class="alert alert-success text-center" role="alert">
                        <h4 class="alert-heading">Selamat Datang, <strong class="text-uppercase"><?= htmlspecialchars($_SESSION['username']); ?></strong>!</h4>
                        <p class="mb-0">Anda telah berhasil melewati proses otentikasi (Login).</p>
                    </div>
                    
                    <div class="text-center mt-4">
                        <p class="text-muted">
                            <em>Halaman index.php (Stub) ini dibuat khusus sebagai titik akhir (endpoint) untuk memvalidasi keberhasilan skenario pengujian UI dan CI/CD.</em>
                        </p>
                        <hr class="my-4">
                        <!-- Tombol Logout yang mengarah ke logic di bagian atas file -->
                        <a href="?action=logout" class="btn btn-danger btn-lg px-5">Logout</a>
                    </div>
                </div>

            </section>
        </section>
    </section>

    <!-- Script Bootstrap -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
</body>
</html>