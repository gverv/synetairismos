from django.urls import path
from . import views
from .views import (
    get_last_final_indication,
    get_params_for_watercons,  # <-- προσθήκη του endpoint
    PersonsUpdateView,
    CountersUpdateView,
    PaidsUpdateView,
    WaterConsCreateView,
    WaterConsUpdateView,
    create_payment,
    report_view,
    select_persons_for_report
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index', views.index, name="index"),
    path('', views.index, name="root"),
    path('about', views.about, name="about"),
    path('report/select-persons/', select_persons_for_report, name='select_persons_for_report'),
    path('report/', report_view, name='report'),
    path('customers/', views.customers, name="customers"),
    path('customers/update/<int:pk>/', PersonsUpdateView.as_view(), name='customers_update'),
    path('counters/', views.counters, name="counters"),
    path('counters/update/<int:pk>/', CountersUpdateView.as_view(), name='counters_update'),
    path('paids/', views.paids, name="paids"),
    path('paids/update/<int:id>/', views.paids_update, name='paids_update'),
    path('paids/create/<int:irrigation_id>/', views.create_payment, name='create_payment'),
    path('add-irrigation/', WaterConsCreateView.as_view(), name='add_irrigation'),
    path('update-irrigation/<int:pk>/', WaterConsUpdateView.as_view(), name='update_irrigation'),
    path('get-final-indication/<int:counter_id>/', get_last_final_indication, name='get_final_indication'),
    path('get-params-for-watercons/', get_params_for_watercons, name='get_params_for_watercons'),  # <-- νέο endpoint
    path('customerIrrigations/<int:customer_id>/', views.customerIrrigations, name="customerIrrigations"),
    path('counter/<int:pk>/', views.counter_detail, name='counter_detail'),
    path('search/', views.global_search, name='global_search'),
    path('get-person-phone/', views.get_person_phone, name='get_person_phone'),
]

