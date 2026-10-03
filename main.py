from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/assistant")
def ask_assistant(q: Question):
    response = ollama.chat(
        model='phi3',
        messages=[
            {'role': 'user', 'content': q.query}
        ]
    )
    return {"answer": response['message']['content']}