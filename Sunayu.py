import main;
import Website
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore



class Sunayu(Website):


    def process(self):
        plaintext_job_data = []
        page_elements = self.webconfig_data['page_elements']

        job_postings = self.get_job_postings(page_elements)
        
        for job_page in job_postings:
            job_data = self.process_job_page(job_page, page_elements)
            main.write_to_sheet(self.process_data(plaintext_job_data))
            quit()
        return 0
    
    def get_job_postings(self, page_elements):
        self.driver.get(self.webconfig_data['URL'])
        main.wait(self.driver, page_elements['careers']) #ensures page text loads.

        links = self.driver.find_elements(By.XPATH, page_elements['careers'])
        job_postings = [el.get_attribute('href') for el in links]

        if not any(char.isdigit() for char in job_postings[0]):
            del job_postings[0] # link to root, we don't need this
        return job_postings
    
    def process_job_page(self, job_page, page_elements):
        self.driver.get(job_page)
        self.wait(self.driver, page_elements['textbox'], By.ID) #ensure page text loads
        raw_lines = self.driver.find_element(By.ID, page_elements['textbox']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += main.clean_out_markup(raw_line)