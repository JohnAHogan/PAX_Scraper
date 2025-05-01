import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


class Website:

    def __init__(self, driver, spreadsheet, webconfig_data):
        self.driver = driver
        self.spreadsheet = spreadsheet
        self.webconfig_data = webconfig_data
        self.page_elements = webconfig_data['page_elements']

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
                print(f"cannot figure out delim {delimiter2}")
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

    # Cleans out HTML markup data. When seperating out the split data, returns in form of array of strings.
    # Also removes 'invisible' chars because python does not understand them.
    def clean_out_markup(marked_text):
        list = Website.remove_between(marked_text, '<','>').split('<>') #clears out tags
        while '' in list:
            list.remove('') #remove empty lines
        for index, item in enumerate(list):
            item = item.replace("&nbsp;","") # nonbreaking space
            item = item.replace('u200b',"") 
            list[index] = item 
        return list

##################################################### Spreadsheet Methods #####################################################

    def write_to_sheet(self, row, duplicative_data):
        # return ""
        self.spreadsheet
        correction = 0
        # When this data comes in it has multiple delimiters for the same thing and needs some trimming
        corrected_columns = Website.correct_columns(duplicative_data)
        for col, field_name in enumerate(duplicative_data):
            self.spreadsheet.cell(row, col, field_name)
            # sheet_tab.write(row, col, field_name)

    #takes a dict and if the key has an int in it combines all similar values in one.
    def correct_columns(duplicative_dict):
        corrected_dict = {}
        for key_val in duplicative_dict:
            key = re.sub(r"\d", "", f"{key_val}") #regex remove all integers from string
            print(key)
            val = duplicative_dict[key_val]
            if(key in corrected_dict):
                val += corrected_dict[key]
            corrected_dict.update({key,val})
        print(corrected_dict)
        return corrected_dict

