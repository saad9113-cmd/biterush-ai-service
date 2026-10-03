import ollama

response = ollama.chat(
    model='phi3',
    messages=[
        {
            'role': 'user',
            'content': 'What is a good vegetarian dish under 200 rupees?'
        }
    ]
)

print(response['message']['content'])