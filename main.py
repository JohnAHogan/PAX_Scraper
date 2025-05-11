
import os 
from openpyxl import Workbook 
from progress_bar import workbook_name
from selenium import webdriver 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from websitefactory import WebsiteFactory

##################################################### Main Method #####################################################
def main():
    options = webdriver.FirefoxOptions()
    # options.add_argument("-headless")

    #This firefox profile defeats CloudFlare.....usually. Continued testing might lead to issues.
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", True)
    options.profile = firefox_profile
    driver = webdriver.Firefox(options)
    driver.set_page_load_timeout(15)

    workbook = Workbook()
    # workbook_name = f'PAX-{date.today()}.xls'
    folder_prefix=  "website_configs/"
    website_factory = WebsiteFactory()
    for file in os.listdir(folder_prefix):
        website_factory.run_algorithm(driver, workbook, os.path.join(folder_prefix, file))
    driver.quit()
    workbook.save(workbook_name)

if __name__ == '__main__':
    main()
