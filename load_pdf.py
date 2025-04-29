from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import pickle

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Load all PDFs in the "pdfs" directory
docs = []
for filename in os.listdir('data'):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join("data", filename))
        docs.extend(loader.load())
print("hello")
# Split text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
documents = text_splitter.split_documents(docs)
print("hello1")
# Create FAISS vectorstore
vectorstore = FAISS.from_documents(documents, embedding)
print("hello3")

# ✅ Save vectorstore using FAISS's method (not pickle!)
vectorstore.save_local("faiss_index")

print("✅ Vectorstore saved to faiss_store.pkl")
