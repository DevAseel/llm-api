from fastapi import FastAPI, Request
from llama_cpp import Llama
import copy
import requests 
import asyncio
from sse_starlette import EventSourceResponse

# loading the model 
print("Loading Model...")
vicuna = "./model/ggml-vic7b-uncensored-q5_1.bin"
gptall= "./model/koala-7B.ggmlv3.q4_0.bin"
llm = Llama(model_path=gptall, n_threads=8)

print("Model Loaded!")

app = FastAPI()


@app.get('/')
async def healthCheck():
    return {"status": "App is healthy!"}

@app.get('/chat')
async def chat(request: Request):
    stream = llm(
            "Question: Who is Elon Musk? Answer:",
            max_tokens=16,
            stop=['\n', " Q:"],
            stream=True,
            temperature=0.8,
            top_p=0,
            top_k=67,
            )

    async def async_gen():
        for item in stream:
            yield item

    async def server_sent_events():
        async for item in async_gen():
            if await request.is_disconnected():
                break
            results = copy.deepcopy(item)
            text = results["choices"][0]["text"]

            yield {"data": text}
    return EventSourceResponse(server_sent_events())
