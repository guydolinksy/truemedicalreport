from sqlalchemy import Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Measurements(Base):
    __tablename__ = "measurements"

    Id_Num = Column("Id_Num", Integer(), primary_key=True)
    Parameter_Date = Column("Parameter_Date", DateTime())
    Parameter_Name = Column("Parameter_Name", String())
    Result = Column("Result", String())
    Warnings = Column("Warnings", String())
