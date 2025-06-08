from dotenv import load_dotenv
from sqlalchemy import Engine,create_engine
from sqlalchemy.orm import sessionmaker,Session
import os

load_dotenv()

DB_URL = os.getenv('DB_URL','')

def get_engine() -> Engine | None :
    try:
        if DB_URL == '':
            raise EnvironmentError('Something went wrong with database url.')
        
        engine : Engine = create_engine(DB_URL,echo=True)

        return engine
    
    except Exception as e:
        print('Something went wrong with engine creation')
        print(f'Error : {str(e)}')

        return None

def get_session() -> Session | None:
    try:
        Session_Factory : sessionmaker[Session] = sessionmaker(autoflush=False, bind=get_engine())
        session : Session = Session_Factory()

        return session
    
    except Exception as e:
        print('Something went wrong with session creation.')
        print(f'Error : {str(e)}')

        return None