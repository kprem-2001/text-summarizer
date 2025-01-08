from textSummarizer.logging import logger
from textSummarizer.pipeline.stage1_data_ingestion import DataIngestionPipeline





STAGE_NAME = "Data imgestion stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
    raise e    
