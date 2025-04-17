from pinecone import Pinecone, ServerlessSpec
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def create_index(index_name="screenplays"):
    pc.create_index(
        name=index_name,
        dimension=1024, # Replace with your model dimensions
        metric="cosine", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )
     # Wait for the index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

def save_vector_embeddings(data, namespace, index_name):
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[d['text'] for d in data],
        parameters={"input_type": "passage", "truncate": "END"}
    )
    print("embeddings[0]", embeddings[0])

    index = pc.Index(index_name)

    vectors = []
    for d, e in zip(data, embeddings):
        vectors.append({
            "id": d['id'],
            "values": e['values'],
            "metadata": {'text': d['text']}
        })

    index.upsert(
        vectors=vectors,
        namespace=namespace
    )
    print(index.describe_index_stats())

import re
from typing import List, Tuple, Dict

def clean_and_chunk_text(text: str) -> List[Dict[str, str]]:
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,          # max characters/tokens per chunk
        chunk_overlap=100,       # preserve context overlap
        separators=[
            "\n\n",              # paragraph
            "\n",                # line
            #".", "!", "?"        # sentence
        ]
    )
    for line_i, line in enumerate(text.split("\n")):
        # Recursively split only if scene is too long
        scene_chunks = splitter.split_text(line)
        for idx, chunk in enumerate(scene_chunks):
            if chunk == '':
                continue
            all_chunks.append({
                "id": f"{line_i}_{idx}",
                "text": chunk,
            })
    return all_chunks

def save_document_embeddings(user_id: str, file_name: str, text: str) -> Tuple[int, str, str]:
    namespace = f"{file_name}-{user_id}-client-documents"
    index_name = "screenplays"

    # Clean and chunk the text
    chunks = clean_and_chunk_text(text)
    print(chunks)
    
    # Save embeddings to Pinecone
    for i in range(0, len(chunks), 96):
        batch = chunks[i:i + 96]
        save_vector_embeddings(batch, namespace=namespace, index_name=index_name)

    return len(chunks), namespace, index_name


def query_related_paragraph(query, user_id, file_name, index_name = "screenplays"):
    namespace = f"{file_name}-{user_id}-client-documents"
    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )
    
    index = pc.Index(index_name)
    results = index.query(
        namespace=namespace,
        vector=embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )

    print(results)
    return results