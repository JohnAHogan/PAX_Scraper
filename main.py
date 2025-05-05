
import time, json, os 
from openpyxl import Workbook 
from parsons import Parsons
from sunayu import Sunayu
from gdit import GDIT
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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



##################################################### Main Method #####################################################

def main():
    driver = webdriver.Firefox()
    workbook = Workbook()
    workbook_name = 'artius.xls'
    folder_prefix=  "website_configs/"
    
    for file in os.listdir(folder_prefix):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            config_path = os.path.join(folder_prefix, filename)
            print("Scraping using file: " + config_path)
            if "sunayu" in filename:
                continue
                website = Sunayu(driver, workbook.create_sheet('sunayu',0), json.load(open(config_path)))
                website.process()
                workbook.save(workbook_name)
            elif "parsons" in filename:
                continue
                website = Parsons(driver, workbook.create_sheet('parsons',0), json.load(open(config_path)))
                website.process()
                workbook.save(workbook_name)
            elif "lockheed" in filename:
                continue 
                lockheed(driver, workbook.create_sheet('lockheed'), json.load(open(config_path)))
            elif "gdit" in filename:
                website = GDIT(driver, workbook.create_sheet('gdit'), json.load(open(config_path)))
                website.process()
            else:
                print(f"Unable to find scraping algorithm for {filename}")
        else:
            print(f"Error decoding file type for file {filename}, issue with json values. Something funny is happening?")
            continue

    driver.quit()
    workbook.save('artius.xls')

if __name__ == '__main__':
    main()
