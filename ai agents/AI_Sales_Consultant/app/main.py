from Product import Product
from AI_Agents import AI_agents
 
 
csv_file_path = "erp_products_catalog_large.csv"
 
catalog_products = Product.from_csv(csv_file_path)
print(f"تم تحميل {len(catalog_products)} منتج بنجاح.\n")
 
first_product = catalog_products[0]
print("--- تفاصيل المنتج الأول ---")
print(f"الكود: {first_product.product_id}")
print(f"الاسم: {first_product.name_ar}")
print(f"السعر الأساسي: {first_product.price_egp} ج.م")
print(f"الخصم: {first_product.discount_pct}%")
print(f"السعر بعد الخصم: {first_product.calculate_final_price()} ج.م")
print(f"الوسوم (Tags): {first_product.tags}")
 
# تشغيل المساعد الذكي على نفس الكتالوج المحمّل
agent = AI_agents(catalog_products)
agent.run()