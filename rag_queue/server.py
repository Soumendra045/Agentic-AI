from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query


app = FastAPI()

@app.get('/')
def root():
    return {'status': 'server is up and running'}

@app.post('/chat')
def chat(
        query: str = Query(..., description="The chat Query of user")
):
    job = queue.enqueue(process_query, query)

    return {'status': 'queued', 'job_id': job.id }

@app.get('/job-status')
def get_result(
        job_id: str = Query(..., description='job-id')
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {'result': result}