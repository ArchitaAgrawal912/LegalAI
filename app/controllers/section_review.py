import uuid
from sqlmodel import Session
from app.models.crud import update_section_approval

def process_section_review(
    session: Session, 
    section_id: uuid.UUID, 
    is_approved: bool, 
    rejection_reason: str | None
) -> dict:
    """
    Handles the business logic for approving/rejecting a section 
    and computes the correct section name to display.
    """
    
    # 🚨 SMART VALIDATION (Safety Net)
    if not is_approved and not rejection_reason:
        raise ValueError("Rejection reason cannot be empty for rejected sections.")
    
    if is_approved:
        rejection_reason = None # Clean up just in case

    # 1. 🗄️ Database CRUD Call
    updated_section = update_section_approval(
        session=session,
        section_id=section_id,
        is_approved=is_approved,
        rejection_reason=rejection_reason
    )

    # 2. 🧠 Smart Logic: Pata lagao ki IPC bhejna hai ya BNS
    sec_name = updated_section.ipc_section if updated_section.ipc_section != "N/A" else updated_section.bns_section

    # 3. Router ke liye ek clean dictionary return karo
    return {
        "updated_section": updated_section,
        "sec_name": sec_name
    }