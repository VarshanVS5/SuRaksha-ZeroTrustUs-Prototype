import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role":"user",
            "content":"hello"
        }
    ]
)

print(response["message"]["content"])