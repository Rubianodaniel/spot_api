from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///database.db")

session =  sessionmaker(bind=engine)

Base = declarative_base()



def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()