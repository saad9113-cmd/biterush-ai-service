import mysql.connector
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT item_id, item_name, category, price, is_available
    FROM Menu_Items
    WHERE is_available = 1
""")
menu_items = cursor.fetchall()
cursor.close()
conn.close()

print(f"Fetched {len(menu_items)} available menu items.")

NON_VEG_KEYWORDS = ["chicken", "mutton", "fish", "prawn", "egg", "beef", "pork", "meat"]

def guess_veg_status(name):
    name_lower = name.lower()
    for word in NON_VEG_KEYWORDS:
        if word in name_lower:
            return "non-vegetarian"
    return "vegetarian"

documents = []
ids = []
metadatas = []

for item in menu_items:
    veg_status = guess_veg_status(item["item_name"])
    text = f"{item['item_name']} - {item['category']}, {veg_status}, price {item['price']} rupees"
    documents.append(text)
    ids.append(str(item["item_id"]))
    metadatas.append({
        "item_id": item["item_id"],
        "price": float(item["price"]),
        "category": item["category"]
    })

model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
embeddings = model.encode(documents).tolist()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("real_menu")

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

print("Menu loaded into Chroma successfully.")