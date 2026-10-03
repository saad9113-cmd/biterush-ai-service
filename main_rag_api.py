from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

print("GROQ KEY LOADED:", os.getenv("GROQ_API_KEY")[:10] if os.getenv("GROQ_API_KEY") else "NOT FOUND")

app = FastAPI()

model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("real_menu")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Question(BaseModel):
    question: str

@app.post("/rag-query")
def rag_query(q: Question):
    q_embedding = model.encode(q.question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=3)

    context = "\n".join(results['documents'][0])
    dish_ids = [meta['item_id'] for meta in results['metadatas'][0]]

    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {q.question}
Answer:"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "message": response.choices[0].message.content,
        "dish_ids": dish_ids
    }