import csv

input_file = "filtered_airplanes.csv"
output_file = "filtered_airplanes_final.csv"


with open(input_file, 'r', newline='',encoding='latin-1') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    header = next(reader)
   
    writer.writerow(header)
    for row in reader:
        if row[1] == '\\N':
            row[1] = ''
        if row[2] == '\\N':
            row[2] = ''
        
        writer.writerow(row)
print("CSV file filtered and saved as", output_file)