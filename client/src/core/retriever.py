from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from pathlib import Path
from pydantic import BaseModel
from src.utils.connection import SocketIOClient


from src.core.generator import QwenGenerator
from src.core.index import Index
from src.utils.io import read


class Retriver:
    def __init__(self, dirname):
        load_dotenv()
        self.dirname = dirname
        self.generator = QwenGenerator()
        self.index = Index(self.dirname)
        self.pdfs = self.load_indexed_pdf()
        self.socket = SocketIOClient(self)
        self.socket()

    def retrieve(self, query, k, remote=True):
        results = []
        # get result from nodes information
        if remote:
            self.query_node(query)
            time.sleep(10)
            response = self.read_temp_file()
            results.append(response)
        # get result from local informations
        for vector_store in self.pdfs:
            senteces = self.similarity_search(vector_store, query, k)
            results.append(self.generator.generate(senteces, query))
        return results

    def load_indexed_pdf(self):
        return self.index.load_pdfs()

    def similarity_search(self, vector_store, query, k):
        return vector_store.similarity_search(query, k=k)

    def query_node(self, node, query, k=10):
        self.socket.send_query(query) 

    def read_temp_file(self):
        path = Path(self.dirname) / "temp/response.json"
        return read(path)

    def __call__(self, query, k=10):
        informations = self.retrieve(query, k)
        response = self.generator.generate(informations, query)
        return response


if __name__ == "__main__":
    import time
    retriver = Retriver('./')
    t1 = time.time()
    print(retriver("How to explain a CNN model layers?", k=10))
    t2 = time.time()
    print("Time to spend: ", t2 - t1)