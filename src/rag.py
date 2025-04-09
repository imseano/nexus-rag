import bs4
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

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    print(f"Prompt: {messages}")
    response = llm.constructResponse(messages)
    return {"answer": response}

embeddings = openAIEmbed().embeddings

vector_store = Chroma(
    collection_name="testcol",
    embedding_function=embeddings,
    persist_directory="./testdir"
)

bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()

assert len(docs) == 1
#print(f"Total characters: {len(docs[0].page_content)}")
#print(docs[0].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True,
)
all_splits = text_splitter.split_documents(docs)

document_ids = vector_store.add_documents(documents=all_splits)

prompt = hub.pull("rlm/rag-prompt")

example_messages = prompt.invoke(
    {"context": "(context goes here)", "question": "(query goes here)"}
).to_messages()

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

result = graph.invoke({"question": "What is the main idea of the article?"})

print(f'Context: {result["context"]}\n\n')
print(f'Answer: {result["answer"]}')