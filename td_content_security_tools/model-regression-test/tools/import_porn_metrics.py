import pandas as pd
from datetime import date

from sqlalchemy.orm import session
from database_util import get_dataset_session
from metrics.porn_metric import PornMetric

DBSession = get_dataset_session()
session = DBSession()


def import_porn_metrics(filename, model_name, session):
    porn_metrics = pd.read_csv(filename)
    print(porn_metrics.head())
    for _, record in porn_metrics.iterrows():
        new_porn_metric = PornMetric(
            model_name=model_name,
            model_version=record["version"],
            abnormal_precision=record["abnormal_precision"],
            abnormal_recall=record["abnormal_recall"],
            sexy_precision=record["sexy_precision"],
            sexy_recall=record["sexy_recall"],
            porn_precision=record["porn_precision"],
            porn_recall=record["porn_recall"],
            labels=record["cls_count"],
            date=date.today(),
            qps=125,
        )
        session.add(new_porn_metric)
    session.commit()


metric_files = {
    "../history_csv/porn_metrics.csv": "porn",
}
for filename, model_name in metric_files.items():
    import_porn_metrics(filename, model_name, session)

### import terror det

# session.close()
