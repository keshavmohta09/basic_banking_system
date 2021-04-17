from django.urls import path
from .views import home, transaction_list, customer_list, transfer_amount, customer_detail, about, terms_conditions

urlpatterns = [
    path('',home,name='home_page'),
    path('transaction/history/page/<int:page_num>/',transaction_list,name='transaction_history'),
    path('customer/list/',customer_list,name='users_list'),
    path('transfer/',transfer_amount,name='transfer_money'),
    path('customer_detail/<int:id>/',customer_detail,name='customer_detail'),
    path('about/',about,name='about'),
    path('terms_conditions/',terms_conditions,name='terms_conditions'),
]