import os
import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db_driver import reset_users_table, seed_user

# Layout REPO KAMU (hasil fork): login.php, register.php, koneksi.php, index.php,
# dst ada langsung di ROOT repo, sedangkan folder tests/ ini adalah subfolder-nya.
# Jadi APP_DIR = root repo = satu level di atas folder tests/.
APP_DIR = os.path.join(os.path.dirname(__file__), "..")
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def php_server():
    """Menjalankan PHP built-in server yang men-serve root repo (tempat
    login.php/register.php/index.php berada) selama satu sesi pytest.
    Ini menggantikan XAMPP/Apache lokal supaya CI tidak perlu instalasi
    web server tambahan."""
    proc = subprocess.Popen(
        ["php", "-S", "127.0.0.1:8000", "-t", APP_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)  # beri waktu server untuk siap
    yield proc
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(autouse=True)
def clean_db():
    """DRIVER: reset tabel users sebelum SETIAP test case, supaya semua
    test case independen dan tidak saling mempengaruhi urutan eksekusi."""
    reset_users_table()
    yield


@pytest.fixture
def existing_user():
    """DRIVER: menyuntikkan satu user valid langsung ke DB (bypass UI),
    sebagai prasyarat untuk test case login sukses / duplikasi registrasi."""
    creds = {"username": "budi01", "password": "Password123",
             "name": "Budi Santoso", "email": "budi@example.test"}
    seed_user(creds["username"], creds["password"],
              name=creds["name"], email=creds["email"])
    return creds


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Ambil screenshot otomatis saat test case gagal, untuk memudahkan
    debugging kegagalan di CI (diupload sebagai artifact)."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            path = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
            try:
                drv.save_screenshot(path)
            except Exception:
                pass
