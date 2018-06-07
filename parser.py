import os
from xbrl import XBRL

def get_report_year(xbrl, file_name):
    year = xbrl.fields['DocumentFiscalYearFocus']
    if (year == 'Fiscal year focus not found'):
        year = file_name.split('-')[1].split('.')[0][:4]
    return year

def parse_reports(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # files.sort(key=os.path.getmtime)
    
    net_income = {}
    equity = {}
    dividends = {}
    revenue = {}
    buy_backs = {}
    ops_cash = {}
    
    for f in files:      
        x = XBRL(os.path.join(folder_path, f))
        fiscal_year = get_report_year(x, f)
        net_income[fiscal_year] = x.fields['NetIncomeLoss']
        equity[fiscal_year] = x.fields['Equity']
        dividends[fiscal_year] = x.fields['PreferredStockDividendsAndOtherAdjustments']
        revenue[fiscal_year] = x.fields['Revenues']
        ops_cash[fiscal_year] = x.fields['NetCashFlowsOperating']
    
    output_file = open(os.path.join(folder_path, "numbers.csv"), "w") 
    output_file.write("Year, Net Income, Equity, Dividends, Revenue, Operating Cash, \n")
    for key in sorted(net_income.iterkeys()):
        output_file.write(key)
        output_file.write(", ")
        output_file.write(str(net_income[key]))
        output_file.write(", ")
        output_file.write(str(equity[key]))
        output_file.write(", ")
        output_file.write(str(dividends[key]))
        output_file.write(", ")
        output_file.write(str(revenue[key]))
        output_file.write(", ")
        output_file.write(str(ops_cash[key]))
        output_file.write(", ")
        output_file.write("\n")