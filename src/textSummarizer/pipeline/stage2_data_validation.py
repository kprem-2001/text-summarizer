from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_validation import Data_validation
from textSummarizer.logging import logger


class DataValidationPipeline():
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        validation_data_config = config.get_data_validation_config()
        data_validation = Data_validation(config= validation_data_config)
        data_validation.validate_files_exist()
        