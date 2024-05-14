from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import json
import concurrent.futures

def getDriver():

    options = Options()
    options.add_argument("window-size=1920,1080")
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    
    # Provide the path to your Chrome driver executable
    chrome_driver_path = "C:/Users/Zusakhe Mbebe/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe"
    service = Service(ChromeDriverManager().install())



    # Define any additional options if needed
    options = Options()
    options.add_argument("window-size=1920,1080")
    # Add any desired options to the options object here

    # Create the webdriver instance with the specified options
    driver = webdriver.Chrome(service= service, options=options)
    driver.get('https://www.mandela.ac.za/Study-at-Mandela/Discovery/Career-study-fields')

    time.sleep(2) 
    button = driver.find_element(By.CLASS_NAME, "acceptcookies")
    button.click()
    time.sleep(3) 
    return driver

Final_List = []
#buttons = ["A", "B", "C","D", "E", "F","G", "H", "I","J", "K", "L","M", "N", "O","P", "Q", "R","S", "T", "U","V", "W", "X","Y", "Z", "A"]

def scrape_module_data(driver):
    modules = driver.find_element(By.ID, 'modulelist')
    tables = modules.find_elements(By.TAG_NAME, 'table')

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:
            link = row.find_element(By.TAG_NAME, 'a')
            x = {'module': row.find_elements(By.TAG_NAME, 'td')[1].text, 'name': link.text, 'description': ''}
            
            link.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(0.2)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            description = driver.find_element(By.XPATH, '/html/body/form/div[5]/main/div[2]/div/div/div[2]/div[1]/div/div').text
            x['description'] = description
            time.sleep(0.1)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            
            Final_List.append(x)
            print(len(Final_List), '-------------current length.')
    with open('output.json', 'a') as file:
        json.dump(Final_List, file, indent=4)
        file.write('\n')
 
    return Final_List


     
def process(r):
    letter, index = r
    driver = getDriver()
    button = driver.find_element(By.LINK_TEXT, letter)
    time.sleep(0.1) 
    button.click()
    if True:
        div = "/html/body/form/div[5]/main/div[2]/div/div/div[2]/div[1]/div[3]"
        div_element = driver.find_element(By.XPATH, div)
        Career_ =  div_element.find_elements(By.TAG_NAME, "a")
        names = [c.text for c in Career_]

        if index > len(names):
            driver.quit()
            return True
        print(names)
        count = 0
        for career in Career_:
            if career.text == '':
                continue

            if count == index:
                career.send_keys(Keys.CONTROL + Keys.RETURN)  # Opens the link in a new tab
                time.sleep(0.2)
                # Access and perform iterations on the career page
                driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab
                time.sleep(0.1)
                div2 = "/html/body/form/div[5]/main/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div/div"
                div_ele = driver.find_element(By.XPATH, div2)
                qualifications =  div_ele.find_elements(By.CLASS_NAME, "card")
                for box in qualifications:
                    button = box.find_element(By.TAG_NAME, "h5")
                    button.click()
                    time.sleep(0.2)
                    button = box.find_element(by=By.CLASS_NAME, value="btn.btn-default.btn-MoreInfo")
                    time.sleep(0.2)
                    button.send_keys(Keys.CONTROL + Keys.RETURN)  # Opens the link in a new tab
                    time.sleep(0.2)
                    # Access and perform iterations on the career page
                    driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab
                    time.sleep(2)
                    button = driver.find_element(By.XPATH,"/html/body/form/div[5]/main/div[2]/div/div/div[2]/div[1]/span/div/ul/li[3]/a")
                    button.click()
                    time.sleep(40)
                    scrape_module_data(driver)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            else:
                count = count+1    

listoftupes = []

for letter in range(ord('A'), ord('Z') + 1):
    for number in range(0, 51):
        tuple_item = (chr(letter), number)
        listoftupes.append(tuple_item)

process(listoftupes[0])


                     


          
