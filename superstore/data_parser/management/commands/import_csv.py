# data_parser/management/commands/import_csv.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from orders.models import Country, State, City, Customer, Product, Order, ProductOrder
from pathlib import Path

class Command(BaseCommand):
    help = 'Imports data from Superstore.csv into the database'

    def handle(self, *args, **options):
        csv_file_path = Path(settings.BASE_DIR) / "data_parser/management/data/superstore.csv"
        
        with open(csv_file_path, 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            
            countries_cache = {}
            states_cache = {}
            cities_cache = {}
            customers_cache = {}
            products_cache = {}
            
            with transaction.atomic():
                for i, row in enumerate(reader, start=1):
                    try:
                        country_name = row['Country']
                        if country_name not in countries_cache:
                            country, _ = Country.objects.get_or_create(country_name=country_name)
                            countries_cache[country_name] = country
                        country = countries_cache[country_name]
                        
                        state_name = row['State']
                        state_key = f"{country_name}_{state_name}"
                        if state_key not in states_cache:
                            state, _ = State.objects.get_or_create(
                                state_name=state_name,
                                country=country
                            )
                            states_cache[state_key] = state
                        state = states_cache[state_key]
                        
                        city_name = row['City']
                        postal_code = int(row['Postal Code']) if row['Postal Code'] else 0
                        city_key = f"{state_key}_{city_name}_{postal_code}"
                        if city_key not in cities_cache:
                            city, _ = City.objects.get_or_create(
                                city_name=city_name,
                                state=state,
                                postal_code=postal_code
                            )
                            cities_cache[city_key] = city
                        city = cities_cache[city_key]
                        
                        customer_id = row['Customer ID']
                        if customer_id not in customers_cache:
                            customer, _ = Customer.objects.get_or_create(
                                id=customer_id,
                                defaults={
                                    'customer_name': row['Customer Name'],
                                    'segment': row['Segment'],
                                    'city': city
                                }
                            )
                            customers_cache[customer_id] = customer
                        customer = customers_cache[customer_id]
                        
                        product_id = row['Product ID']
                        if product_id not in products_cache:
                            product, _ = Product.objects.get_or_create(
                                id=product_id,
                                defaults={
                                    'subcategory': row['Sub-Category'],
                                    'product_name': row['Product Name'],
                                    'sales': float(row['Sales']),
                                    'quantity': int(row['Quantity']),
                                    'discount': float(row['Discount']),
                                    'profit': float(row['Profit']),
                                }
                            )
                            products_cache[product_id] = product
                        product = products_cache[product_id]
                        
                        order_date = datetime.strptime(row['Order Date'], '%m/%d/%Y').date()
                        ship_date = datetime.strptime(row['Ship Date'], '%m/%d/%Y').date()
                        
                        order_id = row['Order ID']
                        order, _ = Order.objects.get_or_create(
                            id=order_id,
                            defaults={
                                'order_date': order_date,
                                'ship_date': ship_date,
                                'ship_mode': row['Ship Mode'],
                                'customer': customer
                            }
                        )
                        
                        ProductOrder.objects.get_or_create(
                            product=product,
                            order=order
                        )
                        
                        if i % 100 == 0:
                            self.stdout.write(f'Processed {i} rows...')
                            
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error on row {i}: {e}'))
                        self.stdout.write(self.style.ERROR(f'Row data: {row}'))
                        raise
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {i} rows'))