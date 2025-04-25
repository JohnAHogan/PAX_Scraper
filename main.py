
import q, time, xlwt, re, json, scrapy, os # type: ignore
from xlwt import Workbook # type: ignore
import Sunayu
import Website
from scrapy.http import TextResponse# type: ignore
from scrapy.selector import Selector# type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

##################################################### Helper Functions #####################################################

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


# Cleans out HTML markup data. When seperating out the split data, returns in form of array of strings.
# Also removes 'invisible' chars because python does not understand them.
def clean_out_markup(marked_text):
    list = Website.remove_between(marked_text, '<','>').split('<>') #clears out tags
    # print(list)
    while '' in list:
        list.remove('') #remove empty lines
    for index, item in enumerate(list):
        item = item.replace("&nbsp;","") # nonbreaking space
        item = item.replace('u200b',"") 
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

def Sunayu(driver, spreadsheet, webconfig_data):
    crude_job_data = []
    page_elements = webconfig_data['page_elements']
    process_data([], webconfig_data['fields'])
    # quit()
    driver.get(webconfig_data['URL'])
    Website.wait(driver, page_elements['careers']) #ensures page text loads.

    links = driver.find_elements(By.XPATH, page_elements['careers'])
    job_postings = [el.get_attribute('href') for el in links]
    if not any(char.isdigit() for char in job_postings[0]):
        del job_postings[0] # link to root, we don't need this
    for href in job_postings:
        driver.get(href)
        Website.wait(driver, page_elements['textbox'], By.ID)
        raw_lines = driver.find_element(By.ID, page_elements['textbox']).get_attribute("innerHTML").splitlines()
        for raw_line in raw_lines:
            crude_job_data += clean_out_markup(raw_line)
        write_to_sheet(process_data(crude_job_data, webconfig_data['fields']), spreadsheet, webconfig_data['fields'])
        quit()
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

    folder_prefix=  "website_configs/"
    
    for file in os.listdir(folder_prefix):
        filename = os.fsdecode(file)
        website
        if filename.endswith(".json"):
            full_path = os.path.join(folder_prefix, filename)
            print("Scraping using file: " + full_path)
            if "sunayu" in filename:
                # continue
                # sunayu(driver, workbook.add_sheet('sunayu'), json.load(open(full_path)))
                website = Sunayu.Sunayu(driver, workbook.add_sheet('sunayu'), json.load(open(full_path)))
            elif "parsons" in filename:
                continue
                parsons(driver, workbook.add_sheet('parsons'), json.load(open(full_path)))
            elif "lockheed" in filename:
                continue 
                lockheed(driver, workbook.add_sheet('lockheed'), json.load(open(full_path)))
            else:
                print(f"Unable to find scraping algorithm for {filename}")
        else:
            print(f"Error decoding file type for file {filename}, issue with json values. Something funny is happening?")
            continue



    driver.quit()
    workbook.save('artius.xls')

if __name__ == '__main__':
    main()
