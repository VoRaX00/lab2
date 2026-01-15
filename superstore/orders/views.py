from django.shortcuts import render
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from orders.models import Country, State, City, Customer, Product, Order, ProductOrder
from orders.forms import OrderForm
from django.shortcuts import render, get_object_or_404, redirect
from django.middleware.csrf import get_token
PAGE_SIZE = 10

def orders_list(request):
    orders = Order.objects.select_related('customer').all().order_by('order_date', 'id')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.products.set(form.cleaned_data["products"])
            return redirect("orders_list")
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {
        "form": form, 
        "mode": "create", 
        'title': 'Create Order',
        'csrf_token': get_token(request)}
    )

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            order.products.set(form.cleaned_data["products"])
            return redirect("orders_list")
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {
        'form': form, 
        'title': 'Edit Order',
        'csrf_token': get_token(request)
    })

def order_delete(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'csrf_token': get_token(request)
    })


def safe_page_number(param):
    try:
        page = int(param)
        return max(page, 1)
    except (TypeError, ValueError):
        return 1

def index(request):
    tables_info = [
        ('countries', Country.objects.all().order_by('id'), ['ID', 'Country Name'], lambda c: [c.id, c.country_name]),
        ('states', State.objects.select_related('country').order_by('id'), ['ID', 'State', 'Country'], lambda s: [s.id, s.state_name, s.country.country_name]),
        ('cities', City.objects.select_related('state').order_by('id'), ['ID', 'City', 'State', 'Postal Code'], lambda c: [c.id, c.city_name, c.state.state_name, c.postal_code]),
        ('products', Product.objects.all().order_by('id'), ['ID', 'Product name', 'Subcategory', 'Sales', 'Quantity', 'Discount', 'Profit'], lambda p: [p.id, p.product_name, p.subcategory, p.sales, p.quantity, p.discount, p.profit]),
        ('customers', Customer.objects.select_related('city').order_by('id'), ['ID', 'Customer', 'Segment', 'City'], lambda c: [c.id, c.customer_name, c.segment, c.city.city_name]),
        ('orders', Order.objects.select_related('customer').order_by('order_date', 'id'), ['ID', 'Customer', 'Order Date', 'Ship date', 'Ship mode', 'Consumer ID'], lambda o: [o.id, o.customer.customer_name, o.order_date, o.ship_date, o.ship_mode, o.customer.id]),
        ('products_orders', ProductOrder.objects.select_related('product', 'order').order_by('order_id', 'product_id'), ['Product ID', 'Order ID'], lambda po: [po.product.id, po.order.id]),
    ]

    tables_data = {}

    for name, queryset, headers, row_func in tables_info:
        page_number = safe_page_number(request.GET.get(f'{name}_page'))
        paginator = Paginator(queryset, PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        rows = [row_func(item) for item in page_obj]

        tables_data[name] = {
            'headers': headers,
            'rows': rows,
            'page_obj': page_obj
        }

    orders_by_country = [
        [c.country_name, c.order_count]
        for c in Country.objects.annotate(
            order_count=Count('states__cities__customers__orders')
        )
    ]

    profit_by_country = [
        [c.country_name, c.total_profit]
        for c in Country.objects.annotate(
            total_profit=Sum('states__cities__customers__orders__products__profit')
        )
    ]

    sales_by_customer_qs = [
        [c.customer_name, c.total_sales]
        for c in Customer.objects.annotate(
            total_sales=Sum('orders__products__sales')
        )
    ]

    sales_page_number = safe_page_number(request.GET.get('sales_page'))
    sales_paginator = Paginator(sales_by_customer_qs, PAGE_SIZE)
    sales_page = sales_paginator.get_page(sales_page_number)

    context = {
        'tables_data': tables_data,
        'orders_by_country': orders_by_country,
        'profit_by_country': profit_by_country,
        'sales_by_customer': sales_page,
        'csrf_token': get_token(request)
    }

    return render(request, 'index.html', context)
