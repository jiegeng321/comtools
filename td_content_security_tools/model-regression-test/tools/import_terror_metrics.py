import pandas as pd
from datetime import date
from sqlalchemy.orm import session
from database_util import get_dataset_session
from metrics.terror_metric import TerrorMetric

DBSession = get_dataset_session()

### import terror cls metrics
terror_cls_pr = pd.read_csv("../history_csv/terror_cls_pr.csv")
terror_cls_labels = pd.read_csv("../history_csv/terror_cls_labels.csv")

terror_cls_metrics = pd.merge(terror_cls_pr, terror_cls_labels, on=["version"])
print(terror_cls_metrics.head())
session = DBSession()
for index, record in terror_cls_metrics.iterrows():
    new_terror_metric = TerrorMetric(
        model_name="terror_cls",
        model_version=record["version"],
        precision=record["precision"],
        recall=record["recall"],
        label_num=record["label"],
        date=date.today(),
        qps=120,
    )
    session.add(new_terror_metric)
session.commit()

### import terror det
terror_det_pr = pd.read_csv("../history_csv/terror_det_tpr_fpr.csv")
terror_det_labels = pd.read_csv("../history_csv/terror_det_labels.csv")

terror_det_metrics = pd.merge(terror_det_pr, terror_det_labels, on=["version", "date"])
print(terror_det_metrics.head())
for index, record in terror_det_metrics.iterrows():
    new_terror_metric = TerrorMetric(
        model_name="terror_det",
        model_version=record["version"],
        precision=record["tpr"],
        recall=record["fpr"],
        label_num=record["label"],
        date=date.today(),
        qps=record["qps"],
    )
    session.add(new_terror_metric)
session.commit()
session.close()
