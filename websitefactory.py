


import json
import os

from akina import Akina
from gdit import GDIT
from grayband import Grayband
from halogen import Halogen
from leidos import Leidos
from parsons import Parsons
from sunayu import Sunayu

from selenium import webdriver 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from progress_bar import workbook_name

class WebsiteFactory:

    def __init__(self, tk):
        self.tk = tk


    # sunayu_toggle = False
    # parsons_toggle = False
    # grayband_toggle = False
    # gdit_toggle = False
    # leidos_toggle = False
    # akina_toggle = False
    # halogen_toggle = False

    def run_algorithm(self, driver, workbook, config_path):
        filename = os.fsdecode(config_path)
        if filename.endswith(".json"):
            if "sunayu" in filename and self.tk.sunayu_toggle.get():
                Sunayu(driver, workbook, 'Sunayu', json.load(open(config_path))).run()
            elif "parsons" in filename and self.tk.parsons_toggle.get():
                Parsons(driver, workbook, "Parsons", json.load(open(config_path))).run()
            elif "grayband" in filename and self.tk.grayband_toggle.get():
                Grayband(driver, workbook, 'Grayband', json.load(open(config_path))).run()
            elif "gdit" in filename and self.tk.gdit_toggle.get():
                GDIT(driver, workbook, 'GDIT', json.load(open(config_path))).run()
            elif ("leidos" in filename) and self.tk.leidos_toggle.get():
                #todo: figure out how to elegantly add more drivers to this factory
                options = webdriver.FirefoxOptions()
                if self.tk.headless_toggle.get():
                    options.add_argument("-headless")
                #This firefox profile defeats CloudFlare.....usually. Continued testing might lead to issues.
                firefox_profile = FirefoxProfile()
                firefox_profile.set_preference("javascript.enabled", False)
                options.profile = firefox_profile
                driver2 = webdriver.Firefox(options)
                Leidos(driver2, workbook, 'Leidos', json.load(open(config_path))).run()
                driver2.quit()
            elif "akina" in filename and self.tk.akina_toggle.get():
                Akina(driver, workbook, 'Akina', json.load(open(config_path))).run()
            elif "halogen" in filename and self.tk.halogen_toggle.get():
                Halogen(driver, workbook, "Halogen", json.load(open(config_path))).run()
            elif "lockheed" in filename:
                pass
            else:
                print(f"Choosing not to run algorithm related to config file {filename}")
        else:
            print(f"Error decoding file type for file {filename}, issue with json values. Something funny is happening?")
        workbook.save(workbook_name)
