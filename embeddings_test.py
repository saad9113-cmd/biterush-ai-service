from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

menu_items = [
    "Paneer Butter Masala - rich creamy tomato gravy with paneer cubes",
    "Veg Biryani - fragrant rice with mixed vegetables and spices",
    "Chicken Tikka - grilled marinated chicken pieces",
    "Masala Dosa - crispy rice crepe with spiced potato filling",
    "Chole Bhature - spicy chickpea curry with fried bread"
]

menu_embeddings = model.encode(menu_items)

query = "something spicy and vegetarian"
query_embedding = model.encode(query)

scores = util.cos_sim(query_embedding, menu_embeddings)[0]

ranked = sorted(zip(menu_items, scores), key=lambda x: x[1], reverse=True)

for item, score in ranked:
    print(f"{score:.3f}  {item}")