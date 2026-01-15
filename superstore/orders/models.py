from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name
    
    class Meta:
        db_table = 'countries'

class State(models.Model):
    state_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.state_name
    
    class Meta:
        db_table = 'states'

class City(models.Model):
    city_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    postal_code = models.IntegerField()

    def __str__(self):
        return self.city_name
    
    class Meta:
        db_table = 'cities'

class Customer(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    customer_name = models.TextField()
    segment = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.customer_name
    
    class Meta:
        db_table = 'customers'

class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    subcategory = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    sales = models.DecimalField(max_digits=20, decimal_places=5)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=10, decimal_places=5)
    profit = models.DecimalField(max_digits=20, decimal_places=5)

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'products'

class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    order_date = models.DateField()
    ship_date = models.DateField()
    ship_mode = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='ProductOrder')

    def __str__(self):
        return f"Order {self.id} - {self.customer.customer_name}"
    
    class Meta:
        db_table = 'orders'

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_orders'
