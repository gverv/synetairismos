# synet/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import chrome_devtools_config
from . import views

urlpatterns = [
    # INDEX
    path('', login_required(views.index), name='index'),

    # AUTH
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # CUSTOMERS
    path('customers/', login_required(views.customers), name='customers'),
    path('customers/<int:pk>/update/', login_required(views.PersonsUpdateView.as_view()), name='persons_update'),
    path('customers/<int:customer_id>/irrigations/', login_required(views.CustomerIrrigationsView.as_view()), name='customer_irrigations'),

    # COUNTERS
    path('counters/', login_required(views.counters), name='counters'),
    path('counters/<int:pk>/update/', login_required(views.CountersUpdateView.as_view()), name='counters_update'),
    path('counters/<int:pk>/detail/', login_required(views.counter_detail), name='counter_detail'),

    # PAIDS
    path('paids/', login_required(views.paids), name='paids'),
    path('paids/<int:pk>/update/', login_required(views.PaidsUpdateView.as_view()), name='paids_update'),
    path('paids/add/<int:pk>/', login_required(views.create_payment), name='create_payment'),

    # IRRIGATIONS / WATERCONSUMPTIONS
    path('irrigations/add/', login_required(views.WaterConsCreateView.as_view()), name='add_irrigation'),
    path('irrigations/<int:pk>/update/', login_required(views.WaterConsUpdateView.as_view()), name='update_irrigation'),

    # AJAX / GET endpoints
    path('ajax/get_person_phone/<int:person_id>/', login_required(views.get_person_phone), name='get_person_phone'),
    path('ajax/get_params_for_watercons/', login_required(views.get_params_for_watercons), name='get_params_for_watercons'),
    path('ajax/get_counter_last_reading/<int:counter_id>/', login_required(views.get_counter_last_reading), name='get_counter_last_reading'),
    path('ajax/get_watercons_params/', login_required(views.get_watercons_params), name='get_watercons_params'),
    path('ajax/get_collector_fee_rate/', login_required(views.get_collector_fee_rate), name='get_collector_fee_rate'),

    # REPORT
    path('report/select-persons/', login_required(views.select_persons_for_report), name='select_persons_for_report'),
    path('report/', login_required(views.report_view), name='report'),

    # SEARCH
    path('search/', login_required(views.global_search), name='global_search'),


    path('.well-known/appspecific/com.chrome.devtools.json', chrome_devtools_config),

]
