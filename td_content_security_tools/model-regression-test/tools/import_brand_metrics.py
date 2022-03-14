import pandas as pd
from datetime import date

from sqlalchemy.orm import session
from database_util import get_dataset_session
from metrics.brand_metric import BrandMetric

DBSession = get_dataset_session()
session = DBSession()


def import_porn_metrics(filename, model_name, session):
    metrics_df = pd.read_csv(filename)
    print(metrics_df.head())
    for _, record in metrics_df.iterrows():
        new_porn_metric = BrandMetric(
            model_version=record["version"],
            brand_num=record["brand_num"],
            style_num=record["style_num"],
            date=date.today(),
        )
        session.add(new_porn_metric)
    session.commit()


metric_files = {
    "../history_csv/brand_metrics2.csv": "brand",
}
for filename, model_name in metric_files.items():
    import_porn_metrics(filename, model_name, session)
