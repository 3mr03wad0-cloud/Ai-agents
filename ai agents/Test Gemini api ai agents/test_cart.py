"""اختبارات السلة - تعمل بدون إنترنت ولا مفتاح: python test_cart.py"""
from assistant import load_catalog
from cart import Cart

c = Cart(load_catalog())
assert c.add(4)["ok"]                          # ماوس
assert c.add(4, 2)["ok"]                       # كمية إضافية
assert c.view()["items"][0]["quantity"] == 3
assert not c.add(4, 100)["ok"]                 # أكثر من المخزون
assert not c.add(3)["ok"]                      # باور بانك غير متوفر
assert not c.add(999)["ok"]                    # منتج غير موجود
assert not c.add(4, 0)["ok"]                   # كمية غير صالحة
assert c.view()["total_egp"] == 180 * 3
assert c.remove(4, 1)["ok"] and c.view()["items"][0]["quantity"] == 2
assert c.remove(4)["ok"] and c.view()["is_empty"]
assert not c.remove(4)["ok"]                   # حذف شيء غير موجود
print("كل اختبارات السلة نجحت")
