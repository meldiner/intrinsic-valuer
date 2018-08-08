import xlsxwriter

def write(db, file):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()

    row = 0
    row = write_big_four_numbers(worksheet, row, db)
    row += 1
    row = write_owner_earnings(worksheet, row, db)
    row += 1
    row = write_margin_of_safety(worksheet, row, db)

def write_row(worksheet, row, values):
    col = 0
    for value in values:
        worksheet.write(row, col, value)
        col += 1

def get_cell(row, col):
    return chr(64 + col) + str(row)

def growth_fx(row, col):
    return "=IFERROR(" + get_cell(row + 1, col) + "/" + get_cell(row, col) + "-1" + ", \"\")"

def average_fx(start, end, col):
    return "=average(" + get_cell(start, col) + ":" + get_cell(end, col) + ")"

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

    values = ["Baseline Windage Growth Rate", "=average(" + get_cell(row, 2) + ":" + get_cell(row, col) + ")"]
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

def write_margin_of_safety(worksheet, row, db):
    write_row(worksheet, row, ["Margin of Safety"])
    row += 1

    year = max(db["eps"].iterkeys())
    write_row(worksheet, row, ["EPS (diluted) for " + str(year), db["eps"][year]])
    row += 1
    eps_row = row
    eps_col = 2

    write_row(worksheet, row, ["Windage Growth Rate", "=0.16"])
    row += 1
    wgr_row = row
    wgr_col = 2

    write_row(worksheet, row, ["Highest P/E", "=22"])
    row += 1
    hpe_row = row
    hpe_col = 2

    write_row(worksheet, row, ["Wideage P/E", "=min(" + get_cell(wgr_row, wgr_col) + "*200," + get_cell(hpe_row, hpe_col) + ")"])
    row += 1
    wpe_row = row
    wpe_col = 2

    write_row(worksheet, row, ["Minimum Acceptable Rate of Return", "15%"])
    row += 1

    write_row(worksheet, row, ["Future 10-Year EPS", "=" + get_cell(eps_row, eps_col) + "*(1+" + get_cell(wgr_row, wgr_col) + ")^10"])
    row += 1
    feps_row = row
    feps_col = 2
    
    write_row(worksheet, row, ["Future 10-Year Share Price", "=" + get_cell(feps_row, feps_col) + "*" + get_cell(wpe_row, wpe_col)])
    row += 1
    fsp_row = row
    fsp_col = 2

    write_row(worksheet, row, ["Sticker Price", "=" + get_cell(fsp_row, fsp_col) + "/4"])
    row += 1
    sp_row = row
    sp_col = 2

    write_row(worksheet, row, ["Buy Price", "=" + get_cell(sp_row, sp_col) + "/2"])
    row += 1

    return row
