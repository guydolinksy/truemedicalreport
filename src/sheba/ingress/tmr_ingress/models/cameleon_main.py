# from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import Column, Integer, String, VARCHAR
# from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship

Base = declarative_base()


class CameleonMain(Base):
    __tablename__ = "chameleon_main"

    Id_Num = Column("id_num", VARCHAR(200), primary_key=True, autoincrement=False)
    patient_id = Column("patient_id", Integer())
    patient_name = Column("patient_name", String(30))
    gender = Column("gender", VARCHAR(100))
    Unit = Column("unit", Integer())
    Unit_wing = Column("unit_wing", String())
    Main_cause = Column("main_cause", String())
    ESI = Column("esi", Integer())
    bed_num = Column("bed_num", Integer())
    warnings = Column("warnings", String())

