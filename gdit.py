import time
from progress_bar import ProgressBar
from website import Website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class GDIT(Website):
    
    #Iterates through all the website pages
    def get_job_postings(self):
        self.driver.get(self.webconfig_data['URL'])
        job_set = set()
        job_postings = []
        old_value = 0

        while True:
            self.wait(self.page_elements['careers']) #ensure page text loads
            Website.infiniscroll_to_bottom(self.driver)
            next_page_button = self.driver.find_elements(By.XPATH, self.page_elements['next_page_button'])[-1]
            links = self.driver.find_elements(By.XPATH, self.page_elements['careers'])
            job_postings = [el.get_attribute('href') for el in links]
            for job in job_postings:
                job_set.add(job)
            #This is a bit of a caveman solution, we iterate until we don't find any new jobs to add.
            if(old_value != len(job_set)):
                old_value = len(job_set)
                self.progress_bar.refresh(0, old_value)
            else:
                break
            next_page_button.click()
        return job_set
    

    def process_job_page(self, job_page):
        try:
            self.driver.get(job_page)
        except Exception as TE:
            self.wiggle() #this speeds things up sometimes. Jank AF.
        plaintext_job_data = []
        raw_lines = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['textbox_css']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            plaintext_job_data += Website.clean_out_markup(raw_line)
        job_data = self.process_data(plaintext_job_data)
        job_data = self.process_special(job_data, plaintext_job_data)
        job_data = self.process_outside_text(job_data)
        job_data.update({"URL":job_page})
        return Website.correct_columns(job_data), plaintext_job_data # remove key duplicates

    def process_outside_text(self, job_data):
        job_row = self.driver.find_element(By.CSS_SELECTOR, self.page_elements['job_description_row_css']).get_attribute("innerHTML")
        job_row = Website.clean_out_markup(job_row)
        try:
            job_data.update({'Clearance':job_row[1]})
            job_data.update({'Location':job_row[5]})
            job_data.update({'Category':job_row[4]})
        except:
            True #this shouldnt fail but I hate dumb NPEs
        job_title = Website.clean_out_markup(self.driver.find_element(By.CSS_SELECTOR, self.page_elements['header_css']).get_attribute("innerHTML"))
        try:
            job_data.update({'LCAT':job_title[0]})
        except:
            job_data.update({'LCAT':str(job_title)}) #caveman solution
        return job_data
    
    # Look. I've tried. I've tried to make this work without this dumb function. 
    # But sometimes we just get stuck and this is the ONLY thing I can think of that speeds things up.
    # I think because certain elements on the GDIT page load when you scroll it gets confused
    def wiggle(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        self.driver.execute_script("window.scrollTo(0, 0);")