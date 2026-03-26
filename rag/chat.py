# Retrive part
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

#? Vector Embeddings
embeddings = OpenAIEmbeddings(
    # model='text-embedding-3-large'  More cost 
    model='text-embedding-3-small',
)

vector_db = QdrantVectorStore.from_existing_collection(
    url='http://localhost:6333',
    collection_name='learning_rag',
    embedding=embeddings
)

# Take a INPUT
user_query = input("Ask Something: ")

# Relavant chunks from the vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])


SYSTEM_PROMPT = f'''
    You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file.

    When answering:
    - Give a proper explanation from the content
    - At the end always mention: 📄 Page Number: X | 📁 File: filename.pdf

    Context:
    {context}
'''

response = openai_client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_query},
    ]
)

print(f'🤖: {response.choices[0].message.content}')