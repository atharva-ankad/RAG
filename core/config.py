import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Settings:
    # --- 1. Database Configuration ---
    # The URL where your MongoDB is running. 
    
    MONGO_URI = os.getenv("key")
    
    # The name of the database (folder) inside MongoDB
    DB_NAME = "RAG_Project"
    
    # The name of the collection (sheet) inside the database
    COLLECTION_NAME = "Knowledge"
    
    
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS = 384
    
    
    CHUNK_SIZE = 500
    
    CHUNK_OVERLAP = 150

    # --- 4. Vector Search Configuration ---
    # The name of the index we will create in MongoDB
    VECTOR_INDEX_NAME = "vector_index"

# We instantiate the class so we can just import 'settings' elsewhere.
settings = Settings()