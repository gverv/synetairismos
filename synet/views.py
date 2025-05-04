from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Counters, Customers, WaterCons, Fields, Paids
from .forms import WaterConsForm, UserForm, CustomersForm, CountersForm, PaidsForm
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse

def get_last_final_indication(request, counter_id):
    last_entry = WaterCons.objects.filter(counter_id=counter_id).order_by('-date').first()
    if last_entry:
        return JsonResponse({'finalIndication': last_entry.finalIndication})
    return JsonResponse({'finalIndication': None})

def index(request):
    sort_by = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = WaterCons.objects.all().order_by(sort_by)    
    context = {'data': data, 'order': 'asc' if order == 'desc' else 'desc'}
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def customers(request):
    sort_by = request.GET.get('sort', 'surname')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'  # Προσθέτει "-" για φθίνουσα ταξινόμηση
    data = Customers.objects.all().order_by(sort_by)    
    context = {'data': data, 'order': 'asc' if order == 'desc' else 'desc'}
    return render(request, 'customers.html', context)


class CustomersUpdateView(UpdateView):
    model = Customers
    form_class = CustomersForm
    template_name = 'customers_update.html'  # Το όνομα του template
    success_url = reverse_lazy('customers')  # Ανακατεύθυνση μετά την ενημέρωση

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
    sort_by = request.GET.get('sort', 'receiptNumber')
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