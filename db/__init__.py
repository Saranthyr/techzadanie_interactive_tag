import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql+psycopg://{os.environ["DB_USER"]}:{os.environ["DB_PASS"]}@{os.environ["DB_HOST"]}:'
                       f'{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}')
Session = sessionmaker(engine, autoflush=False)
