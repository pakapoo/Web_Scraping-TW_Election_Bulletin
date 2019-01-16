#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#county_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', "I", 'J', 'K', "M", "N", "O", "P", "Q", "T", "U", "V", "W", "X", "Z"]

main_driver = webdriver.Chrome('C:\chromedriver.exe')
main_driver.implicitly_wait(30)

data_list = []
main_driver.get('https://pri.land.moi.gov.tw/agents_query/iamqry_11a.asp?Page=1')
total_pages = main_driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/table[3]/tbody/tr/td/p/font[3]')
tp = int(total_pages.get_attribute('innerHTML')[2:])
print("total pages:", tp)

for page in range(1, tp+1):
    time.sleep(5)
    main_driver.get('https://pri.land.moi.gov.tw/agents_query/iamqry_11a.asp?Page='+str(page))
    count_error = 0 
    page+=1
    for people in range(2,17):
        temp_list = []
        try:
            tmp = main_driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr['+str(people)+']/td[2]/p')
            name = tmp.get_attribute('innerHTML').replace(" ","").replace('\n', "")
            temp_list.append(tmp.get_attribute('innerHTML').replace(" ","").replace('\n', ""))
            if(len(name)==4):
                temp_list.append(name[:2])
                temp_list.append(name[2:])
            else:
                temp_list.append(name[0])
                temp_list.append(name[1:])
            temp_list.append('地政士開業資料')
            tmp = main_driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr['+str(people)+']/td[6]/p')
            temp_list.append(tmp.get_attribute('innerHTML').replace(" ","").replace('\n', ""))
            tmp = main_driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr['+str(people)+']/td[3]/p')
            temp_list.append(tmp.get_attribute('innerHTML').replace(" ","").replace('\n', ""))
            data_list.append(temp_list)
        except Exception as e:
            count_error+=1 
            print(e)
        if(count_error>1):
            break

with open('output.csv', 'w', newline='', encoding = 'utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['姓名', '姓', '名', '來源', '法人', '地區'])
    for people in data_list:
        writer.writerow(people)
    
for people in data_list:
    print("[", end="")
    for j in range(len(people)-1):
        print(people[j]+", ", end="")
    print(people[len(people)-1], end="")
    print("]")
        
    


# In[ ]:




