from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import ollama
import pandas as pd
import json
from tqdm import tqdm
import re
import evaluate
import string
from collections import Counter
import numpy as np


#-------------------------------------------------------------- Storing Responses of Model ------------------------------------------------------------------


# print("Loading retriever from disk...")
# embedding_model = HuggingFaceEmbeddings(
#     model_name="facebook/contriever-msmarco",
#     model_kwargs={'device': 'cpu'}
# )
# vector_store = Chroma(
#     persist_directory=r"C:\Users\Mannan Golchha\CMU assign 2\cmu-pittsburgh-rag\chroma_db", 
#     embedding_function=embedding_model
# )
# retriever = vector_store.as_retriever(search_kwargs={"k": 3})
# print("✅ Retriever loaded.")

# --- Load Questions & Answers ---
d1 = pd.read_csv(r"C:\Users\Mannan Golchha\CMU assign 2\cmu-pittsburgh-rag\data\train\train.csv")
d2 = pd.read_csv(r"C:\Users\Mannan Golchha\CMU assign 2\cmu-pittsburgh-rag\data\test\test.csv")

questions = list(d1['question'])
questions.extend(list(d2['question']))

answers = list(d1['answer'])
answers.extend(list(d2['answer']))

# # --- Retrieve Documents ---
# print("Retrieving documents for all questions...")
# retrieved_docs = []
# for q in tqdm(questions, desc="Retrieving"): 
#     retrieved_docs.append(retriever.invoke(q))
# print("✅ Documents retrieved.")

# # --- Construct Context Strings ---
# print("Constructing context strings...")
# context_string = []
# for docs in retrieved_docs:
#     context = ""
#     for doc in docs:
#         source = doc.metadata.get('source', 'Unknown Source')
#         context += f"Source: {source}\nContent: {doc.page_content}\n\n"
#     context_string.append(context.strip())
# print("✅ Context strings constructed.")

# # --- Generate Prompts ---
# print("Generating prompts...")
# templates = []
# for query, c in zip(questions, context_string):
#     prompt_template = f"""
# Answer the question based only on this context:
# --- CONTEXT START ---
# {c}
# --- CONTEXT END ---

# Question: {query}
# """
#     templates.append(prompt_template)
# print("✅ Prompts generated.")

# # --- Generate Responses using Ollama ---
# print("Generating responses from Ollama...")
# responses = []

# for template in tqdm(templates, desc="Generating"):
#     try:
#         response = ollama.chat(
#             model='mistral',
#             messages=[
#                 {'role': 'user', 'content': template} 
#             ],
#             options={'temperature': 0}
#         )
#         responses.append(response['message']['content'])
#     except Exception as e:
#         print(f"\nError processing template: {template[:100]}...\nError: {e}")
#         responses.append(f"Error: {e}")
# print("✅ Responses generated.")

# --- Save Responses ---
output_file_path = r"C:\Users\Mannan Golchha\CMU assign 2\cmu-pittsburgh-rag\data\model_responses.json"
# print(f"Saving responses to {output_file_path}...")
# try:
#     with open(output_file_path, 'w', encoding='utf-8') as f: 
#         json.dump(responses, f, indent=4)
#     print("✅ Responses saved successfully.")
# except Exception as e:
#     print(f"[!] Error saving JSON file: {e}")

    
#-------------------------------------------------------- EVALUATION ----------------------------------------------------------------------------------------


exact_match = evaluate.load('exact_match')

with open(output_file_path, 'r', encoding = 'utf-8') as f:
    responses = json.load(f)

em_results = exact_match.compute(predictions = responses, references = answers)
print(f"\nExact Match: {em_results['exact_match']}")

def lower(t) :
    return t.lower()
def punc(t) :
    s = set(string.punctuation)
    t = [ch for ch in t if ch not in s]
    return ''.join(t)
def articles(t) :
    t = re.sub(r'\b(a|an|the)\b', ' ', t)
    return t
def space(t) :
    return ' '.join(t.split())

def f1_calc(pred, ref) :
    pred = space(articles(punc(lower(pred)))).split()
    ref = space(articles(punc(lower(ref)))).split()
    tp = Counter(pred) & Counter(ref)
    tp = sum(tp.values())
    if tp == 0 :
        return 0., 0., 0.
    precision = tp / len(pred)
    recall = tp / len(ref)
    f1 = 2*precision*recall / (precision + recall)
    return [f1, precision, recall]

scores = []
for p, r in zip(responses, answers) :
    scores.append(f1_calc(p, r))

mean_scores = np.mean(scores, axis = 0)
print(f"F1 Score: {mean_scores[0]: .3f}\nPrecision: {mean_scores[1]: .3f}\nRecall: {mean_scores[2]: .3f}\n")