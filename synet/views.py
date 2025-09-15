from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import UpdateView, CreateView
from django.core.paginator import Paginator

from .models import Counters, Persons, WaterCons, Fields, Paids, Parametroi
from .forms import WaterConsForm, UserForm, PersonsForm, CountersForm, PaidsForm

def get_sort_params(request, default='-id'):
    sort_by = request.GET.get('sort', default)
    order = request.GET.get('order', 'asc')
    if order == 'desc' and not sort_by.startswith('-'):
        sort_by = f'-{sort_by}'
    elif order == 'asc' and sort_by.startswith('-'):
        sort_by = sort_by[1:]
    return sort_by, 'asc' if order == 'desc' else 'desc'

def report_view(request):
    person_ids = request.GET.get('persons', '')
    if person_ids:
        ids = [int(i) for i in person_ids.split(',')]
        persons = Persons.objects.filter(id__in=ids)
    else:
        persons = Persons.objects.none()
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
    # Υπολογισμός συνολικού υπολοίπου για όλα τα άτομα
    grand_total_balance = sum(item['total_balance'] for item in report_data)
    return render(request, 'report.html', {
        'report_data': report_data,
        'grand_total_balance': grand_total_balance
    })

def get_last_final_indication(request, counter_id):
    last_entry = WaterCons.objects.filter(counter_id=counter_id).order_by('-date', '-id').first()
    return JsonResponse({'finalIndication': getattr(last_entry, 'finalIndication', None)})

def index(request):
    # Θέλουμε πάντα φθίνουσα ταξινόμηση κατά id (τα τελευταία πρώτα)
    sort_by, order = get_sort_params(request, default='id')
    if sort_by == 'id' and order == 'asc':
        sort_by = '-id'
    elif sort_by == 'id' and order == 'desc':
        sort_by = '-id'
    all_data = WaterCons.objects.all().order_by(sort_by)
    paginator = Paginator(all_data, 50)  # 50 ανά σελίδα
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    aggregates = WaterCons.objects.aggregate(
        total_cost=Sum('cost'),
        total_hydronomists=Sum('hydronomistsRight'),
        total_cubic=Sum('cubicMeters'),
        total_billable=Sum('billableCubicMeters')
    )
    total_paid = Paids.objects.aggregate(total_paid=Sum('paid'))['total_paid'] or 0
    debt = (aggregates['total_cost'] or 0) - total_paid
    context = {
        'page_obj': page_obj,
        'order': order,
        **aggregates,
        'total_paid': total_paid,
        'debt': debt,
    }
    return render(request, 'index.html', context)

def customerIrrigations(request, customer_id):
    # Dynamic sorting for irrigations (data)
    data_sort = request.GET.get('sort', 'id')
    data_order = request.GET.get('order', 'desc')
    data_sort_by = f'-{data_sort}' if data_order == 'desc' else data_sort
    data = WaterCons.objects.filter(customer_id=customer_id).order_by(data_sort_by)

    # Dynamic sorting for payments (customerPaids)
    paids_sort = request.GET.get('paids_sort', 'receiptNumber')
    paids_order = request.GET.get('paids_order', 'desc')
    paids_sort_by = f'-{paids_sort}' if paids_order == 'desc' else paids_sort
    customerPaids = Paids.objects.filter(customer=customer_id).order_by(paids_sort_by)
    customer = get_object_or_404(Persons, id=customer_id)
    aggregates = WaterCons.objects.filter(customer_id=customer_id).aggregate(
        total_cost=Sum('cost'),
        total_cubic=Sum('cubicMeters'),
        total_billable=Sum('billableCubicMeters')
    )
    total_paid = Paids.objects.filter(customer=customer_id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0
    debt = (aggregates['total_cost'] or 0) - total_paid
    context = {
        'data': data,
        'order': data_order,
        'customer': customer,
        **aggregates,
        'customerPaids': customerPaids,
        'total_paid': total_paid,
        'debt': debt,
        'paids_order': paids_order,
    }
    return render(request, 'customerIrrigations.html', context)

def about(request):
    return render(request, 'about.html')

def customers(request):
    sort_by, order = get_sort_params(request, default='surname')
    data = Persons.customers().order_by(sort_by)
    return render(request, 'customers.html', {'data': data, 'order': order})

class PersonsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_model'
    model = Persons
    form_class = PersonsForm
    template_name = 'persons_update.html'
    success_url = reverse_lazy('customers')

def counters(request):
    sort_by, order = get_sort_params(request, default='collecter')
    data = Counters.objects.all().order_by(sort_by)
    return render(request, 'counters.html', {'data': data, 'order': order})

class CountersUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_model'
    model = Counters
    form_class = CountersForm
    template_name = 'counters_update.html'
    success_url = reverse_lazy('counters')

def paids(request):
    sort_by = request.GET.get('sort', 'receiptNumber')
    order = request.GET.get('order', 'desc')
    sort_field = f'-{sort_by}' if order == 'desc' else sort_by
    all_param = request.GET.get('all')
    all_data = Paids.objects.all().order_by(sort_field)
    if all_param == '1':
        # Επιστρέφει όλες τις εγγραφές χωρίς σελιδοποίηση
        page_obj = all_data
    else:
        paginator = Paginator(all_data, 14)  # 14 ανά σελίδα
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
    return render(request, 'paids.html', {
        # 'data': all_data,
        'page_obj': page_obj,
        'order': order,
        'sort_by': sort_by
    })

class PaidsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_model'
    model = Paids
    form_class = PaidsForm
    template_name = 'paids_update.html'
    success_url = reverse_lazy('paids')

@permission_required('synet.change_model', raise_exception=True)
def paids_update(request, id):
    paid = get_object_or_404(Paids, id=id)
    # Πάρε τα query params για να τα χρησιμοποιήσεις στο redirect
    page = request.GET.get('page', '')
    sort = request.GET.get('sort', '')
    order = request.GET.get('order', '')
    query_string = ''
    if page or sort or order:
        params = []
        if page:
            params.append(f'page={page}')
        if sort:
            params.append(f'sort={sort}')
        if order:
            params.append(f'order={order}')
        query_string = '?' + '&'.join(params)

    if request.method == "POST":
        form = PaidsForm(request.POST, instance=paid)
        if form.is_valid():
            form.save()
            return redirect('/paids/' + query_string)
    else:
        form = PaidsForm(instance=paid)
    return render(request, 'paids_update.html', {'form': form})

class WaterConsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'synet.add_watercons'
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'add_irrigation.html'
    success_url = reverse_lazy('index')

class WaterConsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_watercons'
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'update_irrigation.html'
    success_url = reverse_lazy('index')

def addPayFromIrrigation(request, irrigation_id):
    irrigation = get_object_or_404(WaterCons, id=irrigation_id)
    return render(request, 'addPayFromIrrigation.html', {'irrigation': irrigation})

@permission_required('synet.change_paids', raise_exception=True)
def create_payment(request, irrigation_id):
    irrigation = get_object_or_404(WaterCons, id=irrigation_id)
    last_receipt = Paids.objects.order_by('-receiptNumber').first()
    next_receipt_number = (last_receipt.receiptNumber + 1) if last_receipt else 1

    if request.method == 'POST':
        form = PaidsForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.irrigation = irrigation
            payment.customer = irrigation.customer
            payment.cost = irrigation.cost
            payment.paid = form.cleaned_data['paid'] or 0
            payment.paymentDate = form.cleaned_data['paymentDate']
            payment.receiver = form.cleaned_data['receiver']
            payment.receiptNumber = form.cleaned_data['receiptNumber']
            payment.save()
            irrigation.receipt = payment
            irrigation.save()
            return redirect('index')
    else:
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
    return render(request, 'create_payment.html', {'form': form, 'irrigation': irrigation})

@permission_required('synet.change_model', raise_exception=True)
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

def global_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results += search_model(Persons, ['surname', 'name', 'fathersName', 'afm', 'phone', 'notes'], query, 'Πελάτες')
        results += search_model(Counters, ['collecter', 'counter'], query, 'Μετρητές')
        results += search_model(WaterCons, ['viberMsg', 'notes'], query, 'Ποτίσματα')
        results += search_model(Paids, ['receiptNumber'], query, 'Αποδείξεις')
        results += search_model(Fields, ['field'], query, 'Χωράφια')
    return render(request, 'search_results.html', {'results': results, 'query': query})

def search_model(model, fields, query, model_name):
    q = Q()
    for field in fields:
        q |= Q(**{f"{field}__icontains": query})
    found = []
    for obj in model.objects.filter(q):
        for field in fields:
            value = getattr(obj, field, '')
            if query.lower() in str(value).lower():
                url = get_object_url(obj)
                found.append({
                    'model': model_name,
                    'field': field,
                    'value': value,
                    'id': obj.id,
                    'string': str(obj),
                    'url': url,
                })
    return found

def get_object_url(obj):
    try:
        return reverse(f"{obj._meta.model_name}_detail", args=[obj.id])
    except:
        return None


def select_persons_for_report(request):
    persons = Persons.objects.filter(isActive=True)
    if request.method == 'POST':
        selected = request.POST.getlist('persons')
        if 'all' in selected:
            selected = [str(p.id) for p in persons]
        return redirect(f"/report/?persons={','.join(selected)}")
    return render(request, 'select_persons.html', {'persons': persons})


def get_param(param_name, default=None):
    try:
        return Parametroi.objects.get(param=param_name).value
    except Parametroi.DoesNotExist:
        return default