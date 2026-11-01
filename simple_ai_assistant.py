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

# Safety limit: the max number of model rounds for one user question
MAX_STEPS = 5

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
    
    #Chained Tool Calling
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=Tools
        )
            
        msg = response.choices[0].message
        
        if not msg.tool_calls:
            break
        
        messages.append(msg)
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}
            
            try:
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result = fn(**func_args)
            except Exception as e:
                result = f"Error while running {func_name} : {e}"    
            
            
            
            messages.append(
                {
                    "role" : "tool",
                    "tool_call_id" : tool_call.id,
                    "content" : str(result),
                    
                }
     
            )
    
    else:
        #Ran out of steps: The model never gave the final answer    
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append(
            {
                "role" : "assistant",
                "content" : fallback
            }
        )
        print("Assistant:" +fallback)
        continue
    
 
    messages.append(
        {
            "role" : "assistant",
            "content" : msg.content
        }
    )
    
    
    
    
    
    
    print("Asisstant: " + msg.content)  #response from llm model which is qwen3:1.7b parameter
    print("Role:" + response.choices[0].message.role)