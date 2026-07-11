from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.legal_service import LegalAnalysisService
from app.services.kanoon_service import KanoonService


@lru_cache()
def get_legal_service() -> LegalAnalysisService:
    """Dependency provider for the AI legal service."""
    return LegalAnalysisService()


@lru_cache()
def get_kanoon_service() -> KanoonService:
    """Dependency provider for the Kanoon API service."""
    return KanoonService()


# Expose the shared DB session dependency here for consistency in route imports.
get_db_session = get_session


# "I created a dependency provider file to centralize dependency creation for services and the database. 
# @lru_cache is used on stateless services like LegalAnalysisService and 
# KanoonService so that FastAPI reuses the same service instance instead of creating a new object on every request.
# This improves performance and avoids repeated initialization of clients and configuration.
# I didn't use it for the database session because each request needs its own independent session."
# transaction aur concurrency issues aa sakte hain. if same session sabko dia
# @lru_cache yaha caching ke liye kam aur service object ko ek hi baar create karke reuse karne ke liye use hua hai.

# LegalAnalysisService()

# ke andar

# AsyncGroq(...)

# client banta hai.

# Aur

# KanoonService()

# ke andar

# headers
# url
# token

# initialize hote hain.

# Ye values har request me same rehti hain.

# Har request pe dobara object banana unnecessary hai.

# Isliye ek hi object bana ke reuse kar rahe hain.


# dependencies.py is a centralized place that provides reusable objects (services, database sessions, etc.) to routes through FastAPI's Dependency Injection. 
# This keeps routes clean, avoids duplicate object creation logic, like har route me agar ye LegalAnalysisService() ka object create karna hai toh har route me ye code likhna padega, 
# aur agar future me iske constructor me changes aate hain toh har route me jaake change karna padega.
# and makes future changes easier because object creation is managed in one place.

#  suppose kal ko kannon service ka constructer change ho gya usme aur arguments aagye , now ab jab obj bnage atoh vo arg need to paass
#  toh ab har route me jaake obj chnage karu isse acha dependecy fle bnai and vhi pe obj jo bnana uska tareeka likha dia