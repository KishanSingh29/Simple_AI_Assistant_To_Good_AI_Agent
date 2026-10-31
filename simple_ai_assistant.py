from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() #by default looks for .env file and load all variable in environment file from .env


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append(
    {
        "role" : "system",
        "content" : "Act like a very  humble agent and respond always under 10 words." 
    }
)

while True:
    user_input = input("\n Kishan:")
    
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break
    
    messages.append(
        {
            "role":"user",
            "content": user_input
        }
    )
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )
    
    messages.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
    )
    
    
    print("Asisstant: " + response.choices[0].message.content)  #response from llm model which is qwen3:1.7b parameter
    print("Role:" + response.choices[0].message.role)