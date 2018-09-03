import os
import json
from xbrl import XBRL

def add_missing_fields(xbrl):
        #PaymentsOfDividends
        xbrl.fields['PaymentsOfDividends'] = xbrl.GetFactValue("us-gaap:PaymentsOfDividends", "Duration")
        if xbrl.fields['PaymentsOfDividends']== None:
            xbrl.fields['PaymentsOfDividends'] = 0

        #PaymentsForRepurchaseOfCommonStock
        xbrl.fields['PaymentsForRepurchaseOfCommonStock'] = xbrl.GetFactValue("us-gaap:PaymentsForRepurchaseOfCommonStock", "Duration")
        if xbrl.fields['PaymentsForRepurchaseOfCommonStock']== None:
            xbrl.fields['PaymentsForRepurchaseOfCommonStock'] = 0
        
        #DepreciationDepletionAndAmortization
        xbrl.fields['DepreciationDepletionAndAmortization'] = xbrl.GetFactValue("us-gaap:DepreciationDepletionAndAmortization", "Duration")
        if xbrl.fields['DepreciationDepletionAndAmortization']== None:
            xbrl.fields['DepreciationDepletionAndAmortization'] = 0

        #IncreaseDecreaseInReceivables
        xbrl.fields['IncreaseDecreaseInReceivables'] = xbrl.GetFactValue("us-gaap:IncreaseDecreaseInReceivables", "Duration")
        if xbrl.fields['IncreaseDecreaseInReceivables']== None:
            xbrl.fields['IncreaseDecreaseInReceivables'] = 0
                
        #IncreaseDecreaseInAccountsPayable
        xbrl.fields['IncreaseDecreaseInAccountsPayable'] = xbrl.GetFactValue("us-gaap:IncreaseDecreaseInAccountsPayable", "Duration")
        if xbrl.fields['IncreaseDecreaseInAccountsPayable']== None:
            xbrl.fields['IncreaseDecreaseInAccountsPayable'] = 0

        #CapitalExpenditures
        xbrl.fields['CapitalExpenditures'] = xbrl.GetFactValue("us-gaap:PaymentsForCapitalImprovements", "Duration")
        if xbrl.fields['CapitalExpenditures'] == None:
            xbrl.fields['CapitalExpenditures'] = xbrl.GetFactValue("us-gaap:PaymentsToAcquirePropertyPlantAndEquipment", "Duration")
            if xbrl.fields['CapitalExpenditures'] == None:
                xbrl.fields['CapitalExpenditures'] = 0
        try:
            xbrl.fields['CapitalExpenditures'] += xbrl.GetFactValue("wfm:OtherPropertyAndEquipmentExpenditures", "Duration")
        except:
            print "Caught it!"

        #NumberOfSharesDiluted
        xbrl.fields['NumberOfSharesDiluted'] = xbrl.GetFactValue("us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding", "Duration")
        if xbrl.fields['NumberOfSharesDiluted']== None:
            xbrl.fields['NumberOfSharesDiluted'] = 0

        #EarningsPerShareDiluted
        xbrl.fields['EarningsPerShareDiluted'] = xbrl.GetFactValue("us-gaap:EarningsPerShareDiluted", "Duration")
        if xbrl.fields['EarningsPerShareDiluted']== None:
            xbrl.fields['EarningsPerShareDiluted'] = 0


def get_report_year(xbrl, file_name):
    year = xbrl.fields['DocumentFiscalYearFocus']
    if (year == 'Fiscal year focus not found'):
        year = file_name.split('-')[1].split('.')[0][:4]
    return year

def parse_sec_reports(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith("xml")]
    
    db = {}
    db["net_income"] = {}
    db["equity"] = {}
    db["dividends"] = {}
    db["revenue"] = {}
    db["buy_backs"] = {}
    db["ops_cash"] = {}
    db["depreciation"] = {} # Depreciation and Amortization
    db["receivable"] = {} # Net Change: Accounts Receivable
    db["payable"] = {} # Net Change: Accounts Payable
    db["tax"] = {} # Income Tax
    db["expenditures"] = {} # Capital Expenditures
    db["shares"] = {} #Number of Shares (diluted)
    db["eps"] = {} #EarningsPerShareDiluted
    
    for f in files:      
        x = XBRL(os.path.join(folder_path, f))
        add_missing_fields(x)
        fiscal_year = get_report_year(x, f)

        # TODO: assert if year already exists
        # if fiscal_year in net_income:
        #     assert "Year " + fiscal_year + "parsed twice for " + f

        db["net_income"][fiscal_year] = x.fields['NetIncomeLoss']
        db["equity"][fiscal_year] = x.fields['Equity']
        db["dividends"][fiscal_year] = x.fields['PaymentsOfDividends']
        db["buy_backs"][fiscal_year] = x.fields['PaymentsForRepurchaseOfCommonStock']
        db["revenue"][fiscal_year] = x.fields['Revenues']
        db["ops_cash"][fiscal_year] = x.fields['NetCashFlowsOperating']
        db["depreciation"][fiscal_year] = x.fields['DepreciationDepletionAndAmortization']
        db["receivable"][fiscal_year] = x.fields['IncreaseDecreaseInReceivables']
        db["payable"][fiscal_year] = x.fields['IncreaseDecreaseInAccountsPayable']
        db["tax"][fiscal_year] = x.fields['IncomeTaxExpenseBenefit']
        db["expenditures"][fiscal_year] = x.fields['CapitalExpenditures']
        db["shares"][fiscal_year] = x.fields['NumberOfSharesDiluted']
        db["eps"][fiscal_year] = x.fields['EarningsPerShareDiluted']
    
    return db

def parse_price_ratio_reports(folder_path):
    with open(os.path.join(folder_path, 'historical_price_ratio.json')) as f:
        db = json.load(f)
    return db

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def parse_reports(folder_path):
    db1 = parse_sec_reports(folder_path)
    db2 = parse_price_ratio_reports(folder_path)
    db = merge_two_dicts(db1, db2)
    return db