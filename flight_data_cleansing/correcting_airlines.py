import csv
from datetime import datetime




input_file = "../airlines_cleansing/filtered_airlines.csv"
input_file_1 = 'filtered_flights.csv'
output_file = "filtered_flights_final.csv"
with open(input_file, 'r', newline='') as csvfile_in, open(input_file_1, 'r', newline='') as csvfile_in_1, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    reader_1 = csv.reader(csvfile_in_1)
    writer = csv.writer(csvfile_out)

    header_1 = next(reader_1)
    
    
    writer.writerow(header_1)
    header = next(reader)
    airlines = []
    iata_codes = []
    for row in reader:
        airlines.append(row[0])
        iata_codes.append(row[1])
    for row in reader_1:
        if row[6] in airlines:
            writer.writerow(row)
        else:
            i = 0
            for a in airlines:
                if len(row[6]) < len(a) and row[6] in a:
                    if(row[5] == iata_codes[i]):
                        row[6] = a    
                i+=1
            writer.writerow(row)


print("CSV file filtered and saved as", output_file)
