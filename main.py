from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import datetime
import sys, os
from datetime import date
import time

# to build: pyinstaller ./main.py --onefile  --add-binary "./driver/chromedriver.exe;./driver"

def cardInfo():
    card = input("Enter last 4 digits of card: ")
    swipes = input("Enter number of swipes: ")
    return card, int(swipes)

# Navigates login page
# Unused due to unknown issue, possibly anti-automation security  
# def login(websiteDriver):
    
#     try:
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.ID, "user"))
#         )
#     except:
#         print("Login Error")
#         driver.quit()

#     driver.implicitly_wait(20)
#     userID = driver.find_element_by_id('user')
#     userID.send_keys("")
#     password = driver.find_element_by_id('passwd')
#     password.send_keys("")
#     #password.send_keys(Keys.RETURN)
#     driver.find_element_by_class_name('submit').click()

def paymentPage(paymentDate, websiteDriver, cardNumber):

    try:
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "customAmount"))
    )
    except:
        print("Error navigating payment page")
        driver.quit()
    amount = driver.find_element_by_id("customAmount")
    amount.clear()
    amount.send_keys(str(paymentAmount))

    ''' # Attempts to use calendar widget, selecting final date not working

    # Selects calendar to open up days of the month
    driver.find_element_by_class_name("DayPickerInput").click()
    
    # formerly worked 
    # dateSelector = "div[aria-label="+dateAmount+"]"


    # test option for later
    #test_button4 = driver.find_elements_by_class_name('test_button4') # notice its "find_elementS" with an S
    #submit_element = [x for x in test_button4 if x.get_attribute('value') == 'Update'] 
    
    # Day element name for debug purposes
    # <div class="DayPicker-Day" tabindex="-1" role="gridcell" aria-label="Mon Apr 12 2021" aria-disabled="false" aria-selected="false">12</div>
    
    
    # used to work
    # driver.find_element_by_css_selector(dateSelector).click()
    '''
    element = driver.find_element_by_id("date").click()
    element = driver.find_element_by_id("date").clear()
    element = driver.find_element_by_id("date").click()
    actions = ActionChains(driver) 
    actions.send_keys(dateAmount)
    actions.perform()

    driver.find_element_by_xpath("//*[contains(text(), "+cardNumber+")]").click()
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continue')]")))
    element.click()
    driver.find_element_by_class_name('action__item').click()

    # try:
    #     driver.find_element_by_xpath("//*[contains(text(), 'Continue')]").click()
    #     WebDriverWait(driver, 30).until(
    #     lambda driver: driver.current_url != 'https://payments.xfinity.com/new')
    # except:
    #     print("Error getting to payment screen")
    #     #driver.quit()  
    try:
        WebDriverWait(driver, 30).until(
        lambda driver: driver.current_url == 'https://payments.xfinity.com/new/review')
    except:
        print("Error getting to review screen")
        #driver.quit()  
    
    driver.find_element_by_class_name('action__item').click()

    # try:
    #     WebDriverWait(driver, 30).until(
    #     lambda driver: driver.current_url == 'https://payments.xfinity.com/new/confirmation')
    # except:
    #     print("Error with processing payment")
    #     driver.quit()  

if __name__ == "__main__":
    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # driver
    driver.get("https://payments.xfinity.com/new")
    driver.implicitly_wait(1)
    while input("\nBeginning of swipe loop\nLogin and hit enter to continue or q to quit: ") != "q":
        # TODO: Ability to specify start date in future format MM/DD/YYYY
        # dateStartChoice = int(input("\nEnter (1) to start swipes on today's date or (2) to enter a future start date: "))
        
        paymentDate = date.today()
        #paymentDate += datetime.timedelta(days=4)
        cardNumber, numberSwipes = cardInfo()
        schedule = int(input("Enter (1) for all payments made today or (2) for one cent payments spread out: "))
        if schedule == 1:
            paymentAmount = numberSwipes
        elif schedule == 2:
            paymentAmount = 0.01
        else:
            print("Invalid entry")
            quit(-1)
        for x in range (numberSwipes):
            driver.get("https://payments.xfinity.com/new")
            # below is meant for calendar use
            #dateAmount = "'"+paymentDate.strftime('%A')[0:3]+paymentDate.strftime(' %B')[0:4]+paymentDate.strftime(' %d')+paymentDate.strftime(' %Y')+"'"
            dateAmount = paymentDate.strftime('%m')[0:3]+'/'+paymentDate.strftime('%d')[0:3]+'/'+paymentDate.strftime('%Y')[0:4] 
            paymentPage(dateAmount, driver, cardNumber)
            if schedule == 1:
                paymentAmount -= 1
            elif schedule == 2:
                paymentDate += datetime.timedelta(days=1)

    driver.quit()
    quit(0)
