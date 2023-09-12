import csv
from datetime import datetime
from collections import Counter


aircraft = {}
input_file = "filtered_fleet_data.csv"
input_file_1 = 'filtered_fleet_data.csv'
output_file = "filtered_fleet_data_final.csv"
with open(input_file, 'r', newline='') as csvfile_in, open(input_file_1, 'r', newline='') as csvfile_in_1, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    reader_1 = csv.reader(csvfile_in_1)
    writer = csv.writer(csvfile_out)

    header_1 = next(reader_1)
    
    
    writer.writerow(header_1)
    header = next(reader)
    for row in reader:
        key = row[2]
        if key not in aircraft:
            aircraft[key] = []
        aircraft[key].append(row[7])
    for key in aircraft:
        counter = Counter(aircraft[key])
        aircraft[key] = counter.most_common(1)[0][0]
    print(aircraft)
    for row in reader_1:
        row[7] = aircraft[row[2]]   
        writer.writerow(row)


print("CSV file filtered and saved as", output_file)
