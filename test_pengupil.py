import pytest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost/quiz-pengupil"

# Membuat kredensial acak agar test bisa di-run berulang-kali tanpa error "Username terdaftar"
RANDOM_USER = f"tester_{random.randint(1000,9999)}"
RANDOM_PASS = "rahasia123"

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_register_success_despite_bug(driver):
    """TC-REG-01: Ternyata PHP memaklumi bug $nama, query berhasil, dan redirect ke index."""
    driver.get(f"{BASE_URL}/register.php")
    
    driver.find_element(By.ID, "name").send_keys("User Baru")
    driver.find_element(By.ID, "InputEmail").send_keys(f"{RANDOM_USER}@test.com")
    driver.find_element(By.ID, "username").send_keys(RANDOM_USER)
    driver.find_element(By.ID, "InputPassword").send_keys(RANDOM_PASS)
    driver.find_element(By.ID, "InputRePassword").send_keys(RANDOM_PASS)
    
    driver.find_element(By.NAME, "submit").click()
    
    # Validasi bahwa sistem pindah ke index.php (Registrasi Berhasil)
    WebDriverWait(driver, 5).until(EC.url_contains("index.php"))
    assert "index.php" in driver.current_url

def test_login_success_redirect_to_index(driver):
    """TC-LOG-01: Menguji login sukses menggunakan akun yang baru saja didaftarkan di atas"""
    driver.get(f"{BASE_URL}/login.php")
    
    # Login dengan akun yang baru dibikin
    driver.find_element(By.ID, "username").send_keys(RANDOM_USER)
    driver.find_element(By.ID, "InputPassword").send_keys(RANDOM_PASS)
    driver.find_element(By.NAME, "submit").click()
    
    # Validasi berhasil masuk
    WebDriverWait(driver, 5).until(EC.url_contains("index.php"))
    assert "index.php" in driver.current_url

def test_login_invalid_shows_wrong_error(driver):
    """TC-LOG-02: Menguji bug dosen (User tidak ada malah muncul 'Register User Gagal !!')"""
    driver.get(f"{BASE_URL}/login.php")
    
    driver.find_element(By.ID, "username").send_keys("usernametidakada")
    driver.find_element(By.ID, "InputPassword").send_keys("bebas123")
    driver.find_element(By.NAME, "submit").click()
    
    error_element = driver.find_element(By.XPATH, "//div[contains(@class, 'alert-danger')]")
    assert "Register User Gagal !!" in error_element.text