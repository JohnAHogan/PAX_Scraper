from selenium.webdriver.support.ui import WebDriverWait # type: ignore
import re

class Website:

    def __init__(self, driver, spreadsheet, webconfig_data):
        self.driver = driver
        self.spreadsheet = spreadsheet
        self.webconfig_data = webconfig_data

##################################################### Selenium Helper Methods #####################################################

    def wait(self, identifier, mode=By.XPATH, duration=10):
        element = WebDriverWait(self.driver, duration).until(
            EC.visibility_of_element_located((mode, identifier))
        )
        return element

    def wait_and_click(self, identifier,mode=By.XPATH, duration=10):
        element = self.wait(identifier, mode, duration)
        element.click()

    def load_fields(json_fields):
        fields = []
        for key, value in json_fields.items():
            if value != "":
                fields.append(value)
        return fields

    def remove_between(text, start_delimiter, end_delimiter):
        pattern = re.escape(start_delimiter) + ".*?" + re.escape(end_delimiter)
        return re.sub(pattern, start_delimiter+end_delimiter, text)

    # A bit of a caveman solution but it defeats the parsons website which infiniscrolls.
    # Scroll to bottom of the page, if inifiniscroll is too deep we give up.
    def infiniscroll_to_bottom(driver):
        for i in range(20):
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == old_height:
                break

##################################################### Data Methods #####################################################

def process_multiline(raw_data, delimiter):
    return "Multiline function TBD"

def find_data_array(raw_data, delimiter):
    if "multiline" in delimiter:
        delimiter = delimiter.replace("<multiline>", "")
        return process_multiline(raw_data,  delimiter)
    else:
        for row in raw_data:
            if delimiter in row:
                return row.replace(delimiter,"")

def process_data(raw_data, website_fields):
    findable_fields = dict.fromkeys([key for key,val in website_fields.items() if val != ''])
    for field in findable_fields:
        delimiter = website_fields[field]
        print(f"{field}: {Website.find_data(raw_data, delimiter)}")
    return ""