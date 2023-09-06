import csv

def should_include_row(row):
    return float(row[11]) == 0

input_file = "flight_data.csv"
output_file = "filtered_output.csv"

with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if should_include_row(row):
            writer.writerow(row)

print("CSV file filtered and saved as", output_file)