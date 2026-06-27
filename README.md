# React Interview Expert Bot 🤖

A specialized AI chatbot that answers React interview questions using a local PDF as a knowledge base. Built with a **RAG (Retrieval-Augmented Generation)** architecture.

## 🚀 Features

- **PDF-Grounded**: Answers only from your uploaded study material.
- **Source Citation**: Shows exactly which page the answer came from.
- **Chat Memory**: Remembers previous questions in the session.
- **Local First**: Runs on your machine for privacy and speed.

## 🛠️ Tech Stack

- **AI**: Google Gemini 2.5 Flash
- **Logic**: LangChain (LCEL)
- **Vector DB**: ChromaDB
- **UI**: Streamlit

## ⚙️ Setup Instructions

1. **Activate Virtual Environment**:
   ```bash
   .\venv\Scripts\activate
   Install Libraries:
   ```

Bash
pip install -r requirements.txt
Add API Key:
Create a .env file and add:
GOOGLE_API_KEY=your_key_here

Add PDF:
Place your react.pdf in this folder.

Run App:

Bash
python -m streamlit run app.py

---

### 📂 Your Final Folder View

Your folder should now look exactly like this:

- **`react-interview-bot/`**
  - `venv/` (Folder)
  - **`app.py`** (The code)
  - **`requirements.txt`** (The list of libraries)
  - **`README.md`** (The instructions)
  - **`.env`** (Your API key)
  - **`react.pdf`** (The document)
  - **`.gitignore`** (To keep .env and venv private)
