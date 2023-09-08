import csv
from datetime import datetime


input_file = "filtered_flights.csv"
output_file = "filtered_flights_extended.csv"
columns_to_remove = [11, 13, 17]
with open(input_file, 'r', newline='') as csvfile_in, open(output_file, 'w', newline='') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    header = next(reader)
    new_header = []
    for i in range(len(header)):
        if i == 8:
            new_header.append("departure_day")
            new_header.append("departure_month")
            new_header.append("departure_year")
            new_header.append("departure_time")

        elif i == 9:
            new_header.append("arrival_day")
            new_header.append("arrival_month")
            new_header.append("arrival_year")
            new_header.append("arrival_time")
        else:
            new_header.append(header[i])
    print(new_header)
    writer.writerow(new_header)

    for row in reader:
        date_format = '%Y-%m-%d %H:%M:%S'
        departure_date = datetime.strptime(row[8], date_format) 
        departure_time = departure_date.time()
        departure_day = departure_date.day
        departure_month = departure_date.month
        departure_year = departure_date.year

        arrival_date = datetime.strptime(row[9], date_format) 
        arrival_time = arrival_date.time()
        arrival_day = arrival_date.day
        arrival_month = arrival_date.month
        arrival_year = arrival_date.year

        new_row = []
        for i in range(len(row)):
            if i == 8:
                new_row.append(departure_day)
                new_row.append(departure_month)
                new_row.append(departure_year)
                new_row.append(departure_time)

            elif i == 9:
                new_row.append(arrival_day)
                new_row.append(arrival_month)
                new_row.append(arrival_year)
                new_row.append(arrival_time)
            else:
                new_row.append(row[i])
        writer.writerow(new_row)

print("CSV file filtered and saved as", output_file)
