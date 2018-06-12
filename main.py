import argparse
import pandas as pd
from scraper import download_report
from parser import parse_reports

def main():
    parser = argparse.ArgumentParser(description='Estimate companies intrinsic value.')
    parser.add_argument("--scrape", type=bool)
    parser.add_argument("--parse", type=bool)
    args = parser.parse_args()

    base_path = "./out"
    TickerFile = pd.read_csv("companylist.csv")
    Tickers = TickerFile['Symbol'].tolist()

    tickers = Tickers

    if args.scrape:
        for ticker in tickers:
            dir_path = base_path + "/" + ticker
            download_report(ticker, dir_path)

    if args.parse:
        for ticker in tickers:
            dir_path = base_path + "/" + ticker
            parse_reports(dir_path)

if __name__ == '__main__':
    main()