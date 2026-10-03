import chromadb
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("menu")

menu_items = [
    "Paneer Butter Masala - rich creamy tomato gravy with paneer cubes, vegetarian, price 180 rupees",
    "Veg Biryani - fragrant rice with mixed vegetables and spices, vegetarian, price 150 rupees",
    "Chicken Tikka - grilled marinated chicken pieces, non-vegetarian, price 220 rupees",
    "Masala Dosa - crispy rice crepe with spiced potato filling, vegetarian, price 90 rupees",
    "Chole Bhature - spicy chickpea curry with fried bread, vegetarian, price 120 rupees"
]

embeddings = model.encode(menu_items).tolist()
ids = [f"item_{i}" for i in range(len(menu_items))]
collection.add(documents=menu_items, embeddings=embeddings, ids=ids)

def ask(question):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=3)
    context = "\n".join(results['documents'][0])

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
    return response['message']['content']

print(ask("What's a good spicy vegetarian dish under 150 rupees?"))
print("---")
print(ask("Do you have any desserts?"))