from selenium.webdriver.common.by import By


def open_login(driver, base_url):
    driver.get(f"{base_url}/login.php")


def open_register(driver, base_url):
    driver.get(f"{base_url}/register.php")


def submit_login(driver, base_url, username, password):
    open_login(driver, base_url)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()


def submit_register(driver, base_url, name, email, username, password,
                    repassword, bypass_html5_validation=False):
    open_register(driver, base_url)
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    repass_field = driver.find_element(By.NAME, "repassword")
    repass_field.send_keys(repassword)
    if bypass_html5_validation:
        driver.execute_script(
            "arguments[0].form.setAttribute('novalidate', '');",
            repass_field
        )
        driver.find_element(By.NAME, "submit").click()
    else:
        driver.find_element(By.NAME, "submit").click()


def get_error_alert_text(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
    return elements[0].text if elements else None


def get_validation_text(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, "p.text-danger")
    return elements[0].text if elements else None


def is_on_dashboard(driver, base_url):
    return driver.current_url.rstrip("/").endswith("index.php")


def is_on_login(driver, base_url):
    return "login.php" in driver.current_url


def is_on_register(driver, base_url):
    return "register.php" in driver.current_url
