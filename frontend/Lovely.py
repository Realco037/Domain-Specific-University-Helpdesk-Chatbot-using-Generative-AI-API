import streamlit as st
import google.generativeai as genai

# API
genai.configure(api_key="AIzaSyAuYAmglsuXGpLsR7zmgMSxgGZqMz4o1LU")
model = genai.GenerativeModel("gemini-3-flash-preview")


# Load data
@st.cache_data
def load_data():
    with open("university_dataset.txt", "r") as f:
        return f.read()

# Chatbot logic
def get_response(user_input):
    data = load_data()

    prompt = f"""
You are Lovely 🧡, a friendly and professional university helpdesk assistant.

Your job is to help students with questions about:
- attendance
- classes
- exams
- fees
- academic rules
- general university policies

PERSONALITY:
- Always be polite, warm, and helpful
- Speak like a real assistant, not a robot
- Keep answers clear and easy to understand

RULES:
- Answer briefly (2–4 sentences max)
- ONLY use the information provided below
- DO NOT make up information
- If the answer is not in the data, say:
  "I'm sorry, I don't have that information right now."

UNIVERSITY DATA:
{data}

QUESTION:
{user_input}
"""
    response = model.generate_content(prompt)
    return response.text

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lovely Chatbot", page_icon="🎓", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.chat-bubble-user {
    background-color: orange;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: white;
    text-align: right;
}
.chat-bubble-bot {
    background-color: #262730;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: white;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.image("lpu_logo.png", width=100)
st.title("🎓 Lovely – Student Helpdesk")
st.markdown("### Your friendly university assistant")

#--SIDEBAR--
st.sidebar.title("About Lovely")
st.sidebar.info("AI-powered university assistant")

#--SIDEBUTTONS--
if st.button("Check Attendance Rule"):
    st.session_state.messages.append({"role": "user", "content": "attendance"})

# --- SESSION STATE (CHAT HISTORY) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Add greeting message automatically
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello, I am Lovely 🧡. How can I assist you today?"
    })

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)

# --- INPUT ---
user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Lovely is thinking... 💭"):
        reply = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()