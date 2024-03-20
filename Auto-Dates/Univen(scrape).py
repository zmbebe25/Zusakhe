from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import json

# Specify the path to the chromedriver executable
chrome_driver_path = "C:/Users/Zusakhe Mbebe/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the target page
driver.get('https://www.univen.ac.za/students/student-support-services/how-to-apply/')

# Wait for the page to load
time.sleep(2)

# Try to accept cookies if the button is present
try:
    cookies_button = driver.find_element(By.ID, 'wt-cli-accept-all-btn')
    cookies_button.click()
    # Wait for possible redirections or additional content to load after accepting cookies
    time.sleep(2)
except Exception as e:
    print("Cookies button not found or not clickable.", str(e))

# Find the application closing date information using XPath
closing_date_info_element = driver.find_element(By.XPATH, "//p[strong[contains(text(), 'Application Closing Date')]]")
closing_date_info_text = closing_date_info_element.text

# Extract the closing date from the text
closing_date = closing_date_info_text.split(': ')[1]

# Since there's no opening date mentioned in the provided HTML snippet,
# the opening date will not be included in the JSON output
dates_dict = {
    "closing_date": closing_date
}

# Convert the dates information to JSON
dates_json = json.dumps(dates_dict)

# Print the JSON string
print(dates_json)

# Close the browser
driver.quit()
