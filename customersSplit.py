from synet.models import Customers 

for customer in Customers.objects.all():
    parts = customer.customer.split()  # Διαχωρισμός με βάση τα κενά
    if len(parts) > 0:
        customer.surname = parts[0]  # Το πρώτο κομμάτι στο surname
    if len(parts) > 1:
        customer.name = parts[1]  # Το δεύτερο κομμάτι στο name
    if len(parts) > 2:
        customer.fathersName = parts[2]  # Το τρίτο κομμάτι στο fathersName
    customer.save()  # Αποθήκευση αλλαγών
