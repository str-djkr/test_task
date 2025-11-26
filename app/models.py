from sqlalchemy import Column, Integer, String, BigInteger
from db import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    region = Column(String, nullable=True, index=True)
    population = Column(BigInteger, nullable=False)
    source = Column(String, nullable=True)

    def __repr__(self):
        return f"<Country(name={self.name!r} region={self.region!r} population={self.population})>"
