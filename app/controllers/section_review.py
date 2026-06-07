import uuid
from sqlmodel import Session
from fastapi import HTTPException  # 👈 Isko import zaroor karna
from app.models.crud import update_section_approval
from app.models.legal_case import LegalCase

def process_section_review(
    session: Session, 
    section_id: uuid.UUID, 
    is_approved: bool | None, 
    rejection_reason: str | None
) -> dict:
    
    # 🚨 STRICT VALIDATION (Proper HTTP Error ke sath)
    if is_approved is False and not rejection_reason:
        # Puraane ValueError ki jagah HTTPException use kiya taaki UI ko 400 Bad Request mile
        raise HTTPException(
            status_code=400, 
            detail="Rejection reason cannot be empty for rejected sections."
        )
    
    if is_approved is True:
        rejection_reason = None 

    # 1. 🗄️ Database CRUD Call
    updated_section = update_section_approval(
        session=session,
        section_id=section_id,
        is_approved=is_approved,
        rejection_reason=rejection_reason,
        has_lawyer_verified=True  # Naya flag set ho raha hai
    )

    # 2. 🧠 Smart Logic
    sec_name = updated_section.ipc_section if updated_section.ipc_section != "N/A" else updated_section.bns_section

    # 🎯 MAGIC CHECK HATA DIYA HAI! ✂️
    # Kyunki ab humara '/fetch' route directly sections ka 'has_lawyer_verified' check karta hai,
    # toh LegalCase par flag set karne ki koi zaroorat hi nahi bachi. Code aur bhi fast ho gaya!

    # 3. Router ke liye ek clean dictionary return karo
    return {
        "updated_section": updated_section,
        "sec_name": sec_name
    }