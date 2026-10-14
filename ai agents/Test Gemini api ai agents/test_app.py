"""يختبر الواجهة بنموذج مزيف: python test_app.py"""
import os
os.environ["GEMINI_API_KEY"] = "fake-key-for-test"
import google.genai as genai_mod
from streamlit.testing.v1 import AppTest


class FakeResponse:
    def __init__(self, text): self.text = text


class FakeSession:
    def __init__(self, tools): self.tools = {t.__name__: t for t in tools}

    def send_message(self, text):
        if "ضيف" in text:                       # نحاكي أن النموذج طلب أداة
            result = self.tools["add_to_cart"](4, 1)
            return FakeResponse("تمت الإضافة" if result["ok"] else result["error"])
        return FakeResponse("أهلًا بك!")


class FakeChats:
    def create(self, model, config): return FakeSession(config.tools)


class FakeClient:
    def __init__(self, api_key=None): self.chats = FakeChats()


genai_mod.Client = FakeClient

at = AppTest.from_file("app.py", default_timeout=30).run()
assert not at.exception, at.exception
at.chat_input[0].set_value("مرحبا").run()
assert at.chat_message[-1].markdown[0].value == "أهلًا بك!"
at.chat_input[0].set_value("ضيف الماوس").run()
assert not at.exception, at.exception
sidebar_text = " ".join(m.value for m in at.sidebar.markdown)
assert "ماوس لاسلكي" in sidebar_text and "180" in sidebar_text, sidebar_text
print("اختبار الواجهة نجح: السلة تتحدث في الشريط الجانبي")
