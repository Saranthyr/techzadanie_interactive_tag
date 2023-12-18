from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/techzad_tag_db')
Session = sessionmaker(engine, autoflush=False)
