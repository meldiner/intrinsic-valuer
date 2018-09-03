import urllib2, os
from bs4 import BeautifulSoup

def get_list(ticker):

    base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
    base_url_part2 = "&type=&dateb=&owner=&start="
    base_url_part3 = "&count=100&output=xml"
    href = []
    
    for page_number in range(0,2000,100):
    
        base_url = base_url_part1 + ticker + base_url_part2 + str(page_number) + base_url_part3
        
        sec_page = urllib2.urlopen(base_url)
        sec_soup = BeautifulSoup(sec_page, "html.parser")
        
        filings = sec_soup.findAll('filing')
        
        for filing in filings:
            report_year = int(filing.datefiled.get_text()[0:4])
            if (filing.type.get_text() == "10-K") & (report_year > 2008):
                print filing.filinghref.get_text()
                href.append(filing.filinghref.get_text())
    
    return href

def download_sec_filings(ticker,dir_path):
    url_list = get_list(ticker)
    
    target_base_url = 'http://www.sec.gov'
    
    # type = 'EX-101.INS'
    target_file_type = u'EX-101.INS'
    
    for report_url in url_list:
        report_page = urllib2.urlopen(report_url)
        report_soup = BeautifulSoup(report_page, "html.parser")
        
        xbrl_file = report_soup.findAll('tr')
        
        for item in xbrl_file:
            try:
                if item.findAll('td')[3].get_text() == target_file_type:
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                             
                    target_url = target_base_url + item.findAll('td')[2].find('a')['href']
                    print "Target URL found!"
                    print "Target URL is:", target_url
                    
                    file_name = target_url.split('/')[-1]
                    file_path = os.path.join(dir_path,file_name)

                    if os.path.isfile(file_path):
                        print file_name + " exists, skipping"
                    else:
                        print "downloading " + file_name
                        xbrl_report = urllib2.urlopen(target_url)
                        output = open(file_path,'wb')
                        output.write(xbrl_report.read())
                        output.close()
            except:
                pass