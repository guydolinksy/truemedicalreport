import datetime

from .base import Base
from sqlalchemy import Column, VARCHAR, Integer, DateTime, Date, BigInteger
from enum import Enum

description_codes = {"nurse_summarize": {"code": 901, "title": "סיכום ביקור אחות", "text_list": ["""בדרך כלל בריא, חווה כאבים בצד שמאל מאתמול בערב.
מלווה בכאבי ראש וסחרחורות לסירוגין""", """לא מסוגל להזיז את היד, חשש לשבר במפרק כף היד""",
                                                                                                 """מתלונן על כאבי גב מזה תקופה ארוכה, לטענתו חווה קשיי בעת מעבר בין ישיבה לעמידה"""]},
                     "doctor_summarie": {"code": 889, "title": "סיכום רופא"}}
units_code = {"er": {"code": 5, "title": """מלר"ד"""}}


# real code og er in chameleon is 1184000

class ChameleonMedicalFreeText(Base):
    __tablename__ = "medical_free_text"
    row_id = Column("Row_ID", BigInteger(), auto_increment=True, primary_key=True)
    patient_id = Column("Id", BigInteger())
    medical_record = Column("Medical_Record", BigInteger())
    documenting_date = Column("DocumentingDate", Date())
    documenting_time = Column("DocumentingTime", DateTime())
    unit_name = Column("unit_name", VARCHAR(80))
    unit = Column("Unit", BigInteger())
    medical_text_code = Column("Description_code", BigInteger())
    medical_text_title = Column("Description", VARCHAR(500))
    medical_text = Column("Description_Text", VARCHAR())
    documenting_user = Column("DocumentingUser", BigInteger())
    source = Column("source", VARCHAR(), default="chameleon")
    # date of inserting the row to ARC db
    insert_date = Column("insert_date", DateTime(), default=datetime.datetime.utcnow())

    def to_dal(self):
        return dict(
            since=self.documenting_time,
            code=self.medical_text_code,
            text=self.medical_text
        )
