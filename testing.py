from datetime import date
from html.parser import HTMLParser
import re
import time
from progress_bar import ProgressBar
from website import Website
import nltk
from bs4 import BeautifulSoup

from tkinter import *
from tkinter import messagebox
# from PySimpleGUI import *

# datas = soup.find_all("div", class_="awsm-job-specification-item awsm-job-specification-opening-number")
# print(data)

# PySimpleGUI.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

class ScraperGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraper GUI")
        root.geometry("300x250")
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
        
        frame = Frame(root)
        frame.pack(padx=20, pady=20)

        # check1 = Checkbutton(frame, text="lijuhabndfvjhb", variable=)

        # Create Run Button
        self.run_button = Button(root, text="Run Scraper", command=self.run_main_loop)
        self.run_button.pack(pady=25)

    def update_button_text(button, new_text):
        # Example main loop logic using checkbox values
        button.config(text=new_text)
        # messagebox.showinfo("Checkbox States", result)

    def run_main_loop(self):
        pass

    def get_button_bools(self):
        return self.sunayu_toggle.get(), self.parsons_toggle.get(), self.grayband_toggle.get(), self.gdit_toggle.get(), self.leidos_toggle.get, self.akina_toggle.get(), self.halogen_toggle.get()

if __name__ == "__main__":
    root = Tk()
    # root.
    app = ScraperGui(root)
    root.mainloop()
