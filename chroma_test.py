import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("menu")

menu_items = [
    "Paneer Butter Masala - rich creamy tomato gravy with paneer cubes",
    "Veg Biryani - fragrant rice with mixed vegetables and spices",
    "Chicken Tikka - grilled marinated chicken pieces",
    "Masala Dosa - crispy rice crepe with spiced potato filling",
    "Chole Bhature - spicy chickpea curry with fried bread"
]

embeddings = model.encode(menu_items).tolist()
ids = [f"item_{i}" for i in range(len(menu_items))]

collection.add(
    documents=menu_items,
    embeddings=embeddings,
    ids=ids
)

query = "something spicy and vegetarian"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

for doc, dist in zip(results['documents'][0], results['distances'][0]):
    print(f"{dist:.3f}  {doc}")