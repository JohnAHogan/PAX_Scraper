
import time, json, os 
from datetime import date
from openpyxl import Workbook 
from grayband import Grayband
from leidos import Leidos
from parsons import Parsons
from sunayu import Sunayu
from progress_bar import workbook_name
from gdit import GDIT
from selenium import webdriver 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

##################################################### Main Method #####################################################
def main():
    options = webdriver.FirefoxOptions()
    # options.add_argument("-headless")

    #This firefox profile defeats CloudFlare.....usually. Continued testing might lead to issues.
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", False)
    options.profile = firefox_profile
    driver = webdriver.Firefox(options)
    driver.set_page_load_timeout(15)

    workbook = Workbook()
    # workbook_name = f'PAX-{date.today()}.xls'
    folder_prefix=  "website_configs/"
    
    for file in os.listdir(folder_prefix):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            config_path = os.path.join(folder_prefix, filename)
            print("Scraping using file: " + config_path)
            #todo: Turn this shit into a factory class
            if "sunayu" in filename:
                # continue
                website = Sunayu(driver, workbook, 'Sunayu', json.load(open(config_path)))
                website.run()
                workbook.save(workbook_name)
            elif "parsons" in filename:
                # continue
                website = Parsons(driver, workbook, "Parsons", json.load(open(config_path)))
                website.run()
                workbook.save(workbook_name)
            elif "grayband" in filename:
                # continue 
                website = Grayband(driver, workbook, 'Grayband', json.load(open(config_path)))
                website.run()
                workbook.save(workbook_name)
            elif "gdit" in filename:
                # continue
                website = GDIT(driver, workbook, 'GDIT', json.load(open(config_path)))
                website.run()
                workbook.save(workbook_name)
            elif "leidos" in filename:
                # continue
                website = Leidos(driver, workbook, 'Leidos', json.load(open(config_path)))
                website.run()
                workbook.save(workbook_name)
            elif "akina" in filename:
                # continue
                website = Akina(driver, workbook, 'Akina', json.load(open(config_path)))
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
