from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
import shelve

shelfFile = shelve.open('mydata')
if shelfFile['os'] == 'linux':
	browser = webdriver.Chrome('./chromedriver')
elif shelfFile['os'] == 'mac':
	browser = webdriver.Chrome(executable_path=r"./chromedriver_for_mac")
browser.get('https://www.swiggy.com/')
browser.maximize_window()
browser.find_element_by_css_selector('input#location').send_keys("Infosys Avenue")
time.sleep(1)
browser.find_element_by_css_selector('span').click()
time.sleep(5)

try:
    browser.find_element_by_xpath("//div[text()='ADD MORE DETAILS']").click()
    time.sleep(1)
    browser.find_element_by_css_selector("input#building").send_keys("IIIT-B Back Gate")
    browser.find_element_by_css_selector("input#landmark").send_keys("Opp Infosys Gate 10")
    browser.find_element_by_xpath("//input[text()='SAVE ADDRESS & PROCEED']").click()
    time.sleep(2)
except:
    pass
time.sleep(5)
browser.find_element_by_xpath("//span[text()='Search']").click()
time.sleep(3)
input_restaurant = browser.find_element_by_xpath("//input[@placeholder='Search for restaurants or dishes']")
input_restaurant.send_keys(shelfFile['restaurant'])
input_restaurant.send_keys(Keys.ENTER)
time.sleep(3)
try:
    restaurants = browser.find_elements_by_css_selector("div.nA6kb")
    for i in restaurants:
        if shelfFile['restaurant'].lower() in i.text.lower():
            restaurants = i
            break
    restaurants.click()
except:
    print("RESTAURANT NOT THERE ON SWIGGY")
    sys.exit()
time.sleep(4)
try:
    outlets = browser.find_elements_by_css_selector('a.PjY5w')
    outlets = outlets[-1]
    outlets.click()
    time.sleep(5)
except:
    pass
itemname = shelfFile['itemname']
search_for_item = browser.find_element_by_xpath("//input[@placeholder='Search for dishes...']")
for i in range(4):
    if '&' in itemname[i]:
        itemname[i] = itemname[i].replace('& ','')
    elif 'and' in itemname[i]:
        itemname[i] = itemname[i].replace('and ','')
    search_for_item.send_keys(itemname[i])
    time.sleep(2)
    if(len(browser.find_elements_by_xpath("//div[text()='We couldn’t find any items matching your search. Please try a new keyword.']"))>=1):
        browser.find_element_by_css_selector('span.icon-close-thin').click()
        s=0
        l=itemname[i]
        j=0
        while(j<len(l)):
            if l[j] == " ":
                l = l.replace(l[:j+1],"")
                search_for_item.send_keys(l)
                j=0
                time.sleep(2)
                j+=1
                if(len(browser.find_elements_by_xpath("//div[text()='We couldn’t find any items matching your search. Please try a new keyword.']"))==0):
                    break
                else:
                     browser.find_element_by_css_selector('span.icon-close-thin').click()
            else:
                j+=1
                    

    browser.find_element_by_xpath("//div[text()='ADD']").click()
    time.sleep(2)
    try:
        steps = browser.find_element_by_xpath("//span[contains(text(),'Step')]")
        steps=steps.text[-1]
        for i in range(int(steps)):
             browser.find_element_by_xpath("//span[text()='Continue']").click()
             time.sleep(1)
    except:
        pass
    try:
        browser.find_element_by_xpath("//span[text()='Add Item']").click()
        time.sleep(2)
    except:
        pass
    browser.find_element_by_css_selector('span.icon-close-thin').click()


browser.find_element_by_xpath("//div[contains(text(),'Checkout')]").click()
time.sleep(3)
price_on_swiggy = browser.find_element_by_css_selector('div._3ZAW1')
shelfFile['price_at_swiggy'] = price_on_swiggy.text
shelfFile.close()



