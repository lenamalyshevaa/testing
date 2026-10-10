from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CARD = "5559000000000001"


def choose_account(driver, title):
    driver.find_element(By.XPATH, f"//h2[text()='{title}']").click()


def enter_card(driver, number):
    card_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']")
    card_input.send_keys(number)
    return card_input


def enter_amount(driver, amount):
    amount_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    amount_input.send_keys(Keys.CONTROL, "a")
    amount_input.send_keys(Keys.BACKSPACE)
    amount_input.send_keys(amount)
    return amount_input


def transfer_button(driver):
    return driver.find_elements(By.XPATH, "//button[.//text()='Перевести']")


def not_enough_money(driver):
    return driver.find_elements(By.XPATH, "//span[text()='Недостаточно средств на счете']")


# TC-1
def test_transfer_valid_amount(open_bank):
    driver = open_bank
    choose_account(driver, "Рубли")
    enter_card(driver, CARD)
    enter_amount(driver, "1000")

    transfer_button(driver)[0].click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    text = alert.text
    alert.accept()

    assert text == f"Перевод 1000 ₽ на карту {CARD} принят банком!"


# TC-2
def test_commission_is_10_percent(open_bank):
    driver = open_bank
    choose_account(driver, "Рубли")
    enter_card(driver, CARD)
    enter_amount(driver, "5000")

    assert driver.find_element(By.ID, "comission").text == "500"


# TC-3
def test_amount_more_than_available(open_bank):
    driver = open_bank
    choose_account(driver, "Рубли")
    enter_card(driver, CARD)
    enter_amount(driver, "19000")  # 19000 + 1900 комиссии > 20000 доступно

    assert len(not_enough_money(driver)) == 1
    assert len(transfer_button(driver)) == 0


# TC-4, баг BUG-1: поле карты принимает 17 цифр
def test_card_number_max_16_digits(open_bank):
    driver = open_bank
    choose_account(driver, "Рубли")
    card_input = enter_card(driver, CARD + "1")

    assert card_input.get_attribute("value") == "5559 0000 0000 0001"


# TC-5, баг BUG-2: можно перевести отрицательную сумму
def test_negative_amount_not_allowed(open_bank):
    driver = open_bank
    choose_account(driver, "Рубли")
    enter_card(driver, CARD)
    enter_amount(driver, "-1000")

    assert len(transfer_button(driver)) == 0, "Кнопка 'Перевести' доступна для отрицательной суммы"
