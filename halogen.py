

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

from bs4 import BeautifulSoup



class Halogen(Website):

    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        self.wait(self.page_elements['careers']) #ensures page text loads.
        Website.infiniscroll_to_bottom(self.driver)
        next_page_button = self.driver.find_elements(By.CLASS_NAME, self.page_elements['next_page_button'])
        while True:
            try:
                next_page_button[-1].click()
                Website.infiniscroll_to_bottom(self.driver)
                next_page_button = self.driver.find_elements(By.CLASS_NAME, self.page_elements['next_page_button'])
            except:
                break
        links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
        job_reference = [el.get_attribute('href') for el in links]
        row_elements = self.driver.find_elements(By.CLASS_NAME, self.page_elements['listing_page_job_row_class'])
        job_postings = [JobPosting]
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
        dunk = []
        soup = BeautifulSoup(Job_Data.get_data(), 'html.parser')
            
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)
        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data = self.process_outside(job_data, Job_Data.get_data())
        job_data.update({"URL":Job_Data.get_URL()})
        job_data.update({"Clearance":plaintext_job_data[0]})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates
    
    def process_outside_text(self, job_data):
        return job_data
    
    # Defeating engineers with jank HTML data
    def find_pay_band(self, raw_data_array) -> {str,str}:
        for row in raw_data_array:
            if ('$' in row):
                lower = row.lower()
                if (not "bonus" in lower) and (not 'sign-on' in lower):
                    return {"Payband":str([str(amount) for amount in re.findall(r'\$\d+(?:\.\d+)?k\s*-\s*\$\d+(?:\.\d+)?k\b', row)])}
        return {"Payband":""}
    
    def process_outside(self, job_data, html_soup):
        soup = BeautifulSoup(html_soup, 'html.parser')
        data = soup.find("div", class_="awsm-job-specification-item awsm-job-specification-opening-number")
        if data:
            job_data.update({"Job #":data.get_text()})
        data = soup.find("div", class_="awsm-job-specification-item awsm-job-specification-job-location")
        if data:
            job_data.update({"Location":data.get_text()})
        data = soup.find("div", class_="awsm-job-specification-item awsm-job-specification-project")
        if data:
            job_data.update({"Contract":data.get_text()})
        data = soup.find("div", class_="awsm-job-specification-item awsm-job-specification-job-type")
        if data:
            job_data.update({"Schedule":data.get_text()})
        data = soup.find("div", class_="awsm-job-specification-item awsm-job-specification-job-category")
        if data:
            job_data.update({"Job Category":data.get_text()})
        data = soup.find("div", class_="awsm-job-post-title")
        if data:
            job_data.update({"LCAT":data.get_text()})
        return job_data