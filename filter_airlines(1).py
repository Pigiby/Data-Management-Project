import csv

def should_include_row(row):
    return row[7] == 'Y'

input_file = "airlines(1).csv"
output_file = "filtered_airlines.csv"
columns_to_remove = [0,2,5,7]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if should_include_row(row):
            new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
            print(new_row)
            writer.writerow(new_row)
print("CSV file filtered and saved as", output_file)