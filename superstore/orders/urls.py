from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<str:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<str:pk>/delete/', views.order_delete, name='order_delete'),
]
