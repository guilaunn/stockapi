from sqlalchemy import Column, String, Integer, Float, Date
from app.database import Base

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    purchased_amount = Column(Integer)
    purchased_status = Column(String)
    request_data = Column(Date)
    company_code = Column(String, index=True)
    company_name = Column(String)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    performance_data_five_days = Column(Float)
    performance_data_one_month = Column(Float)
    performance_data_three_months = Column(Float)
    performance_data_year_to_date = Column(Float)
    performance_data_one_year = Column(Float)
