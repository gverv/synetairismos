# forms.py
import datetime
from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, NumberInput, Select

from .models import  Persons, Counters, Paids, Fields, WaterCons, Receivers

class WaterConsForm(ModelForm):
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
            'ydronomistFee',
            'costPerMeter',
            'cost', 
            'hydronomistsRight', 
            'msg',
        ]
        labels = {
         'date': 'Ημ/νία',
         'counter': "Μετρητής",
         'customer': "Καταναλωτής",
         'finalIndication': "Τελική",
         'initialIndication': "Αρχική",
         'cubicMeters': "Κυβικά",
         'billableCubicMeters': "Χρεώσιμα",
         'ydronomistFee': "Ανά κυβικό στον Υδρονομέα",  # <-- Διόρθωση εδώ
         'costPerMeter': 'ΑνάΚυβικό',
         'cost': "Κόστος",
         'hydronomistsRight': "Δικαίωμα Υδρονομέα",
         'msg': "Μήνυμα",
        #  'notes': "Σημειώσεις",
        #  'field': "Χωράφι",
        #  'receipt': "Απόδειξη"
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = forms.DateField().widget.attrs['value'] = date.today().strftime("%Y-%m-%d")
                
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        
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
        fields = ['customer', 'collecter', 'counter', 'lastIndication']
        widgets = {
            'customer': forms.TextInput(attrs={'readonly': 'readonly'}),
            # ...άλλα widgets...
        }
        labels = {
            'customer': 'Καταναλωτης',
            'collecter': 'Κολεκτέρ',
            'counter': 'Μετρητής',
            'lastIndication': 'Τελευταία Ένδειξη',
        }        
 


# class PaidsForm(forms.ModelForm):
#     class Meta:
#         model = Paids
#         fields = [
#             'receiptNumber',  # Αρ Απόδειξης
#             'cost',  # Αξία
#             'paid',  # Πλήρωσε
#             'balance',  # Ισοζύγιο
#             'paymentDate',  # Ημ/νία Πληρωμής
#             'receiver',  # Εισπράκτορας
#             'collectorFeeRate',  # Ποσοστό Εισπράκτορα
#             'collectorFee',  # Αμοιβή Εισπράκτορα
#             'notes',
#             'irrigation',  # Ποτισμός
#             'customer',  # Καταναλωτής
#         ]
#         # widgets = {
#         #     'notes': forms.Textarea(attrs={"rows": 2}),
#         #     'paymentDate': forms.DateInput(attrs={"type": "date"}),
#         #     'irrigation': forms.TextInput(attrs={'readonly': 'readonly'}),
#         #     'customer': forms.TextInput(attrs={'readonly': 'readonly'}),
#         #     'collectorFeeRate': forms.NumberInput(attrs={'step': '0.01'}),
#         #     'collectorFee': forms.NumberInput(attrs={'step': '0.01'}),
#         # }
#         labels = {
#             'receiptNumber': 'Αρ Απόδειξης',
#             'cost': 'Αξία',
#             'paid': 'Πλήρωσε',
#             'balance': 'Ισοζύγιο',
#             'paymentDate': 'Ημ/νία Πληρωμής',
#             'receiver': 'Εισπράκτορας',
#             'irrigation': 'Ποτισμός',
#             'customer': 'Καταναλωτής',
#             'collectorFeeRate': 'Ποσοστό Εισπράκτορα',
#             'collectorFee': 'Αμοιβή Εισπράκτορα',
#             'notes': 'Σημειώσεις',
#         }

#     def __init__(self, *args, **kwargs):
#         # Πιάσε το watercons από τα kwargs
#         watercons = kwargs.pop("watercons", None)
#         super().__init__(*args, **kwargs)

#         if watercons:
#             self.fields["customer"].initial = str(watercons.customer)
#             # self.fields["cubicMeters"].initial = watercons.cubicMeters
#             # self.fields["cost_display"].initial = watercons.cost

class PaidsForm(forms.ModelForm):
    class Meta:
        model = Paids
        fields = [
            'receiptNumber',  # Αρ Απόδειξης
            'cost',  # Αξία
            'paid',  # Πλήρωσε
            'balance',  # Ισοζύγιο
            'paymentDate',  # Ημ/νία Πληρωμής
            'receiver',  # Εισπράκτορας
            'collectorFeeRate',  # Ποσοστό Εισπράκτορα
            'collectorFee',  # Αμοιβή Εισπράκτορα
            'notes',
            # 'irrigation',  # Ποτισμός
            # 'customer',  # Καταναλωτής
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'paymentDate': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            # 'paymentDate': forms.DateInput(attrs={'type': 'date'}),
            # 'irrigation': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'customer': forms.TextInput(attrs={'readonly': 'readonly'}),
            'collectorFeeRate': forms.NumberInput(attrs={'step': '0.01'}),
            'collectorFee': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'receiptNumber': 'Αρ Απόδειξης',
            'cost': 'Αξία',
            'paid': 'Πλήρωσε',
            'balance': 'Ισοζύγιο',
            'paymentDate': 'Ημ/νία Πληρωμής',
            'receiver': 'Εισπράκτορας',
            'irrigation': 'Ποτισμός',
            'customer': 'Καταναλωτής',
            'collectorFeeRate': 'Ποσοστό Εισπράκτορα',
            'collectorFee': 'Αμοιβή Εισπράκτορα',
            'notes': 'Σημειώσεις',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Βάλε default τιμές ή readonly ρυθμίσεις αν χρειάζεται
        self.fields['paid'].initial = self.fields['paid'].initial or 0
        self.fields['balance'].initial = self.fields['balance'].initial or 0
    #     self.fields['paymentDate'].initial = date.today().strftime("%Y-%m-%d")
        # self.fields['paymentDate'].initial = forms.DateField().widget.attrs['value'] = date.today().strftime("%Y-%m-%d")
        # self.fields['collectorFeeRate'].initial = self.fields['collectorFeeRate'].initial or