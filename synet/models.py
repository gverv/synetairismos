from django.db import models

class WaterConsumption(models.Model):
    serialNumber = models.IntegerField(null=True)
    customer = models.CharField(max_length=100)
    date = models.DateField()
    collecter = models.CharField(max_length=20, null=True)
    counter = models.CharField(max_length=20, null=True)
    finalIndication = models.IntegerField()
    initialIndication = models.IntegerField()
    intermediateIndication = models.IntegerField(null=True, blank=True)
    cubicMeters = models.IntegerField(null=True, blank=True)
    billableCubicMeters = models.IntegerField(null=True, blank=True)
    hydronomistsCubicMeters = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hydronomistsRight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paymentDate = models.DateField(null=True)
    receivedBy = models.CharField(max_length=10, null=True)
    receiptNumber = models.IntegerField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    viberMsg = models.CharField(max_length=200, null=True)
    notes = models.TextField(null=True)
    fields = models.CharField(max_length=20, null=True)
    olivesNumber = models.IntegerField(null=True, blank=True)  #
    
    def __str__(self):
        return self.viberMsg


class Customers(models.Model):
    customer = models.CharField(max_length=100)

    def __str__(self):
        return self.customer


class Counters(models.Model):
    collecter = models.CharField(max_length=20, null=True)
    counter = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.counter


class Paids(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paymentDate = models.DateField(null=True)
    receivedBy = models.CharField(max_length=10, null=True)
    receiptNumber = models.IntegerField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class Fields(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    field = models.CharField(max_length=20, null=True)
    olivesNumber = models.IntegerField(null=True, blank=True)


class WaterCons(models.Model):
    serialNumber = models.IntegerField(null=True)
    date = models.DateField()
    finalIndication = models.IntegerField()
    initialIndication = models.IntegerField()
    intermediateIndication = models.IntegerField(null=True, blank=True)
    cubicMeters = models.IntegerField(null=True, blank=True)
    billableCubicMeters = models.IntegerField(null=True, blank=True)
    hydronomistsCubicMeters = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hydronomistsRight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    viberMsg = models.CharField(max_length=200, null=True)
    notes = models.TextField(null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    counter = models.ForeignKey(Counters, on_delete=models.CASCADE)
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
