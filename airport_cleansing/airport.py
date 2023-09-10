import csv

input_file = "airports.csv"
output_file = "filtered_airports.csv"
columns_to_remove = [0,10,12,13]
with open(input_file, 'r', newline='',encoding='latin-1') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)
    for row in reader:
        row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
        if row[3] == '\\N':
            row[3] = ''
        if row[4] == '\\N':
            row[4] = ''
        if row[5] != '':
            row[5] = float(row[5])
        if row[6] != '':
            row[6] = float(row[6])
        if row[7] != '':
            row[7] = float(row[7])
        if row[8] != '':
            if row[8] == "\\N":
                row[8] = ''
            else:
                row[8] = float(row[8])
        if row[9] == '\\N':
            row[9] = ''
        writer.writerow(row)
print("CSV file filtered and saved as", output_file)