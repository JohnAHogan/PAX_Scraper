from datetime import date
import re
import time
from progress_bar import ProgressBar
from website import Website

# Print iterations progress
progressBar = ProgressBar()

# A List of Items
items = list(range(0, 57))
l = len(items)

progressBar.refresh(0,57, prefix = 'GDIT Progress:', suffix = 'Collecting Job Postings')
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    progressBar.refresh(i, 0, prefix = 'GDIT Progress:', suffix = 'Collecting Job Postings')

print()