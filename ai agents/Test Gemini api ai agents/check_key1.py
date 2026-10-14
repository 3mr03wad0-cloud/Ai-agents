"""يفحص مفتاح Gemini ويكشف من أين يأتي:  python check_key.py
لا يطبع المفتاح كاملًا، ولا يستهلك من حصة الرسائل (يطلب قائمة النماذج فقط)."""
import inspect
import os

import config
from config import load_env


def describe(k):
    return f"طول {len(k)} | يبدأ بـ {k[:4]} | ينتهي بـ {k[-3:]}" if k else "غير موجود"


env_before = os.environ.get("GEMINI_API_KEY", "")
env_path = os.path.join(os.path.dirname(os.path.abspath(config.__file__)), ".env")

print("ملف config المستخدم:", config.__file__)
print("نسخة config الجديدة (.env يتغلب)؟", "os.environ[key.strip()]" in inspect.getsource(config.load_env))
print("ملف .env المتوقع:", env_path, "| موجود؟", os.path.exists(env_path))

file_key = ""
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY") and "=" in line:
                file_key = line.split("=", 1)[1].strip().strip('"').strip("'")

print("1) في بيئة النظام/الـ Console قبل قراءة .env:", describe(env_before))
print("2) داخل ملف .env:", describe(file_key))

load_env()
key = os.environ.get("GEMINI_API_KEY", "")
print("3) المستخدم فعليًا الآن:", describe(key))
if env_before and file_key and env_before != file_key:
    print(">> تنبيه: القيمتان 1 و2 مختلفتان. هناك مفتاح قديم في بيئة النظام أو الـ Console.")
print("فيه مسافات أو علامات تنصيص؟", any(c in key for c in " \"'\n\t"))

if not key:
    print("لا يوجد مفتاح.")
else:
    try:
        from google import genai
        client = genai.Client(api_key=key)   # نحتفظ بالكائن حتى لا يُغلق قبل الاستخدام
        names = [m.name for m in client.models.list()]
        print(f"المفتاح يعمل. عدد النماذج المتاحة: {len(names)}")
        for n in names:
            if "flash" in n:
                print("   ", n)
    except Exception as e:
        print("فشل الاتصال:", str(e)[:120])
