"""AI Sales Assistant - الإصدار 2: ربط الكتالوج بنموذج Claude."""
import os
from anthropic import Anthropic
from assistant import load_catalog   # نعيد استخدام كود v1
from prompts import build_system_prompt

MODEL = "claude-sonnet-5-5"   # غيّره هنا فقط إن أردت نموذجًا آخر


# ---------- المحادثة المحادثة ----------
def chat():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("لم يتم العثور على ANTHROPIC_API_KEY. اضبطه كمتغير بيئة أولًا (راجع الشرح).")
        return

    client = Anthropic()                       # يقرأ المفتاح تلقائيًا من البيئة
    system_prompt = build_system_prompt(load_catalog())
    history = []                               # ذاكرة المحادثة

    print("مساعد المبيعات جاهز. اكتب 'خروج' للإنهاء.\n")
    while True:
        user_input = input("أنت: ").strip()
        if user_input in ("خروج", "exit"):
            print("مع السلامة!")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=system_prompt,
                messages=history,
            )
        except Exception as e:
            print("حدث خطأ في الاتصال:", e)
            history.pop()                      # نلغي الرسالة الفاشلة
            continue

        answer = response.content[0].text
        history.append({"role": "assistant", "content": answer})
        print("المساعد:", answer, "\n")


if __name__ == "__main__":
    chat()
