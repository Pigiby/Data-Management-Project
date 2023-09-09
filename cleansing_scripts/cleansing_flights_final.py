import csv

input_file = "filtered_flights_extended__.csv"
output_file = "../final_files/filtered_flights_final.csv"


with open(input_file, 'r', newline='',encoding='latin-1') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    header = next(reader)
   
    writer.writerow(header)
    for row in reader:
        if row[17] != '':
            row[17] = float(row[17])
        elif row[17] == 'None':
            row[17] = ''

        if row[20] != '':
            row[20] = row[20][0:len(row[20])-1]
        if row[20] == 'None':
            row[20] = ''
        writer.writerow(row)
print("CSV file filtered and saved as", output_file)