
import os 
from openpyxl import Workbook 
from progress_bar import workbook_name
from selenium import webdriver 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from tkinter import *

from websitefactory import WebsiteFactory

##################################################### Main Method #####################################################

class ScraperGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraper GUI")
        root.geometry("400x300")
        # self.root.
        # Define BooleanVars to hold checkbox values
        self.sunayu_toggle = BooleanVar()
        self.parsons_toggle = BooleanVar()
        self.grayband_toggle = BooleanVar()
        self.gdit_toggle = BooleanVar()
        self.leidos_toggle =BooleanVar()
        self.akina_toggle = BooleanVar()
        self.halogen_toggle = BooleanVar()

        self.sun = "Sunayu"

        # Create Checkboxes
        self.sunayu_button  = Checkbutton(root, text=self.sun, variable=self.sunayu_toggle)
        my_label = Label(text='Check each box to toggle webscraper visit')
        my_label.pack()
        self.parsons_button  = Checkbutton(root, text="Parsons", variable=self.parsons_toggle)
        self.grayband_button  = Checkbutton(root, text="Grayband", variable=self.grayband_toggle)
        self.leidos_button = Checkbutton(root, text="Leidos", variable=self.leidos_toggle)
        self.gdit_button = Checkbutton(root, text="GDIT", variable=self.gdit_toggle)
        self.akina_button  = Checkbutton(root, text="Akina", variable=self.akina_toggle)
        self.halogen_button  = Checkbutton(root, text="Halogeng", variable=self.halogen_toggle)

        #Toggle headless or not
        self.headless_toggle = BooleanVar()
        self.headless_button = Checkbutton(root, text="Run Headless (Recommended)", variable=self.headless_toggle)
        self.headless_button.pack(anchor='nw')
        self.headless_button.select()

        # Place Checkboxes
        self.sunayu_button.pack(anchor='w')
        self.sunayu_button.select()
        self.parsons_button.pack(anchor='w')
        self.parsons_button.select()
        self.grayband_button.pack(anchor='w')
        self.grayband_button.select()
        self.leidos_button.pack(anchor='w')
        self.leidos_button.select()
        self.gdit_button.pack(anchor='w')
        # self.gdit_button.select() # We don't typically care about GDIT 
        self.akina_button.pack(anchor='w')
        self.akina_button.select()
        self.halogen_button.pack(anchor='w')
        self.halogen_button.select()

        # check1 = Checkbutton(frame, text="lijuhabndfvjhb", variable=)

        # Create Run Button
        self.run_button = Button(root, text="Run Scraper", command=self.run_main_loop)
        self.run_button.pack(pady=25)

    def update_button_text(button, new_text):
        # Example main loop logic using checkbox values
        button.config(text=new_text)
        # messagebox.showinfo("Checkbox States", result)

    def run_main_loop(self):
        options = webdriver.FirefoxOptions()
        if self.headless_toggle.get():
            options.add_argument("-headless")
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", True)
        options.profile = firefox_profile
        driver = webdriver.Firefox(options)
        driver.set_page_load_timeout(15)

        workbook = Workbook()
        folder_prefix=  "website_configs/"
        website_factory = WebsiteFactory(self)
        for file in os.listdir(folder_prefix):
            website_factory.run_algorithm(driver, workbook, os.path.join(folder_prefix, file))
        driver.quit()
        workbook.save(workbook_name)
        quit()


if __name__ == "__main__":
    root = Tk()
    app = ScraperGui(root)
    root.mainloop()