# ??/Zero sort prompting
from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()

client = OpenAI(
    base_url='https://api.groq.com/openai/v1'
)

SYSTEM_PROMPT = 'You should answer the only and only coding related questions. Don not ans anything else. Simply say sorry. You name is Silu'

response =  client.chat.completions.create(
    #??// model="gpt-4o-mini", This is paid of open ai
    model="llama-3.3-70b-versatile", #??This is free of groq
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, Tell me a zoke"}
    ]
)

print(response.choices[0].message.content)

#  /* 1. Zero sort prompting : The model is given a direct question or task without prior examples*/