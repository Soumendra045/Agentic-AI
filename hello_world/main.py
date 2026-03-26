from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
client = OpenAI(
    base_url='https://api.groq.com/openai/v1'
)

response =  client.chat.completions.create(
    #??// model="gpt-4o-mini", This is paid of open ai
    model="llama-3.3-70b-versatile", #??This is free of groq
    messages=[
        {"role": "system", "content": "You are the math except and only and only answer the math related things. If the thing is not math related then just reply sorry this is not my part"},
        {"role": "user", "content": "Hey, can you give the explanation for (a+b)(a+b)"}
    ]
)

print(response.choices[0].message.content)