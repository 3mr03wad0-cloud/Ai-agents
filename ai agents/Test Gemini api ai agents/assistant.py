"""AI Sales Assistant - الإصدار 1 (قائم على القواعد، بدون ذكاء اصطناعي بعد)."""
import csv
import os


# ---------- 1) تحميل البيانات ----------
REQUIRED_COLUMNS = ["id", "name", "category", "price", "stock", "description"]


def load_catalog(path=None):
    """يقرأ ملف CSV ويرجع قائمة منتجات (كل منتج = قاموس dict).

    متسامح مع: علامة BOM، والفاصل ; بدل , (يحدث أحيانًا عند الحفظ من Excel)،
    ومع المسافات في أسماء الأعمدة. ويقرأ الملف من مجلد الكود نفسه.
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = f.read().splitlines()
    if not lines:
        raise ValueError(f"الملف {path} فارغ")

    header = lines[0]
    delimiter = ";" if header.count(";") > header.count(",") else ","
    reader = csv.DictReader(lines, delimiter=delimiter)
    reader.fieldnames = [h.strip().lstrip("\ufeff").lower() for h in reader.fieldnames]

    missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ValueError(f"أعمدة ناقصة في {path}: {missing}. الأعمدة التي وُجدت: {reader.fieldnames}")

    products = []
    for row in reader:
        row = {k: (v or "").strip() for k, v in row.items() if k}
        row["price"] = float(row["price"])   # نحول النص إلى رقم
        row["stock"] = int(row["stock"])
        products.append(row)
    return products


# ---------- 2) دوال البحث والتصفية ----------
def search(products, keyword):
    """بحث نصي في الاسم والوصف والفئة."""
    keyword = keyword.strip().lower()
    return [
        p for p in products
        if keyword in p["name"].lower()
        or keyword in p["description"].lower()
        or keyword in p["category"].lower()
    ]


def filter_by_category(products, category):
    return [p for p in products if p["category"] == category.strip()]


def filter_by_price(products, max_price):
    return [p for p in products if p["price"] <= max_price]


def get_categories(products):
    return sorted({p["category"] for p in products})


def get_by_id(products, product_id):
    for p in products:
        if p["id"] == str(product_id):
            return p
    return None


# ---------- 3) العرض ----------
def format_product(p):
    status = f"متوفر ({p['stock']})" if p["stock"] > 0 else "غير متوفر حاليًا"
    return f"[{p['id']}] {p['name']} | {p['category']} | {p['price']:.0f} جنيه | {status}"


def show(products):
    if not products:
        print("لم أجد منتجات مطابقة.")
        return
    for p in products:
        print(format_product(p))


# ---------- 4) الحلقة الرئيسية ----------
MENU = """
===== مساعد المبيعات =====
1) بحث بكلمة
2) تصفح حسب الفئة
3) منتجات بسعر أقل من حد معين
4) تفاصيل منتج (برقمه)
0) خروج
"""


def main():
    products = load_catalog()
    while True:
        print(MENU)
        choice = input("اختيارك: ").strip()

        if choice == "1":
            show(search(products, input("اكتب كلمة البحث: ")))
        elif choice == "2":
            print("الفئات:", "، ".join(get_categories(products)))
            show(filter_by_category(products, input("اكتب اسم الفئة: ")))
        elif choice == "3":
            try:
                show(filter_by_price(products, float(input("أقصى سعر: "))))
            except ValueError:
                print("من فضلك اكتب رقمًا صحيحًا.")
        elif choice == "4":
            p = get_by_id(products, input("رقم المنتج: ").strip())
            if p:
                print(format_product(p))
                print("الوصف:", p["description"])
            else:
                print("رقم غير موجود.")
        elif choice == "0":
            print("مع السلامة!")
            break
        else:
            print("اختيار غير صحيح.")


if __name__ == "__main__":
    main()
