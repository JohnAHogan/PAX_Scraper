import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class Website:

    def __init__(self, driver, spreadsheet, webconfig_data):
        self.driver = driver
        self.spreadsheet = spreadsheet
        self.webconfig_data = webconfig_data
        self.page_elements = webconfig_data['page_elements']
        for col, field_name in enumerate(Website.correct_columns(webconfig_data['fields'])):
            self.spreadsheet.cell(1, (col+1), field_name)

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
                #if we can't scroll down, we might be at bottom. Try again and return if so. 
                time.sleep(0.2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == old_height:
                    break

##################################################### Data Methods #####################################################

    def get_row_of_delimiter(raw_data, delimiter):
        for index, row in enumerate(raw_data):
                if delimiter in row:
                    return index
        return -1
    
    def get_next_delimiter_row(self, start_row, raw_data):
        for index in range(start_row+1, len(raw_data)):
            if self.contains_delimiter(raw_data[index]):
                return index
        return len(raw_data)
    
    def contains_delimiter(self, string):
        for delimiter in self.webconfig_data["fields"].values():
            if delimiter == "":
                continue
            elif delimiter.replace("<multiline>", "") in string:
                return True
        return False

    def find_data(self, raw_data, delimiter):
        if delimiter == "":
            return ""
        if "<multiline>" in delimiter:
            multirow_data = ""
            delimiter2 = delimiter.replace("<multiline>", "")
            start_delimiter_row = Website.get_row_of_delimiter(raw_data,  delimiter2)
            if start_delimiter_row == -1:
                return ""
            else:
                next_delimiter_row = self.get_next_delimiter_row(start_delimiter_row, raw_data)
                for i in range(start_delimiter_row+1, next_delimiter_row):
                    multirow_data += raw_data[i] + " -"
                return multirow_data
        else:
            for row in raw_data:
                if delimiter in row:
                    return row.replace(delimiter,"")

    def process_data(self, raw_data):
        #Create a dict with empty values 
        sheet_row = dict.fromkeys([key for key in self.webconfig_data["fields"].keys()])
        for field, delimiter in self.webconfig_data["fields"].items():
            sheet_row.update({field: self.find_data(raw_data, delimiter)})
        return sheet_row
    
    #Process some fun things like regex and all that
    def process_special(self, job_data, plaintext_array):
        job_data.update(Website.find_pay_band(plaintext_array))
        return job_data

    # Cleans out HTML markup data. When seperating out the split data, returns in form of array of strings.
    # Also removes 'invisible' chars and others that can be problematic due to UTF limitations. WHEN WILL WE LEARN?
    def clean_out_markup(marked_text):
        list = Website.remove_between(marked_text, '<','>').split('<>') #clears out tags
        while '' in list:
            list.remove('') #remove empty lines
        for index, item in enumerate(list):
            item = item.replace("&nbsp;","") # nonbreaking space
            item = item.replace('u200b',"")
            item = item.replace('●',"") # causes weird issues when viewed in Excel
            list[index] = item 
        return list
    
    # Unfortunately we have to iterate through all the text data and we can't check as we go through. 
    # Job listings have a nasty habit of adding all sorts of ancillary data and dollar amounts and it's just a whole thing. 
    # This function looks weird....and it is.....but it's to defeat HR so hopefully that is forgivable.
    # Here is the regex:
    #     \$: Matches a literal dollar sign.
    #     \s*: Matches zero or more whitespace characters.
    # (\d+(?:,\d{3})*(?:\.\d+)?): This part captures the dollar amount:
    #     \d+: Matches one or more digits.
    #     (?:,\d{3})*: Matches zero or more occurrences of a comma followed by three digits (for thousands separators).
    #     (?:\.\d+)?: Matches an optional decimal point followed by one or more digits.
    # And we want multiple dollar amounts to capture ranges if they happen
    def find_pay_band(raw_data_array) -> {str,str}:
        for row in raw_data_array:
            if ('$' in row) and (',' in row):
                lower = row.lower()
                if (not "bonus" in lower) and (not 'sign-on' in lower):
                    return {"Payband":str(['$'+str(amount) for amount in re.findall(r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)', row)])}
        return {"Payband":""}

##################################################### Spreadsheet Methods #####################################################

    def write_to_sheet(self, row, web_data, plaintext):
        self.spreadsheet
        # When this data comes in it has multiple delimiters for the same thing and needs some trimming
        for col, field_name in enumerate(web_data):
            self.spreadsheet.cell((row), (col+1), web_data[field_name])
            # sheet_tab.write(row, col, field_name)
        self.spreadsheet.cell((row), (len(web_data)+1), str(plaintext))

    #takes a dict and if the key has an int in it combines all similar values in one.
    def correct_columns(duplicative_dict):
        corrected_dict = {}
        for key_val in duplicative_dict:
            key = re.sub(r"\d", "", f"{key_val}") #regex remove all integers from string
            val = duplicative_dict[key_val]
            if(key in corrected_dict):
                val += corrected_dict[key]
            corrected_dict.update({key:val})
        return corrected_dict

