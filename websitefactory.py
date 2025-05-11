


import json
import os

from akina import Akina
from gdit import GDIT
from grayband import Grayband
from leidos import Leidos
from parsons import Parsons
from sunayu import Sunayu

from selenium import webdriver 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from progress_bar import workbook_name

class WebsiteFactory:

    sunayu_toggle = False
    parsons_toggle = False
    grayband_toggle = False
    gdit_toggle = False
    leidos_toggle = False
    akina_toggle = True
    _toggle = False

    def run_algorithm(self, driver, workbook, config_path):
        filename = os.fsdecode(config_path)
        if filename.endswith(".json"):
            if "sunayu" in filename and self.sunayu_toggle:
                Sunayu(driver, workbook, 'Sunayu', json.load(open(config_path))).run()
            elif "parsons" in filename and self.parsons_toggle:
                Parsons(driver, workbook, "Parsons", json.load(open(config_path))).run()
            elif "grayband" in filename and self.grayband_toggle:
                Grayband(driver, workbook, 'Grayband', json.load(open(config_path))).run()
            elif "gdit" in filename and self.gdit_toggle:
                GDIT(driver, workbook, 'GDIT', json.load(open(config_path))).run()
            elif ("leidos" in filename) and self.leidos_toggle:
                #todo: figure out how to elegantly add more drivers to this factory
                options = webdriver.FirefoxOptions()
                options.add_argument("-headless")
                #This firefox profile defeats CloudFlare.....usually. Continued testing might lead to issues.
                firefox_profile = FirefoxProfile()
                firefox_profile.set_preference("javascript.enabled", False)
                options.profile = firefox_profile
                driver2 = webdriver.Firefox(options)
                Leidos(driver2, workbook, 'Leidos', json.load(open(config_path))).run()
                driver2.quit()
            elif "akina" in filename and self.akina_toggle:
                Akina(driver, workbook, 'Akina', json.load(open(config_path))).run()
                
            else:
                print(f"Choosing not to run algorithm related to config file {filename}")
        else:
            print(f"Error decoding file type for file {filename}, issue with json values. Something funny is happening?")
        workbook.save(workbook_name)