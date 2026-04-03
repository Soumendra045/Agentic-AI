from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
import os

load_dotenv()

llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# graph = graph_builder.compile()  #compile


def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


# DB_URL = "mongodb://admin:admin@localhost:27017/?authSource=admin"
DB_URL = os.getenv("DB_URL")
with MongoDBSaver.from_conn_string(DB_URL) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "silu"}}
    # Run :
    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["what is my name?"]}), config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    # print('\n\n updated_state', updated_state)
# /* (START) --> chatbot --> (END)

# //? State = {'messages':['Hey, there']}
# //? node runs = chatbot(state: ['Hey, there']) --> ['Hi, This is a massage from chatBot node']
