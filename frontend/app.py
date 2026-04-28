import streamlit as st
import google.generativeai as genai
import os

# Must be the very first Streamlit call
st.set_page_config(page_title="Lovely Chatbot", page_icon="🎓")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── API SETUP ────────────────────────────────────────────────────────────────
try:
    api_key = st.secrets["AIzaSyDy7iwq9UQpk2R2U7wGd-U6ferQypgEeVA"]
except KeyError:
    st.error("**API key missing.** Add `GOOGLE_API_KEY` to your Streamlit Cloud secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 300},
)

# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> str:
    with open(os.path.join(BASE_DIR, "university_dataset.txt"), "r", encoding="utf-8") as f:
        return f.read()

# ── CHATBOT LOGIC ─────────────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    data = load_data()
    prompt = f"""You are Lovely 🧡, a university helpdesk assistant.

Rules:
- Be polite and clear
- Keep answers short (2–4 sentences)
- Use ONLY the data below
- If unknown, say: "I don't have that information. Please contact university administration."

DATA:
{data}

QUESTION: {user_input}
Lovely:"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "I'm having trouble connecting right now. Please try again."

# ── UI ────────────────────────────────────────────────────────────────────────
logo = os.path.join(BASE_DIR, "lpu_logo.png")
if os.path.exists(logo):
    st.image(logo, width=120)

st.markdown("""
<style>
.stTextInput input { border: 2px solid #FF6B35; border-radius: 10px; }
.stButton button   { background-color: #FF6B35; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Lovely - Student Helpdesk")
st.markdown("Your friendly university assistant")

user_input = st.text_input("Ask your question:")

if user_input:
    with st.spinner("Lovely is thinking..."):
        response = get_response(user_input)
    st.success(response)
