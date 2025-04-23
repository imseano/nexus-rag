import os
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
]

markdownSplitter = MarkdownHeaderTextSplitter(headers, False, True)

def get_chunks_from_documents(rootname: str):
    chunks = []
    for root, _, files in os.walk(rootname):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Split the content into chunks based on headers
                    split_content = markdownSplitter.split_text(content)
                    print(split_content)
                    chunks.extend(split_content)

    print(f"Total chunks: {len(chunks)}")
    return chunks
