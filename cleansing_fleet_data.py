import csv

input_file = "filtered_fleet_data.csv"
output_file = "filtered_fleet_data_final.csv"


with open(input_file, 'r', newline='',encoding='latin-1') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    header = next(reader)
   
    writer.writerow(header)
    for row in reader:
        if row[3] != '':
           row[3] = int(row[3])
        else:
           print("ciao")
        if row[4] != '':
           row[4] = int(row[4])
        if row[5] != '':
           row[5] = int(row[5])
        if row[6] != '':
           row[6] = int(row[6])
        if row[7] != '':
            unit_cost = row[7].replace(",", ".")
            row[7] = float(unit_cost[1:])*1000000
        if row[8] != '':
            total_cost = row[8].replace(",", ".")
            row[8] = float(total_cost[1:])*1000000
        if row[9] != '':
           row[9] = float(row[9])

        #elif row[17] == 'None':
        #    row[17] = ''
#
        #if row[20] != '':
        #    row[20] = row[20][0:len(row[20])-1]
        #if row[20] == 'None':
        #    row[20] = ''
        writer.writerow(row)
print("CSV file filtered and saved as", output_file)