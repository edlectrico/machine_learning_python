# Data acquired from http://pythonprogramming.net/downloads/intraQuarter.zip
import pandas as pd
import os
import time # files' names are dates
from datetime import datetime

path = "/home/edlectrico/Downloads/intraQuarter" 	# the unziped folder path

# Collecting Debt/Equity
def Key_Stats(gather="Total Debt/Equity (mrq)"):	# In the data from each website there
  statspath = path+'/_KeyStats'				# will be a "Total Debt/Equity (mrq)" field
  stock_list = [x[0] for x in os.walk(statspath)]	# for each file in path...

  for each_dir in stock_list[1:]: 	# stock_list[0] points at the root directory...
    each_file = os.listdir(each_dir)
    if len(each_file)>0:
      for file in each_file:
        date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html') # The format of the file's name
        unix_time = time.mktime(date_stamp.timetuple())
        # print date_stamp, unix_time
        file_path = each_dir + '/' + file
	source = open(file_path, 'r').read()	# Storing the full html file
	value = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0] # Splitting by 'gather' term
      time.sleep(15)

Key_Stats()
    
