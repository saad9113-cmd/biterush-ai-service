from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from groq import Groq
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HF_TOKEN = os.getenv("HF_TOKEN")

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("real_menu")


def get_embedding(text):
    response = requests.post(
        "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )
    return response.json()


class Question(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/rag-query")
def rag_query(q: Question):
    try:
        q_embedding = get_embedding(q.question)
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
        answer = response.choices[0].message.content

        return {
            "message": answer,
            "dish_ids": dish_ids
        }

    except Exception as e:
        print("FULL ERROR:", repr(e))
        return {"error": str(e)}