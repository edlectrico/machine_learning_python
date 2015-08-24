# Data acquired from http://pythonprogramming.net/downloads/intraQuarter.zip
import pandas as pd
import os
import time # filenames are dates
from datetime import datetime

path = "/home/edlectrico/Downloads/intraQuarter" 	# the unziped folder path

# Collecting Debt/Equity
def Key_Stats(gather="Total Debt/Equity (mrq)"):	# In the data from each website there
  statspath = path+'/_KeyStats'				# will be a "Total Debt/Equity (mrq)" field
  stock_list = [x[0] for x in os.walk(statspath)]	# for each file in path...
  df = pd.DataFrame(columns = ['Date','Unix','Ticker','DE Ratio'])
  
  for each_dir in stock_list[1:]: 			# stock_list[0] points at the root directory...
    each_file = os.listdir(each_dir)
    # print 'each_dir: ' + str(each_dir)
    # print 'each_file: ' + str(each_file)
    ticker = each_dir.split('home/edlectrico/Downloads/intraQuarter/_KeyStats/')[1] # home/edlectrico/Downloads/intraQuarter/_KeyStats/
    print 'ticker: ' + str(ticker)
    if len(each_file) > 0:
      for file in each_file:
        date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html') # The format of the file's name
        unix_time = time.mktime(date_stamp.timetuple())
        # print date_stamp, unix_time
        file_path = each_dir + '/' + file
	source = open(file_path, 'r').read()	# Storing the full html file
	print file_path
	try:
	  value = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0] # Splitting by 'gather' term
	  df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,}, ignore_index = True)
	  print ticker + ":" + str(value)
	except IndexError:
	  print "Can't get value from %s" %file_path

      time.sleep(15)
  save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
  print save
  df.to_csv(save)

Key_Stats()
