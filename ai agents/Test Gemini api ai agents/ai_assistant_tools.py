"""AI Sales Assistant - الإصدار 4: أدوات البحث + سلة المشتريات."""
import os
from google import genai
from google.genai import types
from config import load_env
from prompts import build_system_prompt_tools
from cart import Cart
from tools import make_tools, PRODUCTS

MODEL = "gemini-3.8-flash"   # نفس الاسم الذي اشتغل معك


def chat():
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("لم يتم العثور على GEMINI_API_KEY. اضبطه أولًا.")
        return

    client = genai.Client(api_key=api_key)
    session = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt_tools(),
            tools=make_tools(Cart(PRODUCTS)),
            max_output_tokens=1000,
        ),
    )

    print("مساعد المبيعات (v4) جاهز. اكتب 'خروج' للإنهاء.\n")
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
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("انتهت الحصة المجانية لهذا النموذج. جرّب لاحقًا أو غيّر MODEL إلى نموذج آخر.\n")
                break
            print("حدث خطأ في الاتصال:", e)


if __name__ == "__main__":
    chat()
