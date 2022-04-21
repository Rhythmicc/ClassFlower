from ..tables import Reasons
from . import APIFuncWrapper, Session, Success, to_dict, desc


class ReasonsAPI:
    @staticmethod
    @APIFuncWrapper
    def add_reason(rdate, rcontent, session: Session = None):
        obj = Reasons(date=rdate, content=rcontent)
        session.add(obj)
        return Success

    @staticmethod
    @APIFuncWrapper
    def del_reason(rdate, rcontent, session: Session = None):
        obj = session.query(Reasons).filter(Reasons.date == rdate, Reasons.content == rcontent).first()
        if obj:
            session.delete(obj)
            return Success
        else:
            return {
                'status': False,
                'message': 'Reason not found'
            }

    @staticmethod
    @APIFuncWrapper
    def list_reasons_ordered_by_date(session: Session = None):
        return {
            'status': True,
            'data': [to_dict(i) for i in session.query(Reasons).filter().order_by(desc(Reasons.date)).all()]
        }
