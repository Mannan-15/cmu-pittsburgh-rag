# End-to-End RAG System for Pittsburgh QA

This repository implements an **end-to-end Retrieval-Augmented Generation (RAG)** system designed for factual **question answering about Pittsburgh and Carnegie Mellon University (CMU)**.  
It includes the full pipeline—from **data scraping** and **chunking**, to **vector retrieval**, **answer generation**, and **evaluation**—along with custom datasets and retriever/reader modules.

**Repository URL:** [https://github.com/Mannan-15/cmu-pittsburgh-rag](https://github.com/Mannan-15/cmu-pittsburgh-rag)

---

## Project Overview

Large Language Models (LLMs) often lack domain-specific or up-to-date knowledge.  
This project bridges that gap using a **Retrieval-Augmented Generation (RAG)** framework (Lewis et al., 2021), enabling local LLMs (via **Ollama**) to answer questions using **retrieved factual content** from a custom-built Pittsburgh knowledge base.

---

## Pipeline Stages

### 1. **Data Collection** (`scraper.ipynb`)
- Web scraping of Wikipedia, CMU pages, and city sites using `requests` + `BeautifulSoup4`.
- Extracted content from official PDFs like the *City of Pittsburgh Operating Budget 2024* using `pypdf`.
- Cleaned and structured data saved in `data/data.json`.

### 2. **Chunking and Preprocessing** (`chunks_code.ipynb`)
- Used `langchain.text_splitter.RecursiveCharacterTextSplitter` for chunking large texts into 512-token segments with overlaps.
- Added metadata for traceability.
- Saved final processed chunks in `data/chunks.json`.

### 3. **Retriever Construction** (`retriever_py.py`)
- Embedded all chunks using **Sentence Transformers** (`all-MiniLM-L6-v2`, `facebook/contriever-msmarco`, etc.).
- Stored embeddings in a **ChromaDB** vector store located under `/chroma.db/`.
- Allows efficient semantic search for relevant document chunks during inference.

### 4. **Reader Model (RAG Pipeline)** (`reader_model.py`)
- Connects retriever output to a local LLM (via **Ollama**, e.g., `mistral` model).
- Uses a LangChain **RAG chain** built with:
  - `ChatPromptTemplate`
  - `RunnablePassthrough`
  - `ChatOllama`
- Retrieves relevant context for a query and synthesizes a concise, factual answer.

### 5. **Evaluation Framework** (`evaluation.py`)
- Evaluates model outputs on both train and test sets:
  - **Exact Match (EM)**
  - **F1 Score**
  - **Recall**
- Reads data from:
  - `data/train/` → `train.csv`, `reference_answers.txt`
  - `data/test/` → `test.csv`, `reference_answers.txt`
- Logs outputs in `model_responses.json`.

---

## Repository Structure

```
cmu-pittsburgh-rag/
│
├── chroma.db/                          # Local vector store
├── data/
│   ├── data.json                       # Raw scraped text data
│   ├── chunks.json                     # Preprocessed text chunks
│   ├── 24731_2024_operating_budget_2.pdf
│   ├── test/
│   │   ├── questions.txt
│   │   ├── reference_answers.txt
│   │   └── test.csv
│   └── train/
│       ├── questions.txt
│       ├── reference_answers.txt
│       └── train.csv
│
├── retriever_model/                    # Saved retriever files (if applicable)
├── retriever_py.py                     # Retriever building script
├── reader_model.py                     # Reader model (RAG chain)
├── evaluation.py                       # Evaluation metrics and benchmarking
├── chunks_code.ipynb                   # Chunking notebook
├── scraper.ipynb                       # Data scraping notebook
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Tech Stack

**Programming Language:** Python 3.11  
**Core Libraries:**
- `requests`, `beautifulsoup4` – web scraping
- `pypdf` – PDF text extraction  
- `langchain`, `chromadb` – retrieval & RAG pipeline  
- `sentence-transformers` – embeddings  
- `ollama` – local LLM inference (Mistral-7B)  
- `numpy`, `evaluate` – metrics computation  

---

## Data Sources

Knowledge base compiled from:
- Wikipedia: *Pittsburgh*, *Carnegie Mellon University*, *History of Pittsburgh*
- [City of Pittsburgh Official Website](https://pittsburghpa.gov)
- [Visit Pittsburgh](https://www.visitpittsburgh.com)
- [CMU Official Pages](https://www.cmu.edu)
- City Budget & Tax PDFs
- Event calendars (City Paper, CMU Events)

---

## How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Mannan-15/cmu-pittsburgh-rag.git
   cd cmu-pittsburgh-rag
   ```

2. **Set up Environment**
   ```bash
   conda create -n rag_pitt python=3.11
   conda activate rag_pitt
   pip install -r requirements.txt
   ```

3. **Run Ollama**
   - Install from [https://ollama.com](https://ollama.com)
   - Pull the Mistral model:
     ```bash
     ollama pull mistral
     ```
   - Ensure Ollama is running in the background.

4. **Build Vector Store**
   ```bash
   python retriever_py.py
   ```

5. **Run Inference**
   ```bash
   python reader_model.py
   ```

6. **Evaluate Results**
   ```bash
   python evaluation.py
   ```

---

## Future Work

- **Hypothetical Document Embeddings (HyDE):**
  - Generate a “hypothetical answer” using the reader model before retrieval to improve embedding relevance.
  - Experiment with replacing or augmenting query embeddings with these HyDE-based ones.
- **Hybrid Search (Dense + BM25):**
  - Combine semantic and lexical retrieval for better coverage.
- **Fine-tuning Embeddings:**
  - Domain adaptation of Contriever/MiniLM models on CMU-Pittsburgh-specific data.
- **Model Comparisons:**
  - Test Llama 3, Phi-3, and Gemma models locally via Ollama.
- **Evaluation Expansion:**
  - Add Rouge-L and BLEU-based metrics for richer analysis.

---
