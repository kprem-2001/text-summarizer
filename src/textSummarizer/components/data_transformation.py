import os
from datasets import load_dataset , load_from_disk
from transformers import AutoTokenizer
from textSummarizer.logging import logger
from textSummarizer.entity import  DataTransformationConfig

class DataTransformation:
    def __init__(self,config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)
        
    def convert_example_to_feature(self,example_batch):
        input_encoding = self.tokenizer(example_batch['dialogue'] , max_length=1024 , truncation=True)
        
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'] , max_length=128 , truncation= True)
            
        return{
            'input_ids' : input_encoding['input_ids'],
            'attention_mask' : input_encoding['attention_mask'],
            'labels':target_encodings['input_ids']
        }
    
    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_example_to_feature ,batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir , "samsum_dataset"))            