# 📄 DocuFlow — Intelligent Multi-PDF AI Assistant

DocuFlow is a **Retrieval-Augmented Generation (RAG)** application that allows users to upload **multiple PDF documents** and interact with them through a **context-aware AI chat interface**.  
It uses **Google Gemini**, **LangChain**, and **FAISS** to deliver **accurate, grounded answers strictly based on the uploaded documents**, preventing hallucinations.

---

## 🚀 Key Features

- **Multi-PDF Upload Support**
  - Upload and index multiple PDFs in a single session
  - Each document is chunked, embedded, and stored with source metadata

- **Persistent Vector Knowledge Base**
  - FAISS index is stored locally (`faiss_index/`)
  - Documents do **not** need to be re-uploaded after server restarts

- **True RAG Pipeline**
  - Semantic chunking with overlap
  - Vector similarity search (FAISS)
  - Context-grounded responses using Gemini

- **Hallucination-Safe Responses**
  - The AI answers **only from retrieved document context**
  - If the answer is not present, it explicitly responds with *“I don’t know”*

- **Modern Chat UI**
  - Glassmorphic, responsive UI built with Tailwind CSS
  - Real-time PDF upload status
  - Markdown-rendered AI responses

---

## 🧠 How DocuFlow Works (Architecture)

```

PDF Upload
↓
Text Extraction (PyPDF2)
↓
Chunking (LangChain RecursiveCharacterTextSplitter)
↓
Embeddings (Google text-embedding-004)
↓
Vector Storage (FAISS)
↓
User Question
↓
Similarity Search (Top-K chunks)
↓
Prompt Construction
↓
Gemini 1.5 Flash
↓
Grounded AI Response

````

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Marked.js (Markdown rendering)
- Font Awesome

### Backend
- Python
- Flask

### AI & RAG
- **LLM:** Google Gemini 1.5 Flash
- **Embeddings:** Google Text Embedding 004
- **Vector Store:** FAISS
- **Orchestration:** LangChain

### Document Processing
- PyPDF2

---

## 📋 Prerequisites

- Python **3.9+**
- Google Gemini API Key  
  👉 Get one from: https://aistudio.google.com/

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sai-11011/DocFlow-main.git
cd DocFlow-main
````

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> ⚠️ Never commit your API key to GitHub.

---

### 5️⃣ Run the Application

```bash
python app.py
```

The server will start at:

```
http://localhost:5000
```

---

## 🖥️ Usage Guide

1. Open the application in your browser
2. Upload one or more PDF files
3. Wait for indexing to complete
4. Ask questions related to the uploaded documents
5. Receive **context-aware, document-grounded answers**

---

## 🧪 Behavior & Guarantees

* ✅ Answers are based **only** on uploaded PDFs
* ❌ External or fabricated knowledge is not used
* 📄 Each response is derived from **retrieved document chunks**
* 🔁 Index persists across server restarts

---

## ⚠️ Limitations

* Scanned PDFs (image-only) may not extract text
* Large PDFs may take longer to index
* Designed for **single active knowledge base** at a time

---

## 🔮 Future Enhancements

* User authentication & session-based document stores
* Source citations per answer
* PDF text highlighting
* Audio responses (TTS)
* Quiz & summary generation
* Cloud-based vector storage

---

## 🎯 Ideal Use Cases

* Resume analysis
* Research paper Q&A
* Study notes assistant
* Policy & documentation analysis
* Legal / academic document review

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 👨‍💻 Author

Developed by **Sai**
GitHub: [https://github.com/Sai-11011](https://github.com/Sai-11011)

---

> **DocuFlow demonstrates a production-ready RAG architecture using modern AI tooling, suitable for real-world applications and technical interviews.**


---
