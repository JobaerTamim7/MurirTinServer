from .database import get_engine
from sqlalchemy import Engine
from models.Base import Base
import os


def create_datafolder():
    os.makedirs('data',exist_ok=True)

def init_db():
    try:
        engine : Engine = get_engine() #type:ignore
        print('Creating database tables ...... ')
        Base.metadata.create_all(engine)
        print('All tables have been created.')

    except Exception as e:
        print('Something went wrong with database initialized.')
        print(f'Error : {str(e)}')

def main():
    create_datafolder()
    init_db()