# app/db/database.py
from sqlmodel import create_engine, SQLModel, Session

# Config folder se URL import kar rahe hain
from app.config.db_config import DATABASE_URL

# Connection Engine setup for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    #  echo  true means we can see all queries of sql in terminal when we create ro delete or update
    echo=True,           #    Logs queries in terminal for debugging
    #  means 10 connects  of backend with supabase are ready to use , so when api hit we can quickly use them
    pool_size=10,   
       #  if load  increaee toh we have temerory 20 more connections            
    max_overflow=20,
     # mean ki har connection har ghante me renew hoga  taaki agar koi connection dead tha toh uspe req na jaye and vo ab renew hojaye
    pool_recycle=3600 
        #   
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



















#    DATABASE_URL,
#     #  echo  true means we can see all queries of sql in terminal when we create ro delete or update
#     echo=True,           #    Logs queries in terminal for debugging
#     #  means 10 connects  of backend with supabase are ready to use , so when api hit we can quickly use them
#     pool_size=10,   
#        #  if load  increaee toh we have temerory 20 more connections            
#     max_overflow=20,
#      # mean ki har connection har ghante me renew hoga  taaki agar koi connection dead tha toh uspe req na jaye and vo ab renew hojaye
#     pool_recycle=3600 
#         #   
# # )

# Session(engine): Yeh ek workspace ya "Transaction" boundary create karta hai. Jab tak tum session.commit() nahi karte, 
# saara data memory
#  mein rehta hai aur database mein permanently write nahi hota. Agar error aaya, toh yeh automatic rollback kar dega.




# lekin database ki duniya mein Database Session bilkul alag cheez hoti hai:

# Auth Session (Jo tum baad mein banaoge): "Kya Arpit logged in hai?"

# Database Session (Jo db.py mein hai): "Supabase ke saath ek temporary safe connection banana." Isey tum ek Transaction 
# ya "Baatcheet" samajh sakte ho.
# isi.session ko leke we go to route  and then cna create or do update aor jo bhi karna 
#         Jab FastAPI ko Supabase se data chahiye hota hai, toh woh get_session() ko call karta hai, apna data nikalta hai,
#  aur session close kar deta ha