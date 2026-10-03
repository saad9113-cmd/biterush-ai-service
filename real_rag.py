import chromadb
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("real_menu")

def ask(question):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=3)

    context = "\n".join(results['documents'][0])
    dish_ids = [meta['item_id'] for meta in results['metadatas'][0]]

    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}
Answer:"""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return {
        "message": response['message']['content'],
        "dish_ids": dish_ids
    }

result = ask("What's a good vegetarian main course?")
print("AI message:", result["message"])
print("Matched dish IDs:", result["dish_ids"])