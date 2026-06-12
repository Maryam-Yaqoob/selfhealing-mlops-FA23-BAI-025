import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)
        
        # Elements Find karein via fixed IDs
        text_input = driver.find_element(By.ID, "text-input")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        
        # Test input send karein (Assigned Category: BOOK)
        text_input.send_keys("Reading books gives wonderful experience.")
        submit_btn.click()
        time.sleep(3)
        
        result_output = driver.find_element(By.ID, "result-output").text
        
        assert result_output != ""
        assert any(word in result_output for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()
