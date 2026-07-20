<?php
/**
 * STUB MODULE — logout.php
 * Tidak ada di repo asli. Dibuat semata-mata sebagai pelengkap stub
 * index.php agar sesi bisa diakhiri secara bersih selama pengujian.
 */
session_start();
session_unset();
session_destroy();
header('Location: login.php');
exit;
