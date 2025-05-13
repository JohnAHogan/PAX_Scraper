import time
from website import Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Parsons(Website):
    
    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        self.wait(self.page_elements['header'], By.CSS_SELECTOR) #ensure page text loads
        time.sleep(3) #above wait sometimes fails
        Website.infiniscroll_to_bottom(self.driver)
        links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
        job_postings = [el.get_attribute('href') for el in links]
        return set(job_postings)
    

    def process_job_page(self, job_page):
        self.driver.get(job_page)
        self.wait(self.page_elements['header'], By.CSS_SELECTOR) #ensure page text loads
        plaintext_job_data = []
        raw_lines = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['textbox']).get_attribute("innerHTML").splitlines()
        # print(raw_lines)
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)
        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data = self.process_outside_text(job_data)
        job_data.update({"URL":job_page})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates

    def process_outside_text(self, job_data):
        job_row = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['job_description_row']).get_attribute("innerHTML")
        job_row = Website.clean_out_markup(job_row)
        try:
            job_data.update({'Location':job_row[0]})
            job_data.update({'Requisition ID':job_row[1]})
            job_data.update({'Clearance':job_row[3]})
        except:
            #we dont really do anything here. The data is inconsistent on 0.1% of pages for some reason. Legacy?
            print("Error parsing jobs row on Parsons site. ")
        job_title = Website.clean_out_markup(self.driver.find_element(By.CSS_SELECTOR, self.page_elements['header']).get_attribute("innerHTML"))
        # print(job_title)
        job_data.update({'LCAT':job_title[0]})
        return job_data