
import time, json, os 
from datetime import date
from openpyxl import Workbook 
from grayband import Grayband
from parsons import Parsons
from sunayu import Sunayu
from gdit import GDIT
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##################################################### Main Method #####################################################

def main():
    driver = webdriver.Firefox()
    workbook = Workbook()
    workbook_name = f'PAX-{date.today()}.xls'
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
            elif "grayband" in filename:
                # continue 
                website = Grayband(driver, workbook.create_sheet('grayband',0), json.load(open(config_path)))
                website.process()
                workbook.save(workbook_name)
            elif "gdit" in filename:
                continue
                website = GDIT(driver, workbook.create_sheet('gdit',0), json.load(open(config_path)))
                website.process()
                workbook.save(workbook_name)
            else:
                print(f"Unable to find scraping algorithm for {filename}")
        else:
            print(f"Error decoding file type for file {filename}, issue with json values. Something funny is happening?")
            continue

    driver.quit()
    workbook.save(workbook_name)

if __name__ == '__main__':
    main()
