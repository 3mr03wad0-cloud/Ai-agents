"""منطق سلة المشتريات - بايثون عادي بدون أي ذكاء اصطناعي."""


class Cart:
    def __init__(self, products):
        self.products = {int(p["id"]): p for p in products}
        self.items = {}   # {رقم المنتج: الكمية}

    def add(self, product_id, quantity=1):
        p = self.products.get(product_id)
        if p is None:
            return {"ok": False, "error": "المنتج غير موجود"}
        if quantity < 1:
            return {"ok": False, "error": "الكمية يجب أن تكون 1 أو أكثر"}
        if p["stock"] <= 0:
            return {"ok": False, "error": f"{p['name']} غير متوفر حاليًا"}
        new_qty = self.items.get(product_id, 0) + quantity
        if new_qty > p["stock"]:
            return {"ok": False,
                    "error": f"المتاح من {p['name']} هو {p['stock']} فقط (في سلتك {self.items.get(product_id, 0)})"}
        self.items[product_id] = new_qty
        return {"ok": True, "message": f"تمت إضافة {quantity} × {p['name']}", "cart": self.view()}

    def remove(self, product_id, quantity=0):
        """quantity=0 تعني حذف المنتج بالكامل من السلة."""
        if product_id not in self.items:
            return {"ok": False, "error": "هذا المنتج ليس في السلة"}
        name = self.products[product_id]["name"]
        if quantity <= 0 or quantity >= self.items[product_id]:
            del self.items[product_id]
        else:
            self.items[product_id] -= quantity
        return {"ok": True, "message": f"تم تحديث السلة بخصوص {name}", "cart": self.view()}

    def view(self):
        lines, total = [], 0
        for pid, qty in self.items.items():
            p = self.products[pid]
            subtotal = p["price"] * qty
            total += subtotal
            lines.append({"id": pid, "name": p["name"], "price_egp": p["price"],
                          "quantity": qty, "subtotal_egp": subtotal})
        return {"items": lines, "total_egp": total, "is_empty": not lines}
