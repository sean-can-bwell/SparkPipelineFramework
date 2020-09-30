from typing import Optional, Dict, Any

from pyspark import keyword_only
from pyspark.sql.dataframe import DataFrame

from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.proxy_generator.python_proxy_base import PythonProxyBase


class FeatureTransformer(PythonProxyBase):
    # noinspection PyUnusedLocal
    @keyword_only
    def __init__(self,
                 name: str = None,
                 parameters: Optional[Dict[str, Any]] = None,
                 progress_logger: Optional[ProgressLogger] = None,
                 verify_count_remains_same: bool = False
                 ) -> None:
        super(FeatureTransformer, self).__init__(name=name,
                                                 parameters=parameters,
                                                 progress_logger=progress_logger,
                                                 verify_count_remains_same=verify_count_remains_same)

    def _transform(self, df: DataFrame) -> DataFrame:
        pass
