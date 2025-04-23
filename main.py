
import q
import time
import xlwt
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

def wait(driver, xpath, duration=10):
    element = WebDriverWait(driver, duration).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )

    return element

def wait_and_click(driver, xpath, duration=10):
    element = wait(driver, xpath, duration)
    element.click()

def load_fields(json_fields):
    fields = []
    for key, value in json_fields.items():
        if value != "":
            fields.append(value)
    return fields

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
    links = driver.find_elements_by_xpath(xpath['hrefs'])
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
    links = driver.find_elements_by_xpath(xpath['hrefs'])
    print(links)
    hrefs = [el.get_attribute('href') for el in links]
    print(hrefs)
    return 0


##################################################### Main Method #####################################################

def main():

    with open('website_configs/lockheed.json') as file:
        webconfig_data = json.load(file)

    all_responses = []

    driver = webdriver.Firefox()
    workbook = Workbook()
    
    sheet = wb.add_sheet('Sunayu_Raw')
    with open('website_configs/sunayu.json') as file:
        webconfig_data = json.load(file)
    sunayu(driver, sheet, webconfig_data)
    
    for file in os.listdir("website_configs/"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print("Scraping using file: " + os.path.join("website_configs/", filename))
            if "lockheed" in filename:
                continue # lockheed(driver, workbook.add_sheet('lockheed'), json.load(file))
            elif "sunayu" in filename:
                sunayu(driver, workbook.add_sheet('sunayu'), json.load(file))
            else:
                print(f"Unable to find scraping algorithm for {filename}")
        else:
            print("Error decoding file type, issue with json values. Something funny is happening?")
            continue



    driver.quit()
    wb.save('artius.csv')

if __name__ == '__main__':
    main()
