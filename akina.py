

import re
import sys
import time
import traceback
from job_posting import JobPosting
from website import Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from progress_bar import workbook_name



class Akina(Website):

    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        self.wait(self.page_elements['careers']) #ensures page text loads.
        links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
        job_reference = [el.get_attribute('href') for el in links]
        row_elements = self.driver.find_elements(By.CSS_SELECTOR, self.page_elements['listing_page_job_row_css'])
        job_postings = []
        for ref, elem in zip(job_reference, row_elements):
            job_postings.append(JobPosting(ref, elem))
        return set(job_postings)
    

    def process_job_page(self, Job_Data):
        try:
            self.driver.get(Job_Data.get_URL())
        except:
            return {}, []
        self.wait(self.page_elements['textbox_css'], By.CSS_SELECTOR) #ensure page text loads
        plaintext_job_data = []
        raw_lines = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['textbox_css']).get_attribute("innerHTML").splitlines()
        raw_lines += Job_Data.get_data().splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)
        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data.update({"URL":Job_Data.get_URL()})
        job_data.update({"Clearance":plaintext_job_data[0]})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates
    
    def process_outside_text(self, job_data):
        return job_data