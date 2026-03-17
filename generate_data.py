import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

rows = 50000

products = [
    ("Laptop","Electronics",800),
    ("Phone","Electronics",600),
    ("Headphones","Electronics",120),
    ("Shoes","Fashion",80),
    ("Tshirt","Fashion",30),
    ("Jeans","Fashion",60),
    ("Watch","Accessories",150),
    ("Backpack","Accessories",70),
    ("Chair","Furniture",200),
    ("Desk","Furniture",350)
]

data = []

for i in range(rows):

    product, category, price = random.choice(products)

    data.append({
        "order_id": i+1,
        "customer_id": f"C{random.randint(1000,9999)}",
        "order_date": fake.date_between(start_date="-2y", end_date="today"),
        "product": product,
        "category": category,
        "price": price,
        "quantity": random.randint(1,5)
    })

df = pd.DataFrame(data)

df.to_csv("data/ecommerce_data.csv",index=False)

print("Dataset created successfully!")