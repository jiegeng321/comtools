from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float

Base = declarative_base()


class PatternMetric(Base):
    __tablename__ = "brand_pattern_metrics"
    id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    model_version = Column(String(30))
    recall = Column(Float)
    precision = Column(Float)
    brand_num = Column(Integer)
    style_num = Column(Integer)
    date = Column(Date)
