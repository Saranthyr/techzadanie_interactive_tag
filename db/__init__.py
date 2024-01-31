import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql+psycopg://postgres:postgres@localhost:'
                       f'5432/test_exeed')
Session = sessionmaker(engine, autoflush=False)
