import streamlit as st
from google import genai
import os
import base64

# Must be the very first Streamlit call
st.set_page_config(
    page_title="Lovely - University Helpdesk",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "lpu_logo.png")
DATA_PATH = os.path.join(BASE_DIR, "university_dataset.txt")

# ── API SETUP ────────────────────────────────────────────────────────────────
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("**API key missing.** Add `GOOGLE_API_KEY` to your Streamlit Cloud secrets.")
    st.code('GOOGLE_API_KEY = "your-google-api-key-here"', language="toml")
    st.stop()

client = genai.Client(api_key=api_key)

# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> str:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return f.read()

# ── CHATBOT LOGIC ─────────────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    data = load_data()
    history = st.session_state.get("messages", [])

    history_text = ""
    for msg in history[-6:]:
        label = "Student" if msg["role"] == "user" else "Lovely"
        history_text += f"{label}: {msg['content']}\n"

    prompt = f"""You are Lovely, a warm and professional university helpdesk assistant.

PERSONALITY: Friendly, clear, and concise. Never robotic.

RULES:
- Answer ONLY using the university data below.
- Keep answers to 2-4 sentences.
- If the answer is not in the data, say: "I'm sorry, I don't have that information. Please contact the university administration."
- Never invent information.
- Do not repeat the student's question back to them.

UNIVERSITY DATA:
{data}

RECENT CONVERSATION:
{history_text}
Student: {user_input}
Lovely:"""

    models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]
    last_error = None
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            last_error = e
            continue
    return f"Sorry, I could not reach the AI service. Error: {last_error}"

# ── QUICK-QUESTION HELPER ────────────────────────────────────────────────────
def ask_quick(question: str):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Lovely is thinking..."):
        reply = get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ── LOGO HELPER ───────────────────────────────────────────────────────────────
def centered_logo(width: int) -> str:
    with open(LOGO_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (
        f'<div style="display:flex;justify-content:center;margin-bottom:8px">'
        f'<img src="data:image/png;base64,{b64}" width="{width}"/>'
        f'</div>'
    )

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }

.user-msg {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0 4px 60px;
}
.user-msg-inner {
    background: linear-gradient(135deg, #FF6B35, #FF8C42);
    color: #fff;
    padding: 12px 18px;
    border-radius: 20px 20px 4px 20px;
    max-width: 82%;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 3px 12px rgba(255,107,53,.25);
    word-wrap: break-word;
}
.bot-msg {
    display: flex;
    justify-content: flex-start;
    margin: 10px 60px 4px 0;
    gap: 10px;
    align-items: flex-start;
}
.bot-avatar {
    width: 36px; height: 36px; min-width: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FF6B35, #FF8C42);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 2px 8px rgba(255,107,53,.3);
    flex-shrink: 0;
}
.bot-msg-inner {
    background: #F8F9FB;
    color: #1a1a2e;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 4px;
    max-width: 82%;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,.06);
    border: 1px solid #eee;
    word-wrap: break-word;
}
.page-header { text-align: center; padding: 8px 0 4px; }
.page-title  { font-size: 2rem; font-weight: 700; color: #FF6B35; margin: 0; }
.page-sub    { color: #888; font-size: .95rem; margin: 2px 0 0; }

div[data-testid="stSidebar"] div.stButton > button {
    border-radius: 20px;
    border: 1.5px solid #FF6B35;
    color: #FF6B35;
    background: transparent;
    font-size: 13px;
    text-align: left;
    padding: 7px 14px;
    transition: all .18s ease;
    width: 100%;
    margin-bottom: 4px;
}
div[data-testid="stSidebar"] div.stButton > button:hover {
    background: #FF6B35;
    color: #fff;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am Lovely, your university helpdesk assistant. "
                "I can help with attendance policies, exam rules, academic regulations, and more. "
                "What would you like to know?"
            ),
        }
    ]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.markdown(centered_logo(120), unsafe_allow_html=True)

    st.markdown("### Lovely Helpdesk")
    st.markdown("*AI-powered university assistant*")
    st.markdown("---")
    st.markdown("**Quick Questions**")

    QUICK = {
        "Attendance Policy":  "What is the minimum attendance requirement?",
        "Exam Rules":         "What are the exam rules and requirements?",
        "Evaluation System":  "How does the evaluation and grading system work?",
        "Dress Code":         "What is the dress code policy?",
        "Hostel Information": "What are the hostel rules?",
        "Academic Rules":     "What are the main academic rules I should know?",
        "Class Schedule":     "How are class schedules managed?",
    }

    for label, question in QUICK.items():
        if st.button(label, use_container_width=True, key=f"q_{label}"):
            ask_quick(question)

    st.markdown("---")

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am Lovely. How can I assist you today?"}
        ]
        st.rerun()

    st.markdown("---")
    st.caption("Lovely answers questions about attendance, exams, evaluation, dress code, hostel rules, and campus policies.")

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
if os.path.exists(LOGO_PATH):
    st.markdown(centered_logo(100), unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <p class="page-title">Lovely</p>
    <p class="page-sub">Your University Helpdesk Assistant</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── RENDER MESSAGES ───────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg"><div class="user-msg-inner">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="bot-msg"><div class="bot-avatar">L</div>'
            f'<div class="bot-msg-inner">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# ── INPUT ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything about the university..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Lovely is thinking..."):
        reply = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
