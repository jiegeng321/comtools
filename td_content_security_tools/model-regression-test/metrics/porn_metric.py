from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float

Base = declarative_base()


class PornMetric(Base):
    __tablename__ = "brand_logo_tm_metrics"
    id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    abnormal_precision = Column(Float)
    abnormal_recall = Column(Float)
    sexy_precision = Column(Float)
    sexy_recall = Column(Float)
    porn_precision = Column(Float)
    porn_recall = Column(Float)
    model_version = Column(String(30))
    labels = Column(Integer)
    date = Column(Date)
    qps = Column(Integer)
