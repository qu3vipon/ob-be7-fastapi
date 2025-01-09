from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = "mysql+pymysql://root:be7-fastapi-pw@127.0.0.1:33060/be7-fastapi"

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
