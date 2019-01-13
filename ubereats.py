from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
import shelve

browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.ubereats.com')
address = "IIIT Bangalore Back Gate, Infosys Avenue, Electronic City Phase 1, Bangalore, Infosys Avenue, Electronic City Phase 1, Bangalore"
restaurant = 'paradise'
browser.find_element_by_css_selector('input#address-selection-input').send_keys('Infosys Avenue')

time.sleep(3)

browser.find_element_by_css_selector('div.ue-iq').click()

time.sleep(5)
search = browser.find_element_by_css_selector('input')
search.send_keys("paradise")
search.send_keys(Keys.ENTER)
time.sleep(5)

rest = browser.find_elements_by_css_selector("a.base_") 

for i in rest:
    if 'paradise' in i.text.lower():
        rest = i
        break
try:
    rest.click()
except:
    print("Restaurant not there")
    
time.sleep(10)
shelfFile = shelve.open('mydata')
itemname = shelfFile['itemname']
free_of_cost_selection = shelfFile['free_of_cost_selection']
uberitem=[]
for i in range(4):
    uberitem.append(browser.find_element_by_xpath("//div[@title='{0}']".format(itemname[i])))

t=0
for i in range(4):
        name_of_item = browser.find_element_by_xpath("//div[text()='{0}']".format(itemname[i]))
        browser.execute_script("arguments[0].click();",name_of_item)
        time.sleep(2)
        try:
           select =  browser.find_element(By.XPATH, "//div[text()='{0}']".format(free_of_cost_selection[t]))
           t+=1
           select.click()
        except:
            pass
        add_to_cart = browser.find_elements_by_xpath("//button[@type='button']")
        for i in add_to_cart:
            if "Add" in i.text:
                add_to_cart = i
                print(add_to_cart.text)
                break
        add_to_cart.click()
        time.sleep(3)



