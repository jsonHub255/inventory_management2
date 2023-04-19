from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Order, OrderProduct, DeliveryOrder, Invoice, Vehicle, Reparation, ReparationProduct
from django.shortcuts import render, redirect
from .models import Order, Product, OrderProduct
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    if request.method == 'POST':
        order_number = request.POST['order_number']
        product_ids = request.POST.getlist('products')
        products = Product.objects.filter(id__in=product_ids)
        total_price = sum([product.price for product in products])
        supplier = request.POST['supplier']
        admin = request.user
        order = Order.objects.create(order_number=order_number, total_price=total_price, supplier=supplier, admin=admin)
        for product in products:
            OrderProduct.objects.create(order=order, product=product)
        return redirect('order_detail', order_id=order.id)
    else:
        products = Product.objects.all()
        return render(request, 'create_order.html', {'products': products})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_detail.html', {'order': order})



# Path: inventory\templates\create_order.html
# Compare this snippet from inventory\templates\create_order.html:
# {% extends 'base.html' %}
#   {% block content %}
#     <h1>Create Order</h1>
#     <form method="POST">      
#       {% csrf_token %}
#       <div class="form-group">    
#         <label for="order_number">Order Number</label>