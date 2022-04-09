from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship

Base = declarative_base()


class Measurements(Base):
    __tablename__ = "measurements"

    Id_Num = Column("id_num", VARCHAR(200), primary_key=True)
    Parameter_Date = Column("Parameter_Date", DateTime())
    Parameter_ID = Column("Parameter_Id", Integer(), primary_key=True)
    Parameter_Name = Column("Parameter_Name", VARCHAR(100))
    Result = Column("Result", Float())
    Min_Value = Column("Min_Value", Float())
    Max_Value = Column("Max_Value", Float())
    Warnings = Column("Warnings", VARCHAR(100))
