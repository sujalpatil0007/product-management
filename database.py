from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
Base = declarative_base()


db_url="postgresql://postgres:0007@localhost:5432/sujal2db"
engine=create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)



