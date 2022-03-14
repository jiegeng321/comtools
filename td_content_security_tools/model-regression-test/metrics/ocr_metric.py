from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float

Base = declarative_base()


class OCRMetric(Base):
    __tablename__ = "ocr_metrics"

    id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    line_recall = Column(Float)
    label_num = Column(Integer)
    qps = Column(Integer)
    model_version = Column(String(30))
    date = Column(Date)
