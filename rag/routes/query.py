from fastapi import APIRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


router = APIRouter(prefix="/query", tags=["query"])


openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant that can answer questions about the React documentation.
You are given a question and you need to answer it based on the React documentation.
Plase answer the question in the same language as the question. Add page number to the answer.
"""


#embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large" )

#vector store
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="react_docs",
    url="http://localhost:6333",
)


@router.post("/")
def query(query: str):
   search_results =  vector_store.similarity_search(query)
   context = " ".join([
    f"Page {result.metadata['page']}: {result.page_content}" for result in search_results
   ])
   SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE + "\n\n" + context

   response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
   )
   return {"message": "Query received", "query": query, "search_results": context, "answer": response.choices[0].message.content}