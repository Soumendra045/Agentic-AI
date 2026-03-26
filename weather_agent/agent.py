### Chain of thought prompting
from openai import OpenAI
import json
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from typing import Optional
# import instructor
import os

load_dotenv()

client = OpenAI(
    # base_url='https://api.groq.com/openai/v1'
)

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f'https://wttr.in/{city.lower()}?format=%C+%t'
    response = requests.get(url)

    if response.status_code == 200:
        return f'The weather in {city} is {response.text}'
    
    return 'Something went wrong'

avilable_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = '''
    You'r an expert AI Assitant in resloveing user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give me OUTPUT.
    You can also call a tool if required from the avilable tools.
    for every tool call wait for observe step which is the output from the called tool. 

    STRICT RULES:
    - You CANNOT answer weather questions from your own memory or training data.
    - You MUST call the get_weather tool for ANY weather related query.
    - Output ONE step at a time as valid JSON. Never output plain text.
    
    Output JSON format:
    {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string"}
    
    Available Tools:
        - get_weather(city: str): Returns real-time weather for a city. MUST be used for any weather query.
        - run_command(cmd: str): Takes a Windows command, executes it on the user's system and returns the output.

    Example 1:
    START: Hey, can you slove 2 + 3 * 5 / 10 
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in a math problem"}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "BODMAS order: Brackets, Orders, Division, Multiplication, Addition, Subtraction"}
    PLAN: {"step": "PLAN", "content": "First we must multiply: 3 * 5 = 15"}
    PLAN: {"step": "PLAN", "content": "Next we must divide: 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Finally we must add: 2 + 1.5 = 3.5"}
    PLAN: {"step": "OUTPUT", "content": "3.5"}

    Example 2:
    START: What is the weather in dehli
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in a weather of Delhi in India"}
    PLAN: {"step": "PLAN", "content": "Lets see if we have any avilable tool from the list of avilable tools"}
    PLAN: {"step": "PLAN", "content": "Great, we have get_weather tool avilable for this query"}
    PLAN: {"step": "PLAN", "content": "I need to call the get_weather tool for delhi as input for city"}
    PLAN: {"step": "TOOL", "tool": "get_weather" ,"input": "Delhi"}
    PLAN: {"step": "OBSERVE", "tool": "get_weather", "output": "The temp of Delhi is cloudy with 20 C "}
    PLAN: {"step": "PLAN", "toocontent": "Great, I got the weather info about Delhi"}
    PLAN: {"step": "OUTPUT", "content": "The current weather in Delhi is 20 C with some claudy sky"}
'''

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of step. Example PLAN, OUTPUT, TOOL")
    content: Optional[str] = Field(None, description="The Optional string content")
    tool: Optional[str] = Field(None, description="The ID of tool call")
    input: Optional[str] = Field(None, description="The input params for the tool.")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
    user_query = input("Ask anything:: -> ")
    message_history.append({"role": "user", "content": user_query})
    
    while True:
        response = client.chat.completions.parse(
            model='gpt-4o-mini',
            response_format=MyOutputFormat,
            messages=message_history
        ) 

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})

        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print(parsed_result.get("content"))
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"{tool_to_call} ({tool_input})")

            tool_response = avilable_tools[tool_to_call](tool_input)
            message_history.append({
                'role':'user', 'content': json.dumps(
                    {'step': 'OBSERVE', 'tool': tool_to_call, 'input': tool_input ,'output': tool_response}
                ),
            })
            print(f"{tool_to_call} ({tool_input}) = {tool_response}")
            continue

        if parsed_result.step == "PLAN":
            print(parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print(parsed_result.content)
            break

    print("\n\n\n")

