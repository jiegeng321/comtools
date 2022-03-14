from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_dataset_session():
    dataset_name = "image_model_metrics"
    host = "192.168.6.70"
    port = "3306"
    username = "image_model_metrics"
    password = "nchvvbol"
    engine = create_engine(
        f"mysql://{username}:{password}@{host}:{port}/{dataset_name}",
        pool_pre_ping=True,
        pool_recycle=2400,
    )
    DBSession = sessionmaker(bind=engine)
    return DBSession
