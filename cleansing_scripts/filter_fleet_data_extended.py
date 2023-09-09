import csv

input_file = "fleet_data_extended.csv"
input_file1 = "filtered_airplanes.csv"
output_file = "filtered_fleet_data.csv"
columns_to_remove = [7]
aircrafts = []
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out, open(input_file1, 'r', newline='') as csvfile_in1:
    reader = csv.reader(csvfile_in)
    reader1 = csv.reader(csvfile_in1)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    header1 = next(reader1)

    for row in reader1:
        aircrafts.append(row[0])

    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)

    for row in reader:
        if row[2] in aircrafts:
            new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
            writer.writerow(new_row)
print("CSV file filtered and saved as", output_file)