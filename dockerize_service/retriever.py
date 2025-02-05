from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from openai import OpenAI
from index import index
from dotenv import load_dotenv


class Retriver:
    def __init__(self, dirname):
        load_dotenv()
        self.dirname = dirname
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.indexes = self.load_indexes()
        self.model = OpenAI()

    def index(self, filename):
        index(filename)

    def __call__(self, query, k=10):
        results = []
        for vector_store in self.indexes:
            senteces = self.retrieve(vector_store, query, k)
            results.append(self.generate(senteces, query))
        response = self.generate(results, query)
        return response

    def retrieve(self, vector_store, query, k):
        return vector_store.similarity_search(query, k=k)

    def load_indexes(self):
        dir_path = [path.name for path in Path(f"{self.dirname}/index/").iterdir() if path.is_dir()]
        files = []
        for file in Path(f"{self.dirname}/data/").iterdir():
            if file.suffix == '.pdf' and file.name not in dir_path:
                files.append(file)
        for file in files:
            self.index(file.name)
        data = []
        dir_path = [path for path in Path(f"{self.dirname}/index/").iterdir() if path.is_dir()]
        for index_path in dir_path:
            data.append(FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True))
        return data

    def summerize(self, sentences, query):
        prompt = f"""

        """

    def generate(self, sentences, query):
        sentences = [sentence.page_content if isinstance(sentence, Document) else sentence for sentence in sentences]
        prompt = f"""
        Answer the request only using the below senteces.
        senteces:
        
        {"              ".join(sentences)}

        Request: {query}"""
        return self.query(prompt)

    def query(self, prompt):
        completion = self.model.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "Combine only Context section provided and answer based on it only, summerizer it and dont use of your knowlegde in answer."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    retriver = Retriver('./')
    print(retriver("How to deploy a CNN model, ", k=10))
