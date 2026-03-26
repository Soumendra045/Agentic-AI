### Chain of thought prompting
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    base_url='https://api.groq.com/openai/v1'
)
SYSTEM_PROMPT = '''
    You'r an expert AI Assitant in resloveing user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give me OUTPUT.

    Rules:
    - Strictly follows the given JSON output format.
    - Only one step run at a time
    - The sequenceof steps is START(Where user gives input), PLAN (That can be multiple times) and finally OUTPUT (which is going to displeyed to the user )

    Output JSON format:
    {'step': 'START' | 'PLAN' | 'OUTPUT', "content": "string"}

    Example:
    START: Hey, can you slove 2 + 3 * 5 / 10 
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in a math problem"}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "BODMAS order: Brackets, Orders, Division, Multiplication, Addition, Subtraction"}
    PLAN: {"step": "PLAN", "content": "First we must multiply: 3 * 5 = 15"}
    PLAN: {"step": "PLAN", "content": "Next we must divide: 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Finally we must add: 2 + 1.5 = 3.5"}
    PLAN: {"step": "OUTPUT", "content": "3.5"}
'''

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("Ask anything:: -> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        response_format={ "type": "json_object" },
        messages=message_history
    ) 

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print(parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "PLAN":
        print(parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print(parsed_result.get("content"))
        break

print("\n\n\n")


# *! This is manualy 
# response = client.chat.completions.create(
#     model='llama-3.3-70b-versatile',
#     response_format={ "type": "json_object" },
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "can you give python program that calculte area of circle"},
#         {"role": "assistant", "content":json.dumps("To calculate the area of a circle, we need to use the formula A = πr^2, where A is the area and r is the radius of the circle. We can write a Python function to implement this.")},
#         {"role": "assistant", "content":json.dumps("We will import the math module for the value of pi and define a function to calculate the area of the circle.")},
#         {"role": "assistant", "content":json.dumps("The function will take the radius as input, calculate the area using the formula, and return the result. Then we will combine all the steps into a single function and execute it to get the final answer")},
#     ]
# )

# print(response.choices[0].message.content)