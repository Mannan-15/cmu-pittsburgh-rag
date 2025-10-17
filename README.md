# CMU Advanced NLP: End-to-End RAG System for Pittsburgh QA

This repository contains the source code and documentation for an end-to-end Retrieval Augmented Generation (RAG) system, developed as part of the CMU Advanced NLP (11-711) assignment. The system is designed to answer factual questions about Pittsburgh and Carnegie Mellon University by augmenting a Large Language Model with a custom-built, domain-specific knowledge base.

## Project Overview

The core challenge addressed by this project is the limitation of standard LLMs in providing accurate answers for niche or time-sensitive domains. This RAG system overcomes this by:
1.  **Collecting** a diverse set of documents about Pittsburgh and CMU from web pages and PDFs.
2.  **Indexing** this information into a searchable vector database.
3.  **Retrieving** the most relevant document chunks for a given user question.
4.  **Generating** a concise, accurate answer by feeding the question and the retrieved context to an LLM (e.g., Llama 2).

## Key Components & Pipeline

-   **Data Collection & Preprocessing:** Scripts to scrape and clean data from various websites (Wikipedia, city event calendars, etc.) and PDF documents using Python libraries like `BeautifulSoup4` and `pypdf`.
-   **Knowledge Base:** A curated collection of processed text documents that serves as the "external brain" for the LLM.
-   **RAG Pipeline:**
    -   **Document Retriever:** Employs sentence-transformer models to embed text chunks and a vector store (e.g., ChromaDB) to perform efficient semantic search.
    -   **Answer Generator:** Utilizes a powerful instruction-tuned LLM (Llama 2) to synthesize the final answer from the retrieved context.
-   **Evaluation:** The system's performance is measured against a manually annotated test set using standard QA metrics like **Exact Match (EM)** and **F1-Score**.

## Tech Stack

-   **Programming Language:** Python
-   **Core NLP/ML Libraries:** Hugging Face `transformers`, `LangChain` / `LlamaIndex`
-   **Web Scraping:** `requests`, `BeautifulSoup4`
-   **PDF Processing:** `pypdf`
-   **Vector Store:** ChromaDB / FAISS
-   **LLM:** Llama 2

---
