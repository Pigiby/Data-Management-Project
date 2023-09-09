import csv

input_file = "fleet_data_extended.csv"
output_file = "filtered_fleet_data.csv"
columns_to_remove = [7]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)

    for row in reader:
        new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
        writer.writerow(new_row)
print("CSV file filtered and saved as", output_file)