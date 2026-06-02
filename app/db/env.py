import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Root folder ko path me add karna taaki 'app' imports kaam karein
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Tumhare SQLModel metadata aur tables ko import karna
from app.models import SQLModel
from app.models.user import User
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection

# 🎯 NAYA: Tumhare central config folder se DB URL import kar rahe hain
from app.config.db_config import DATABASE_URL

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = SQLModel.metadata

def get_url():
    # 🎯 NAYA: Ab yahan seedha config wala URL return hoga
    return DATABASE_URL

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()









# run_migrations_online() -> this runs when we give command alembic upgrade head

    #  run_migrations_offline() ->Yeh kab use hota hai? Jab tumhare paas direct database access nahi hota (jaise kuch badi companies mein developers
    #  directly DB update nahi kar sakte, unhe sirf ek .sql file generate karke Database Admin ko deni hoti hai).

# Technically: Yeh function bina database se connect kiye, sirf tumhare Python models ko padhta hai aur raw SQL script generate kar deta hai. 
# literal_binds=True ka matlab hai ki variables ki jagah actual values SQL string mein daal do.



# NullPool ka matlab hai: "Ek connection banao, table create karo, aur connection turant destroy kar do." No pooling required.