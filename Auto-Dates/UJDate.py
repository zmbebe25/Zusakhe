from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import json  # Import JSON module for JSON output

# Specify the path to the chromedriver executable
chrome_driver_path = "C:/Users/Zusakhe Mbebe/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the target page
driver.get('https://www.uj.ac.za/about/about/internationalisation/international-students-2/applying-to-uj/')

# Wait for the page to load
time.sleep(2)

# Accept cookies if present
cookies_button = driver.find_element(By.ID, 'wt-cli-accept-all-btn')
cookies_button.click()

# Wait for possible redirections or additional content to load
time.sleep(2)

# Find the date information element using XPath
date_info_element = driver.find_element(By.XPATH, "//div[@class='wpb_wrapper']//p[strong[text()='APPLICATION AND CLOSING DATE']]/following-sibling::p[1]")
date_info_text = date_info_element.text

# Print the extracted text (for verification)
#print(date_info_text)

# Close the browser
driver.quit()
# String manipulation to extract dates
start_phrase = "Applications open on "
end_phrase = " and closes on "
closing_date_phrase = " at 12:00."

# Finding start and end indices
start_index = date_info_text.find(start_phrase) + len(start_phrase)
end_index = date_info_text.find(end_phrase)
closing_date_index = date_info_text.find(closing_date_phrase, end_index)  # Adjust to capture date only

# Extracting the opening and closing dates
opening_date = date_info_text[start_index:end_index].strip()
closing_date = date_info_text[end_index + len(end_phrase):closing_date_index].strip()

# Create a JSON object
date_json = json.dumps({"opening_date": opening_date, "closing_date": closing_date}, indent=4)

# Print the JSON output
print(date_json)
