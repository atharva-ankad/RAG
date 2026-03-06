from core.db_client import mongo_client
from ingestion.embedder import Embedder
from core.config import settings

class VectorRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.collection = mongo_client.get_collection()

    def retrieve(self, query, top_k=5):
        print(f"🔍 Searching Atlas for: '{query}'")
        
        # 1. Vectorize the Query
        query_vector = self.embedder.model.encode(query).tolist()
        
        # 2. Build the Atlas Vector Search Pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": settings.VECTOR_INDEX_NAME, # "vector_index"
                    "path": "vector",       # The field where we stored the numbers
                    "queryVector": query_vector,
                    "numCandidates": 100,   # Look at 100 nearest neighbors roughly
                    "limit": top_k          # Return the top 5
                }
            },
            {
                "$project": {
                    "_id": 0, 
                    "text": 1, 
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"} # Get the similarity score
                }
            }
        ]
        
        # 3. Execute Search (Server-side)
        results = list(self.collection.aggregate(pipeline))
        
        # 4. Display Results
        print("\n--- TOP RESULTS ---")
        if not results:
            print("⚠️ No results found. (Check if Index is ready/active)")
        
        for result in results:
            print(f"Confidence: {result.get('score', 0):.4f}")
            print(f"Text: {result.get('text', '')[:]}\n")
            
        return results

if __name__ == "__main__":
    retriever = VectorRetriever()
    # Test Query
    retriever.retrieve("How many moons does Jupiter have?")