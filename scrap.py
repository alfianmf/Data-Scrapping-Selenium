from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd
from cleantext import clean
import time
import emoji

driver = webdriver.Edge(executable_path="msedgedriver.exe")
link_gmaps = "https://goo.gl/maps/UoRzBKDT6WJ1cVjbA"
driver.get(link_gmaps)

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
some_timeout = 10

clickable = driver.find_element(By.CLASS_NAME, 'F7nice')
ActionChains(driver).click(clickable).perform()
time.sleep(1)

hasil = {
    'Review Time': [],
    'Review Text' : []
    }
count = 0
for i in range(1,5 ):
    clickable = WebDriverWait(driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')))
    clickable = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')
    ActionChains(driver).click(clickable).perform()
    time.sleep(1)

    clickable = WebDriverWait(driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        .until(expected_conditions.presence_of_element_located((By.XPATH, f'//*[@id="action-menu"]/div[{i}]')))
    clickable = driver.find_element(By.XPATH, f'//*[@id="action-menu"]/div[{i}]')
    ActionChains(driver).click(clickable).perform()

    time.sleep(1)

    loop = 130  # 50, 100

    for _ in range(loop):
        lihat=driver.find_elements(By.CLASS_NAME,"w8nwRe")
        for i in lihat:
            i.click()
        review_windows = driver.find_element(By.CLASS_NAME, 'lXJj5c')
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", review_windows)
        time.sleep(1)
        print(_)

    temp = []
    
    element = WebDriverWait(driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'wiI7pd')))
    time.sleep(1)
    element = driver.find_elements(By.CLASS_NAME, 'wiI7pd')

    waktu = WebDriverWait(driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'rsqaWe')))
    time.sleep(1)
    # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[1]/div/div[3]/div[4]/div[1]/span[3]
    waktu = driver.find_elements(By.CLASS_NAME, 'rsqaWe')
    print('ket waktu',len(waktu))
    print('teks',len(element))
    for x in range(len(waktu)):
        emoji.demojize(element[x].text)
        text = element[x].text
        text = text.encode("utf-8")

        emoji.demojize(waktu[x].text)
        kapan = waktu[x].text
        kapan = kapan.encode("utf-8")
        if text in temp:
            print("UDAH PERNAH DI PRINT")
            continue
        elif len(text) < 10:
            print("KEPENDEKAN REVIEWNYA")
            continue
        temp.append(text)
        hasil['Review Time'].append(kapan)
        hasil['Review Text'].append(text)
        count += 1
hasil=pd.DataFrame(hasil)
hasil=hasil.drop_duplicates()
hasil.to_csv("coba.csv")

print("Berhasil traverse review:", count)
