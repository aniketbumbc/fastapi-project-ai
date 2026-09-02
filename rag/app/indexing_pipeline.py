from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
pdf_path = Path('./pdf/React.pdf')

# pdf loader
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# split docs into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

#embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")


# create vector store
vector_store = QdrantVectorStore.from_documents(
    chunks,
    embedding=embedding_model,
    collection_name="react_docs",
    url="http://localhost:6333",
)

