from .. import rt_dir
from functools import wraps
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(f'sqlite:///{rt_dir}/dist/flower.db', encoding='utf-8')
Session = sessionmaker(bind=engine)
Success = {'status': True}


def APIFuncWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = scoped_session(Session)
        try:
            ret = func(*args, **kwargs, session=session)
            session.commit()
        except Exception as e:
            ret = {'status': False, 'message': repr(e)}
            session.rollback()
        finally:
            session.close()
        return ret
    return wrapper


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
