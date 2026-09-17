# NEXA-RAG ✦

> **An AI-powered document knowledge assistant built by Hasandeep Kaur.**

NEXA-RAG lets users upload **PDF, TXT, and DOCX files**, search their content using semantic retrieval, and ask questions about the documents using **Google Gemini 3.5 Flash**.

It combines document processing, AI embeddings, vector search, and Retrieval-Augmented Generation (RAG) into a simple interactive application.

---

## 🚀 Live Demo

**Try NEXA-RAG:**
`ADD YOUR STREAMLIT LINK HERE`

---

## ✨ Features

* 📄 Upload PDF, TXT, and DOCX files
* 🔎 Semantic document search
* 🤖 Gemini 3.5 Flash AI responses
* 📚 Answers based on uploaded documents
* 🔗 Source information for retrieved content
* 🗄️ ChromaDB vector database
* 🧠 Sentence Transformers embeddings
* ♻️ Duplicate document protection
* 🗑️ Remove individual documents
* ⚙️ Adjustable retrieval settings
* 💬 Interactive chat interface
* 🛡️ Prompt-injection-aware document handling

---

## 🧠 How It Works

```text
Upload Documents
       ↓
Extract & Clean Text
       ↓
Split Into Chunks
       ↓
Create Embeddings
       ↓
Store in ChromaDB
       ↓
Search Relevant Content
       ↓
Send Context to Gemini
       ↓
Generate Answer + Sources
```

---

## 🏗️ Architecture

```text
NEXA-RAG
│
├── app.py
│
├── src/
│   ├── ingestion
│   ├── embeddings
│   ├── storage
│   ├── retrieval
│   └── generation
│
├── tests/
│
├── data/
│   └── uploads/
│
├── vectorstore/
│   └── chroma/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

| Technology              | Purpose                   |
| ----------------------- | ------------------------- |
| Python                  | Application development   |
| Streamlit               | Web interface             |
| ChromaDB                | Vector database           |
| Sentence Transformers   | Text embeddings           |
| Google Gemini 3.5 Flash | AI generation             |
| PyMuPDF                 | PDF processing            |
| python-docx             | DOCX processing           |
| python-dotenv           | Environment configuration |
| pytest                  | Testing                   |

---

## ⚙️ Run Locally

### 1. Clone the repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd NEXA-RAG
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Add Gemini API credentials

Create a `.env` file:

```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
GEMINI_MODEL="gemini-3.5-flash"
```

**Never upload your API key to GitHub.**

### 5. Start the application

```powershell
streamlit run app.py
```

---

## 🧪 Testing

Run:

```powershell
python -m compileall app.py src tests
```

Then:

```powershell
python -m pytest -q
```

---

## ☁️ Deployment

NEXA-RAG can be deployed using Streamlit Community Cloud.

Add your Gemini credentials through Streamlit **Secrets**:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-3.5-flash"
```

Never expose your API key in the repository or screenshots.

---

## 📸 Screenshots

Add screenshots of:

1. Main NEXA-RAG interface
2. Document upload/indexing
3. Retrieval results
4. Gemini-generated answer

Example:

```markdown
![NEXA-RAG Interface](docs/screenshots/main-interface.png)

![Document Retrieval](docs/screenshots/retrieval.png)

![AI Response](docs/screenshots/answer.png)
```

---

## 🔮 Future Improvements

* OCR for scanned PDFs
* Local LLM support
* Multiple knowledge bases
* Better search and reranking
* Streaming AI responses
* Chat export
* RAG evaluation
* User authentication
* Multi-user support

---

## 💡 What NEXA-RAG Demonstrates

NEXA-RAG demonstrates practical experience with:

* Retrieval-Augmented Generation
* Large Language Models
* Semantic search
* Vector databases
* Text embeddings
* Document processing
* Python application development
* Streamlit
* API integration
* Automated testing
* AI security considerations

---

## 👩‍💻 Author

### Hasandeep Kaur

**BCA | AI & Data Projects | Software & Analytics**

NEXA-RAG is an independent portfolio project exploring practical applications of **AI, RAG, semantic search, vector databases, and LLM-powered document assistants**.

---

