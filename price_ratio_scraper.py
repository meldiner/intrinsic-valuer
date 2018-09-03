
#April 18, 2015 written by /u/greatluck

#scrape a list of current S&P500 public companies from wikipedia
#and loop through them to scrape historical p/e ratios from morningstar
#results are saved in a CSV file

#a couple of things make this a bit tricky
#the morningstar website is populated by javascript, not html, so scraping requires pulling from a different url
#that secondary url changes depending on what market the stock trades in: NYSE or nasdaq

#this is definitely not written in a very pythonic or clean way, but it works


import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
import json

def download_historical_price_ratio(ticker,dir_path):
    print 'Scraping historical price ratios for ' + ticker + '...'

    #javascript populated site
    morningstar_url = 'http://financials.morningstar.com/valuation/price-ratio.html?t=' + ticker
    morningstar_r = requests.get(morningstar_url)
    morningstar_html = morningstar_r.text

    #the actual data is stored on a different site, but the url depends on where the stock trades
    value_check = 'XNYS:' + ticker
    if value_check in morningstar_html:
        url_pe = 'http://financials.morningstar.com/valuation/valuation-history.action?&t=XNYS:'+ticker+'&region=usa&culture=en-US&cur=&type=price-earnings'
    else:
        url_pe = 'http://financials.morningstar.com/valuation/valuation-history.action?&t=XNAS:'+ticker+'&region=usa&culture=en-US&cur=&type=price-earnings'

    #scrape the site with the data
    r_pe = requests.get(url_pe)
    html_pe = r_pe.text
    soup_pe = BeautifulSoup(html_pe,'html.parser')

    #table with all the data
    new_tables = soup_pe.find_all('table')
    valuation_table = new_tables[0]

    #find the rows we need
    rows = valuation_table.findChildren(['th', 'tr'])

    #the cells with data
    price_earnings_data = rows[1].find_all('td')
    price_book_data = rows[6].find_all('td')
    price_sales_data = rows[11].find_all('td')
    price_cash_data = rows[16].find_all('td')

    #create the list which will later be populated with the data
    db = { 
        'Price/Earnings': {},
        'Price/Book': {},
        'Price/Sales': {},
        'Price/Cash Flow': {}
    }
    year = datetime.datetime.now().year - len(price_earnings_data) + 1

    for i in range(0, len(price_earnings_data), 1):
        db['Price/Earnings'][year + i] = price_earnings_data[i].text.encode('ascii','ignore')
        db['Price/Book'][year + i] = price_book_data[i].text.encode('ascii','ignore')
        db['Price/Sales'][year + i] = price_sales_data[i].text.encode('ascii','ignore')
        db['Price/Cash Flow'][year + i] = price_cash_data[i].text.encode('ascii','ignore')

    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    #create and open output file for writing
    filename = os.path.join(dir_path, 'historical_price_ratio.json')
    with open(filename, 'w') as file:
        file.write(json.dumps(db))

    print 'Done scraping ' + ticker