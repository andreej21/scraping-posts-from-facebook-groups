import io
import json
import os
import time
from datetime import date, datetime, timedelta

import pandas as pd
import requests
from numpy import random
from openpyxl import load_workbook
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

f = open("parameters.json")
data = json.load(f)

PATH = 'venv\msedgedriver.exe'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'
edge_options = Options()
edge_options.add_experimental_option('detach',True)
edge_options.add_argument(f'user_agent={user_agent}')
edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
edge_options.add_argument("--disable-popup-blocking")
edge_options.add_argument('--disable-default-apps')
edge_options.add_argument('--allow-silent-push')
edge_options.add_argument('--disable-notifications')
edge_options.add_argument('--suppress-message-center-popups')
edge_options.add_argument('--inprivate')

edge_service = Service(PATH)
driver = webdriver.Edge(service=edge_service,options=edge_options)

text_contents=[]

num=0
image_directory = 'image folder'
full_directory = data["image_saving_directory"]
driver.get('https://www.facebook.com/')
time.sleep(1)
username = data["email"]
password = data["password"]
user_box = driver.find_element(By.XPATH,'//*[@id="email"]').send_keys(username)
user_pw = driver.find_element(By.XPATH,'//*[@id="pass"]').send_keys(password,Keys.RETURN)
time.sleep(2)
list_groups = ['https://www.facebook.com/groups/3207403259329762/','https://www.facebook.com/groups/jesusadrianromeromusicacristiana/','https://www.facebook.com/groups/jesusadrianromerooficial/','https://www.facebook.com/groups/JesusAdrianRomeroMusicaCristiana1/','https://www.facebook.com/groups/1175792979441047']

try:

    for i in list_groups:

        driver.get(i)


        time.sleep(2)

        for i in range(0,12):
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(2)

        try:

            feed = driver.find_element(By.XPATH,'//div[@role="feed"]')
            all_posts = feed.find_elements(By.XPATH,'./div[@class="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]')
            time.sleep(1)
        except:
            continue

        for post in all_posts:
            try:
                likes = post.find_element(By.XPATH,'.//span[@class="x16hj40l"]').get_attribute('innerText')

            except:
                pass
            if 'K' in likes:
                
                try:
                    try:
                        post.find_element(By.XPATH,'.//div[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f" and @role="button"]').click()
                        time.sleep(1)
                        text_content = post.find_element(By.XPATH,'.//div[@dir="auto" and @style="text-align: start;"]').get_attribute('innerText')
                        if "See more" in text_content:
                            text_content.replace("See more",'')    
                        text_contents.append(text_content)                        
                    except:                            
                        text_content = post.find_element(By.XPATH,'.//div[@dir="auto" and @style="text-align: start;"]').get_attribute('innerText')
                        if "See more" in text_content:
                            text_content.replace("See more",'')
                        text_contents.append(text_content)
                except:
                    pass
                try:
                    image = post.find_element(By.TAG_NAME,'img').get_attribute("src")
                    
                    try:

                        img_content = requests.get(image).content
                        img_file = io.BytesIO(img_content)
                        img = Image.open(img_file)
                        file_pth = full_directory+f'\img{num}.jpeg'
                        with open(file_pth,'wb') as file:
                            img.save(file,'JPEG')
                        num+=1

                    except:
                        pass
                except:
                    pass


        text_data = pd.DataFrame({'Content':text_contents})
        text_data.to_excel('Fb.xlsx',index=False)
    
except:
    driver.quit()
group_for_posting = data["post_link"]

dir_list = os.listdir(full_directory)
desc =  data["description"]
now = datetime.now() + timedelta(minutes=1)
for element in dir_list:
    try:

        date = now.strftime("%B %d, %Y")
        time_now_hours = now.strftime("%H")
        time_int = int(time_now_hours)
        if time_int > 12:
            time_int-=12
            
        time_now_hours = str(time_int)

        time_now_mins = now.strftime(":%M%p")
        time_now = time_now_hours + time_now_mins

        
        
        
        driver.get(group_for_posting)
        time.sleep(1)
        file_name = full_directory+'\\'+element
        driver.find_element(By.XPATH,'//input[@accept="image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv"]').send_keys(file_name)

        time.sleep(1)
        driver.find_element(By.XPATH,'//div[@role="textbox" and @style ="outline: none; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;"]').send_keys(desc)
        time.sleep(1)
        driver.find_element(By.XPATH,'//div[@aria-label="Schedule post"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//div[@style="transform: translateX(0%) translateZ(1px);"]//input[@dir="ltr" and @role="combobox"]').send_keys(date)
        driver.find_element(By.XPATH,'//input[@aria-haspopup="listbox"]').send_keys(time_now)
        driver.find_element(By.XPATH,'//div[@aria-label="Schedule"]').click()
        time.sleep(5)
        os.remove(file_name)
        now+=timedelta(hours=data["schedule_hours_increment"])
    except:
        continue


folder = 'C:\pyprojects\scraping fb\image folder'


data_file = 'Fb.xlsx'

wb = load_workbook(data_file)

ws = wb['Sheet1']

all_rows = list(ws.rows)
row_values = []

first = True
for row in all_rows:
    if first:
        first=False
        continue
    row_values.append(row[0].value)

my_set = set(row_values)
try:
        
    for element in my_set:
        if 'See more' in element:
            continue
        driver.get(group_for_posting)
        time.sleep(0.2)
        e = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div')))
        e= driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div').click()
        time.sleep(1)
        post_space = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div')
        post_space.click()
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div[1]/span').send_keys(element)
        time.sleep(0.1)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div').click()
        time.sleep(5)
except:
    pass

