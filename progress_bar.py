
from datetime import date

workbook_name = f'PAX-{date.today()}.xls'

class ProgressBar:

    def __init__(self, fill = '=', empty = ' ', printEnd = "\r"):
        self.fill = fill
        self.length = 50
        self.empty = empty
        self.printEnd = printEnd

    """
    Call in a loop to create terminal progress bar
        iteration -  : current iteration (Int)
        total     -  : total iterations (Int)
        prefix    -  : prefix string (Str)
        suffix    -  : suffix string (Str)
    """
    def refresh (self, iteration, total, prefix = 'Progress: ', suffix = ''):
        if(total == 0):
            total = 1 
        iteration += 1
        if (iteration > total):
            iteration = total - 1
        percent = 100 * (iteration / float(total))
        color = ProgressBar.get_color(percent)
        filledLength = int(self.length * iteration // total)
        bar = color + self.fill * filledLength + self.white + self.empty * (self.length - filledLength)
        
        print(f'\r{prefix} [{bar}] {iteration}/{total} {suffix}', end = self.printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    #colors
    white = "\033[0m"
    blue = "\033[1;34m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    red = "\033[1;31m"

    def get_color(percent):
        if (percent == 100):
            return ProgressBar.blue
        elif (percent > 80):
            return ProgressBar.green
        elif(percent > 40):
            return ProgressBar.yellow
        else:
            return ProgressBar.red