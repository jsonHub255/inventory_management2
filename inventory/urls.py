from django.urls import path
from .views import create_order, order_detail

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('<int:order_id>/', order_detail, name='order_detail'),
]