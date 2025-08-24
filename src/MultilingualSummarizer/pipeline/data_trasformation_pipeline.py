from src.MultilingualSummarizer.components.data_transformation import DataTransformation
from src.MultilingualSummarizer.entity import DataTransformationConfig
from src.MultilingualSummarizer.logging import logger
from src.MultilingualSummarizer.config.configuration import ConfigurationManager


class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        config=ConfigurationManager()
        data_transformation_config=config.get_data_transformation_config()
        data_transformation=DataTransformation(config=data_transformation_config)
        data_transformation.convert()