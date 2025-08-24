from src.MultilingualSummarizer.logging import logger
from src.MultilingualSummarizer.pipeline.data_ingestion_pipeline import DataIngestionPipeline

STAGE_NAME="Data Ingestion Stage"

try:
    logger.info(f"stage {STAGE_NAME} initiated")
    data_ingestion_pipeline=DataIngestionPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f"Stage {STAGE_NAME} Completed")
except Exception as e:
    logger.exception(e)
    raise e