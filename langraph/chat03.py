from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    lllm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    print('chatBot node', state)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': state.get('user_query')}]
    )
    state['lllm_output'] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal['chatbot_gemini', 'endnode']:
    """Use an LLM to judge if the response is good enough."""
    
    eval_prompt = f"""You are a strict response quality evaluator.

User Query: {state.get('user_query')}
LLM Response: {state.get('lllm_output')}

Is this response accurate, helpful, and complete? 
Reply with ONLY one word: GOOD or BAD."""

    eval_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': eval_prompt}]
    )

    verdict = eval_response.choices[0].message.content.strip().upper()
    print(f'Evaluator verdict: {verdict}')

    is_good = verdict == 'GOOD'
    state['is_good'] = is_good

    return 'endnode' if is_good else 'chatbot_gemini'


def chatbot_gemini(state: State):
    print('chatBot gemini node', state)
    response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=[{'role': 'user', 'content': state.get('user_query')}]
    )
    state['lllm_output'] = response.choices[0].message.content
    return state


def endnode(state: State):
    print('End node', state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('chatbot_gemini', chatbot_gemini)
graph_builder.add_node('endnode', endnode)

graph_builder.add_edge(START, 'chatbot')
graph_builder.add_conditional_edges('chatbot', evaluate_response)

graph_builder.add_edge('chatbot_gemini', 'endnode')
graph_builder.add_edge('endnode', END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({'user_query': 'Hey, what is 2+2?'}))
print(updated_state)