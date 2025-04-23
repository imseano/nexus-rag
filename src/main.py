from Models.openAI import openAI, openAIEmbed
from utils import get_chunks_from_documents
from rag import RAGHandler
from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pydantic.deprecated.decorator # for pydantic compatibility with PyInstaller
import onnxruntime
from langchain_chroma import Chroma
import os 
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = openAI()
embeddings = openAIEmbed().embeddings
vector_store = None # Chroma(

#response = llm.constructResponse("What is chatGPT and why should I use it?")
rag = None # RAGHandler(vector_store)

class QueryRequest(BaseModel):
    query: str

class LoadRequest(BaseModel):
    folder_path: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query(request: QueryRequest):
    if rag is None:
        return {"message": "RAGHandler is not initialized. Please load a folder first."}
    response = rag.query_and_answer(request.query)
    return {"response": response}

@app.post("/load-folder")
async def load_folder(path: LoadRequest):
    global vector_store, rag  # Declare as global to update the global variables
    # Load documents from the specified folder path
    # Implement your loading logic here
    if path.folder_path == "":
        return {"message": "Folder path cannot be empty."}
    if not os.path.exists(path.folder_path):
        return {"message": f"Folder path {path.folder_path} does not exist."}
    if not os.path.isdir(path.folder_path):
        return {"message": f"Path {path.folder_path} is not a directory."}
    
    nested_path = os.path.join(path.folder_path, ".nexus", "vectorstore")
    if not os.path.exists(nested_path):
        print(f"Creating directory: {nested_path}")
        os.makedirs(nested_path)
    try:
        vector_store = Chroma(
            collection_name="testcol",
            embedding_function=embeddings,
            persist_directory=nested_path  # Use the corrected nested_path
        )
        rag = RAGHandler(vector_store)  # Update the global rag variable
    except Exception as e:
        print(f"Error initializing Chroma: {e}")
        return {"error": f"Failed to initialize Chroma: {str(e)}"}
    
    chunks = get_chunks_from_documents(path.folder_path)
    document_ids = vector_store.add_documents(documents=chunks)
    if not document_ids:
        return {"message": "No documents were loaded."}
    

    return {"message": f"Loaded documents from {path.folder_path}"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    # Uncomment the following lines to run the FastAPI app directly