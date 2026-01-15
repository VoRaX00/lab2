from django import forms
from .models import Order, Product, Customer

class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Order
        fields = ['id', 'order_date', 'ship_date', 'ship_mode', 'customer']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'ship_date': forms.DateInput(attrs={'type': 'date'}),
        }
