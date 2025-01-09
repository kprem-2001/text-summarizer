from textSummarizer.logging import logger
from textSummarizer.pipeline.stage1_data_ingestion import DataIngestionPipeline
from textSummarizer.pipeline.stage2_data_validation import DataValidationPipeline
from textSummarizer.pipeline.stage3_data_transformation import DataTransformationPipeline
from textSummarizer.pipeline.stage4_model_trainer import ModelTrainerPipeline
from textSummarizer.pipeline.stage5_model_evaluation import ModelEvaluationPipeline

STAGE_NAME = "Data imgestion stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
        


STAGE_NAME = "Data Validation stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
       


STAGE_NAME = "Data transformation stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)
    raise e
        


STAGE_NAME = "Model Trainer stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    Model_trainer = ModelTrainerPipeline()
    Model_trainer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)  
    raise e

STAGE_NAME = "Model Evaluation stage "
try:
    logger.info(f">>>>>> stage {STAGE_NAME} Started <<<<<<<")
    Model_evaluation = ModelEvaluationPipeline()
    Model_evaluation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n")
except Exception as e:
    logger.exception(e)  
    raise e