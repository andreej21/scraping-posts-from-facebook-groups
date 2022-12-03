from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy
from numpy import random
import time

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

driver.get('https://www.facebook.com/')
time.sleep(1)
username = 'tefavo1297@cnogs.com'
password = 'abc123456789'
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

                    image = post.find_element(By.TAG_NAME,'img').get_attribute("alt")
                    img_text =''
                    num = 0
                    for i in image:
                        if i == '\'' and num ==0:
                            num+=1
                        elif i == '\'' and num ==1:
                            break
                        else:
                            img_text +=i
                        
                    if img_text !='':
                            text_contents.append(img_text)
                except:
                    pass


        text_data = pd.DataFrame({'Content':text_contents})
        text_data.to_excel('Fb.xlsx',index=False)
    
except:
    driver.quit()