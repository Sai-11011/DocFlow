from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import PyPDF2

# LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

load_dotenv()

app = Flask(__name__)

# Initialize LangChain Components
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Fixed version

# Global Vector Store
vector_store = None
DB_PATH = "faiss_index"

# LOAD logic: Only run if the folder exists
if os.path.exists(DB_PATH):
    try:
        # allow_dangerous_deserialization is required for loading local FAISS files
        vector_store = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        print("✅ Existing FAISS index loaded successfully.")
    except Exception as e:
        print(f"⚠️ Could not load existing index: {e}")

def extract_text_from_pdf(file_stream):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text: text += page_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    global vector_store
    
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    files = request.files.getlist('file')
    documents = []
    
    for file in files:
        if file and file.filename.endswith('.pdf'):
            raw_text = extract_text_from_pdf(file.stream)
            if raw_text:
                doc = Document(page_content=raw_text, metadata={"source": file.filename})
                documents.append(doc)
    
    if documents:
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documents)

            # Create new or update existing
            if vector_store is None:
                vector_store = FAISS.from_documents(splits, embeddings)
            else:
                vector_store.add_documents(splits)

            # SAVE logic: Save to disk AFTER processing
            vector_store.save_local(DB_PATH)
            
            return jsonify({"message": "Files processed and index saved!", "filenames": [f.filename for f in files]})
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
    return jsonify({"message": "No valid text found"}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    global vector_store
    data = request.get_json()
    question = data.get('question', '')

    if vector_store is None:
        return jsonify({"answer": "Please upload a PDF first."}), 400

    try:
        relevant_docs = vector_store.similarity_search(question, k=5)
        context_text = "\n\n".join([f"Source: {d.metadata.get('source')}\n{d.page_content}" for d in relevant_docs])

        prompt_template = """Answer the question based ONLY on the context. 
        If unsure, say you don't know.
        
        Context: {context}
        Question: {question}"""
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        response = llm.invoke(prompt.format(context=context_text, question=question))
        
        return jsonify({"answer": response.content})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)