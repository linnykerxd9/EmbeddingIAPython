import chromadb
from chromadb.utils.embedding_functions import openai_embedding_function
import os
from chromadb.errors import InvalidCollectionException
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

def InitChroma():
    print("Connecting to ChromaDB")
    global chroma_client
    current_dir = os.getcwd()
    data_folder = os.path.join(current_dir, "dataEmbeddingSmallTesteSemEmbedding")
    
    chroma_client = chromadb.PersistentClient(data_folder)

    return chroma_client

InitChroma()

def CreateCollection(collection_name):
    print("Creating collection {}".format(collection_name))
    global collection

    try:
        collection = chroma_client.get_collection(collection_name, embedding_function=openai_ef)
        print(f"Collection {collection_name} already exists.")
    except InvalidCollectionException:
        print(f"Collection {collection_name} does not exist. Creating new collection.")
        collection = chroma_client.create_collection(
            name=collection_name,
            embedding_function=openai_ef
        )
    return collection

def AddColections(documents,ids,metadatas):
    print("Adding documents to collection")
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas,
       # embeddings=embedding
    )

def GetCollectionByQueryText(query_texts,n_results):
    print("Querying collection")
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results,
    )
    return results

def GetCollectionByQueryEmbeddings(query_embedding,n_results):
    print("Querying collection")
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
    return results
