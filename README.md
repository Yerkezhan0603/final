## **Overview**  
This is a collaborative AI-powered knowledge base built with **Streamlit**, **LangChain**, **FAISS**, and **OpenAI**. It allows users to:  
- Upload and process documents (PDFs, text files, and web content)  
- Ask natural language questions and get AI-generated answers  
- Visualize insights using word clouds  
- Store and manage contributions in MongoDB  

---

## Features  
✅ LLM-based chatbot using Llama3  
✅ FAISS-powered knowledge retrieval  
✅ Google Search API integration  
✅ PDF, TXT, and Web content ingestion  
✅ Word cloud analytics for documents  
✅ Chat history storage in MongoDB  
✅ User contributions management  

---

## Installation  
### Prerequisites  
Ensure you have Python 3.8+ installed.  

### Clone the Repository  
git clone https://github.com/your-username/ai-knowledge-base.git
cd ai-knowledge-base

### Create a Virtual Environment  
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

### Install Dependencies  
pip install -r requirements.txt

---

## Configuration  
### 1. Set up Environment Variables  
Create a .env file in the app/ directory with the following variables:  
MONGO_URI = "mongodb+srv://tolegenova:tolegenova@erke.0k8le.mongodb.net/?retryWrites=true&w=majority&appName=Erke"
API_KEY = "e4a88d82e8dfc3e11a39733bdf82e7df2ae83a341cbb81a6921ac973ab3665c9"
OLLAMA_MODEL = "llama3:latest"
VECTOR_DB_PATH = "vector_db"

## Usage  
### Run the Web App  
treamlit run final.py
Access the knowledge base via your browser at http://localhost:8501.  

---

## How It Works  
### 1. Document Upload and Processing  
- Upload PDFs, text files, or provide a URL for web content extraction.  
- Documents are processed and embedded into a FAISS vector database for efficient retrieval.  

### 2. AI-Powered Q&A  
- Users can ask natural language questions.  
- The system searches the FAISS vector database and Google Search for context.  
- The answer is generated using the Llama3 model and displayed to the user.  

### 3. Data Visualization  
- Generate Word Clouds from uploaded documents to visualize key terms and insights.  

### 4. User Contributions Management  
- Questions and answers are stored in MongoDB.  
- Contributions can be reviewed and managed for collaborative knowledge sharing.
