import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

class Database:

    def __init__(self):
        load_dotenv() # load pass from environmental vars.
        DB_USER=os.getenv("USER")
        DB_HOST=os.getenv("HOST")
        DB_PORT=os.getenv("PORT")
        DB_NAME=os.getenv("NAME")
        DB_PASS=os.getenv("PASS")
        db_url = f'postgresql://jmgiorgi:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(db_url)

    def execute(self, query, params=None):
        """Run a SQL command and return the result."""
        with self.engine.connect() as conn:
            with conn.begin():
                result = conn.execute(text(query), params)
                return result
 
    def connect(self):
        return self.engine.connect()