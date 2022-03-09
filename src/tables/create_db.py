from .__dependence__ import Base
from . import *
from ..API import engine


if __name__ == "__main__":
    Base.metadata.create_all(engine)
