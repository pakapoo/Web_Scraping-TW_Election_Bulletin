#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import win32api
import win32con
main_driver = webdriver.Chrome('C:\\chromedriver')
main_driver.get('http://eebulletin.cec.gov.tw/107/')#把你們要測試的網頁放在這邊\
ignore_list = ["臺南市","高雄市","新竹縣","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","基隆市","新竹市","嘉義市"]
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
    time.sleep(1)
    win32api.keybd_event(13,0,0,0)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
            
            
col = main_driver.find_element_by_xpath('/html/body/font/table')
cols = col.get_attribute('border')
sites = Stack()
homepage = 'http://eebulletin.cec.gov.tw/107/'
sites.push(homepage)
end = True
filetype = 'html'
while(not sites.isEmpty()):
    try:
        sites.pop()
        for x in range(1,250):
            for y in range(1, int(cols)+1):
                block = main_driver.find_element_by_xpath('/html/body/font/table/tbody/tr['+str(x)+']/th['+str(y)+']/a')
                if ("有聲" not in block.get_attribute('innerHTML')) and (block.get_attribute('innerHTML') not in ignore_list) and ("公民" not in block.get_attribute('innerHTML')) and ("?" not in block.get_attribute('innerHTML')):
                    sites.push(block.get_attribute('href'))
                    filetype = block.get_attribute('href')
    except:
        if filetype == 'pdf':
            time.sleep(1)
            download()
            time.sleep(2)
            main_driver.get(sites.peek())
            filetype = sites.peek()[-3:]
        elif filetype == 'mp3':
            filetype = sites.peek()[-3:]
            main_driver.get(sites.peek())
        else:
            filetype = sites.peek()[-3:]
            main_driver.get(sites.peek())


# In[ ]:




