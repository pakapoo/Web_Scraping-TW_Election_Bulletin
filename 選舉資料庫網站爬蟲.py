#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

website_list = []
simple_list = []
complex_list = []
county_list = ['http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101E1D1&qryType=ctks', 'http://db.cec.gov.tw/histMain.jsp?voteSel=20141101D1',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20091201D1D1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20051201D1D1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20020101D1D1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=19980101D1D1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101F1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101F2D2&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R2D2&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20100601C1D2&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101G1D3&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101D2D3&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101H1D4&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101R3D4&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101J1E1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20141101V1E1&qryType=ctks', 'http://db.cec.gov.tw/histQuery.jsp?voteCode=20101101V1E1&qryType=ctks',
              'http://db.cec.gov.tw/histQuery.jsp?voteCode=20100601S1E1&qryType=ctks']
county_list1 = ['http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101E1D1&qryType=ctks', 'http://db.cec.gov.tw/histMain.jsp?voteSel=20141101D1']
simple_list1 = ['http://db.cec.gov.tw/histQuery.jsp?voteCode=20181101A1B1&qryType=ctks']

def listappend(temp_list, name, party, place, position):
    temp_list.append(name)
    if(len(name)==4):
        temp_list.append(name[:2])
        temp_list.append(name[2:])
    else:
        temp_list.append(name[0])
        temp_list.append(name[1:])
    temp_list.append("選舉資料庫網站")
    temp_list.append(party+"，"+position)
    temp_list.append(place)
    return temp_list

main_driver = webdriver.Chrome('C:\chromedriver.exe')
main_driver.implicitly_wait(2)

for county in county_list1:
    main_driver.get(county)
    nothing=0
    for i in range(2, 10):
        if(nothing>2):
            break
        else:
            count_error=0
            include_one=0
            for j in range(1, 8):
                try:
                    place = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(i)+']/td['+str(j)+']/a')
                    href = place.get_attribute('href')
                    complex_list.append(href)
                    if(j==1):
                        include_one=1
                except Exception as e:
                    count_error+=1
                    if(j==1):
                        pass
                    elif(j==2 and include_one!=1):
                        nothing+=1
                        break
                    else:
                        break
            
website_list = complex_list + simple_list1
data_list = []
for website in website_list: 
    main_driver.get(website)
    rows = 2
    while(True):
        try:
            tmp = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[1]')
            subrows = tmp.get_attribute('rowspan')
            tmp_place = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[1]/a')
            place = tmp_place.get_attribute('innerHTML')
            tmp_name = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[2]/a')
            name = tmp_name.get_attribute('innerHTML')
            tmp_party = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[6]')
            party = tmp_party.get_attribute('innerHTML')
            tmp_pos = main_driver.find_element_by_xpath('//div[@class="titlebox"]/div/div')
            pos = tmp_pos.get_attribute('innerHTML')
            start = pos.find('年')+1
            end = pos.find('選')
            position = pos[start:end]
            temp_list = []
            temp_list = listappend(temp_list, name, party, place, position)
            data_list.append(temp_list)
            rows+=1
            for i in range(int(subrows)-1):
                tmp_name = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[1]/a')
                name = tmp_name.get_attribute('innerHTML')
                tmp_party = main_driver.find_element_by_xpath('//table[@class="ctks"]/tbody/tr['+str(rows)+']/td[5]')
                party = tmp_party.get_attribute('innerHTML')  
                tmp_pos = main_driver.find_element_by_xpath('//div[@class="titlebox"]/div/div')
                pos = tmp_pos.get_attribute('innerHTML')
                start = pos.find('年')+1
                end = pos.find('選')
                position = pos[start:end]
                temp_list = []
                temp_list = listappend(temp_list, name, party, place, position)
                data_list.append(temp_list)
                rows+=1
        except Exception as e:
            break

for people in data_list:
    print("[", end="")
    for j in range(len(people)-1):
        print(people[j]+", ", end="")
    print(people[len(people)-1], end="")
    print("]")
    
with open('complex_list.csv', 'w', newline='', encoding = 'utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['姓名', '姓', '名', '來源', '法人', '地區'])
    for people in data_list:
        writer.writerow(people)


# In[ ]:





# In[ ]:




