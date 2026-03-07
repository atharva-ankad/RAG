from groq import Groq
from core.config import settings

class GroqGenerator:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY is missing in core/config.py")
            
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    def generate_answer(self, query, retrieved_chunks):
        """
        Streams the answer from Groq.
        """
        if not retrieved_chunks:
            print("🤖 Groq: I couldn't find relevant documents.")
            return

        # 1. Prepare Context
        context_text = ""
        for i, chunk in enumerate(retrieved_chunks):
            page = chunk.get('metadata', {}).get('page', '?')
            context_text += f"Source {i+1} (Page {page}):\n{chunk['text']}\n\n"

        # 2. System Prompt
        messages = [
        {
        "role": "system",
        "content": (
            "You are a precise document analysis AI. You must answer the user's question strictly based on the provided context.\n\n"
                    "STRICT RULES:\n"
                    "1. NO OUTSIDE KNOWLEDGE: If the answer is not explicitly in the context below, output EXACTLY: "
                    "'The provided documents do not contain this information.'\n"
                    "2. NO HALLUCINATIONS: Do not make up facts.\n"
                    "3. CITATIONS: Every claim must be followed by a citation like [Page X].\n"
                    "4. OUTPUT FORMAT: Provide the direct answer only. Do not output <think> tags or reasoning steps."
        )
        },
        {
        "role": "user",
        "content": (
            f"Document Context:\n{context_text}\n\n"
            f"Question:\n{query}\n\n"
            "Answer:"
        )
        }
        ]

        # 3. Stream Response
        print("🤖 Groq Response:")

        try:
            stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
    
            # RAG tuning
            temperature=0.4,           # lower = more factual answers
            top_p=0.9,

            # response control
            max_completion_tokens=1024,

            # streaming
            stream=True,

            # stopping
            stop=None
            )

            # Print chunks as they arrive (no buffering!)
            full_response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                full_response += content
            
            print("\n" + "-"*50)
            return full_response

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None