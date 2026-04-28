# Domain-Specific University Helpdesk Chatbot — Lovely 🧡

An AI-powered university helpdesk chatbot built with **Streamlit** and the **Google Gemini API**. Lovely answers student questions about attendance, exams, academic rules, dress code, hostel policies, and more — using only verified university data.

---

## Features

- Conversational chat interface with message history
- Quick-question sidebar buttons for common topics
- Domain-restricted answers (only responds from university data)
- Orange university-branded UI theme
- Clear conversation button
- Deployed on Streamlit Cloud

---

## Project Structure

```text
├── frontend/
│   ├── Lovely.py              # Main app (primary entry point)
│   ├── app.py                 # Simple single-response version
│   ├── university_dataset.txt # University knowledge base
│   └── lpu_logo.png           # University logo
├── backend/
│   ├── Lovely.ipynb           # Prototype notebook
│   └── university_dataset.txt
├── .streamlit/
│   └── config.toml            # Theme configuration
├── requirements.txt
└── README.md
```

---

## Deploying to Streamlit Cloud

### 1. Push this repo to GitHub

```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push
```

### 2. Create a new app on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
1. Click **New app**
1. Select your repository
1. Set **Main file path** to: `frontend/Lovely.py`
1. Click **Deploy**

### 3. Add your API key as a Secret

> **Important:** The old API key in the code history is exposed — generate a fresh one.

1. Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. In Streamlit Cloud, open your app → **⋮ menu → Settings → Secrets**
3. Paste:

```toml
GOOGLE_API_KEY = "your-new-key-here"
```

4. Click **Save** — the app will restart automatically.

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run frontend/Lovely.py
```

Then create a `.streamlit/secrets.toml` file (never commit this):

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
```

---

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Frontend | Streamlit                   |
| AI Model | Google Gemini 1.5 Flash     |
| Language | Python 3.9+                 |
