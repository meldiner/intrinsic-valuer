import xlsxwriter

def write(db, file):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()

    row = 0
    row = write_big_four_numbers(worksheet, row, db)
    row += 1
    row = write_owner_earnings(worksheet, row, db)
    row += 1
    row = write_sticker_price(worksheet, row, db)

def write_row(worksheet, row, values):
    col = 0
    for value in values:
        worksheet.write(row, col, value)
        col += 1

def growth_fx(row, col):
    return "=IFERROR(" + chr(64 + col) + str(row + 1) + "/" + chr(64 + col) + str(row) + "-1" + ", \"\")"

def average_fx(start, end, col):
    return "=average(" + chr(64 + col) + str(start) + ":" + chr(64 + col) + str(end) + ")"

def write_big_four_numbers(worksheet, row, db):
    write_row(worksheet, row, ["Big Four Numbers"])
    row += 1

    write_row(worksheet, row, ["Year", "Net Income", "", "Equity + Dividends", "", "Sales", "", "Operating Cash", ""])
    row += 1

    start = row + 1

    for key in sorted(db["net_income"].iterkeys()):
        values = [key]
        col = 1
        values.append(str(db["net_income"][key]))
        col += 1
        values.append(growth_fx(row, col))
        col += 1
        values.append("=" + str(db["equity"][key]) + "+" + str(db["dividends"][key]))
        col += 1
        values.append(growth_fx(row, col))
        col += 1
        values.append(str(db["revenue"][key]))
        col += 1
        values.append(growth_fx(row, col))
        col += 1
        values.append(str(db["ops_cash"][key]))
        col += 1
        values.append(growth_fx(row, col))
        col += 1
        write_row(worksheet, row, values)
        row += 1

    values = ["Average"]
    col = 2
    values.append("")
    col += 1
    values.append(average_fx(start, row, col))
    col += 1
    values.append("")
    col += 1
    values.append(average_fx(start, row, col))
    col += 1
    values.append("")
    col += 1 
    values.append(average_fx(start, row, col))
    col += 1
    values.append("")
    col += 1
    values.append(average_fx(start, row, col))
    col += 1
    values.append("")
    col += 1
    write_row(worksheet, row, values)
    row += 1

    values = ["Baseline Windage Growth Rate", "=average(" + chr(64 + 2) + str(row) + ":" + chr(64 + col) + str(row) + ")"]
    write_row(worksheet, row, values)
    row += 1

    return row

def write_owner_earnings(worksheet, row, db):
    write_row(worksheet, row, ["Owner Earnings"])
    row += 1

    write_row(worksheet, row, ["Year", "Operating Cash", "Capital Expenditures", "Number of Shares (diluted)", "Owners Earnings"])
    row += 1

    for key in sorted(db["net_income"].iterkeys()):
        values = [key, str(db["ops_cash"][key]), str(db["expenditures"][key]), str(db["shares"][key])]

        if db["shares"][key] != 0: 
            values.append(str((db["ops_cash"][key] - db["expenditures"][key]) / db["shares"][key]))
        else:
            values.append("ZERO SHARES ERROR")

        write_row(worksheet, row, values)
        row += 1

    return row

def write_sticker_price(worksheet, row, db):
    write_row(worksheet, row, ["Sticker Price"])
    row += 1

    write_row(worksheet, row, ["Minimum Acceptable Rate of Return", "15%"])
    row += 1

    write_row(worksheet, row, ["Year", "Earnings per Share (diluted)"])
    row += 1

    year = max(db["eps"].iterkeys())
    write_row(worksheet, row, [year, db["eps"][year]])
    row += 1

    return row
