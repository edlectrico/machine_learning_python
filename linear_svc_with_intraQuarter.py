# Data aquired from http://pythonprogramming.net/downloads/intraQuarter.zip
import pandas as pd
import os
import time # filenames are dates
from datetime import datetime
# visualization
from time import mktime
import matplotlib
import matplotlib.pyplot as pl

import re
import urllib

# This code is pretty similar to the data_acquisition.py python script
# In this case we will work with many more features (see 'gather' as
# parameter in Key_Stats function header)

data_dir = "/home/edlectrico/Downloads/"
path = data_dir + "intraQuarter"	# data folder

def Key_Stats(gather=["Total Debt/Equity",'Trailing P/E',
                      'Price/Sales','Price/Book',
                      'Profit Margin','Operating Margin',
                      'Return on Assets','Return on Equity',
                      'Revenue Per Share','Market Cap',
                      'Enterprise Value','Forward P/E',
                      'PEG Ratio','Enterprise Value/Revenue',
                      'Enterprise Value/EBITDA','Revenue',
                      'Gross Profit','EBITDA',
                      'Net Income Avl to Common ','Diluted EPS',
                      'Earnings Growth','Revenue Growth',
                      'Total Cash','Total Cash Per Share',
                      'Total Debt','Current Ratio',
                      'Book Value Per Share','Cash Flow',
                      'Beta','Held by Insiders',
                      'Held by Institutions','Shares Short (as of',
                      'Short Ratio','Short % of Float',
                      'Shares Short (prior ']):

    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    # We have to update also the DataFrame (as the Key_Stats definition)
    df = pd.DataFrame(columns = ['Date','Unix',
                                 'Ticker','Price',
                                 'stock_p_change','SP500',
                                 'sp500_p_change','Difference',
                                 'DE Ratio','Trailing P/E',
                                 'Price/Sales','Price/Book',
                                 'Profit Margin','Operating Margin',
                                 'Return on Assets','Return on Equity',
                                 'Revenue Per Share','Market Cap',
                                 'Enterprise Value','Forward P/E',
                                 'PEG Ratio','Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA','Revenue',
                                 'Gross Profit','EBITDA',
                                 'Net Income Avl to Common ', 'Diluted EPS',
                                 'Earnings Growth','Revenue Growth',
                                 'Total Cash','Total Cash Per Share',
                                 'Total Debt','Current Ratio',
                                 'Book Value Per Share','Cash Flow',
                                 'Beta','Held by Insiders',
                                 'Held by Institutions','Shares Short (as of',
                                 'Short Ratio','Short % of Float',
                                 'Shares Short (prior ','Status'])

    ticker_list = []
    # https://www.quandl.com/data/YAHOO/INDEX_GSPC-S-P-500-Index 
    sp500_df = pd.DataFrame.from_csv(data_dir + "YAHOO-INDEX_GSPC.csv")

    for each_dir in stock_list[1:]: # Only to 25 to keep it simple. We avoid the stock_list[0] because it points at the root directory
        ticker = each_dir.split(path + '/_KeyStats/')[1] # home/edlectrico/Downloads/intraQuarter/_KeyStats/
        each_file = os.listdir(each_dir)
        ticker_list.append(ticker)
        
        starting_stock_value = False
        starting_sp500_value = False
        
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html') # The format of the file's name
                unix_time = mktime(date_stamp.timetuple())
                file_path = each_dir + '/' + file
                source = open(file_path, 'r').read() # Reading each html file to extract the desired value
			
		try:
                    value_list = []
                    for each_data in gather:
                        try:
			    # First, we have to escape the data: re.escape('^a.*$') -> '\\^a\\.\\*\\$'
			    # Search for a digit with a length between 1 and 8 with a period (\.) followed by a digit.
			    # M for "Million", B for "Billion". We also have percentages. The question mark says 0 
			    # or 1 (we might have the character before the question mark or not)
			    # .*? will handle everything (all the gather) until it finds (\d{1,8}\...
			    # Data examples: -144.00M, 2.17%, N/A, 2.29B
                            regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}K?M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace("B",'')) * 1000000000
                            elif "M" in value:
                                value = float(value.replace("M",'')) * 1000000
                            elif "K" in value:
                                value = float(value.replace("K",'')) * 1000

                            value_list.append(value)
                            
                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)
		    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
			sp500_value = float(row["Adjusted Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row['Adjusted Close'])

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except:
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                        except:
                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                                stock_price = float(stock_price.group(1))
                            except:
                                print('wtf stock price lol',ticker,file, value)
                                
                    if not starting_stock_value:
                        starting_stock_value = stock_price

                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    location = len(df['Date'])

                    difference = stock_p_change-sp500_p_change
                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

		    if value_list.count("N/A") > (0): # Forget about it (we might want to assign a value, as -1, but not for now)
                        pass
		    else:
                        try:
                            df = df.append({'Date':date_stamp,'Unix':unix_time,
                                            'Ticker':ticker,'Price':stock_price,
                                            'stock_p_change':stock_p_change,'SP500':sp500_value,
                                            'sp500_p_change':sp500_p_change,'Difference':difference,
                                            'DE Ratio':value_list[0],#'Market Cap':value_list[1],
                                            'Trailing P/E':value_list[1],'Price/Sales':value_list[2],
                                            'Price/Book':value_list[3],'Profit Margin':value_list[4],
                                            'Operating Margin':value_list[5],'Return on Assets':value_list[6],
                                            'Return on Equity':value_list[7],'Revenue Per Share':value_list[8],
                                            'Market Cap':value_list[9],'Enterprise Value':value_list[10],
                                            'Forward P/E':value_list[11],'PEG Ratio':value_list[12],
                                            'Enterprise Value/Revenue':value_list[13],
					    'Enterprise Value/EBITDA':value_list[14],'Revenue':value_list[15],
                                            'Gross Profit':value_list[16],'EBITDA':value_list[17],
                                            'Net Income Avl to Common ':value_list[18],'Diluted EPS':value_list[19],
                                            'Earnings Growth':value_list[20],'Revenue Growth':value_list[21],
                                            'Total Cash':value_list[22],'Total Cash Per Share':value_list[23],
                                            'Total Debt':value_list[24],'Current Ratio':value_list[25],
                                            'Book Value Per Share':value_list[26],'Cash Flow':value_list[27],
                                            'Beta':value_list[28],'Held by Insiders':value_list[29],
                                            'Held by Institutions':value_list[30],'Shares Short (as of':value_list[31],
                                            'Short Ratio':value_list[32],'Short % of Float':value_list[33],
                                            'Shares Short (prior ':value_list[34],'Status':status},
                                             ignore_index=True)

                        except Exception as e:
                            print(str(e),'df creation')
                            time.sleep(15)
     
                except Exception as e:
                    pass

    df.to_csv('out/key_stats.csv')

Key_Stats()
