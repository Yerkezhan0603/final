import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import PyPDFLoader, WebBaseLoader, TextLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import tempfile
from pymongo import MongoClient

st.set_page_config(page_title="AI Knowledge Base", layout="wide")

st.markdown(
    """
    <style>
        .stApp { background-color: #121212; }
        .big-font { font-size:28px !important; color: #FFAA33; font-weight: bold; }
        .stButton>button { background-color: #FFAA33; color: white; font-size: 18px; border-radius: 10px; }
        .stTextInput>div>div>input { font-size: 16px !important; padding: 10px; border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

OLLAMA_MODEL = "llama3:latest"
VECTOR_DB_PATH = "vector_db"

llm = Ollama(model=OLLAMA_MODEL)

memory = ConversationBufferMemory()

MONGO_URI = "mongodb+srv://tolegenova:tolegenova@erke.0k8le.mongodb.net/?retryWrites=true&w=majority&appName=Erke"
DATABASE_NAME = "advanced"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
contributions = db.contributions

def google_search(query): 
    API_KEY = "e4a88d82e8dfc3e11a39733bdf82e7df2ae83a341cbb81a6921ac973ab3665c9"   
    url = f"https://serpapi.com/search.json?q={query}&api_key={API_KEY}" 
    try: 
        response = requests.get(url) 
        if response.status_code == 200: 
            results = response.json().get("organic_results", []) 
            if results: 
                return "\n".join(item.get("snippet", "") for item in results) 
        return "" 
    except Exception as e: 
        st.error(f"Error searching Google: {e}") 
        return ""  

def load_documents(file, file_type):
    if file_type == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        loader = PyPDFLoader(tmp_file_path)
    elif file_type == "text":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        loader = TextLoader(tmp_file_path)
    elif file_type == "web":
        loader = WebBaseLoader(file)
    documents = loader.load()
    return documents


def create_vector_db(documents):
    embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)
    return vectorstore


def load_vector_db():
    embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
    vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return vectorstore


def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='coolwarm').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def store_contribution(user, query, response, file_type, file_name):
    contribution_data = {
        "user": user,
        "query": query,
        "response": response,
        "file_type": file_type,
        "file_name": file_name,
        "timestamp": st.session_state.get('timestamp')
    }
    contributions.insert_one(contribution_data)

st.title("🚀 AI-Powered Knowledge Base")
st.write("Welcome to the AI-powered knowledge base!")

user = st.text_input("Enter your name:")
if not user:
    st.stop()

st.header("📄 Upload Documents")
file_type = st.radio("Document Type", ["pdf", "text", "web"])
if file_type == "web":
    file = st.text_input("Enter URL:")
    file_name = file
else:
    file = st.file_uploader("Upload a file", type=["pdf", "txt"])
    file_name = file.name if file else None

if file:
    documents = load_documents(file, file_type)
    vectorstore = create_vector_db(documents)
    st.success("✅ Documents successfully uploaded and processed!")

st.header("🔍 Ask a Question")
query = st.text_input("Enter your question:")
if query:
    st.warning("Searching the internet...")
    context = google_search(query)

    if not os.path.exists(VECTOR_DB_PATH):
        st.error("❌ Vector database not found. Upload documents first.")
    else:
        vectorstore = load_vector_db()
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), memory=memory)
        response = qa_chain.run(f"Context:\n{context}\n\nQuestion:\n{query}\nanswer:")
        st.write("🧠 Answer:", response)

        store_contribution(user, query, response, file_type, file_name)
        st.success("✅ Question and Answer recorded!")

st.header("📊 Data Visualization")
if st.button("Generate Word Cloud"):
    if not os.path.exists(VECTOR_DB_PATH):
        st.error("❌ Vector database not found. Upload documents first.")
    else:
        vectorstore = load_vector_db()
        all_text = " ".join([doc.page_content for doc in vectorstore.docstore._dict.values()])
        generate_word_cloud(all_text)

st.header("👥 User Management")
if st.button("Show Chat History"):
    st.write(memory.buffer)