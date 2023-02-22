import time
import emoji
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from scrapper.mongodb_config import MongoDBConfig
from scrapper.utils import process_date

class WebDriver:
    def __init__(self, driver_path: str):
        self.PATH = driver_path
        self.driver = webdriver.Edge(executable_path=self.PATH)
        self.ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.some_timeout = 10
        self.mongodb_conn = MongoDBConfig('config.yaml')

    def open_review_page(self, sort_by: int = 1):
        clickable = self.driver.find_element(By.CLASS_NAME, 'F7nice')
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(1)

        clickable = WebDriverWait(self.driver, self.some_timeout, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')))
        clickable = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(1)

        clickable = WebDriverWait(self.driver, self.some_timeout, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, f'//*[@id="action-menu"]/div[{sort_by}]')))
        clickable = self.driver.find_element(By.XPATH, f'//*[@id="action-menu"]/div[{sort_by}]')
        ActionChains(self.driver).click(clickable).perform()
        time.sleep(1)

    def scroll_page(self, loop: int = 1):
        for _ in range(loop):
            expand_review = self.driver.find_elements(By.CLASS_NAME, "w8nwRe")

            for i in expand_review:
                i.click()

            review_windows = self.driver.find_element(By.CLASS_NAME, 'lXJj5c')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_windows)
            time.sleep(1)
    
    def get_review_data(self, location:str):
        review_text = WebDriverWait(self.driver, self.some_timeout, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'wiI7pd')))
        time.sleep(1)
        review_text = self.driver.find_elements(By.CLASS_NAME, 'wiI7pd')

        review_rate = WebDriverWait(self.driver, self.some_timeout, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'kvMYJc')))
        time.sleep(1)
        review_rate = self.driver.find_elements(By.CLASS_NAME, 'kvMYJc')

        review_date = WebDriverWait(self.driver, self.some_timeout, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'rsqaWe')))
        time.sleep(1)
        review_date = self.driver.find_elements(By.CLASS_NAME, 'rsqaWe')

        for x in tqdm(range(len(review_date))):
            emoji.demojize(review_text[x].text)
            emoji.demojize(review_date[x].text)

            text = review_text[x].text
            datetime = review_date[x].text
            rate = review_rate[x].get_attribute('aria-label')

            if len(text) < 10:
                continue

            text = text.encode('utf-8').decode('utf-8')
            datetime = datetime.encode('utf-8').decode('utf-8')
            datetime = process_date(datetime)

            datas = {
                'location': location,
                'text': text,
                'rating': int(rate.split()[0]),
                'datetime': datetime
            }

            self.mongodb_conn.insert_one(datas)
    
    def scrape(self, location, location_url, loop_optimizer):

        self.driver.get(location_url)
        self.open_review_page()
        self.scroll_page(loop=loop_optimizer)
        self.get_review_data(location=location)
        
        self.driver.quit()

        # sort_by = 1

        # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        # some_timeout = 10

        # clickable = self.driver.find_element(By.CLASS_NAME, 'F7nice')
        # ActionChains(self.driver).click(clickable).perform()
        # time.sleep(1)

        # clickable = WebDriverWait(self.driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        #     .until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')))
        # clickable = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button')
        # ActionChains(self.driver).click(clickable).perform()
        # time.sleep(1)

        # clickable = WebDriverWait(self.driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        #     .until(expected_conditions.presence_of_element_located((By.XPATH, f'//*[@id="action-menu"]/div[{sort_by}]')))
        # clickable = self.driver.find_element(By.XPATH, f'//*[@id="action-menu"]/div[{sort_by}]')
        # ActionChains(self.driver).click(clickable).perform()
        # time.sleep(1)

        # loop = 9
        # for _ in range(loop):
        #     lihat = self.driver.find_elements(By.CLASS_NAME, "w8nwRe")
        #     for i in lihat:
        #         i.click()
        #     review_windows = self.driver.find_element(By.CLASS_NAME, 'lXJj5c')
        #     self.driver.execute_script("arguments[0].scrollIntoView(true);", review_windows)
        #     time.sleep(1)
        
        # element = WebDriverWait(self.driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        #     .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'wiI7pd')))
        # time.sleep(1)
        # element = self.driver.find_elements(By.CLASS_NAME, 'wiI7pd')

        # rate = WebDriverWait(self.driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        #     .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'kvMYJc')))
        # time.sleep(1)
        # rate = self.driver.find_elements(By.CLASS_NAME, 'kvMYJc')

        # waktu = WebDriverWait(self.driver, some_timeout, ignored_exceptions=ignored_exceptions)\
        #     .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'rsqaWe')))
        # time.sleep(1)
        # waktu = self.driver.find_elements(By.CLASS_NAME, 'rsqaWe')

        # for x in tqdm(range(len(waktu))):
        #     emoji.demojize(element[x].text)
        #     emoji.demojize(waktu[x].text)

        #     text = element[x].text
        #     kapan = waktu[x].text
        #     rate_review = rate[x].get_attribute('aria-label')

        #     text = text.encode('utf-8').decode('utf-8')
        #     kapan = kapan.encode('utf-8').decode('utf-8')

        #     datetime = process_date(kapan)

        #     datas = {
        #         'location': location,
        #         'text': text,
        #         'rating': int(rate_review.split()[0]),
        #         'datetime': datetime
        #     }

        #     if len(text) < 10:
        #         continue

        #     self.mongodb_conn.insert_one(datas)
        
        # self.driver.quit()