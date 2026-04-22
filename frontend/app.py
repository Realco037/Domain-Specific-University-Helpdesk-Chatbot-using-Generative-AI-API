import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyAuYAmglsuXGpLsR7zmgMSxgGZqMz4o1LU")
model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    generation_config={
        "temperature": 0.3,
        "max_output_tokens": 150
    }
)

#Loading the data
def load_data():
    with open("university_dataset.txt", "r") as f:
        return f.read()
def get_response(user_input):
    data = load_data()

    prompt = f"""
You are Lovely 🧡, a university helpdesk assistant.

Rules:
- Be polite and clear
- Start with: "Hello, I am Lovely 🧡."
- Keep answers short (2–4 sentences)
- Use ONLY the data below
- If unknown, say: "I don't have that information."

DATA:
{data}

QUESTION:
{user_input}
"""

    response = model.generate_content(prompt)
    return response.text

#UI Design
st.set_page_config(page_title="Lovely Chatbot", page_icon="🎓")
st.image("lpu_logo.png", width=120)
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
    }
    .stTextInput input {
        border: 2px solid orange;
        border-radius: 10px;
    }
    .stButton button {
        background-color: orange;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

#Introduction Title
st.title("🎓 Lovely - Student Helpdesk")
st.markdown("Your friendly university assistant")

#Input
user_input = st.text_input("Ask your question:")

if user_input:
    response = get_response(user_input)
    st.success(response)