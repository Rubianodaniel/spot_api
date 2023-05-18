from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

# Crea una instancia de SQLAlchemy
engine = create_engine("sqlite:///database.db")

session =  sessionmaker(bind=engine)

Base = declarative_base()
