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
        ]
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 2,
                'style': 'resize: vertical; max-height: 100px; overflow-y: auto;'
            }),
            'paymentDate': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'collectorFeeRate': forms.NumberInput(attrs={'step': '0.01'}),
            'collectorFee': forms.NumberInput(attrs={'step': '0.01', 'readonly': 'readonly'}), 
        }
        labels = {
            'receiptNumber': 'Αρ. Απόδειξης', 'cost': 'Αξία', 'paid': 'Πλήρωσε',
            'balance': 'Ισοζύγιο', 'paymentDate': 'Ημ/νία Πληρωμής', 'receiver': 'Εισπράκτορας',
            'collectorFeeRate': 'Ποσοστό Εισπρ.', 'collectorFee': 'Αμοιβή Εισπρ.', 'notes': 'Σημειώσεις',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['receiver'] = forms.ModelChoiceField(
            queryset=Receivers.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=False,
            empty_label="Επιλέξτε εισπράκτορα"
        )

        self.fields['balance'].widget.attrs['readonly'] = 'readonly'
        self.fields['receiptNumber'].widget.attrs['readonly'] = 'readonly'

        self.helper = FormHelper()
        self.helper.form_id = 'receiptForm'
        self.helper.layout = Layout(
            Row(
                Column('receiptNumber', css_class='form-group col-6 mb-0'),
                Column('cost', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('paid', css_class='form-group col-6 mb-0'),
                Column('balance', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('paymentDate', css_class='form-group col-4 mb-0'),
                Column('receiver', css_class='form-group col-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('collectorFeeRate', css_class='form-group col-6 mb-0'),
                Column('collectorFee', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            'notes',
        )

        if self.instance.pk is None:
            self.fields['paid'].initial = self.fields['paid'].initial or 0
            self.fields['balance'].initial = self.fields['balance'].initial or 0
        # 4. Αρχικές τιμές για update (μόνο αν δεν υπάρχουν)
        # self.fields['collectorFeeRate'].initial = self.fields['collectorFeeRate'].initial or 0.06
        