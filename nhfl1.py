# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:22:50 2019

@author: kumar.shivam
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import glob
import sys
import getpass



aa = sys.argv[1]
aa = int(aa)
zz = sys.argv[2]
zz = int(zz)

user = getpass.getuser()

def downloads_done():
#    for i in os.listdir("C:\\Users\\1540\\Downloads\\"):
#        if ".crdownload" in i:
#            return True
    count = 0     
    for name in glob.glob('C:\\Users\\'+user+'\\Downloads\\*.crdownload'):
        count = count+1
    if count > 5:
        return True
        


def wait_until(period=0.25):
  mustend = time.time() + 100000000
  while time.time() < mustend:
    if downloads_done() != True: 
        return True
    time.sleep(period)
  return False

driver = webdriver.Chrome()
driver.get('https://msc.fema.gov/portal/advanceSearch#searchresultsanchor')

for j in range(aa,zz):
    my1 = None
    while my1 is None:
        try:
            mySelect = Select(driver.find_element_by_name("selstate"))
            print(j)
            k = str(j)
            my = mySelect.select_by_index(k)
            my1 = 2
        except:
             pass
    print(my1)
    
    my1 = None
    while my1 is None:
        try:
            print(my1)
            mySelect1 = Select(driver.find_element_by_name("selcounty"))
            my1 = mySelect1.select_by_index("1")
            my1 = 2
        except:
             pass
        
    my2 = None
    while my2 is None:
        try:
            print(my2)
            mySelect2 = Select(driver.find_element_by_name("selcommunity"))
            my2 = mySelect2.select_by_index("1")
            my2 = 3
        except:
            pass
    
    python_button = driver.find_element_by_id('mainSearch')
    python_button.click()
    
    my3 = None
    while my3 is None:
        try:
            python_button = driver.find_element_by_id('eff_root')
            python_button.click()
            my3 = 3
        except:
            pass
            
    
    my4 = None
    while my4 is None:
        try:
            python_button = driver.find_element_by_id('eff_nfhl_state_root')
            python_button.click()
            my4 = 4
        except:
            pass
    
    time.sleep(3)
    
    text1 = str(driver.find_element_by_xpath("//*[@id='nfhl_state_list']/tr[1]/td[3]").text)
    
    print(text1)
#    date_str = "05/11/2019"
#    format_str = '%d/%m/%Y' # The format
#    format_str1 = '%m/%d/%Y'
#    date_str = datetime.datetime.strptime(date_str, format_str)
#    text12 = datetime.datetime.strptime(str(text1), format_str)
     
    if 0 == 0:                                    
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if "STATE" in elem.get_attribute("href"):        
                x = elem    
                
                if wait_until() == True:
                    x.click()
                    
            
        driver.refresh()
    else:
        print("kaboom")

#

#            
#
#if downloads_done() == False:
#    print("hero")

    


