import csv
from datetime import datetime

def transform_date(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Ελέγχει αν η ημερομηνία υπάρχει στην τρίτη στήλη
            if len(row) >= 3 and row[2]:
                try:
                    original_date = datetime.strptime(row[2], '%d/%m/%y')
                    row[2] = original_date.strftime('%Y-%m-%d')
                except ValueError:
                    # Αν η ημερομηνία δεν είναι σε σωστή μορφή, αγνοείται
                    pass
            writer.writerow(row)

# Χρήση της συνάρτησης
input_file = 'file.csv'
output_file = 'file-out.csv'
transform_date(input_file, output_file)
