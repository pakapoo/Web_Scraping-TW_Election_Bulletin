#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.getcwd()
os.chdir('C:/Users/Mark/Desktop/選舉公報')
os.getcwd()


# In[86]:


import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import win32api
import win32con

class Stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)

def download():
    win32api.keybd_event(17,0,0,0)
    win32api.keybd_event(83,0,0,0)
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(5)
    win32api.keybd_event(13,0,0,0)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
                  
def main_program(homepage, ignore_list):
    now = ''
    main_driver = webdriver.Chrome('C:\\chromedriver')
    main_driver.get(homepage)
    sites = Stack()
    sites.push(homepage)
    end = True
    filetype = 'html'
    now = ''
    possible_two_column = 0
    while(not sites.isEmpty()):
        try:
            sites.pop()
            #col = main_driver.find_element_by_xpath('/html/body/font/table')
            #cols = col.get_attribute('border')
            for x in range(1,100):
                for y in range(1, 4):
                    if y==3 and possible_two_column == 0:
                        try:
                            block = main_driver.find_element_by_xpath('/html/body/font/table/tbody/tr['+str(x)+']/th['+str(y)+']/a')
                        except Exception as e:
                            possible_two_columns = 1
                            continue
                    else:
                        block = main_driver.find_element_by_xpath('/html/body/font/table/tbody/tr['+str(x)+']/th['+str(y)+']/a')
                    if ("?" in block.get_attribute('innerHTML')):  #To record error and manually download them (if any)
                        print(block.get_attribute('innerHTML'))
                    if all(s not in (block.get_attribute('innerHTML')) for s in ignore_list):
                        possible_two_columns = 0
                        sites.push(block.get_attribute('href'))
        except:
            if filetype == 'pdf' or filetype == 'PDF':
                if "台北市" in now or "臺北市" in now:    #臺北通常要load比較久
                    time.sleep(10)
                else:
                    time.sleep(3)
                download()
                time.sleep(1)
                if(not sites.isEmpty()):
                    filetype = sites.peek()[-3:]
                    now = sites.peek()
                    main_driver.get(sites.peek())
            elif filetype == 'mp3':
                if(not sites.isEmpty()):
                    filetype = sites.peek()[-3:]
                    main_driver.get(sites.peek())
            else:
                if(not sites.isEmpty()):
                    filetype = sites.peek()[-3:]
                    main_driver.get(sites.peek())

                            
                
#--------------------Main Program--------------------#
ignore_list_107 = ["區長", "議員", "有聲", "公民", "里長", "代表", "鄉鎮市", "?"]
homepage_107 = 'http://eebulletin.cec.gov.tw/107/'
homep = 'http://ebulletin.cec.gov.tw/%E9%81%B8%E8%88%89/%E7%B8%A3%E5%B8%82%E9%95%B7/86%E5%B9%B4/list2.php'
ignore_list_old = []
homepage_old = []  #http://bulletin.cec.gov.tw/bin/home.php
with open("web_list_old.txt") as file:
    alllines = file.readlines()
    for line in alllines:
        homepage_old.append(line)
        
try:
    main_program(homepage_107, ignore_list_107)  #「花蓮縣縣長議員選舉公報」需另外抓
except Exception as e:
    print(e)
try:
    for sites in homepage_old:
        print(sites)
        main_program(sites, ignore_list_old)
        time.sleep(20)
except Exception as e:
    print(e)


# In[ ]:











# In[ ]:





# In[ ]:




