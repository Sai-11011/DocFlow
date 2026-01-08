from google import genai
from flask import Flask , request , render_template, jsonify
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
app = Flask(__name__)

pdf_content = ""

UPLOAD_FOLDER = "uploaded_pdfs" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_text(file_stream):
    text = ""
    reader = PyPDF2.PdfReader(file_stream)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
        else:
            print(f"Warning: Page {i} returned no text.") #DEBUG
    return text

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    global pdf_content
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        pdf_content = extract_text(file.stream)
        return jsonify({"message":"File uploaded and text extracted successfully"})

    return jsonify({"message": "File upload failed"}), 400



@app.route('/ask', methods=['POST'])
def ask_question():
    global pdf_content
    question = request.json.get('question', '')

    if not pdf_content:
        return {"answer": "No PDF content available. Please upload a PDF first."}, 400
    
    if not question:
        return {"answer": "No question provided."}, 400

    prompt = f"""
    You are a helpful assistant. Answer the question based ONLY on the provided context below.
    Context from the PDF: 
    {pdf_content}
    Question: 
    {question}
    """

    response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
    return jsonify({"answer": response.text})


app.run(port=5000)