import os

class Settings:
    # --- 1. Database Configuration ---
    # The URL where your MongoDB is running. 
    
    MONGO_URI = "mongodb://localhost:27017/"
    
    # The name of the database (folder) inside MongoDB
    DB_NAME = "rag_db_v1"
    
    # The name of the collection (sheet) inside the database
    COLLECTION_NAME = "knowledge_base"
    
    
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS = 384
    
    
    CHUNK_SIZE = 1000
    
    CHUNK_OVERLAP = 200

# We instantiate the class so we can just import 'settings' elsewhere.
settings = Settings()