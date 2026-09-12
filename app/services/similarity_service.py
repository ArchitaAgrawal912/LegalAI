# app/services/similarity_service.py
import numpy as np
from sentence_transformers import SentenceTransformer, util

# 🧠 Model ko globally load kar rahe hain taaki memory save ho
try:
  
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

except Exception as e:
    print(f"❌ Error loading embedding model: {str(e)}")
    embedding_model = None


def compute_similarity_percentage(current_case_text: str, precedent_case_text: str) -> int:
    """
    Takes two text blocks, converts them to embeddings, 
    and returns a rounded similarity percentage (0-100).
    """
    if not embedding_model:
        return 0 
        
    if not current_case_text.strip() or not precedent_case_text.strip():
        return 0

    # 1. Text ko multi-dimensional vectors mein badlo
    embedding_current = embedding_model.encode(current_case_text, convert_to_tensor=True)
    embedding_precedent = embedding_model.encode(precedent_case_text, convert_to_tensor=True)

    # 2. Cosine Similarity calculate karo (Result ranges from -1 to 1)
    cosine_score = util.cos_sim(embedding_current, embedding_precedent)

    # 3. Score ko extract karo aur negative values ko handle karne ke liye clamp karo
    score_val = cosine_score.item()
    if score_val < 0:
        score_val = 0.0

    # 4. Percentage mein convert karke absolute round integer return karo
    return int(round(score_val * 100))




# SentenceTransformer

# Ye HuggingFace ka library hai.

# Iska kaam

# Text ko numbers (vectors/embeddings) me convert karna.

# util

# Iske andar helper functions hote hain.

# Jaise

# util.cos_sim()

# jo cosine similarity calculate karta hai.

#   model ko sabse upar likha instead of function ke andar isliye kiya kyuki model ko baar baar load na karna pade.
#    when we call fn


    # embedding_current = embedding_model.encode(current_case_text, convert_to_tensor=True)
    #  this line convert text to vector
    
    
    
    
    
    #  embedding is used to compare two text blocks and get a similarity score between them. It converts the text into multi-dimensional vectors and 
    #  then calculates the cosine similarity between those vectors. The result is a score that indicates how similar the two texts are, 
    #  which is then converted into a percentage (0-100).
    
#      why embedding if llm call se hojata hai kaam
#      dis adv of llm
#      Problems

# Slow (2-10 sec)
# API cost
# Token cost
# Har baar internet/API call


#  embedding is Fast

# Cheap

# Offline bhi chal sakta hai.


# Lekin util.cos_sim() ko PyTorch Tensor pasand hai. isiliye we write  convert_to_tensor=True

# util.cos_sim(...)
# un dono vectors ko compare karti hai. with the help of their direction

#   score_val = cosine_score.item() .item karke we get real data from the tensor