from .__dependence__ import *


class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(10), nullable=False)
    count = Column(Integer, nullable=False, default=0)
