"""AI Sales Assistant - الإصدار 2 (مجاني): نفس الفكرة لكن بنموذج Gemini."""
import os
from google import genai
from google.genai import types
from assistant import load_catalog
from prompts import build_system_prompt
from config import load_env

MODEL = "gemini-3.8-flash"   # لو ظهر خطأ 429 أو 404 جرّب: "gemini-2.5-flash-lite"


def chat():
    load_env()   # يقرأ ملف .env إن وُجد
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("لم يتم العثور على GEMINI_API_KEY. اضبطه أولًا (راجع الشرح).")
        return

    client = genai.Client(api_key=api_key)
    # chat يحتفظ بذاكرة المحادثة تلقائيًا (لا نحتاج history يدويًا)
    session = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(load_catalog()),
            max_output_tokens=1000,
        ),
    )

    print("مساعد المبيعات جاهز. اكتب 'خروج' للإنهاء.\n")
    while True:
        user_input = input("أنت: ").strip()
        if user_input in ("خروج", "exit"):
            print("مع السلامة!")
            break
        if not user_input:
            continue
        try:
            response = session.send_message(user_input)
            print("المساعد:", response.text, "\n")
        except Exception as e:
            print("حدث خطأ في الاتصال:", e)


if __name__ == "__main__":
    chat()
