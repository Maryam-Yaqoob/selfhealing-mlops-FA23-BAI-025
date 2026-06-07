import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(BASE_URL)
        text_input = driver.find_element(By.ID, "text-input")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        result_output = driver.find_element(By.ID, "result-output")

        text_input.send_keys("This product is amazing")
        submit_btn.click()
        time.sleep(3)

        result_text = result_output.text
        assert result_text != ""
        assert (
            "POSITIVE" in result_text
            or "NEGATIVE" in result_text
            or "Confidence" in result_text
        )
    finally:
        driver.quit()
