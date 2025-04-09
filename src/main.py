from Models.openAI import openAI
from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage

app = FastAPI()

llm = openAI()

#response = llm.constructResponse("What is chatGPT and why should I use it?")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query(query: str):
    messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=query)
            ]
    response = llm.constructResponse(messages)
    return {"response": response}