<div align="center">

# MongoDB Atlas Vector Search RAG
A high-performance Retrieval-Augmented Generation system for querying PDF documents using semantic search and context-grounded LLM responses.

![Architecture](https://img.shields.io/badge/Architecture-RAG-blueviolet)
<br>
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Embeddings](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-FFD700)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas_Vector_Search-green)
![LLM](https://img.shields.io/badge/LLM-Groq_API-orange)

</div>

## Overview

This project is a high-performance **Retrieval-Augmented Generation (RAG)** system designed to **ingest PDF documents**, index them using **semantic vectors**, and allow users to **query the content using natural language**.

The system combines **MongoDB Atlas Vector Search** for retrieval with Groq's fast inference API (using the Qwen model). **Crucially, the system operates on a "Zero Outside Knowledge" principle: it is strictly engineered to answer queries only using the information contained within the ingested documents, ignoring the LLM's pre-trained internal knowledge to ensure factual accuracy and eliminate hallucinations.**

## Key Features

* **📄 PDF Ingestion:** Robust parsing of PDF documents using `PyMuPDF` with custom text cleaning and normalization.
* **🧩 Smart Chunking:** Context-aware text splitting using `LangChain`, preserving paragraph structure and semantic meaning.
* **🧠 Local Embeddings:** Generates embeddings locally using `SentenceTransformers` (`all-MiniLM-L6-v2`) for privacy and efficiency.
* **⚡ High-Speed Vector Search:** Utilizes MongoDB Atlas Vector Search for scalable similarity retrieval.
* **🤖 Strict Contextual Generation:** Integrates with Groq API using a system prompt that **enforces strict adherence to the provided context, rejecting any outside information.**
* **📚 Citation Support:** Every answer includes references to the specific page numbers and relevance scores of the source material.

## System Architecture

![](data\RAG_Final.png)

The project operates in two distinct pipelines:

1. **Ingestion Pipeline (Write Path):**
* Extracts text from PDFs.
* Cleans and normalizes the text.
* Chunks text into overlapping segments.
* Generates vector embeddings (384 dimensions).
* Stores text, metadata, and vectors in MongoDB.


2. **Retrieval Pipeline (Read Path):**
* Embeds the user's natural language query.
* Performs a Vector Search (`$vectorSearch`) in MongoDB to find the top $k$ relevant chunks.
* Constructs a prompt with the retrieved context.
* Streams the response from the Groq LLM.

## Technologies Used

* **Language:** Python
* **Database:** MongoDB Atlas (Vector Search)
* **LLM:** Groq API (Qwen 3 32B)
* **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
* **PDF Parsing:** PyMuPDF (Fitz)
* **Orchestration:** LangChain (Text Splitters)


## Project Structure

```text
rag-project/
│
├── core/
│   ├── config.py          # Central configuration (DB URI, Model names, Chunk settings)
│   └── db_client.py       # Singleton MongoDB connection manager
│
├── ingestion/
│   ├── parser.py          # PDF text extraction and cleaning logic
│   ├── chunker.py         # Recursive text splitter with metadata handling
│   ├── embedder.py        # SentenceTransformer wrapper for generating vectors
│   └── ingest.py          # Main script to run the ingestion pipeline
│
├── rag/
│   ├── retriever.py       # Logic for performing vector search against MongoDB
│   ├── generator.py       # Interface for Groq LLM generation
│   └── setup_index.py     # Utility to programmatically create the Atlas Search Index
│
├── data/
│   └── pdfs/              # Source directory for PDF documents
│
├── app.py                 # Main CLI application entry point
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

```


## Prerequisites

* **Python 3.10+**
* **MongoDB Atlas Cluster:** You need a cluster (M0 sandbox works) with Vector Search enabled.
* **Groq API Key:** For the LLM generation.

## Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project

```


2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Environment Configuration**
Create a `.env` file in the root directory and add your credentials:
```ini
MongoDB_key=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
LLM_API=gsk_your_groq_api_key_here

```



## Usage

### 1. Ingest Data

Place your PDF files into the `data/pdfs/` directory. Run the ingestion script to parse, embed, and upload the data to MongoDB.

```bash
# Must be run from the root directory
python -m ingestion.ingest

```

*Note: The current configuration clears the database before inserting new data to prevent duplicates during testing.*

### 2. Create Vector Index

If this is your first time running the project, you must create the Vector Search Index in MongoDB Atlas.

```bash
python -m rag.setup_index

```

*Wait approximately 1 minute after running this for Atlas to build the index.*

### 3. Run the Chat Application

Start the interactive command-line interface to chat with your documents.

```bash
python app.py

```

## Configuration

You can tweak the system behavior in `core/config.py`:

| Variable | Description | Default |
| --- | --- | --- |
| `CHUNK_SIZE` | Size of text chunks (characters) | `500` |
| `CHUNK_OVERLAP` | Overlap between chunks | `150` |
| `EMBEDDING_MODEL` | HuggingFace model name | `all-MiniLM-L6-v2` |
| `LLM_MODEL` | Model used by Groq | `qwen/qwen3-32b` |
| `DB_NAME` | MongoDB Database Name | `RAG_Project` |
