
import q
import time
import xlwt
import re
from xlwt import Workbook
import json
import scrapy
import os
from scrapy.http import TextResponse
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##################################################### Helper Functions #####################################################

def wait(driver, identifier, mode=By.XPATH, duration=10):
    element = WebDriverWait(driver, duration).until(
        EC.visibility_of_element_located((mode, identifier))
    )
    return element

def wait_and_click(driver, identifier,mode=By.XPATH, duration=10):
    element = wait(driver, identifier, mode, duration)
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

def write_to_sheet(response_data, sheet_tab, fields):
    for col, field_name in enumerate(fields):
        # worksheet.write(0, col, field_name)
        sheet_tab.write(0, col, field_name)
    for row, response in enumerate(fields, start=1):
        for col, field in enumerate(fields):
            xpath = special_xpath.get(field, standard_xpath(field))
            selector = response.xpath(xpath)
            if field in big_fields:
                content = '\n'.join(selector.extract())
            else:
                content = selector.extract_first()

            sheet_tab.write(row, col, content)

def get_text_excluding_children(driver, element):
    return driver.execute_script("""
        var parent = arguments[0];
        var child = parent.firstChild;
        var ret = "";
        while(child) {
            if (child.nodeType === Node.TEXT_NODE)
                ret += child.textContent;
            child = child.nextSibling;
        }
        return ret;
        """, element)

def clean_out_markup(marked_text):
    list = remove_between(marked_text, '<','>').split('<>') #clears out tags
    # print(list)
    while '' in list:
        list.remove('') #remove empty lines
    for index, item in enumerate(list):
        #I can't oneline this and it's killing me. A better python dev might be able to save it.
        item = item.replace("&nbsp;","") # remove nonbreaking space characters
        list[index] = item 
    return list

##################################################### Page Specific functions #####################################################

#Currently unable to test this due to not having a login to Taleo. 
def lockheed(driver, spreadsheet, webconfig_data):
    all_responses = []
    xpath = webconfig_data['page_elements']
    by_previous_text = lambda t:  '//td[contains(text(), "' + t + '")]/following::b/text()' # This isn't used I think?
    standard_xpath = lambda t: '//td[contains(text(),"' + t + '")]/following-sibling::td//text()'
    
    driver.get(webconfig_data['URL'])
    dropdown = WebDriverWait(driver, 90).until(
        EC.visibility_of_element_located((By.XPATH, xpath['dropdown']))
    )
    action = ActionChains(driver)
    action.move_to_element(dropdown).perform()

    time.sleep(3)
    links = driver.find_elements(By.XPATH, xpath['hrefs'])
    hrefs = [el.get_attribute('href') for el in links]

    for href in hrefs:
        driver.get(href)
        wait(driver, xpath['detail_loaded'])
        html = driver.execute_script("return document.documentElement.outerHTML;")
        res = Selector(text=html)
        all_responses.append(res)

    write_to_sheet(spreadsheet, all_responses)

def sunayu(driver, spreadsheet, webconfig_data):
    all_responses = []
    xpath = webconfig_data['page_elements']
    driver.get(webconfig_data['URL'])
    wait(driver, xpath['careers']) #ensures page text loads.

    links = driver.find_elements(By.XPATH, xpath['careers'])
    job_postings = [el.get_attribute('href') for el in links]
    results = []
    if not any(char.isdigit() for char in job_postings[0]):
        del job_postings[0] # link to root, we don't need this
    for href in job_postings:
        driver.get(href)
        wait(driver, "descriptionWrapper", By.ID)
        raw_lines = driver.find_element(By.ID, "descriptionWrapper").get_attribute("innerHTML")
        # print(raw_lines)
        for raw_line in raw_lines:
            results += clean_out_markup(raw_line)
        # print(results)
        # quit()
    return 0

# Lots of room for improvement here. Ideas from worst to best:
# 1: Can enhance speed some
# 2: Pulls all jobs globally. Not ideal. filter DMV only somehow.
# 3: Job data comes out super weird. 
def parsons(driver, spreadsheet, webconfig_data):
    driver.get(webconfig_data['URL'])
    time.sleep(3) # can't figure out how to load page properly, caveman wait only
    infiniscroll_to_bottom(driver)
    xpath = webconfig_data['page_elements']
    links = driver.find_elements(By.XPATH, xpath['careers'])
    job_postings = [el.get_attribute('href') for el in links]

##################################################### Main Method #####################################################

def main():

    with open('website_configs/lockheed.json') as file:
        webconfig_data = json.load(file)

    all_responses = []

    driver = webdriver.Firefox()
    workbook = Workbook()
    
    for file in os.listdir("website_configs/"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print("Scraping using file: " + os.path.join("website_configs/", filename))
            if "sunayu" in filename:
                sunayu(driver, workbook.add_sheet('sunayu'), json.load(open("website_configs/sunayu.json")))
            elif "parsons" in filename:
                # continue
                parsons(driver, workbook.add_sheet('parsons'), json.load(open("website_configs/parsons.json")))
            elif "lockheed" in filename:
                continue 
                lockheed(driver, workbook.add_sheet('lockheed'), json.load(open("website_configs/parsons.json")))
            else:
                print(f"Unable to find scraping algorithm for {filename}")
        else:
            print("Error decoding file type, issue with json values. Something funny is happening?")
            continue



    driver.quit()
    workbook.save('artius.xls')

if __name__ == '__main__':
    main()
