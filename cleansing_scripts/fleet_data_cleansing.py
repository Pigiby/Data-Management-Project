import csv
from datetime import datetime



def should_include_row(row,airlines):
    return row[1] in airlines or row[0] in airlines


input_file = "../final_files/filtered_airlines.csv"
input_file_1 = 'filtered_fleet_data.csv'
output_file = "fleet_data_extended.csv"
with open(input_file, 'r', newline='', encoding="utf8") as csvfile_in, open(input_file_1, 'r', newline='', encoding="utf8") as csvfile_in_1, open(output_file, 'w', newline='', encoding="utf8") as csvfile_out:
    reader = csv.reader(csvfile_in)
    reader_1 = csv.reader(csvfile_in_1)
    writer = csv.writer(csvfile_out)

    header_1 = next(reader_1)
    
    
    writer.writerow(header_1)
    header = next(reader)
    airlines = []
    for row in reader:
        airlines.append(row[0])
    for row in reader_1:
        if should_include_row(row,airlines):
            writer.writerow(row)

print("CSV file filtered and saved as", output_file)
