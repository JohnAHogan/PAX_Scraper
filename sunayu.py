import Website
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore



class Sunayu(Website.Website):
    
    #process through the website pages, format data, write to sheet
    def process(self):
        job_postings = self.get_job_postings()
        for job_page in job_postings:
            job_data = self.process_job_page(job_page)
            # self.write_to_sheet(self.process_data(plaintext_job_data))
            quit()
        return 0
    
    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        self.wait(self.page_elements['careers']) #ensures page text loads.

        links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
        job_postings = [el.get_attribute('href') for el in links]

        if not any(char.isdigit() for char in job_postings[0]):
            del job_postings[0] # link to root, we don't need this
        return job_postings
    
    def process_job_page(self, job_page):
        self.driver.get(job_page)
        self.wait(self.page_elements['textbox'], By.ID) #ensure page text loads

        raw_lines = self.driver.find_element(By.ID, self.page_elements['textbox']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += self.clean_out_markup(raw_line)