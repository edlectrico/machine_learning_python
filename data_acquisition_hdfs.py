#!/usr/bin/env python

# This file represents the data_acquisition.py version launched within a Hadoop environment.
# The example is not finished, and it just shows how to deal with the distributed dataset.

# Usage
# hadoop fs -rm -R intraQuarter/out
# hadoop jar $STREAMING -input intraQuarter/_KEyStats/* -output intraQuarter/out -mapper data_acquisition_hdfs.py -file data_acquisition_hdfs.py -reducer "uniq -c"
# hadoop fs -cat intraQuarter/out/part-*

import sys
import os
import pandas as pd # sudo pip install pandas
import time
from datetime import datetime

gather="Total Debt/Equity (mrq)" # The variable we seek
before_gather = ':</td><td class="yfnc_tabledata1">'
after_gather = '</td>'

file_name = os.getenv('map_input_file')
# print file_name
df = pd.DataFrame(columns = ['Date','Unix',
				'Ticker','DE Ratio', 
				'Price','stock_p_change',
				'SP500','sp500_p_change',
				'Difference', 'Status'])

# yahoo_csv_file = sub.Popen(["hadoop", "fs", "-cat", "/user/cloudera/intraQuarter/YAHOO-INDEX_GSPC.csv"], stdout=sub.PIPE, shell=True)

'''
try:
  sp500_df = pd.from_csv('hdfs://localhost.localdomain:8020/user/cloudera/intraQuarter/YAHOO-INDEX_GSPC.csv')
  print 'DF Loaded!'
except Exception as e:
  print 'First', str(e)
'''

# File name example: hdfs://localhost.localdomain:8020/user/cloudera/intraQuarter/_KeyStats/a/20040130190102.html
# So we split by '/' and take just the last element with [-1]
date_stamp = datetime.strptime(file_name.split('/')[-1], '%Y%m%d%H%M%S.html') # The format of the file's name
unix_time = time.mktime(date_stamp.timetuple())

for line in sys.stdin:
    line = line.strip()
    
    if before_gather in line:
      try:
        try:
	  value = float(line.split(gather + before_gather)[1].split(after_gather)[0])
          print file_name, value
        except Exception as e:
          try:
	    value = float(line.split(gather + ':</td>\n<td class="ynfc_tabledata1">')[1].split(after_gather)[0])
	    print str(e), file_name
	  except Exception as e:
            # print str(e), file_name
            pass
        try:
	  sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
	  row = sp500_df[(sp500_df.index == sp500_date)]
	  sp500_value = float(row["Adjusted Close"])
	  print file_name, 'SP500:', sp500_value
        except Exception as e:
	  print str(e)
      except Exception as e:
        print str(e)
