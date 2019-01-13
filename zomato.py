from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import shelve
import sys

######INITIALIZING ALL DATA AND TAKING INPUTS
shelfFile = shelve.open('mydata')
program_run = input("ARE YOU RUNNING THE PROGRAM FOR THE FIRST TIME(y/n) ")
os = input("ARE YOU RUNNING MACOS OR LINUX(mac/linux) ")
shelfFile['os'] = os
if program_run == 'y':
    print("MAKE SURE YOU HAVE A VALID ZOMATO ACCOUNT AND IIIT-B WORKING ADDRESS SETUP")
    loginid = input('ENTER YOUR GMAIL ID ')
    password = input('ENTER YOUR GMAIL PASSWORD ')
    shelfFile['loginid'] = loginid
    shelfFile['password'] = password
else:
    email_change = input("DID YOU CHANGE YOUR EMAIL ID OR PASSWORD(y/n) ")
    if email_change == 'y':
        loginid = input('ENTER YOUR GMAIL ID ')
        password = input('ENTER YOUR GMAIL PASSWORD ')
        shelfFile['loginid'] = loginid
        shelfFile['password'] = password


restaurant = input('PLEASE ENTER THE NAME OF THE RESTAURANT ')
shelfFile['restaurant'] = restaurant
if shelfFile['os'] == 'linux':
	browser = webdriver.Chrome(executable_path=r"./chromedriver")
elif shelfFile['os'] == 'mac':
	browser = webdriver.Chrome(executable_path=r"./chromedriver_for_mac")
address = "IIIT Bangalore Back Gate, Infosys Avenue"

###STARTING ZOMATO

browser.get('https://www.zomato.com/bangalore/order-food-online')
time.sleep(3)
browser.find_element_by_xpath("//a[@id='signin-link']").click()
time.sleep(7)
google_signin = browser.find_element_by_css_selector("a.ui.basic.fluid.massive.button.zs-google-connect-btn.google-redirect-link")
google_signin.click()
time.sleep(3)

default = browser.current_window_handle
browser.switch_to_window(browser.window_handles.pop())

###GOOGLE SIGN IN
google_signin_email = browser.find_element_by_css_selector('input#identifierId')
google_signin_email.send_keys(shelfFile['loginid'])
google_signin_email.send_keys(Keys.ENTER)
time.sleep(3)
google_signin_password = browser.find_element_by_css_selector('input.whsOnd.zHQkBf')
google_signin_password.send_keys(shelfFile['password'])
google_signin_password.send_keys(Keys.ENTER)
time.sleep(3)
for i in range(2):
    try:
        browser.find_element_by_css_selector('span.RveJvd.snByac').click()
    except:
        continue
time.sleep(7)
browser.switch_to_window(default)
browser.find_element_by_css_selector('i.close.icon').click()
#SIGN IN OVER

#PUTTING STREET NAME
inputaddr = browser.find_elements_by_css_selector('input')
for i in inputaddr:
    if i.get_attribute('placeholder') == 'Please select your delivery location':
        inputaddr=i
        break

inputaddr.send_keys('Infosys')
time.sleep(5)
inputaddr.send_keys(' Avenue')
time.sleep(7)
s=browser.find_elements_by_css_selector("div.title")
for i in s:
    if i.text == "Infosys Avenue, Electronic City Phase 1, Bangalore":
        s=i
        break
s.click()
time.sleep(5)
input_restaurant = browser.find_elements_by_css_selector('input.prompt.input_box')
for  i in input_restaurant:
    if i.get_attribute('placeholder') == "Search for restaurants or cuisines...":
        input_restaurant = i
        break

##PUTTING RESTAURANT
input_restaurant.send_keys(restaurant)
time.sleep(3)

##CLICKING THE ORDER ONLINE BUTTON
orderbuttons = browser.find_elements_by_xpath("//div[@data-position='1-1']")
orderbuttons = orderbuttons[len(orderbuttons)-1]
time.sleep(10)
orderlink = orderbuttons.find_elements_by_tag_name("a")
currently_offline = orderbuttons.find_elements_by_tag_name('p')

##CHECKING FOR CURRENTLY OFFLINE
for i in currently_offline:
    if i.text == "Currently Offline":
        print("RESTAURANT NOT THERE ON ZOMATO")
        sys.exit()
for i in orderlink:
    if i.text == "Order Online":
        orderlink = i
orderlink.click()
time.sleep(5)

##FOR RESTAURANTS LIKE DOMINOS PUTTING ADDRESS AT THE START
try:
        browser.find_element_by_css_selector('div.ui.green.vendorAddressPromptButton').click()
        time.sleep(2)
        browser.find_element_by_css_selector('input.prompt').send_keys('INTERNATIONAL INSTITUTE OF INFORMATION TECHNOLOGY')
        time.sleep(2)
        browser.find_element_by_css_selector('a.result').click()
        time.sleep(2)
        browser.find_element_by_css_selector('input.street_add').send_keys(address)

        time.sleep(2)
        browser.find_element_by_css_selector('div.ui.button.green.save-new-address').click()
except:
        pass

time.sleep(5)

##GETTING ALL ITEMS ITEMNAMES AND ITEM ADD BUTTONS
item = browser.find_elements_by_css_selector('div.ui.item.item-view')
item = item[:10]
itemname =[]
itemadd=[]
##CHECKING FOR DUPILCACY OF ANY ELEMENT AND REMOVING IT
for i in range(len(item)):
    itemadd.append(item[i].find_element_by_tag_name("a"))
    itemname.append(item[i].find_element_by_css_selector("div.header"))
    for j in itemname[:-1]:
        if j.text == itemname[-1].text:
            itemadd.pop(-1)
            itemname.pop(-1)

##TAKING ONLY 4 ITEMS
itemadd = itemadd[:4]
itemname = itemname[:4]
l = [i.text for i in itemname]
shelfFile['itemname']=l
for i in itemname:
    print(i.text)

#ADDING ITEMS IN CART
for i in itemadd:
    i.click()
    time.sleep(3)
    try:
        add_to_cart = browser.find_element_by_css_selector('div.ui.green.button')
        add_to_cart.click()
        time.sleep(3)
    except:
        continue
##PRESSING THE CONTINUE BUTTON
continue_button = browser.find_element_by_css_selector("button.ui.large.green.fluid.button.checkout")
continue_button.click()

time.sleep(3)
try:
    browser.switch_to_window(browser.window_handles.pop())
    address_select = browser.find_element_by_xpath("//input[@name='address']")
    address_select.click()
    time.sleep(3)
    continuebtn = browser.find_elements_by_css_selector("button.ui.green.button")
    continuebtn = continuebtn[len(continuebtn)-1]
    continuebtn.click()
    time.sleep(3)
    browser.switch_to_window(default)
except:
    pass

tot = browser.find_element_by_css_selector('li.total.clear.clearfix')

##GETTING THE PRICE AT ZOMATO
price_at_zomato = tot.find_elements_by_xpath("//span[@class='price right']")
price_at_zomato = price_at_zomato[-1]
shelfFile['price_at_zomato'] = price_at_zomato.text
shelfFile.close()

