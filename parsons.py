import time
import website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Parsons(website.Website):

    # Lots of room for improvement here. Ideas from worst to best:
    # 1: Can enhance speed some
    # 2: Pulls all jobs globally. Not ideal. filter DMV only somehow.
    # 3: Job data comes out super weird. 
    def parsons(driver, spreadsheet, webconfig_data):
        driver.get(webconfig_data['URL'])
        time.sleep(3) # can't figure out how to load page properly, caveman wait only
        website.infiniscroll_to_bottom(driver)
        xpath = webconfig_data['page_elements']
        links = driver.find_elements(By.XPATH, xpath['careers'])
        job_postings = [el.get_attribute('href') for el in links]