import pandas as pd
from scraper import download_report
from parser import parse_reports

def main():
    base_path = "./out"
    TickerFile = pd.read_csv("companylist.csv")
    Tickers = TickerFile['Symbol'].tolist()

    tickers = Tickers

    for ticker in tickers:
        dir_path = base_path + "/" + ticker
        download_report(ticker, dir_path)

    for ticker in tickers:
        dir_path = base_path + "/" + ticker
        parse_reports(dir_path)

if __name__ == '__main__':
    main()