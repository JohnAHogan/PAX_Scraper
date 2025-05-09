from website import Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC



class Sunayu(Website):

    # #process through the website pages, format data, write to sheet
    # def process(self):
    #     job_postings = self.get_job_postings()
    #     for index, job_page in enumerate(job_postings):
    #         try:
    #             job_data, plaintext_data = self.process_job_page(job_page)
    #             self.write_to_sheet(index+2, job_data, plaintext_data)
    #         except:
    #             print(f"Fail on webpage, might be worth looking into.    {job_page}")
    #             continue
    #     return 0
    
    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        self.wait(self.page_elements['careers']) #ensures page text loads.

        links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
        job_postings = [el.get_attribute('href') for el in links]

        if not any(char.isdigit() for char in job_postings[0]):
            del job_postings[0] # link to root, we don't need this
        return set(job_postings)
    

    def process_job_page(self, job_page):
        self.driver.get(job_page)
        self.wait(self.page_elements['textbox'], By.ID) #ensure page text loads
        plaintext_job_data = []
        raw_lines = self.driver.find_element(By.ID, self.page_elements['textbox']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)
        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data.update({"URL":job_page})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates
    
    def process_outside_text(self, job_data):
        #We dont need to do any of this because all relevant data is in the text box
        return job_data