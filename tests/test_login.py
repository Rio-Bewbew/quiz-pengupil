"""
Test case module: Login (login.php)
ID mengacu ke TESTCASES.md bagian A.
"""
from pages import (
    open_login,
    submit_login,
    get_error_alert_text,
    is_on_dashboard,
    is_on_login,
)


def test_LG01_login_sukses_dengan_kredensial_valid(driver, base_url, existing_user):
    submit_login(driver, base_url, existing_user["username"], existing_user["password"])

    assert is_on_dashboard(driver, base_url), (
        f"Diharapkan redirect ke index.php, tapi URL sekarang: {driver.current_url}"
    )
    assert existing_user["username"] in driver.page_source


def test_LG02_login_password_salah_tidak_ada_pesan_error(driver, base_url, existing_user):
    """BUG-01: login.php tidak punya cabang 'else' untuk password_verify()
    gagal, sehingga tidak ada pesan error yang tampil sama sekali."""
    submit_login(driver, base_url, existing_user["username"], "PasswordSalah999")

    assert is_on_login(driver, base_url), "Tidak boleh berhasil redirect ke dashboard"
    error = get_error_alert_text(driver)
    assert error is None, (
        f"BUG-01 mestinya tidak ada alert error sama sekali, tapi ditemukan: {error!r}"
    )


def test_LG03_login_username_tidak_terdaftar_pesan_salah_konteks(driver, base_url):
    """BUG-02: pesan error untuk username tidak ditemukan seharusnya bicara
    soal login, tapi teksnya justru 'Register User Gagal !!' (copy-paste)."""
    submit_login(driver, base_url, "user_tidak_ada", "bebas123")

    assert is_on_login(driver, base_url)
    error = get_error_alert_text(driver)
    assert error == "Register User Gagal !!", (
        f"BUG-02: pesan error tidak sesuai ekspektasi (mislabel), didapat: {error!r}"
    )


def test_LG04_username_kosong(driver, base_url):
    submit_login(driver, base_url, "", "Password123")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_LG05_password_kosong(driver, base_url, existing_user):
    submit_login(driver, base_url, existing_user["username"], "")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_LG06_username_dan_password_kosong(driver, base_url):
    submit_login(driver, base_url, "", "")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_LG07_input_whitespace_saja(driver, base_url):
    submit_login(driver, base_url, "   ", "   ")
    assert get_error_alert_text(driver) == "Data tidak boleh kosong !!"


def test_LG08_sql_injection_pada_username_tidak_bypass(driver, base_url):
    submit_login(driver, base_url, "' OR '1'='1", "apapun")

    assert is_on_login(driver, base_url), "Login TIDAK BOLEH berhasil lewat SQL injection"
    assert not is_on_dashboard(driver, base_url)


def test_LG09_redirect_otomatis_jika_sudah_login(driver, base_url, existing_user):
    submit_login(driver, base_url, existing_user["username"], existing_user["password"])
    assert is_on_dashboard(driver, base_url)

    open_login(driver, base_url)  # akses ulang login.php via URL langsung
    assert is_on_dashboard(driver, base_url), (
        "User yang sudah login harus otomatis diarahkan kembali ke index.php"
    )


def test_LG10_gagal_login_tidak_membentuk_session(driver, base_url, existing_user):
    submit_login(driver, base_url, existing_user["username"], "SalahLagi123")
    assert is_on_login(driver, base_url)

    driver.get(f"{base_url}/index.php")
    assert is_on_login(driver, base_url), (
        "Karena login gagal, akses index.php harus tetap ditolak (redirect ke login.php)"
    )
