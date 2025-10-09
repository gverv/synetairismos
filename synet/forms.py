# synet/forms.py
import datetime
from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, NumberInput, Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

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
 

class PaidsForm(forms.ModelForm):
    class Meta:
        model = Paids
        fields = [
            'receiptNumber', 'cost', 'paid', 'balance', 'paymentDate', 'receiver',
            'collectorFeeRate', 'collectorFee', 'notes',
            # Αφαιρέστε τα 'irrigation' και 'customer' από τα fields της φόρμας
            # καθώς τα χειρίζεστε χειροκίνητα στο view και στο template.
        ]
        widgets = {
            # ... (widgets) ...
            'notes': forms.Textarea(attrs={'rows': 2, 'style': 'resize: vertical; max-height: 100px; overflow-y: auto;'}),
            'paymentDate': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'collectorFeeRate': forms.NumberInput(attrs={'step': '0.01'}),
            'collectorFee': forms.NumberInput(attrs={'step': '0.01', 'readonly': 'readonly'}), 
        }
        labels = {
            # ... (labels) ...
            'receiptNumber': 'Αρ. Απόδειξης', 'cost': 'Αξία', 'paid': 'Πλήρωσε',
            'balance': 'Ισοζύγιο', 'paymentDate': 'Ημ/νία Πληρωμής', 'receiver': 'Εισπράκτορας',
            'collectorFeeRate': 'Ποσοστό Εισπρ.', 'collectorFee': 'Αμοιβή Εισπρ.', 'notes': 'Σημειώσεις',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['balance'].widget.attrs['readonly'] = 'readonly'
        self.fields['receiptNumber'].widget.attrs['readonly'] = 'readonly'

        self.helper = FormHelper()
        self.helper.form_id = 'receiptForm'
        self.helper.layout = Layout(
            # 1η Σειρά: Αρ. Απόδειξης (6) & Αξία (6) - Χρησιμοποιούμε 'col-6'
            Row(
                Column('receiptNumber', css_class='form-group col-6 mb-0'),
                Column('cost', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            # 2η Σειρά: Πλήρωσε (6) & Ισοζύγιο (6) - Χρησιμοποιούμε 'col-6'
            Row(
                Column('paid', css_class='form-group col-6 mb-0'),
                Column('balance', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            # 3η Σειρά: Ημ/νία Πληρωμής (4) & Εισπράκτορας (8) - Χρησιμοποιούμε 'col-4' & 'col-8'
            Row(
                Column('paymentDate', css_class='form-group col-4 mb-0'),
                Column('receiver', css_class='form-group col-8 mb-0'),
                css_class='form-row'
            ),
            # 4η Σειρά: Ποσοστό Εισπρ. (6) & Αμοιβή Εισπρ. (6) - Χρησιμοποιούμε 'col-6'
            Row(
                Column('collectorFeeRate', css_class='form-group col-6 mb-0'),
                Column('collectorFee', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            # 5η Σειρά: Σημειώσεις (12)
            'notes',
        )
        # 3. Αρχικές τιμές για create (μόνο αν δεν υπάρχουν)        
        if self.instance.pk is None:
            self.fields['paid'].initial = self.fields['paid'].initial or 0
            self.fields['balance'].initial = self.fields['balance'].initial or 0
        
        # 4. Αρχικές τιμές για update (μόνο αν δεν υπάρχουν)
        # self.fields['collectorFeeRate'].initial = self.fields['collectorFeeRate'].initial or 0.06
        