from synet.models import WaterConsumption, Customers, Counters, Paids, Fields, WaterCons

# Δημιουργία πελατών
for obj in WaterConsumption.objects.all():
    customer, created = Customers.objects.get_or_create(customer=obj.customer)
    counter, created = Counters.objects.get_or_create(collecter=obj.collecter, counter=obj.counter)
    field, created = Fields.objects.get_or_create(customer=customer, field=obj.fields, olivesNumber=obj.olivesNumber)
    # Μεταφορά δεδομένων σε WaterCons
    WaterCons.objects.create(
        serialNumber=obj.serialNumber,
        date=obj.date,
        finalIndication=obj.finalIndication,
        initialIndication=obj.initialIndication,
        intermediateIndication=obj.intermediateIndication,
        cubicMeters=obj.cubicMeters,
        billableCubicMeters=obj.billableCubicMeters,
        hydronomistsCubicMeters=obj.hydronomistsCubicMeters,
        cost=obj.cost,
        hydronomistsRight=obj.hydronomistsRight,
        viberMsg=obj.viberMsg,
        notes=obj.notes,
        customer=customer,
        counter=counter,
        field=field
    )
