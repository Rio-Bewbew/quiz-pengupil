"""
Test case module: Register (register.php)
ID mengacu ke TESTCASES.md bagian B.
"""
from pages import (
    open_register,
    submit_login,
    submit_register,
    get_error_alert_text,
    get_validation_text,
    is_on_dashboard,
    is_on_register,
)
from db_driver import get_user_row, count_users, table_exists


def test_RG01_registrasi_sukses_data_valid_dan_unik(driver, base_url):
    submit_register(
        driver, base_url,
        name="Dewi Lestari", email="dewi@test.com", username="dewi01",
        password="Password123", repassword="Password123",
    )

    assert is_on_dashboard(driver, base_url), (
        f"Diharapkan redirect ke index.php, tapi URL sekarang: {driver.current_url}"
    )
    assert count_users("dewi01") == 1


def test_RG02_registrasi_username_sudah_terdaftar(driver, base_url, existing_user):
    submit_register(
        driver, base_url,
        name="Nama Lain", email="lain@test.com", username=existing_user["username"],
        password="Password123", repassword="Password123",
    )

    assert is_on_register(driver, base_url)
    assert get_error_alert_text(driver) == "Username sudah terdaftar !!"
    assert count_users(existing_user["username"]) == 1, "Tidak boleh ada baris duplikat"


def test_RG03_password_dan_repassword_tidak_sama(driver, base_url):
    submit_register(
        driver, base_url,
        name="Coba User", email="coba@test.com", username="coba01",
        password="Password123", repassword="Berbeda123",
    )

    assert is_on_register(driver, base_url)
    assert get_validation_text(driver) == "Password tidak sama !!"
    assert count_users("coba01") == 0


def test_RG04_nama_kosong(driver, base_url):
    submit_register(driver, base_url, name="", email="a@test.com",
                     username="a01", password="Password123", repassword="Password123")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_RG05_email_kosong(driver, base_url):
    submit_register(driver, base_url, name="A", email="",
                     username="a01", password="Password123", repassword="Password123")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_RG06_username_kosong(driver, base_url):
    submit_register(driver, base_url, name="A", email="a@test.com",
                     username="", password="Password123", repassword="Password123")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_RG07_password_dan_repassword_kosong(driver, base_url):
    submit_register(driver, base_url, name="A", email="a@test.com",
                     username="a01", password="", repassword="")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_RG08_semua_field_whitespace(driver, base_url):
    submit_register(driver, base_url, name="   ", email="   ",
                     username="   ", password="   ", repassword="   ")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_RG09_format_email_tidak_valid_lolos_ke_server(driver, base_url):
    """BUG-03: server tidak memvalidasi format email. Constraint validation
    HTML5 browser sengaja dilewati (submit via JS) untuk membuktikan bahwa
    validasi ini TIDAK ADA di sisi server."""
    submit_register(
        driver, base_url,
        name="Rudi", email="bukan-email-valid", username="rudi01",
        password="Password123", repassword="Password123",
        bypass_html5_validation=True,
    )

    assert is_on_dashboard(driver, base_url), (
        "BUG-03: registrasi dengan email tidak valid seharusnya tetap "
        "diterima oleh server karena tidak ada validasi format email"
    )
    row = get_user_row("rudi01")
    assert row is not None
    assert row["email"] == "bukan-email-valid"


def test_RG10_kolom_name_kosong_di_database_akibat_bug_variabel(driver, base_url):
    """BUG-04: query INSERT memakai $nama (undefined) bukan $name, sehingga
    kolom `name` di DB selalu tersimpan kosong walau form diisi lengkap."""
    submit_register(
        driver, base_url,
        name="Dewi Lestari", email="dewi2@test.com", username="dewi02",
        password="Password123", repassword="Password123",
    )
    assert is_on_dashboard(driver, base_url)

    row = get_user_row("dewi02")
    assert row is not None, "Row user harus tetap tersimpan"
    assert row["name"] == "", (
        f"BUG-04: kolom name diharapkan kosong (bug), tapi tersimpan: {row['name']!r}"
    )


def test_RG11_sql_injection_pada_field_nama_tidak_merusak_tabel(driver, base_url):
    submit_register(
        driver, base_url,
        name="Robert'); DROP TABLE users;--",
        email="robert@test.com", username="robert01",
        password="Password123", repassword="Password123",
    )

    assert table_exists("users"), "Tabel users tidak boleh hilang akibat SQL injection"


def test_RG12_guard_sudah_login_tidak_berfungsi_di_register(driver, base_url, existing_user):
    """BUG-05: register.php mengecek $_SESSION['user'] (typo), padahal
    login.php menyimpan session di $_SESSION['username']. Akibatnya user
    yang sudah login TIDAK diarahkan pergi dari register.php."""
    submit_login(driver, base_url, existing_user["username"], existing_user["password"])
    assert is_on_dashboard(driver, base_url)

    open_register(driver, base_url)
    assert is_on_register(driver, base_url), (
        "BUG-05: form register seharusnya tetap tampil (guard tidak berfungsi) "
        "meskipun user sudah login — ini mendokumentasikan bug session-key mismatch"
    )
