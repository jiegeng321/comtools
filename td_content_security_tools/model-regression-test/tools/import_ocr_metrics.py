import pandas as pd
from datetime import date

from sqlalchemy.orm import session
from database_util import get_dataset_session
from metrics.ocr_metric import OCRMetric

DBSession = get_dataset_session()
session = DBSession()


def import_ocr_metrics(filename, model_name, session):
    ocr_fast_metric = pd.read_csv(filename)
    ocr_fast_metric.drop(ocr_fast_metric.head(3).index, inplace=True)
    ocr_fast_metric["line_recall"] = ocr_fast_metric[
        ["LR_AD964", "LR_AD964ROT", "LR_RB500"]
    ].apply(
        lambda x: x["LR_AD964"] * 0.45546256
        + x["LR_AD964ROT"] * 0.45546256
        + x["LR_RB500"] * 0.08907488,
        axis=1,
    )
    for _, record in ocr_fast_metric.iterrows():
        new_terror_metric = OCRMetric(
            model_name=model_name,
            model_version=record["VERSION"],
            line_recall=record["line_recall"],
            date=date.today(),
            qps=record["QPS"],
        )
        session.add(new_terror_metric)
    session.commit()


metric_files = {
    "../history_csv/ai-adver-ocr-metric.csv": "ocr_fast",
    "../history_csv/ai-adver-ocr-acc-metric.csv": "ocr_acc",
}
for filename, model_name in metric_files.items():
    import_ocr_metrics(filename, model_name, session)
