import pandas as pd

class Product:
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_csv(cls, file_path: str) -> list['Product']:
       
        df = pd.read_csv(file_path)
        
     
        if 'tags' in df.columns:
            df['tags'] = df['tags'].fillna('').apply(lambda x: [t.strip() for t in str(x).split(',') if t.strip()])
            
        products = []
        for _, row in df.iterrows():
            
            products.append(cls(**row.to_dict()))
            
        return products

    def calculate_final_price(self):
       
        return self.price_egp * (1 - self.discount_pct / 100)

    def __repr__(self):
        return f"<Product {self.product_id}: {self.name_ar} - {self.price_egp} EGP>"


















































'''class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    
    def show_info(self):
        print(f"Product: {self.name}")
        print(f"Price: {self.price} EGP")
        print(f"Category: {self.category}")
        print("-" * 20)

product1 = Product("HP Laptop", 18000, "Laptops")
product2 = Product("Dell Laptop", 22000, "Laptops")
product3 = Product("Lenovo Laptop", 19500, "Laptops")
budget = 19000
taxs=-5
products = [product1, product2, product3]

def find_products(all_products, max_budget):
    storage = []
    for product in all_products:
        if product.price <= max_budget:
            storage.append(product)
    return storage

# تعديل الدالة لتستقبل منتج واحد وكمية، وتحسب السعر الإجمالي شامل الضريبة (14%)
def calculate_total_item(product, qty, tax_rate):
    if qty <= 0:
        raise ValueError("Quantity must be greater than zero")

    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = product.price * qty
    tax_amount = subtotal * tax_rate / 100
    total_with_tax = subtotal + tax_amount

    return total_with_tax

suitable_products = find_products(products, budget)

for p in suitable_products:
    p.show_info()
    # حساب السعر لعدد قطعتين مثلاً شامل الضريبة
    try:
        total = calculate_total_item(p, 2,taxs)
        print(f"Total with {taxs}% tax (for 2 pcs): {total:.2f} EGP")
        print("=" * 30)
    except ValueError as error:
        print(f"Error->{error}")

print(f"Total suitable products found: {len(suitable_products)}")'''

