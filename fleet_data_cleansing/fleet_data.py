import csv

input_file = "fleet_data.csv"
output_file = "filtered_fleet_data.csv"
columns_to_remove = [7]
with open(input_file, 'r', newline='',encoding='latin-1') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    header = next(reader)
    new_header =  [value for idx, value in enumerate(header) if idx not in columns_to_remove]
    writer.writerow(new_header)
    for row in reader:
        row =  [value for idx, value in enumerate(row) if idx not in columns_to_remove]
        row[0] = row[0].lower()
        row[1] = row[1].lower()
        if row[3] != '':
           row[3] = int(row[3])
        else:
           row[3] = 0
        if row[4] != '':
           row[4] = int(row[4])
        else:
           row[4] = 0
        if row[5] != '':
           row[5] = int(row[5])
        else:
           row[5] = 0
        if row[6] != '':
           row[6] = int(row[6])
        else:
           row[6] = 0
        if row[7] != '':
            unit_cost = row[7].replace(",", ".")
            row[7] = float(unit_cost[1:])*1000000
        if row[8] != '':
            total_cost = row[8].replace(",", ".")
            row[8] = float(total_cost[1:])*1000000
        if row[9] != '':
           row[9] = float(row[9])
        writer.writerow(row)
print("CSV file filtered and saved as", output_file)




        