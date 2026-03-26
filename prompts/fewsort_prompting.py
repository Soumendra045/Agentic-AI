## Few sort prompting
# * Zero sort prompting
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
client = OpenAI(
    base_url='https://api.groq.com/openai/v1'
)
#! Few sort prompting: Directly giving  the inst to model  and few example.
SYSTEM_PROMPT = '''You should answer the only and only coding related questions. Don not ans anything else. Simply say sorry. You name is Silu

Rule
- Strictly follow the json format

Output Format:
{{
"code": "string" or null,
"isCodingQuestion": boolean
}}

Example:
Q1) give me (a+b)^2
  ans: {{"code": null, "isCodingQuestion": False}}

Q2) Give a python code for adding 2 numbers
 ans:{{"Code": def slove(a, b):
                 return a+b, "isCodingQuestion": True}}
'''

response =  client.chat.completions.create(
    #??// model="gpt-4o-mini", This is paid of open ai
    model="llama-3.3-70b-versatile", #??This is free of groq
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "can you give python program that calculte area of circle"}
    ]
)

print(response.choices[0].message.content)
