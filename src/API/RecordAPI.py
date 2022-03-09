from ..tables import Record
from . import APIFuncWrapper, Success, Session, to_dict, desc


class RecordAPI:
    @staticmethod
    @APIFuncWrapper
    def update_record(name, add, session: Session = None):
        student = session.query(Record).filter_by(name=name).first()
        if student:
            student.count = student.count + add
        return Success

    @staticmethod
    @APIFuncWrapper
    def list_records_order_by_count(session: Session = None):
        return {
            'status': True,
            'data': [
                to_dict(i) for i in session.query(Record).filter().order_by(desc(Record.count)).all()
            ]
        }
