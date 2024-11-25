from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up Chrome options
options = Options()
profile_path = r"C:\Users\Salma\AppData\Local\Google\Chrome\User Data"
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("profile-directory=Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.telegram.org/")

# Wait for the search box to appear
search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='searchinput']")))
search_box.click()
time.sleep(1)

search_box.send_keys("+6289653310328")  # Change with the desired recipient
time.sleep(2)
search_box.send_keys(Keys.ENTER)
time.sleep(3)

message_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
message_box.click()
message = """
🎓 *BOOKING CONFIRMATION AND PAYMENT INSTRUCTIONS*

Dear *John Doe*,

Thank you for your booking for *Advanced Programming*. Please complete payment before *November 30, 2024 at 15:00 WIB*.
"""
message_box.send_keys(message)
time.sleep(1)

message_box.send_keys(Keys.ENTER)
print("Message sent!")
driver.quit()

