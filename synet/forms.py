import datetime
from datetime import date
from django import forms
from synet.models import  Persons, Counters, Paids, Fields, WaterCons, Receivers
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, NumberInput, Select

class WaterConsForm(ModelForm):
    class Meta:
        model = WaterCons
        # fields = '__all__'
        fields = [
            'date', 
            'counter', 
            'customer', 
            'finalIndication', 
            'initialIndication', 
            'cubicMeters', 
            'billableCubicMeters', 
            'hydronomistsCubicMeters', 
            'costPerMeter',
            'cost', 
            'hydronomistsRight', 
            'viberMsg',
            # 'receipt'
            ]
        labels = {
         'date': 'Ημ/νία',
         'counter': "Μετρητής",
         'customer': "Καταναλωτής",
         'finalIndication': "Τελική",
         'initialIndication': "Αρχική",
         'cubicMeters': "Κυβικά",
         'billableCubicMeters': "Χρεώσιμα",
         'hydronomistsCubicMeters': "ΥδρΚυβικά",
         'costPerMeter': 'ΑνάΚυβικό',
         'cost': "Κόστος",
         'hydronomistsRight': "ΔικΥδρον",
         'viberMsg': "Μήνυμα",
         'notes': "Σημειώσεις",
         'field': "Χωράφι",
         'receipt': "Απόδειξη"
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = forms.DateField().widget.attrs['value'] = date.today().strftime("%Y-%m-%d")
                
    # def save(self, *args, **kwargs):
    #     if self.initialIndication is not None and self.finalIndication is not None:
    #         difference = self.finalIndication - self.initialIndication
    #         self.cubicMeters = difference
    #         self.billableCubicMeters = difference
    #         self.hydronomistsCubicMeters = difference

    #     if self.billableCubicMeters is not None:
    #         self.cost = self.billableCubicMeters * 0.30  # Χρήση του default costPerMeter
    #         self.hydronomistsRight = self.hydronomistsCubicMeters * 0.05

    #     self.viberMsg = f"{self.customer}, {self.date}, {self.finalIndication} - {self.initialIndication} = {self.cost}"

    #     super().save(*args, **kwargs)
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        
# class CustomerForm(ModelForm):
#     class Meta:
#         model = Customers
#         fields = '__all__'
#         widgets = {
#             'surname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Customer Name'}),
#             'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Customer Name'}),
#             'fathersName': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Customer Name'}),
#             'afm': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Customer Name'}),
#             'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Customer Name'}),
#         }        

class PersonsForm(forms.ModelForm):
    class Meta:
        model = Persons
        fields = '__all__'
        # fields = ['surname', 'name', 'fathersName', 'afm', 'member', 'payAsMember']
        labels = {
            'surname': 'Επώνυμο',
            'name': 'Όνομα',
            'fathersName': 'Πατρώνυμο',
            'afm': 'ΑΦΜ',
            'phone': 'Τηλέφωνο',
            'member': 'Μέλος',
            'payAsMember': 'Πληρωμή ως μέλος',
            'isActive': 'Ενεργός',
            'aa': 'Α/Α μέλους',
            'placeOfResidence': 'Κατοικία',
            'Notes': 'Σημειώσεις',
        }
        
class CountersForm(forms.ModelForm):
    class Meta:
        model = Counters
        fields = ['customer', 'collecter', 'counter']
        labels = {
            'customer': 'Καταναλωτης',
            'collecter': 'Κολεκτέρ',
            'counter': 'Μετρητής',
        }        
 


class PaidsForm(forms.ModelForm):
    class Meta:
        model = Paids
        fields = '__all__'
        labels = {
            'irrigation': 'Ποτισμός',
            'customer': 'Καταναλωτης',
            'cost': 'Αξία',
            'paid': 'Πλήρωσε',
            'paymentDate': 'Ημ/νίαΠληρωμής',
            'receiver': 'Εισπράκτορας',
            'receiptNumber': 'ΑρΑπόδειξης',
            'balance': 'Ισοζύγιο',
        }        

