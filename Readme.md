app/models/ ke andar Python classes likhte ho (jaise User, Case). Yeh tumhare database ka blueprint hai.



(Alembic env.py): Jab tum alembic revision --autogenerate chalate ho, toh Alembic tumhare Python models ko padhta hai, aur Supabase ke live database ko dekhta hai. Fir dono ko compare karke detect karta hai ki "Naya kya add ya delete hua hai?".




(Versions Folder): Alembic us difference ko samajh kar ek SQL file generate karta hai (jo tumhare app/db/versions/ folder mein aati hai)



[alembic upgrade head] chalate ho, toh Alembic us script ko lekar seedha Supabase ke paas jata hai, queries run karta hai, aur tables live create/update kar deta hai.



db_config.py: Iska sirf ek kaam hai—.env file se chupke se tumhara Supabase URL padhna aur pure app ko securely provide karna. Isse tumhare code mein kahin bhi password leak nahi hota.




usertable.py, casetable.py, etc.: Yahan tum Python classes banate ho. SQLModel in Python classes ko SQL tables ki tarah samajhta hai.


__init__.py: Yeh file sabse important "Gatekeeper" hai. Isme likhi ek line (from sqlmodel import SQLModel) pure app ko batati hai ki saare models yahan bundle ho chuke hain, taaki Alembic unhe ek sath dekh sake.


database.py: Yeh "Pipeline" hai. Yeh tumhare config se URL leti hai aur Supabase ke sath ek connection (Engine/Session) banati hai, jiska use karke baad mein tumhari FastAPI live data fetch ya save karegi.


env.py: Yeh Alembic ka "Dimaag" hai. Yeh file config se URL leti hai, models se blueprint leti hai, aur Alembic ko batati hai ki kis database par kaunse models compare karne hain.


script.py.mako: Yeh ek "Template" hai. Jab tum naya version generate karte ho, toh Alembic is structure ko copy karke nayi script likhta hai.



Yeh file terminal ko rasta dikhati hai. Jab tum root folder se alembic command chalate ho, toh terminal is file ko padhta hai jisme likha hai script_location = app/db, jisse use pata chalta hai ki saara migration ka setup app/db ke andar rakha hai.



 we made 3 serializer named
 1 case 
 2 ipc
2 user
 we made three controller for same
 and made 3 routr for same 
 and 1 base class for the content jo har model me repeat hora tha jaise , id , crreated at and updated at , humne us base class me daaldia ye  sab and inherit karlia jha bhi need thi

  why we made 3 orm controller( functions)
  ans: humne model bnaya , ab fir hume table bnani hai db me toh in function ke bina table nhi bnegi 
  user controller me user table ke crud operations ke functions hai


 controlllenr bnane se pehle meaine just models bnaye and alembic ke 2 commands run kiye the toh supabase me schema and table archie dikh gya tha
  par ye  controller help to put content there
  