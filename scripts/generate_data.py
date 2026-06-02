import csv
import random
from datetime import datetime, timedelta
import os

def generate_transactions(start_date, end_date, num_per_day=500):
    """Генерация транзакций для диапазона дат"""
    current = start_date
    transactions = []
    product_ids = list(range(1, 10))  # 10 товаров
    while current <= end_date:
        for _ in range(num_per_day):
            trans = {
                'transaction_id': random.randint(100000, 999999),
                'date': current.strftime('%Y-%m-%d'),
                'product_id': random.choice(product_ids),
                'quantity': random.randint(1, 5),
                'price': round(random.uniform(10.0, 200.0), 2),
                'customer_id': random.randint(1, 10000)
            }
            transactions.append(trans)
        current += timedelta(days=1)
    return transactions

if __name__ == '__main__':
    start = datetime(2026, 1, 1)
    end = datetime(2026, 1, 31)
    data = generate_transactions(start, end, num_per_day=500)  # ~15 500 строк
    os.makedirs('../data/raw', exist_ok=True)
    with open('../data/raw/sales_jan.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['transaction_id','date','product_id','quantity','price','customer_id'])
        writer.writeheader()
        writer.writerows(data)
    print("Файл data/raw/sales_jan.csv создан")