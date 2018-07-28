
def write(db, file):
    output_file = open(file, "w")

    output_file.write("Big Four Numbers\n")
    output_file.write("Year, Net Income, Equity + Dividends, Sales, Operating Cash, \n")
    for key in sorted(db["net_income"].iterkeys()):
        output_file.write(key)
        output_file.write(", ")
        output_file.write(str(db["net_income"][key]))
        output_file.write(", ")
        output_file.write(str(db["equity"][key] + db["dividends"][key]))
        output_file.write(", ")
        output_file.write(str(db["revenue"][key]))
        output_file.write(", ")
        output_file.write(str(db["ops_cash"][key]))
        output_file.write(", ")
        output_file.write("\n")

    output_file.write("\n")

    output_file.write("Owner Earnings\n")
    output_file.write("Year, Operating Cash, Capital Expenditures, Number of Shares (diluted), Owners Earnings, \n")
    for key in sorted(db["net_income"].iterkeys()):
        output_file.write(key)
        output_file.write(", ")
        output_file.write(str(db["ops_cash"][key]))
        output_file.write(", ")
        output_file.write(str(db["expenditures"][key]))
        output_file.write(", ")
        output_file.write(str(db["shares"][key]))
        output_file.write(", ")

        if db["shares"][key] != 0: 
            output_file.write(str((db["ops_cash"][key] - db["expenditures"][key]) / db["shares"][key]))
        else:
            output_file.write("ZERO SHARES ERROR")

        output_file.write(", ")
        output_file.write("\n")

    output_file.write("\n")

    output_file.write("Sticker Price\n")
    output_file.write("Year, Earnings per Share (diluted), Book Value, Dividend, \n")
    for key in sorted(db["net_income"].iterkeys()):
        output_file.write(key)
        output_file.write(", ")
        output_file.write(str(db["eps"][key]))
        output_file.write(", ")

        if db["shares"][key] != 0: 
            output_file.write(str(db["equity"][key] / db["shares"][key]))
            output_file.write(", ")
            output_file.write(str(db["dividends"][key] / db["shares"][key]))
            output_file.write(", ")
        else:
            output_file.write("ZERO SHARES ERROR")
            output_file.write(", ")
            output_file.write("ZERO SHARES ERROR")
            output_file.write(", ")

        output_file.write("\n")

    output_file.write("\n")