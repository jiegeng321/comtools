import pandas as pd
from datetime import date

from sqlalchemy.orm import session
from database_util import get_dataset_session
from metrics.face_metric import FaceMetric

DBSession = get_dataset_session()
session = DBSession()


def import_metrics(filename, model_name, session):
    metrics_df = pd.read_csv(filename)
    print(metrics_df.head())
    for _, record in metrics_df.iterrows():
        new_porn_metric = FaceMetric(
            model_version=record["version"],
            person_ids=record["person_ids"],
            person_faces=record["faces_num"],
            egao_ids=record["egao_ids"],
            egao_faces=record["egao_faces_num"],
            recall=float(record["recall"][:-2]) / 100,
            fpr=float(record["fpr"][:-2]),
            date=date.today(),
        )
        session.add(new_porn_metric)
    session.commit()


metric_files = {
    "../history_csv/face_metrics.csv": "face",
}
for filename, model_name in metric_files.items():
    import_metrics(filename, model_name, session)
