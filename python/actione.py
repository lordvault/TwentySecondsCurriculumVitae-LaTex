import getpass
import time
from linkedin_scraper import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def __prompt_email_password():
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return (u, p)


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def login(driver, email=None, password=None, cookie=None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)

    if not email or not password:
        email, password = __prompt_email_password()

    print("1L")
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    print("2L")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email_elem = driver.find_element_by_id("username")
    email_elem.send_keys(email)
    time.sleep(3)
    print("3L")
    password_elem = driver.find_element_by_id("password")
    password_elem.send_keys(password)
    time.sleep(5)
    print("4L")
    password_elem.submit()

    try:
        print(driver.current_url)
        if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
            remember = driver.find_element_by_id(c.REMEMBER_PROMPT)
            if remember:
                remember.submit()

        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, c.VERIFY_LOGIN_ID)))
        print('pass')
    except Exception as ex:
        print(f"Por el error {str(ex)}")
        pass


def _login_with_cookie(driver, cookie):
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
        "name": "li_at",
        "value": cookie
    })
