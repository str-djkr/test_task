from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time
from config import DATABASE_URL

Base = declarative_base()


class Database:
    def __init__(self, db_url: str = DATABASE_URL, echo: bool = False):
        self.db_url = db_url
        self.echo = echo
        self._engine = None
        self._Session = None

    def connect(self, retries: int = 30, wait_seconds: int = 1):
        last_exc = None
        for i in range(retries):
            try:
                self._engine = create_engine(self.db_url, echo=self.echo, pool_pre_ping=True)
                self._Session = sessionmaker(bind=self._engine)
                # try simple connection
                with self._engine.connect():
                    pass
                return
            except Exception as e:
                last_exc = e
                time.sleep(wait_seconds)
        raise last_exc

    @property
    def engine(self):
        return self._engine

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def get_session(self):
        return self._Session()
