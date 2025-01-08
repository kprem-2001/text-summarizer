from textSummarizer.logging import logger
from textSummarizer.pipeline.stage1_data_ingestion import DataIngestionPipeline
from textSummarizer.pipeline.stage2_data_validation import DataValidationPipeline






STAGE_NAME = "Data imgestion stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
    raise e    


STAGE_NAME = "Data Validation stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
    raise e    