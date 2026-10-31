from openai import OpenAI
from dotenv import load_dotenv
from tools import Tools, FUNCTION_NAME_TO_FUNCTION_MAP
import os
import json

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
        messages=messages,
        tools=Tools
    )
    
    messages.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
    )
    
    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)
        
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            
            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)
            
            messages.append(
                {
                    "role" : "tool",
                    "tool_call_id" : tool_call.id,
                    "content" : str(result),
                    
                }
            )
    
        #2nd call to llm api
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        
        msg = response.choices[0].message
        
    messages.append(
        {
            "role" : "assistant",
            "content" : msg.content
        }
    )
    
    
    
    
    
    
    print("Asisstant: " + msg.content)  #response from llm model which is qwen3:1.7b parameter
    print("Role:" + response.choices[0].message.role)