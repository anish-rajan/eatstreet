import time
print("                           WELCOME TO EAT STREET")
time.sleep(1)
print("                    THE BEST PLACE TO MAKE THE BEST ORDER")
time.sleep(1)
print("       THIS IS AN APPLICATION TO FIND OUT WHERE A RESTAURANT IS CHEAPER")
time.sleep(1)
print("                              ZOMATO OR SWIGGY")
time.sleep(1)
print("             JUST SAY THE NAME OF THE RESTAURANT AND SIT BACK AND RELAX")
time.sleep(1)
print("                           LET YOUR LAPTOP DO THE JOB.\n")
time.sleep(1)
print("           PLEASE DO NOT USE YOUR LAPTOP AS THE PROGRAM EXECUTES\n")

print("CURRENTLY DOMINOS DOES NOT WORK")

import zomato
import swiggy
import shelve

print("                         THE PRICES IN BOTH ARE")

shelfFile = shelve.open('mydata')

print("PRICE AT ZOMATO: "+shelfFile['price_at_zomato'])
print("PRICE AT SWIGGY: "+shelfFile['price_at_swiggy'])

shelfFile.close()

