from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CameleonMain(Base):
    __tablename__ = "cameleon_main"

    Id_Num = Column("Id_Num", String(), primary_key=True),
    patient = Column("patient", Integer()),
    name = Column("name", String(30)),
    Unit = Column("Unit", Integer()),
    Unit_wing = Column("Unit_wing", String()),
    Main_cause = Column("Main_cause", String()),
    ESI = Column("ESI", Integer()),
    bed = Column("bed", Integer()),
    warnings = Column("warnings", String())

