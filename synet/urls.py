from django.urls import path
from . import views
from .views import get_last_final_indication, PersonsUpdateView, CountersUpdateView, PaidsUpdateView, WaterConsCreateView, WaterConsUpdateView,  create_payment

urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.index, name="root"),
    path('about', views.about, name="about"),
    path('customers/', views.customers, name="customers"),
    path('customers/update/<int:pk>/', PersonsUpdateView.as_view(), name='customers_update'),
    path('counters/', views.counters, name="counters"),
    path('counters/update/<int:pk>/', CountersUpdateView.as_view(), name='counters_update'),
    path('paids/', views.paids, name="paids"),
    path('paids/update/<int:id>/', views.paids_update, name='paids_update'),
    path('paids/create/<int:irrigation_id>/', views.create_payment, name='create_payment'),
    # path('paids/update/<int:pk>/', PaidsUpdateView.as_view(), name='paids_update'),
    path('add-irrigation/', WaterConsCreateView.as_view(), name='add_irrigation'),
    path('update-irrigation/<int:pk>/', WaterConsUpdateView.as_view(), name='update_irrigation'),    # path('insert', views.insertData, name="insertData"),
    path('get-final-indication/<int:counter_id>/', get_last_final_indication, name='get_final_indication'),    # path('update/<int:id>', views.updateData, name="updateData"),
    path('customerIrrigations/<int:customer_id>/', views.customerIrrigations, name="customerIrrigations"),
    ## diplo onoma # path('payment/add/<int:irrigation_id>/', create_payment, name='create_payment'),
    # path('delete/<int:id>', views.deleteData, name="deleteData"),
    # path('add-student', views.addStudent, name="addStudent"),
]

