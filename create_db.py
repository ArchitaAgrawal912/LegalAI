import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_database():
    pdf_path = "Bharatiya_Nyaya_Sanhita_2023.pdf" # Tumhari downloaded PDF ka naam
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found in the project folder.")
        return

    print("📄 Loading Official BNS PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("✂️ Splitting 358 Sections into chunks...")
    # PDF ke liye chunk size thoda bada rakhte hain taaki pura section ek chunk mein aaye
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=300
    )
    chunks = text_splitter.split_documents(documents)

    print(f"🧠 Creating embeddings for {len(chunks)} chunks... (This might take a minute)")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("legal_faiss_index")
    
    print("✅ Complete BNS FAISS Vector Database created successfully!")

if __name__ == "__main__":
    create_database()