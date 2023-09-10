import csv

input_file = "aircraft.csv"
output_file = "filtered_aircraft.csv"
columns_to_remove = [0]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)

    for row in reader:
        #set to null missing iata and icao codes
        if row[2] == '\\N':
            row[2] = ''
        if row[3] == '\\N':
            row[3] = ''
        #remove the first column
        new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
        writer.writerow(new_row)
print("CSV file filtered and saved as", output_file)