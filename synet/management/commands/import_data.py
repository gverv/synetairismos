import csv
from django.core.management.base import BaseCommand
from synet.models import WaterConsumption  

class Command(BaseCommand):
    help = 'Imports data from a CSV file to the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
#        with open(csv_file_path, 'r') as file:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
#            header = next(reader)  # Διάβασε την πρώτη γραμμή για τα headers (προαιρετικά)
            for row in reader:
                # Ανάλογα με τη δομή του CSV σου, αντιστοίχισε τις τιμές στις στήλες του μοντέλου σου
                try:
                    WaterConsumption.objects.create(
                            # serialNumber=row[0],
                            customer=row[1],
                            date=row[2],
                            collecter=row[3],
                            counter=row[4],
                            finalIndication=row[5],
                            initialIndication=row[6],
                            intermediateIndication=row[7] if row[7] else None,
                            cubicMeters=row[8] if row[8] else None,
                            billableCubicMeters=row[9] if row[9] else None,
                            hydronomistsCubicMeters=row[10] if row[10] else None,
                            cost=row[11],
                            hydronomistsRight=row[12] if row[12] else None,
                            paid=row[13] if row[13] else None,
                            paymentDate=row[14] if row[14] else None,
                            receivedBy=row[15],
                            receiptNumber=row[16] if row[16] else None,
                            balance=row[17] if row[17] else None,
                            viberMsg=row[18],
                            notes=row[19],
                            fields=row[20],
                            olivesNumber=row[21] if row[21] else None,
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row: {row} - {e}"))
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))