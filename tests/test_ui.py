import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)
        text_input = driver.find_element(By.ID, "text-input")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        text_input.send_keys("Reading books gives wonderful experience.")
        submit_btn.click()
        time.sleep(3)
        result_output = driver.find_element(By.ID, "result-output").text
        assert result_output != ""
        assert any(word in result_output for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()
