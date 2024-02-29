from db import engine, Base, Session
from models import URL

# engine and base to create table
Base.metadata.create_all(bind = engine)