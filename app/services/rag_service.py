import os
import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db_path = "legal_faiss_index"
        self.vector_db = None

        # Load database if it exists
        if os.path.exists(self.vector_db_path):
            self.vector_db = FAISS.load_local(
                self.vector_db_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            logger.info("✅ FAISS Vector Database loaded successfully.")
        else:
            logger.warning("⚠️ FAISS Vector DB not found. Run create_db.py first.")

    def get_relevant_laws(self, case_description: str, k: int = 3) -> str:
        """Searches the database and returns relevant laws as a formatted string."""
        if not self.vector_db:
            return "" # Return empty string if DB is not ready
        
        relevant_docs = self.vector_db.similarity_search(case_description, k=k)
        
        # Format the rules
        laws_text = "\n\n--- STRICT LEGAL REFERENCE DIRECTIVE ---\n"
        laws_text += "You MUST prioritize the following official legal sections when extracting charges:\n"
        for i, doc in enumerate(relevant_docs):
            laws_text += f"{i+1}. {doc.page_content}\n"
            
        return laws_text