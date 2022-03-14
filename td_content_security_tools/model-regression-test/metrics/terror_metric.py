from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float

Base = declarative_base()


class TerrorMetric(Base):
    __tablename__ = "terror_metrics"
    id = Column(Integer, primary_key=True)
    model_name = Column(String(30))
    precision = Column(Float)
    recall = Column(Float)
    label_num = Column(Integer)
    model_version = Column(String(30))
    date = Column(Date)
    qps = Column(Integer)

    def __repr__(self):
        return "<state(id='%s', model_name='%s', precision='%f', recall='%f',label_num='%d', model_version='%s', date='%s', qps='%d')>" % (
            self.id,
            self.model_name,
            self.precision,
            self.recall,
            self.label_num,
            self.model_version,
            self.date,
            self.qps,
        )
