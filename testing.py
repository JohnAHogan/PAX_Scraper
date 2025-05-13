from datetime import date
from html.parser import HTMLParser
import re
import time
from progress_bar import ProgressBar
from website import Website
import nltk
from bs4 import BeautifulSoup


innerHTML = """<div class="awsm-list-left-col"><h2 class="awsm-job-post-title"><a href="https://halogeneng.com/jobs/front-end-full-stack-engineer/">Front End/Full Stack Engineer</a></h2></div><div class="awsm-list-right-col"><div class="awsm-job-specification-wrapper"><div class="awsm-job-specification-item awsm-job-specification-job-category"><span class="awsm-job-specification-term">Software Engineering</span> </div><div class="awsm-job-specification-item awsm-job-specification-job-type"><span class="awsm-job-specification-term">Full Time</span> <span class="awsm-job-specification-term">Hybrid</span> </div><div class="awsm-job-specification-item awsm-job-specification-job-location"><span class="awsm-job-specification-term">NBP131</span> </div><div class="awsm-job-specification-item awsm-job-specification-opening-number"><span class="awsm-job-specification-term">7065</span> </div><div class="awsm-job-specification-item awsm-job-specification-project"><span class="awsm-job-specification-term">BT</span> </div></div><div class="awsm-job-more-container"><a class="awsm-job-more" href="https://halogeneng.com/jobs/front-end-full-stack-engineer/">More Details <span></span></a></div>"""
# innterHTML = 
soup = BeautifulSoup(innerHTML, 'html.parser')
print(soup.prettify())

# datas = soup.find_all("div", class_="awsm-job-specification-item awsm-job-specification-opening-number")
# print(data)
