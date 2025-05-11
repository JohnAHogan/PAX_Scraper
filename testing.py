from datetime import date
import re
import time
from progress_bar import ProgressBar
from website import Website

# Print iterations progress
progressBar = ProgressBar()

# A List of Items
items = list(range(0, 5))
l = len(items)

progressBar.refresh(0,57, prefix = 'GDIT Progress:', suffix = 'Collecting Job Postings')
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    progressBar.refresh(i, l, prefix = 'GDIT Progress:', suffix = 'Collecting Job Postings')
print()

innerHtml = """
    <div class="cats-job-title cats-job-column">
      <a target="_blank" href="https://akina.catsone.com/careers/99975-General/jobs/16656406-Software-Integration-Engineer-SIE--4-Linux-CLI-Linux-tools-Bash-scripting-Python/"><!---->Software Integration Engineer (SIE) - 4 (Linux CLI, Linux tools, Bash scripting, Python)<!----></a>
    </div>
    <!----><!----><!---->
  <div class="cats-job-column">
    <div class="cats-mobile-column-name"><!---->Position Type<!----></div>
    <div class="cats-job-column-value">
      Software Integration Engineer
    </div>
  </div>
<!----><!---->
  <div class="cats-job-column">
    <div class="cats-mobile-column-name"><!---->Job ID<!----></div>
    <div class="cats-job-column-value">
      02-412-SIE
    </div>
  </div>
<!----><!---->
  <div class="cats-job-column">
    <div class="cats-mobile-column-name"><!---->Location<!----></div>
    <div class="cats-job-column-value">
      Annapolis Junction, Maryland
    </div>
  </div>
<!---->
  """

print(Website.clean_out_markup(innerHtml))