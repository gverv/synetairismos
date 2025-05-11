from django.db import models

class WaterConsumption(models.Model):
    serialNumber = models.IntegerField(null=True, )
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
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    fathersName = models.CharField(max_length=100, null=True, blank=True)
    afm = models.CharField(max_length=9, null=True, blank=True)
    member = models.BooleanField(default=True) # Είναι μέλος του συνεταιρισμού
    payAsMember = models.BooleanField(default=True) # Πληρώνει σαν μέλος του συνεταιρισμού
    isActive = models.BooleanField(default=False) # Είναι ενεργός στον πολτισμό

    class Meta:
        ordering = ['surname', 'name']
    
    def __str__(self):
        return f"{self.surname} {self.name} {self.fathersName}".strip()  # Αφαιρεί επιπλέον κενά


class Counters(models.Model):
    collecter = models.CharField(max_length=20)
    counter = models.CharField(max_length=20, null=True, blank=True)
    customer = models.ForeignKey(Customers, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['collecter']
        
    def __str__(self):
        return f"{self.collecter} {self.counter} {self.customer}".strip()

class Receivers(models.Model):
    receiver = models.CharField(max_length=30)
    
    def __str__(self):
        return self.receiver
    

class Fields(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    field = models.CharField(max_length=20, null=True, blank=True)
    olivesNumber = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer} {self.field}".strip()  # Αφαιρεί επιπλέον κενά


class WaterCons(models.Model):
    serialNumber = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    counter = models.ForeignKey(Counters, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    finalIndication = models.IntegerField()
    initialIndication = models.IntegerField()
    intermediateIndication = models.IntegerField(null=True, blank=True)
    cubicMeters = models.IntegerField(null=True, blank=True)
    billableCubicMeters = models.IntegerField(null=True, blank=True)
    hydronomistsCubicMeters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costPerMeter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.30)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hydronomistsRight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    viberMsg = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField( null=True,blank=True)
    field = models.ForeignKey(Fields, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.serialNumber:  # Αν δεν έχει ήδη οριστεί το serialNumber
            last_entry = WaterCons.objects.order_by('-serialNumber').first()
            if last_entry:
                self.serialNumber = last_entry.serialNumber + 1
            else:
                self.serialNumber = 1  # Αν δεν υπάρχει προηγούμενη εγγραφή, ξεκινά από το 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.customer} {self.date} {self.billableCubicMeters} {self.cost}".strip()  # Αφαιρεί επιπλέον κενά


class Paids(models.Model):
    # customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    irrigation = models.ForeignKey(WaterCons, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paymentDate = models.DateField(null=True, blank=True)
    receiver = models.ForeignKey(Receivers, on_delete=models.CASCADE, null=True, blank=True)
    receiptNumber = models.IntegerField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.receiptNumber} {self.irrigation} {self.paymentDate} {self.paid}".strip()


