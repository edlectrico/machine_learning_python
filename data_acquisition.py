# Data aquired from http://pythonprogramming.net/downloads/intraQuarter.zip
import pandas as pd
import os
import time # filenames are dates
from datetime import datetime
# visualization
from time import mktime
import matplotlib
import matplotlib.pyplot as pl
from matplotlib import style
style.use("dark_background")
import re

data_dir = "/home/edlectrico/Downloads/"
path = data_dir + "intraQuarter" 			# data folder
split_before_value = ':</td><td class="yfnc_tabledata1">'
split_after_value = '</td>'
split_before_stock = '</small><big><b>'
split_after_stock = '</b></big>'

# Collecting Debt/Equity
def Key_Stats(gather="Total Debt/Equity (mrq)"):	# In the data from each website there
  statspath = path+'/_KeyStats'				# will be a "Total Debt/Equity (mrq)" field
  stock_list = [x[0] for x in os.walk(statspath)]	# for each file in path...
  df = pd.DataFrame(columns = ['Date','Unix',
				'Ticker','DE Ratio', 
				'Price','stock_p_change',
				'SP500','sp500_p_change',
				'Difference', 'Status'])

  # https://www.quandl.com/data/YAHOO/INDEX_GSPC-S-P-500-Index  
  sp500_df = pd.DataFrame.from_csv(data_dir + "YAHOO-INDEX_GSPC.csv")
  ticker_list = []
  
  for each_dir in stock_list[1:]: 			# stock_list[0] points at the root directory...
    each_file = os.listdir(each_dir)
    ticker = each_dir.split(path + '/_KeyStats/')[1] 	# home/edlectrico/Downloads/intraQuarter/_KeyStats/
    ticker_list.append(ticker)

    starting_stock_value = False
    starting_sp500_value = False    

    if len(each_file) > 0:
      for file in each_file:
        date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html') # The format of the file's name
        unix_time = time.mktime(date_stamp.timetuple())
        file_path = each_dir + '/' + file
	source = open(file_path, 'r').read() 		# Reading each html file to extract the desired value

	try:
	  try:
            value = float(source.split(gather + split_before_value)[1].split(split_after_value)[0]) # Split by 'gather' term  
          except Exception as e:
	    try:
	      value = float(source.split(gather + ':</td>\n<td class="ynfc_tabledata1">')[1].split(split_after_value)[0])
	      print str(e), ticker, file
	    except Exception as e:
	      pass

	  try:
	    sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
	    row = sp500_df[(sp500_df.index == sp500_date)]
	    sp500_value = float(row["Adjusted Close"])
	  except:
            sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d') # 3 days in seconds (avoid weekends)
            row = sp500_df[(sp500_df.index == sp500_date)]
            sp500_value = float(row["Adjusted Close"]) 
	
	  try:
	    stock_price = float(source.split(split_before_stock)[1].split(split_after_stock)[0])
	  except Exception as e:
	    try:
	      stock_price = (source.split(split_before_stock)[1].split(split_after_stock)[0])
	      stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price) # Search for a digit with a length between 1 and 8 with a period (\.) followed by a digit
	      stock_price = float(stock_price.group(1))
	    except Exception as e:
	      stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
	   	  

	  if not starting_stock_value:
	    starting_stock_value = stock_price
	  if not starting_sp500_value:
	    starting_sp500_value = sp500_value

	  stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
	  sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

	  difference = stock_p_change - sp500_p_change

	  if (difference > 0):
	    status = "outperform"
	  else:
	    status = "underperform"

	  # Finally assign the values to the DataFrame columns
	  df = df.append({'Date':date_stamp,'Unix':unix_time,
                          'Ticker':ticker,'DE Ratio':value,
                          'Price':stock_price,'stock_p_change':stock_p_change,
                          'SP500':sp500_value,'sp500_p_change':sp500_p_change,
			  'Difference':difference, 'Status':status},
			   ignore_index = True)
	except Exception as e:
	  pass

      time.sleep(15)

  for each_ticker in ticker_list:
    try:
      plot_df = df[(df['Ticker'] == each_ticker)]
      plot_df = plot_df.set_index(['Date'])

      if (plot_df['Status'][-1] == "underperform"): # -1 for the last one
	color = 'r'
      else:
	color = 'g'

      plot_df['Difference'].plot(label = each_ticker, color = color)
      pl.legend()

    except:
      pass

  pl.savefig('out/plot.pdf')
  pl.show()

  save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
  print save
  df.to_csv(save)

Key_Stats()
