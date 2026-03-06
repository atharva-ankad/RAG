# RAG Knowledge Base with MongoDB Atlas

## Overview
This project is a modular **Retrieval-Augmented Generation (RAG)** system designed to ingest, process, and semantically search through PDF documents. By leveraging **MongoDB Atlas Vector Search**, it transforms static documents into a dynamic knowledge base that can be queried using natural language.

The system solves the problem of efficiently retrieving specific information from large documents without manual searching. It uses local embedding models to convert text into vectors, ensuring high privacy and zero inference costs for the embedding step.

## Key Features
* **Automated PDF Ingestion:** Robust parsing of PDF files with text cleaning and normalization.
* **Smart Chunking:** Content-aware text splitting that preserves paragraph structure and context.
* **Local Embeddings:** Uses Hugging Face's `sentence-transformers` to generate embeddings locally on the CPU.
* **Vector Search:** Utilizes MongoDB Atlas for scalable, high-speed vector similarity search.
* **Modular Architecture:** Clean separation of concerns between configuration, ingestion, and retrieval logic.
* **Singleton Database Connection:** Efficient connection management using the Singleton design pattern.

## System Architecture
The system is built on two main pipelines:

1.  **The Ingestion Pipeline (Write Path):**
    * **Parsing:** Raw text is extracted from PDFs using `PyMuPDF`.
    * **Chunking:** Text is split into overlapping chunks to maintain semantic context.
    * **Embedding:** Each chunk is converted into a 384-dimensional vector using the `all-MiniLM-L6-v2` model.
    * **Storage:** Chunks and their vectors are stored in MongoDB Atlas.

2.  **The Retrieval Pipeline (Read Path):**
    * **Query Embedding:** The user's question is converted into a vector using the same model.
    * **Vector Search:** A `$vectorSearch` aggregation pipeline finds the most similar document chunks in MongoDB.
    * **Ranking:** Results are ranked by cosine similarity score and returned to the user.

## Project Structure
```
VECTORDB_PROJECT/
│
├── core/
│   ├── config.py          # Central configuration (DB URI, Model names, Chunk settings)
│   └── db_client.py       # Singleton MongoDB connection manager with Atlas support
│
├── ingestion/
│   ├── parser.py          # Extracts and cleans text from PDFs (PyMuPDF)
│   ├── chunker.py         # Splits text into manageable chunks with overlap
│   ├── embedder.py        # Generates vector embeddings using SentenceTransformers
│   └── ingest.py          # Orchestrator script to run the full ingestion pipeline
│
├── rag/
│   ├── retriever.py       # Performs vector search queries against MongoDB Atlas
│   └── setup_index.py     # Script to programmatically create the Vector Search Index
│
├── data/
│   └── pdfs/              # Directory for storing source PDF files
│
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

##Workflow (Step-by-Step)
Data Ingestion (ingest.py):

The system loads a PDF from the data/ directory.

parser.py cleans artifacts (like hyphenation) and standardizes whitespace.

chunker.py breaks the text into segments (e.g., 500 characters) with overlap.

embedder.py calculates the vector representation for each text segment.

The final documents (Text + Vector + Metadata) are inserted into the MongoDB collection.

Index Creation (setup_index.py):

A search index definition is sent to MongoDB Atlas to map the vector field for similarity search using the Cosine algorithm.

Vector Retrieval (retriever.py):

A user inputs a query (e.g., "What is the summary?").

The query is embedded into a vector.

The system executes a vector search query on Atlas.

The top K most relevant text chunks are displayed with their confidence scores.

##Technologies Used
Python 3.10+: Core programming language.

MongoDB Atlas: Cloud-native database for storing data and performing Vector Search.

PyMongo: Official MongoDB driver for Python.

Sentence Transformers (Hugging Face): Library for generating state-of-the-art text embeddings (all-MiniLM-L6-v2).

PyMuPDF (fitz): High-performance PDF parsing and text extraction.

LangChain Text Splitters: Utilities for smart text chunking.

NumPy: Used for efficient numerical operations and data handling.
