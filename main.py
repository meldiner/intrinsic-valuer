import argparse
import pandas as pd
from scraper import download_report
from parser import parse_reports
from csv_writer import write as write_csv
from xlsx_writer import write as write_xlsx
import os

def main():
    parser = argparse.ArgumentParser(description='Estimate companies intrinsic value.')
    parser.add_argument("--scrape", type=bool, const=True, nargs='?')
    parser.add_argument("--parse", type=bool, const=True, nargs='?')
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
            db = parse_reports(dir_path)
            write_csv(db, os.path.join(dir_path, "numbers.csv"))
            write_xlsx(db, os.path.join(dir_path, "numbers.xlsx"))


if __name__ == '__main__':
    main()