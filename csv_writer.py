import datetime

def write(db, file):
    output_file = open(file, "w")

    end_year = datetime.datetime.now().year 
    start_year = end_year - 10 # we are analysing a history of 10 years

    output_file.write("Year")
    output_file.write(", ")

    for key in sorted(db):
        output_file.write(key)
        output_file.write(", ")

    output_file.write("\n")

    for year in (range(start_year, end_year + 1, 1)):
        year_str = str(year)
        output_file.write(year_str)
        output_file.write(", ")

        for key in sorted(db):
            if year_str in db[key] and db[key][year_str]:
                output_file.write(str(db[key][year_str]))
                output_file.write(", ")
            else:
                output_file.write("")
                output_file.write(", ")

        output_file.write("\n")