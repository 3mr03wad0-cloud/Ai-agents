"""الأدوات (Tools): دوال بايثون يستدعيها النموذج بنفسه عند الحاجة."""
from assistant import load_catalog, search, filter_by_category, filter_by_price, get_categories as _cats

PRODUCTS = load_catalog()
SHOW_CALLS = True   # اطبع كل استدعاء أداة في الطرفية


def _clean(p):
    """نرجع للنموذج بيانات بسيطة (أرقام ونصوص فقط)."""
    return {
        "id": int(p["id"]), "name": p["name"], "category": p["category"],
        "price_egp": p["price"], "in_stock": p["stock"] > 0,
        "stock": p["stock"], "description": p["description"],
    }


def make_tools(cart, products=PRODUCTS, calls=None):
    """ينشئ قائمة الأدوات مربوطة بسلة محددة.

    لماذا مصنع؟ لو جعلنا السلة متغيرًا عامًا (global) فسيشاركها كل المستخدمين.
    هنا كل جلسة تنشئ أدواتها وسلتها الخاصة. و calls قائمة اختيارية نسجّل فيها الاستدعاءات.
    """

    def _log(text):
        if SHOW_CALLS:
            print("   [أداة]", text)
        if calls is not None:
            calls.append(text)

    def find_products(keyword: str = "", category: str = "", max_price: float = 0,
                      in_stock_only: bool = False) -> list[dict]:
        """يبحث في كتالوج المتجر ويرجع المنتجات المطابقة.

        Args:
            keyword: كلمة واحدة قصيرة للبحث في الاسم والوصف (مثل: مكتب، حقيبة، سماعة). اتركها فارغة لعدم التقييد.
            category: اسم الفئة بالضبط (استخدم get_categories لمعرفة الفئات). اتركها فارغة لعدم التقييد.
            max_price: أقصى سعر بالجنيه. اتركه 0 لعدم التقييد.
            in_stock_only: True لإرجاع المنتجات المتوفرة فقط.
        """
        _log(f"find_products(keyword={keyword!r}, category={category!r}, "
             f"max_price={max_price}, in_stock_only={in_stock_only})")
        results = products
        if keyword:
            results = search(results, keyword)
        if category:
            results = filter_by_category(results, category)
        if max_price and max_price > 0:
            results = filter_by_price(results, max_price)
        if in_stock_only:
            results = [p for p in results if p["stock"] > 0]
        return [_clean(p) for p in results]

    def get_categories() -> list[str]:
        """يرجع قائمة فئات المنتجات المتاحة في المتجر."""
        _log("get_categories()")
        return _cats(products)

    def get_product(product_id: int) -> dict:
        """يرجع تفاصيل منتج واحد برقمه، أو رسالة خطأ إذا لم يوجد."""
        _log(f"get_product({product_id})")
        for p in products:
            if p["id"] == str(product_id):
                return _clean(p)
        return {"error": "المنتج غير موجود"}

    def add_to_cart(product_id: int, quantity: int = 1) -> dict:
        """يضيف منتجًا إلى سلة العميل بعد التحقق من وجوده وتوفره. استخدمه فقط عندما يطلب العميل الإضافة صراحة.

        Args:
            product_id: رقم المنتج (id) كما يظهر في نتائج البحث.
            quantity: الكمية المطلوبة (افتراضيًا 1).
        """
        _log(f"add_to_cart({product_id}, {quantity})")
        return cart.add(product_id, quantity)

    def remove_from_cart(product_id: int, quantity: int = 0) -> dict:
        """يحذف منتجًا من السلة.

        Args:
            product_id: رقم المنتج.
            quantity: الكمية المراد حذفها. اتركها 0 لحذف المنتج بالكامل.
        """
        _log(f"remove_from_cart({product_id}, {quantity})")
        return cart.remove(product_id, quantity)

    def view_cart() -> dict:
        """يعرض محتويات سلة العميل الحالية والإجمالي بالجنيه."""
        _log("view_cart()")
        return cart.view()

    return [find_products, get_categories, get_product,
            add_to_cart, remove_from_cart, view_cart]
