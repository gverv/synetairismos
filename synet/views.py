# synet\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import UpdateView, CreateView, ListView
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from .models import Counters, Persons, WaterCons, Paids, Parametroi, Fields
from .forms import WaterConsForm, PersonsForm, CountersForm, PaidsForm
from .utils import send_sms


def get_sort_params(request, default='-id'):
    sort_by = request.GET.get('sort', default)
    order = request.GET.get('order', 'asc')  # ή 'desc' αν θέλεις default φθίνουσα
    if order == 'desc' and not sort_by.startswith('-'):
        sort_by = f'-{sort_by}'
    elif order == 'asc' and sort_by.startswith('-'):
        sort_by = sort_by[1:]
    return sort_by, 'asc' if order == 'desc' else 'desc'


# ---------------------------
# INDEX
# ---------------------------
def index(request):
    sort_by, order = get_sort_params(request, default='-id')  # default φθίνουσα id
    all_mode = request.GET.get('all') == '1'
    # queryset = WaterCons.objects.all().order_by(sort_by)
    queryset = WaterCons.objects.all().order_by('-id')  # Πάντα φθίνουσα id

    aggregates = WaterCons.objects.aggregate(
        total_cost=Sum('cost'),
        total_hydronomists=Sum('hydronomistsRight'),
        total_cubic=Sum('cubicMeters'),
        total_billable=Sum('billableCubicMeters')
    )
    total_paid = Paids.objects.aggregate(total_paid=Sum('paid'))['total_paid'] or 0
    debt = (aggregates['total_cost'] or 0) - total_paid

    if all_mode:
        page_obj = None
        objects = queryset  # Όλες οι εγγραφές με φθίνουσα id
    else:
        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        objects = page_obj.object_list

    return render(request, 'index.html', {
        'objects': objects,
        'page_obj': page_obj,
        'order': order,
        'sort_by': sort_by,
        **aggregates,
        'total_paid': total_paid,
        'debt': debt,
    })


# ---------------------------
# CUSTOMERS
# ---------------------------
def customers(request):
    sort_by, order = get_sort_params(request, default='surname')
    data = Persons.objects.filter(isActive=True).order_by(sort_by)
    return render(request, 'customers.html', {'data': data, 'order': order})


class PersonsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_model'
    model = Persons
    form_class = PersonsForm
    template_name = 'persons_update.html'
    success_url = reverse_lazy('customers')


# ---------------------------
# COUNTERS
# ---------------------------
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


# ---------------------------
# PAIDS
# ---------------------------
def paids(request):
    sort_by = request.GET.get('sort', 'receiptNumber')
    order = request.GET.get('order', 'desc')
    sort_field = f'-{sort_by}' if order == 'desc' else sort_by
    all_param = request.GET.get('all')
    all_data = Paids.objects.all().order_by(sort_field)

    if all_param == '1':
        page_obj = all_data
    else:
        paginator = Paginator(all_data, 14)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

    return render(request, 'paids.html', {
        'page_obj': page_obj,
        'order': order,
        'sort_by': sort_by
    })

# # ---------------------------
# # UPDATE PAYMENT
# # ---------------------------
# class PaidsUpdateView(PermissionRequiredMixin, UpdateView):
#     permission_required = 'synet.change_model'
#     model = Paids
#     form_class = PaidsForm
#     template_name = 'paid_create_update.html'
#     success_url = reverse_lazy('paids')

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         if not obj.irrigation:
#             obj.irrigation = self.get_object().irrigation
#         if not obj.customer:
#             obj.customer = self.get_object().customer
#         obj.save()

#         messages.success(self.request, f"💾 Η απόδειξη #{obj.receiptNumber} ενημερώθηκε επιτυχώς.")
#         return super().form_valid(form)


# # ---------------------------
# # CREATE PAYMENT
# # ---------------------------
# def create_payment(request, pk):
#     watercons = get_object_or_404(WaterCons, pk=pk)
#     last_paid = Paids.objects.order_by("-receiptNumber").first()
#     next_receipt_no = (last_paid.receiptNumber + 1) if last_paid else 1

#     if request.method == "POST":
#         form = PaidsForm(request.POST)
#         if form.is_valid():
#             paid = form.save(commit=False)
#             paid.customer = watercons.customer
#             paid.irrigation = watercons
#             paid.save()
#             messages.success(request, f"✅ Δημιουργήθηκε επιτυχώς η απόδειξη #{paid.receiptNumber}.")
#             return redirect("paids")
#     else:
#         form = PaidsForm(initial={
#             "receiptNumber": next_receipt_no,
#             "cost": watercons.cost,
#             "paid": 0,
#             "balance": -watercons.cost,
#             "irrigation": watercons,
#             "customer": watercons.customer,
#         })

#     return render(request, "paid_create_update.html", {"form": form})


# ---------------------------
# UPDATE PAYMENT
# ---------------------------
class PaidsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_model'
    model = Paids
    form_class = PaidsForm
    template_name = 'paid_create_update.html'
    success_url = reverse_lazy('paids')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Το 'object' είναι το Paids instance που ενημερώνουμε (self.object)
        
        # Προσθέτουμε το αντικείμενο Paids (object) και τα σχετικά του αντικείμενα
        # για να τα χρησιμοποιήσουμε στα readonly πεδία στο template.
        paids_instance = self.get_object() 
        context['irrigation'] = paids_instance.irrigation
        context['customer'] = paids_instance.customer
        
        return context

    def form_valid(self, form):
        # ... (Ο υπόλοιπος κώδικας form_valid παραμένει ίδιος) ...
        obj = form.save(commit=False)
        # Τα irrigation & customer είναι ήδη attached στο obj αν είναι instance (update)
        # Αλλά τα ξαναβάζουμε για λόγους ασφαλείας, αν και δεν χρειάζεται πια.
        if not obj.irrigation:
             obj.irrigation = self.get_object().irrigation
        if not obj.customer:
             obj.customer = self.get_object().customer
             
        obj.save()

        next_url = self.request.POST.get('next_url', self.success_url)
        
        messages.success(self.request, f"💾 Η απόδειξη #{obj.receiptNumber} ενημερώθηκε επιτυχώς.")
        return redirect(next_url)

# ---------------------------
# CREATE PAYMENT
# ---------------------------
def create_payment(request, pk):
    watercons = get_object_or_404(WaterCons, pk=pk)
    last_paid = Paids.objects.order_by("-receiptNumber").first()
    next_receipt_no = (last_paid.receiptNumber + 1) if last_paid else 1

    if request.method == "POST":
        form = PaidsForm(request.POST)
        if form.is_valid():
            paid = form.save(commit=False)
            paid.customer = watercons.customer
            paid.irrigation = watercons
            paid.save()

            # Διαχείριση URL επιστροφής
            next_url = request.POST.get('next_url', reverse_lazy('paids'))
            
            messages.success(request, f"✅ Δημιουργήθηκε επιτυχώς η απόδειξη #{paid.receiptNumber}.")
            return redirect(next_url) # Χρησιμοποιούμε το next_url
    else:
        # ... (Ο κώδικας initial values παραμένει ο ίδιος)
        form = PaidsForm(initial={
            "receiptNumber": next_receipt_no,
            "cost": watercons.cost,
            "paid": 0,
            "balance": -watercons.cost,
        })
        # Προσθέστε τα customer και irrigation στα context αν θέλετε να τα χρησιμοποιήσετε στο template
    
    return render(request, "paid_create_update.html", {
        "form": form,
        # Περνάμε τα αντικείμενα για να τα δείξουμε στα readonly πεδία στο template
        "watercons": watercons, 
        "customer": watercons.customer 
    })
    
    
# ---------------------------
# WATERCONSUMPTIONS / IRRIGATIONS
# ---------------------------
class WaterConsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'synet.add_watercons'
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'add_irrigation.html'
    success_url = reverse_lazy('index')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['customer'].queryset = Persons.objects.filter(isActive=True)
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.cubicMeters is not None and obj.cubicMeters < 0:
            form.add_error('cubicMeters', 'Τα κυβικά πρέπει να είναι θετικός αριθμός.')
            return self.form_invalid(form)
        if obj.costPerMeter is not None and obj.costPerMeter < 0:
            form.add_error('costPerMeter', 'Το κόστος ανά κυβικό πρέπει να είναι θετικός αριθμός.')
            return self.form_invalid(form)
        obj.save()

        # SMS
        if obj.customer and obj.msg:
            phone = getattr(obj.customer, 'phone', None)
            if phone:
                try:
                    sms_result = send_sms(phone, obj.msg)
                    messages.success(self.request, f"SMS στάλθηκε: {sms_result}")
                except Exception as e:
                    messages.error(self.request, f"Σφάλμα κατά την αποστολή SMS: {e}")
            else:
                messages.warning(self.request, "Δεν βρέθηκε τηλεφωνικό για τον πελάτη, SMS δεν στάλθηκε.")
        return super().form_valid(form)


class WaterConsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'synet.change_watercons'
    model = WaterCons
    form_class = WaterConsForm
    template_name = 'update_irrigation.html'
    success_url = reverse_lazy('index')


# ---------------------------
# CUSTOMER IRRIGATIONS (class-based)
# ---------------------------
class CustomerIrrigationsView(PermissionRequiredMixin, ListView):
    permission_required = 'synet.view_watercons'
    model = WaterCons
    template_name = 'customerIrrigations.html'
    context_object_name = 'data'
    paginate_by = 50

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        return WaterCons.objects.filter(customer_id=customer_id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs.get('customer_id')
        customer = get_object_or_404(Persons, id=customer_id)
        customerPaids = Paids.objects.filter(customer=customer_id).order_by('-receiptNumber')
        aggregates = WaterCons.objects.filter(customer_id=customer_id).aggregate(
            total_cost=Sum('cost'),
            total_cubic=Sum('cubicMeters'),
            total_billable=Sum('billableCubicMeters')
        )
        total_paid = Paids.objects.filter(customer=customer_id).aggregate(total_paid=Sum('paid'))['total_paid'] or 0
        debt = (aggregates['total_cost'] or 0) - total_paid
        context.update({
            'customer': customer,
            'customerPaids': customerPaids,
            'order': 'desc',
            'paids_order': 'desc',
            **aggregates,
            'total_paid': total_paid,
            'debt': debt
        })
        return context


# ---------------------------
# AJAX / GET endpoints
# ---------------------------

@require_GET
def get_counter_last_reading(request, counter_id):
    if not counter_id:
        return JsonResponse({"last_reading": ""})
    last_entry = (
        WaterCons.objects.filter(counter_id=counter_id)
        .order_by("-date", "-id")
        .first()
    )
    if last_entry:
        return JsonResponse({"last_reading": last_entry.finalIndication})
    return JsonResponse({"last_reading": ""})


@require_GET
def get_person_phone(request, person_id):
    phone = ""
    if person_id:
        try:
            person = Persons.objects.get(id=person_id)
            phone = person.phone or ""
        except Persons.DoesNotExist:
            pass
    return JsonResponse({'phone': phone})


@require_GET
def get_params_for_watercons(request):
    customer_id = request.GET.get('customer_id')
    counter_id = request.GET.get('counter_id')
    params = {}

    params['ydronomistFee'] = float(get_param('ydronomistFee', 0) or 0)

    payAsMember = False
    if customer_id:
        try:
            person = Persons.objects.get(id=customer_id)
            payAsMember = person.payAsMember
        except Persons.DoesNotExist:
            pass
    params['payAsMember'] = payAsMember

    cost_per_meter = float(get_param('baseCostPerMeter', 0) or 0)
    if not payAsMember:
        cost_per_meter += float(get_param('additionNotMember', 0) or 0)
    if counter_id and str(counter_id) == "4":
        cost_per_meter += float(get_param('additionSecondPump', 0) or 0)
    params['costPerMeter'] = cost_per_meter

    return JsonResponse(params)


@require_GET
def get_collector_fee_rate(request):
    try:
        rate = Parametroi.objects.get(param="collectorFeeRate").value
    except Parametroi.DoesNotExist:
        rate = "0"
    return JsonResponse({"collectorFeeRate": rate})


def get_param(param_name, default=None):
    try:
        return Parametroi.objects.get(param=param_name).value
    except Parametroi.DoesNotExist:
        return default


# ---------------------------
# REPORT
# ---------------------------
def select_persons_for_report(request):
    persons = Persons.objects.filter(isActive=True)
    if request.method == 'POST':
        selected = request.POST.getlist('persons')
        if 'all' in selected:
            selected = [str(p.id) for p in persons]
        return redirect(f"/report/?persons={','.join(selected)}")
    return render(request, 'select_persons.html', {'persons': persons})


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
    grand_total_balance = sum(item['total_balance'] for item in report_data)
    return render(request, 'report.html', {
        'report_data': report_data,
        'grand_total_balance': grand_total_balance
    })


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
        # Παράδειγμα αναζήτησης σε κάποια μοντέλα
        results += search_model(Persons, ['surname', 'name', 'fathersName', 'afm', 'phone', 'notes'], query, 'Πελάτες')
        results += search_model(Counters, ['collecter', 'counter'], query, 'Μετρητές')
        results += search_model(WaterCons, ['msg', 'notes'], query, 'Ποτίσματα')
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
                url = None
                try:
                    from django.urls import reverse
                    url = reverse(f"{obj._meta.model_name}_detail", args=[obj.id])
                except:
                    pass
                found.append({
                    'model': model_name,
                    'field': field,
                    'value': value,
                    'id': obj.id,
                    'string': str(obj),
                    'url': url,
                })
    return found




def get_watercons_params(request):
    customer_id = request.GET.get('customer_id')
    counter_id = request.GET.get('counter_id')

    def get_param(name, default=0):
        try:
            return float(Parametroi.objects.get(param=name).value)
        except Parametroi.DoesNotExist:
            return default

    ydronomistFee = get_param('ydronomistFee')
    baseCostPerMeter = get_param('baseCostPerMeter')
    additionNotMember = get_param('additionNotMember')
    additionSecondPump = get_param('additionSecondPump')

    # Έλεγχος αν ο πελάτης πληρώνει ως μέλος
    pay_as_member = True
    if customer_id:
        try:
            person = Persons.objects.get(id=customer_id)
            pay_as_member = person.payAsMember
        except Persons.DoesNotExist:
            pay_as_member = True

    is_second_pump = str(counter_id) == "4" if counter_id else False

    costPerMeter = baseCostPerMeter
    if not pay_as_member:
        costPerMeter += additionNotMember
    if is_second_pump:
        costPerMeter += additionSecondPump

    return JsonResponse({
        'ydronomistFee': ydronomistFee,
        'costPerMeter': costPerMeter,
        'payAsMember': pay_as_member,
    })


# ---------------------------
# MY LIST VIEW
# ---------------------------
def my_list_view(request):
    all_mode = request.GET.get('all') == '1'
    queryset = WaterCons.objects.all().order_by('...')

    if all_mode:
        page_obj = None
        objects = queryset  # Όλες οι εγγραφές
    else:
        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        objects = page_obj.object_list

    return render(request, 'my_template.html', {
        'objects': objects,
        'page_obj': page_obj,
        # ...άλλα context...
    })



