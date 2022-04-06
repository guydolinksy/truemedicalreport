from sqlalchemy import Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Measurements(Base):
    __tablename__ = "measurements"

    Id_Num = Column("Id_Num", String(), primary_key=True)
    Parameter_Date = Column("Parameter_Date", DateTime())
    Parameter_Id =Column("Parameter_Id",Integer())
    Parameter_Name = Column("Parameter_Name", String())
    Result = Column("Result", Float())
    Warnings = Column("Warnings", String())
    Min = Column("min",Integer(),nullable=True)
    Max = Column("max", Integer(),nullable=True)