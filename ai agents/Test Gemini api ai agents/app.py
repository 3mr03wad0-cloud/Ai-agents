"""AI Sales Assistant - الإصدار 5: واجهة ويب بـ Streamlit.
التشغيل (من الطرفية داخل المجلد):  streamlit run app.py
"""
import os
import streamlit as st
from google import genai
from google.genai import types
from assistant import load_catalog
from cart import Cart
from config import load_env
from prompts import build_system_prompt_tools
from tools import make_tools

MODEL = "gemini-3.8-flash"   # نفس الاسم الذي اشتغل معك

st.set_page_config(page_title="مساعد المبيعات", page_icon="🛒", layout="wide")
st.markdown(
    "<style>.stApp,[data-testid='stChatMessage'],section[data-testid='stSidebar']"
    "{direction:rtl;text-align:right;}</style>",
    unsafe_allow_html=True,
)

load_env()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("لم يتم العثور على GEMINI_API_KEY. ضعه في ملف .env بجانب app.py ثم أعد التشغيل.")
    st.stop()


# ---------- حالة الجلسة: تبقى بين كل تفاعل وآخر ----------
def new_session():
    products = load_catalog()
    cart = Cart(products)
    calls = []
    client = genai.Client(api_key=api_key)
    st.session_state.cart = cart
    st.session_state.calls = calls
    st.session_state.messages = []
    st.session_state.chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt_tools(),
            tools=make_tools(cart, products, calls),
            max_output_tokens=1000,
        ),
    )


if "chat" not in st.session_state:
    new_session()

# ---------- 1) معالجة الرسالة الجديدة (قبل الرسم لتتحدث السلة فورًا) ----------
prompt = st.chat_input("اكتب رسالتك هنا...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    start = len(st.session_state.calls)
    try:
        with st.spinner("جاري التفكير..."):
            reply = st.session_state.chat.send_message(prompt).text or "(لم يصل رد)"
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            reply = "انتهت الحصة المجانية لهذا النموذج. جرّب لاحقًا أو غيّر MODEL."
        else:
            reply = f"حدث خطأ في الاتصال: {e}"
    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "tools": st.session_state.calls[start:]}
    )

# ---------- 2) الشريط الجانبي: السلة ----------
with st.sidebar:
    st.header("🛒 سلة المشتريات")
    cart_view = st.session_state.cart.view()
    if cart_view["is_empty"]:
        st.write("السلة فارغة.")
    for item in cart_view["items"]:
        st.write(f"{item['quantity']} × {item['name']} — {item['subtotal_egp']:.0f} جنيه")
    st.subheader(f"الإجمالي: {cart_view['total_egp']:.0f} جنيه")
    if st.button("محادثة جديدة"):
        new_session()
        st.rerun()

# ---------- 3) عرض المحادثة ----------
st.title("مساعد المبيعات")
if not st.session_state.messages:
    st.info("جرّب: «عايز حاجة للمكتب أقل من 500» ثم «ضيف الماوس في السلة»")
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("tools"):
            with st.expander("الأدوات المستخدمة"):
                for t in m["tools"]:
                    st.code(t, language="python")
