from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, Float, \
    UniqueConstraint, Date, Index, PrimaryKeyConstraint, ForeignKey
Base = declarative_base()
