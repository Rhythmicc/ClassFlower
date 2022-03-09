from .__dependence__ import *


class Reasons(Base):
    __tablename__ = 'reasons'
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    date = Column(Date)
    content = Column(String(128))
