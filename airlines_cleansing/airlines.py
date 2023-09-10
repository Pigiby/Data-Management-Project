import csv

def should_include_row(row):
    #active airlines, not null iata and icao codes
    return row[7] == 'Y'

input_file = "airlines.csv"
output_file = "filtered_airlines.csv"
columns_to_remove = [0,2,5,7]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)

    for row in reader:
        if should_include_row(row):
            if row[3] == '-' or row[3] == '\\N' or row[3] == 'N/A':
                row[3] = ''
            if row[4] == '-' or row[4] == '\\N' or row[4] == 'N/A':
                row[4] = ''
            if row[6] == '-' or row[6] == '\\N' or row[6] == 'N/A':
                row[6] = ''
            #airline in lowercase 
            row[1] = row[1].lower()
            new_row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
            writer.writerow(new_row)
print("CSV file filtered and saved as", output_file)
