from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from Models.openAI import openAI, openAIEmbed

from langchain import hub
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph


llm = openAI()
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

class RAGHandler:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.prompt = hub.pull("rlm/rag-prompt")
        self.example_messages = self.prompt.invoke(
        {"context": "(context goes here)", "question": "(query goes here)"}
    ).to_messages()

    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        print(f"Prompt: {messages}")
        response = llm.constructResponse(messages)
        return {"answer": response}


    def query_and_answer(self, query: str):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        result = graph.invoke({"question": query})

        print(f'Context: {result["context"]}\n\n')
        print(f'Answer: {result["answer"]}')

        return result["answer"]