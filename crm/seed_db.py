from .models import Customer, Product
import random

def run():
    customers = [
        {"name": "John Doe", "email": "john@example.com", "phone": "123456789"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "987654321"},
    ]
    products = [
        {"name": "Laptop", "price": 1000, "stock": 5},
        {"name": "Phone", "price": 500, "stock": 10},
    ]
    for c in customers:
        Customer.objects.get_or_create(**c)
    for p in products:
        Product.objects.get_or_create(**p)
    print("Database seeded successfully!")
