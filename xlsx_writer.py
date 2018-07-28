import xlsxwriter

def write(db, file):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()