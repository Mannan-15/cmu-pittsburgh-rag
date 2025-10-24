from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama 
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
import ollama

# Load Retriever
print("Loading retriever from disk...")
embedding_model = HuggingFaceEmbeddings(
    model_name="facebook/contriever-msmarco",
    model_kwargs={'device': 'cpu'}
)
vector_store = Chroma(
    persist_directory = r"C:\Users\Mannan Golchha\CMU assign 2\cmu-pittsburgh-rag\chroma_db", 
    embedding_function = embedding_model
)
retriever = vector_store.as_retriever(search_kwargs = {"k" : 3})
print("✅ Retriever loaded.")

query = input("User : ")

retrieved_docs = retriever.invoke(query)

context_string = ""
for doc in retrieved_docs:
    context_string += doc.metadata['source'] + "\n" + doc.page_content + "\n\n"

prompt_template = f"""
Answer the question based only on this context:
{context_string}

Question: {query}
"""

response = ollama.chat(
    model='mistral',
    messages=[
        {'role': 'user', 'content': prompt_template}
    ]
)

print(f"---"*51)
print(f"Model : \n ---{response['message']['content']} \n\n")