from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Counters, Persons, WaterCons, Fields, Paids
from .forms import WaterConsForm, UserForm, PersonsForm, CountersForm, PaidsForm
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum

def report_view(request):
    # Φιλτράρουμε τα άτομα που έχουν υπόλοιπο διαφορετικό από 0
    persons = Persons.objects.filter(paids__balance__isnull=False).distinct()
    
    report_data = []
    for person in persons:
        payments = Paids.objects.filter(customer=person).exclude(balance=0)
        total_balance = payments.aggregate(total=Sum('balance'))['total'] or 0
        report_data.append({
            'surname': person.surname,
            'name': person.name,
            'fathersName': person.fathersName,
            'payments': payments,
            'total_balance': total_balance
        })

    return render(request, 'report.html', {'report_data': report_data})

def get_last_final_indication(request, counter_id):
    last_entry = WaterCons.objects.filter(counter_id=counter_id).order_by('-date').first()
    if last_entry:
        return JsonResponse({'finalIndication': last_entry.finalIndication})
    return JsonResponse({'finalIndication': None})

def index(request):
    sort_by = request.GET.get('sort', '-id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = WaterCons.objects.all().order_by(sort_by)    
    total_cost = WaterCons.objects.all().aggregate(Sum('cost'))['cost__sum']
    total_hydronomists = WaterCons.objects.all().aggregate(Sum('hydronomistsRight'))['hydronomistsRight__sum']
    total_cubic = WaterCons.objects.all().aggregate(Sum('cubicMeters'))['cubicMeters__sum']
    total_billable = WaterCons.objects.all().aggregate(Sum('billableCubicMeters'))['billableCubicMeters__sum']
    total_paid = Paids.objects.all().aggregate(Sum('paid'))['paid__sum']
    debt = total_cost - total_paid
    context = {
        'data': data, 
        'order': 'asc' if order == 'desc' else 'desc',
        'total_cost': total_cost,
        'total_cubic': total_cubic,
        'total_billable': total_billable,
        'total_hydronomists': total_hydronomists,
        'total_paid': total_paid,
        'debt': debt,
        }
    return render(request, 'index.html', context)

def customerIrrigations(request, customer_id):
    sort_by = request.GET.get('sort', '-id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = WaterCons.objects.all().filter(customer_id=customer_id).order_by(sort_by)    
    customerPaids = Paids.objects.all().filter(customer=customer_id).order_by(sort_by)    
    customer = Persons.customers().filter(id=customer_id).first()
    total_cost = WaterCons.objects.filter(customer_id=customer_id).aggregate(Sum('cost'))['cost__sum']
    total_cubic = WaterCons.objects.filter(customer_id=customer_id).aggregate(Sum('cubicMeters'))['cubicMeters__sum']
    total_billable = WaterCons.objects.filter(customer_id=customer_id).aggregate(Sum('billableCubicMeters'))['billableCubicMeters__sum']
    total_paid = Paids.objects.filter(customer=customer_id).aggregate(Sum('paid'))['paid__sum']
    debt = total_cost - total_paid
    context = {
        'data': data, 
        'order': 'asc' if order == 'desc' else 'desc', 
        'customer': customer, 
        'total_cost': total_cost,
        'total_cubic': total_cubic,
        'total_billable': total_billable,
        'customerPaids': customerPaids,
        'total_paid': total_paid,
        'debt': debt,
        }
    return render(request, 'customerIrrigations.html', context)

def about(request):
    return render(request, 'about.html')

def customers(request):
    sort_by = request.GET.get('sort', 'surname')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = Persons.customers().order_by(sort_by)    
    context = {'data': data, 'order': 'asc' if order == 'desc' else 'desc'}
    return render(request, 'customers.html', context)


class PersonsUpdateView(UpdateView):
    model = Persons
    form_class = PersonsForm
    template_name = 'persons_update.html'
    success_url = reverse_lazy('customers')

def counters(request):
    sort_by = request.GET.get('sort', 'collecter')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = Counters.objects.all().order_by(sort_by)    
    context = {'data': data, 'order': 'asc' if order == 'desc' else 'desc'}
    return render(request, 'counters.html', context)

class CountersUpdateView(UpdateView):
    model = Counters
    form_class = CountersForm
    template_name = 'counters_update.html'  # Το όνομα του template
    success_url = reverse_lazy('counters')  # Ανακατεύθυνση μετά την ενημέρωση


def paids(request):
    sort_by = request.GET.get('sort', '-receiptNumber')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = Paids.objects.all().order_by(sort_by)    
    context = {'data': data, 'order': 'asc' if order == 'desc' else 'desc'}
    return render(request, 'paids.html', context)

class PaidsUpdateView(UpdateView):
    model = Paids
    form_class = PaidsForm
    template_name = 'paids_update.html'  # Το όνομα του template
    success_url = reverse_lazy('paids')  # Ανακατεύθυνση μετά την ενημέρωση

def paids_update(request, id):
    paid = get_object_or_404(Paids, id=id)
    if request.method == "POST":
        form = PaidsForm(request.POST, instance=paid)
        if form.is_valid():
            form.save()
            # return redirect('paids')
            return redirect('index')
    else:
        form = PaidsForm(instance=paid)
    return render(request, 'paids_update.html', {'form': form})

class WaterConsCreateView(CreateView):
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'add_irrigation.html'
    success_url = reverse_lazy('index')  # Ανακατεύθυνση μετά την προσθήκη

class WaterConsUpdateView(UpdateView):
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'update_irrigation.html'
    success_url = reverse_lazy('index')  # Ανακατεύθυνση μετά την ενημέρωση
    
def addPayFromIrrigation(request, irrigation_id):
    irrigation = WaterCons.objects.filter(id=irrigation_id).first()
    context = { 'irrigation': irrigation }
    return render(request, 'addPayFromIrrigation.html', context)


def create_payment(request, irrigation_id):
    irrigation = get_object_or_404(WaterCons, id=irrigation_id)

    # Βρίσκουμε το τελευταίο receiptNumber και υπολογίζουμε το επόμενο
    last_receipt = Paids.objects.order_by('-receiptNumber').first()
    next_receipt_number = (last_receipt.receiptNumber + 1) if last_receipt else 1

    if request.method == 'POST':
        form = PaidsForm(request.POST)
        if form.is_valid():
            # Δημιουργούμε νέο `Paids`
            payment = form.save(commit=False)
            payment.irrigation = irrigation
            payment.customer = irrigation.customer
            payment.cost = irrigation.cost
            payment.paid = form.cleaned_data['paid'] or 0
            payment.paymentDate = form.cleaned_data['paymentDate']
            payment.receiver = form.cleaned_data['receiver']
            # payment.receiptNumber = next_receipt_number
            payment.receiptNumber = form.cleaned_data['receiptNumber']
            
            payment.save()

            # Ενημερώνουμε το `receipt` στο `WaterCons`
            irrigation.receipt = payment
            irrigation.save()

            return redirect('index')
            # return redirect('paids')

    else:
        # Προσυμπληρωμένες τιμές στη φόρμα
        form = PaidsForm(initial={
            'irrigation': irrigation.id,
            'customer': irrigation.customer,
            'cost': irrigation.cost,
            'paid': 0,
            'paymentDate': None,
            'receiver': None,
            'receiptNumber': next_receipt_number,
            'balance': -irrigation.cost,
        })
        context = {'form': form, 'irrigation': irrigation}

    return render(request, 'create_payment.html', context)


def update_irrigation(request, irrigation_id):
    waterCons = get_object_or_404(WaterCons, id=irrigation_id)
    form = WaterConsForm(instance=waterCons)
    return render(request, 'update_irrigation.html', {'form': form, 'waterCons': waterCons})


def counter_detail(request, pk):
    counter = get_object_or_404(Counters, pk=pk)
    consumptions = WaterCons.objects.filter(counter=counter).order_by('-date', '-finalIndication')
    return render(request, 'counter_detail.html', {
        'counter': counter,
        'consumptions': consumptions
    })
    