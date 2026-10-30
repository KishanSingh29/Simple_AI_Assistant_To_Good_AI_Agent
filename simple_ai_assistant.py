from openai import OpenAI

client = OpenAI(
    base_url="http://172.29.16.1:11434/v1",
    api_key="dummy_key"
)

response = client.chat.completions.create(
    model="qwen3:1.7b",
    messages=[
        {
            "role":"user",
            "content":"Hello LLM!"
        }
    ]
)

print("LLM Response:")
print(response.choices[0].message.content)  #response from llm model which is qwen3:1.7b parameter