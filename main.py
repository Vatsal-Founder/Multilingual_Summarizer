from src.MultilingualSummarizer.logging import logger
from src.MultilingualSummarizer.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.MultilingualSummarizer.pipeline.data_trasformation_pipeline import DataTransformationPipeline
from src.MultilingualSummarizer.pipeline.model_trainer_pipeline import ModelTrainerPipeline

STAGE_NAME="Data Ingestion Stage"

try:
    logger.info(f"stage {STAGE_NAME} initiated")
    data_ingestion_pipeline=DataIngestionPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f"Stage {STAGE_NAME} Completed")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Data Transformation Stage"

try:
    logger.info(f"stage {STAGE_NAME} initiated")
    data_transformation_pipeline=DataTransformationPipeline()
    data_transformation_pipeline.initiate_data_transformation()
    logger.info(f"Stage {STAGE_NAME} Completed")
except Exception as e:
    logger.exception(e)

STAGE_NAME="Model Training Stage"

try:
    logger.info(f"stage {STAGE_NAME} initiated")
    model_trainer_pipeline=ModelTrainerPipeline()
    model_trainer_pipeline.initiate_model_training()
    logger.info(f"Stage {STAGE_NAME} Completed")
except Exception as e:
    logger.exception(e)
    raise e