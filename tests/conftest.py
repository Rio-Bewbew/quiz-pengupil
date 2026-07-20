import os
import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db_driver import reset_users_table, seed_user

APP_DIR = os.path.join(os.path.dirname(__file__), "..")
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def php_server():
    proc = subprocess.Popen(
        ["php", "-S", "127.0.0.1:8000", "-t", APP_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    yield proc
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(autouse=True)
def clean_db():
    reset_users_table()
    yield


@pytest.fixture
def existing_user():
    # Reset + seed dalam satu fixture, tidak bergantung pada
    # urutan autouse clean_db agar tidak terjadi race condition.
    reset_users_table()
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
