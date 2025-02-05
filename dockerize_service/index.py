from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss
from typing import List
from uuid import uuid4
import nltk
from nltk.tokenize import sent_tokenize


def index(filename):
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
    index('')