import os

import pytest
from selenium import webdriver

BASE_URL = os.getenv("BASE_URL", "http://localhost:9999")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,1000")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


@pytest.fixture
def open_bank(driver):
    # на счету 30 000 ₽, в резерве 10 000 ₽ -> доступно 20 000 ₽
    driver.get(f"{BASE_URL}/?balance=30000&reserved=10000")
    return driver
