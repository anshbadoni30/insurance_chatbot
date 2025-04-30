import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini embedding model
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# ✅ Load FAISS vectorstore using `load_local` (no pickle)
vectorstore = FAISS.load_local("faiss_index", embeddings=embedding, allow_dangerous_deserialization=True)

# Default prompt for the assistant
DEFAULT_PROMPT = """
You are an intelligent insurance assistant. 
Answer the user's query clearly and concisely using bullet points, numbered steps, or sections when appropriate.
Only give answers related  to insurance
ALWAYS use Markdown-style formatting like:
- Bullet points
- Headings
- Line breaks

Make the response easy to read and user-friendly.
"""

# Keywords that signal fallback
FALLBACK_KEYWORDS = [
    "not sure", "don't know", "no idea", "unsure", "can't help",
    "i'm confused", "unavailable", "uncertain", "no information",
    "outside my scope", "irrelevant", "unanswerable", "cannot answer"
]

FALLBACK_RESPONSE = (
    "I'm sorry, I couldn't find the right information for your query. "
    "Please reach out to our human agent at 📞 +919136497175 for assistance."
)

# Get similar documents from the knowledge base
def get_knowledge_base_answer(query):
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return None
    return "\n".join([doc.page_content for doc in docs])

# Main response handler
def handle_response(user_query):
    context = get_knowledge_base_answer(user_query)

    if context:
        prompt = f"{DEFAULT_PROMPT}\n\nContext:\n{context}\n\nUser: {user_query}\nAssistant:"
    else:
        prompt = f"{DEFAULT_PROMPT}\n\nUser: {user_query}\nAssistant:"

    # tuning of Settings
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    #generation_config=generation_config,
    )
    response = model.generate_content(prompt)
    reply = response.text.strip()

    if any(keyword in reply.lower() for keyword in FALLBACK_KEYWORDS):
        return FALLBACK_RESPONSE
    else:
        return reply
