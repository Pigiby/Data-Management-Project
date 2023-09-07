import csv


input_file = "filtered_output.csv"
output_file = "filtered_flights.csv"
columns_to_remove = [17]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)

    for row in reader:
        airline = row[6][1:len(row[6])-1]
        row[6] = airline
        new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
        writer.writerow(new_row)

print("CSV file filtered and saved as", output_file)
