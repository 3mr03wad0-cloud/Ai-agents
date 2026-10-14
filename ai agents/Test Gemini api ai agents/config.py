"""قراءة المفاتيح من ملف .env بجانب الكود (بدون كتابتها داخل الكود)."""
import os


def load_env(filename=".env"):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            # لا نكتب فوق متغير موجود أصلًا في البيئة
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
