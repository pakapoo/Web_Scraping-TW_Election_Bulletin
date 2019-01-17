#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import json

county_list = ['http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101E1D1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101D1D1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20091201D1D1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20051201D1D1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20020101D1D1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=19980101D1D1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101F1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101F2D2&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R2D2&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20100601C1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101G1D3&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101D2D3&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101H1D4&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R3D4&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101J1E1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101V1E1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20101101V1E1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20100601S1E1&qryType=ctks']
county_list1 = ['http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101E1D1&qryType=ctks']
main_driver = webdriver.Chrome('C:\\Users\\User\\.conda\\chromedriver')  # 注意你們放CHROMEDRIVER的位置
main_driver.implicitly_wait(2)
for county in county_list1:
    main_driver.get(county)
    body = main_driver.find_element_by_tag_name('tbody')
    trs = body.find_elements_by_xpath('.//tr[contains(@class, "data")]')
    state_and_href_list =[]
    for tr in trs :
        tds = tr.find_elements_by_xpath('.//td')#'.//td[not(@rowspan)]')
        try:
            for td in tds:
                if(td.get_attribute('rowspan') is not None): 
                    state_name = td.text
                else: 
                    state_and_href_list.append([state_name,td.find_element_by_tag_name('a').get_attribute("href"),td.find_element_by_tag_name('a').text])
        except NoSuchElementException: print("empty")
main_driver.close()
all_name_and_data =[]
for state_and_href in  state_and_href_list:
    driver = webdriver.Chrome('C:\\Users\\User\\.conda\\chromedriver')  # 注意你們放CHROMEDRIVER的位置
    driver.implicitly_wait(2)
    driver.get(state_and_href[1])
    body = driver.find_element_by_tag_name('tbody')
    trs = body.find_elements_by_xpath('.//tr[contains(@class, "data")]')
    for tr in trs :
        tds = tr.find_elements_by_xpath('.//td')#'.//td[not(@rowspan)]')
        temp_name_and_data=[]
        for td in tds:
            if(td.get_attribute('rowspan') is not None): 
                county_name = td.text
            else: 
                temp_name_and_data.append(td.text)
        all_name_and_data.append([temp_name_and_data[0],temp_name_and_data[4],county_name])
    driver.close()
#print("State: "+state_and_href[0]+" Href is:"+state_and_href[1]+" County is: "+state_and_href[2])
with open('output.csv', 'w', newline='', encoding = 'utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['姓名', '姓', '名', '來源', '法人', '地區'])
    for people in all_name_and_data:
        temp_list = []
        temp_list.append(people[0])
        if(len(people[0])==4):
            temp_list.append(people[0][:2])
            temp_list.append(people[0][2:])
        else:
            temp_list.append(people[0][0])
            temp_list.append(people[0][1:])
        temp_list.append('選舉資料庫網站')
        temp_list.append(people[1])
        temp_list.append(people[2])
        writer.writerow(temp_list)
 
for name_and_data in all_name_and_data:
    print("姓名:"+name_and_data[0]+" 法人:"+name_and_data[1]+" 地區:"+name_and_data[2])


# In[ ]:




