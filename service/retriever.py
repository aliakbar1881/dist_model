from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from openai import OpenAI
from index import index
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from pydantic import BaseModel


from model import OpenAIModel
from index import Index


class Retriver:
    def __init__(self, dirname):
        load_dotenv()
        self.dirname = dirname
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.model = OpenAIModel('openai')
        self.index = Index()
        self.pdfs = self.load_indexed_pdf()
        self.listen()

    def retrieve(self, query, k, remote=True):
        results = []
        # get result from nodes information
        if remote:
            for node in self.nodes:
                sentence = self.query_node(node, query, k=k)
                results.append(sentence)
        # get result from local informations
        for vector_store in self.pdfs:
            senteces = self.similarity_search(vector_store, query, k)
            results.append(self.model.generate(senteces, query))
        return results

    def load_indexed_pdf(self):
        return self.index.load_pdfs()

    def similarity_search(self, vector_store, query, k):
        return vector_store.similarity_search(query, k=k)

    def query_node(self, node, query, k=10):
        result = requests.post(node, data={"query" : query, "k" : k})
        return result.text

    def listen(self):
        class Query(BaseModel):
            query: str
            k: int

        app = FastAPI()


        @app.post("/query/")
        async def create_item(query: Query):
            return self.retrieve(query['query'], query['k'], remote=False)

    def __call__(self, query, k=10):
        informations = self.retrieve(query, k)
        response = self.model.generate(informations, query)
        return response


if __name__ == "__main__":
    retriver = Retriver('./')
    print(retriver("How to deploy a CNN model, ", k=10))
