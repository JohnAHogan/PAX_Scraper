import time
from typing import List
from website import Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Leidos(Website):
    
    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        job_set = set()
        job_postings = []
        old_value = 0

        while True:
            self.wait(self.page_elements['careers']) #ensure page text loads
            next_page_button = self.driver.find_elements(By.XPATH, self.page_elements['next_page_button'])
            ActionChains(self.driver).scroll_by_amount(0, 750).perform()
            ActionChains(self.driver).scroll_by_amount(0, 750).perform()
            ActionChains(self.driver).scroll_by_amount(0, 500).perform()
            links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
            job_postings = set([el.get_attribute('href') for el in links])
            for job in job_postings:
                job_set.add(job)
            #This is a bit of a caveman solution, we iterate until we don't find any new jobs to add.
            if(old_value != len(job_set)):
                old_value = len(job_set)
                self.progress_bar.refresh(0, old_value)
            else:
                break
            try:
                next_page_button[-1].click()
            except:
                break
        return job_set
    

    def process_job_page(self, job_page):
        self.driver.get(job_page)
        plaintext_job_data = []
        self.wait(self.page_elements['header_css'], By.CSS_SELECTOR) #ensures page text loads.
        
        raw_lines = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['textbox_css']).get_attribute("innerHTML").splitlines()
        raw_lines += self.driver.find_element(By.CSS_SELECTOR, self.page_elements['job_description_data_css']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)

        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data = self.process_outside_text(job_data)
        job_data.update({"URL":job_page})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates

    def process_outside_text(self, job_data):
        job_title = Website.clean_out_markup(self.driver.find_element(By.CSS_SELECTOR, self.page_elements['header_css']).get_attribute("innerHTML"))
        try:
            job_data.update({'LCAT':job_title[0]})
        except:
            job_data.update({'LCAT':str(job_title)}) #caveman solution
        return job_data