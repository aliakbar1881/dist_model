from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss
from pathlib import Path
from typing import List
from uuid import uuid4
import nltk
from nltk.tokenize import sent_tokenize



class Index:
    def __init__(self):
        pass
        
    def load_pdfs(self):
        dir_path = [path.name for path in Path(f"{self.dirname}/index/").iterdir() if path.is_dir()]
        files = []
        for file in Path(f"{self.dirname}/data/").iterdir():
            if file.suffix == '.pdf' and file.name not in dir_path:
                files.append(file)
        for file in files:
            self.index_pdf(file.name)
        data = []
        dir_path = [path for path in Path(f"{self.dirname}/index/").iterdir() if path.is_dir()]
        for index_path in dir_path:
            data.append(FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True))
        return data

    def index_pdf(filename):
        nltk.download('punkt')
        nltk.download('punkt_tab')
        pdf_loader = PDFMinerLoader(f"./data/{filename}")
        documents = pdf_loader.load()
        text = documents[0].page_content

        sentences = sent_tokenize(text)

        documents: List[Document] = [
            Document(page_content=sentence, metadata={"source": filename}) for sentence in sentences
        ]

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )


        uuids = [str(uuid4()) for _ in range(len(documents))]
        vector_store.add_documents(documents=documents, ids=uuids)
        vector_store.save_local(f"./index/{filename}")


if __name__ == "__main__":
    index = Index()
    pdfs = index.load_pdfs()
    print(pdfs)
    