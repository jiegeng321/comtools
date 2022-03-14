from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float

Base = declarative_base()


class FaceMetric(Base):
    __tablename__ = "face_metrics"
    id = Column(Integer, primary_key=True)
    model_version = Column(String(30))
    person_ids = Column(Integer)
    person_faces = Column(Integer)
    egao_ids = Column(Integer)
    egao_faces = Column(Integer)
    recall = Column(Float)
    fpr = Column(Float)
    date = Column(Date)
