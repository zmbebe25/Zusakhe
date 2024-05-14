from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import json  # Import JSON module for JSON output

# Specify the path to the chromedriver executable
chrome_driver_path = "C:/Users/Zusakhe Mbebe/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe"
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the target page
driver.get('https://www.cut.ac.za/application-process#:~:text=The%20application%20cycle%20for%202024,closed%20on%2030%20September%202023.')

# Wait for the page to load
time.sleep(2)

# Try to accept cookies if the button is present
try:
    cookies_button = driver.find_element(By.ID, 'c-p-bn')
    cookies_button.click()
    # Wait for possible redirections or additional content to load after accepting cookies
    time.sleep(2)
except:
    print("Cookies button not found or not clickable.")

# Find the date information element using XPath
date_info_element = driver.find_element(By.XPATH, "//div[@class='col-sm-9']/p[contains(text(), '2024 Applications')]/following-sibling::p[1]")
date_info_text = date_info_element.text

# Extracting opening and closing dates from the text
parts = date_info_text.split('opened on ')[1]  # This splits the text and takes the part after 'opened on '
opening_date = parts.split(' and closed on ')[0]
closing_date = parts.split(' and closed on ')[1]

# Prepare the dates in a dictionary
dates_dict = {
    "opening_date": opening_date,
    "closing_date": closing_date
}

# Convert dictionary to JSON
dates_json = json.dumps(dates_dict)

# Print the JSON string
print(dates_json)

# Close the browser
driver.quit()
