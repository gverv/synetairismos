import datetime
from datetime import date
from django import forms
from synet.models import  Customers, Counters, Paids, Fields, WaterCons, Receivers
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, NumberInput, Select

class WaterConsForm(ModelForm):
    costPerMeter = forms.DecimalField(
        max_digits=5, decimal_places=2, initial=0.30, label="Κόστος ανά κυβικό"
    )
    class Meta:
        model = WaterCons
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
            'viberMsg'
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
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['date'].initial = forms.DateField().widget.attrs['value'] = forms.DateField().widget.format_value(forms.DateField().to_python('today'))
        self.fields['date'].initial = forms.DateField().widget.attrs['value'] = date.today().strftime("%Y-%m-%d")
        # self.fields['counter'].initial = Counters.objects.get(id=1)  # Προτείνει τον μετρητή με id=1
                
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

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['surname', 'name', 'fathersName', 'afm', 'member', 'payAsMember']
        labels = {
            'surname': 'Επώνυμο',
            'name': 'Όνομα',
            'fathersName': 'Πατρώνυμο',
            'afm': 'ΑΦΜ',
            'member': 'Μέλος',
            'payAsMember': 'Πληρωμή ως μέλος',
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
            # 'customer': 'Καταναλωτης',
            'irrigation': 'Ποτισμός',
            'paid': 'Πλήρωσε',
            'paymentDate': 'Ημ/νίαΠληρωμής',
            'receiver': 'Εισπράκτορας',
            'receiptNumber': 'ΑρΑπόδειξης',
            'balance': 'Ισοζύγιο',
        }        

