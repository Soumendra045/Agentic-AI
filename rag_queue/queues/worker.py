from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

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

def process_query(query: str):
    print('Searching chunks', query)
    search_results = vector_db.similarity_search(query=query)
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
            {'role': 'user', 'content': query},
        ]
    )
    print(f'🤖: {response.choices[0].message.content}')
    return response.choices[0].message.content