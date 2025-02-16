from dotenv import load_dotenv
import requests
from fastapi import FastAPI
import uvicorn 
from pydantic import BaseModel


from src.core.generator import QwenGenerator
from src.core.index import Index


class Retriver:
    def __init__(self, dirname):
        load_dotenv()
        self.dirname = dirname
        self.generator = QwenGenerator()
        self.index = Index(self.dirname)
        self.pdfs = self.load_indexed_pdf()
        self.nodes = []

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
            results.append(self.generator.generate(senteces, query))
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
        async def query(query: Query):
            return self.retrieve(query['query'], query['k'], remote=False)

        uvicorn.run(app, host="0.0.0.0", port=8000)

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