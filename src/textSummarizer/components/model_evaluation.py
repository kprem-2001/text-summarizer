from dataclasses import dataclass
from pathlib import Path
import logging
import torch
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from evaluate import load
from tqdm import tqdm
from textSummarizer.entity import ModelEvaluationConfig
from transformers import GenerationConfig
from transformers import AutoConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def clean_text(self, text):
        return text.strip().replace("\n", " ").replace("\r", " ")
    
    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]
            
    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer, generation_config,
                                  batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
                                  column_text="dialogue", column_summary="summary"):
        
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))
        
        all_decoded_summaries = []
        all_target_summaries = []
        
        for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total=len(article_batches)):
            inputs = tokenizer(
                article_batch,
                max_length=1024,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            ).to(device)
            
            with torch.no_grad():
                summaries = model.generate(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    generation_config=generation_config
                )
            
            decoded_summaries = [
                self.clean_text(tokenizer.decode(s, skip_special_tokens=True))
                for s in summaries
            ]
            
            target_summaries = [self.clean_text(t) for t in target_batch]
            
            all_decoded_summaries.extend(decoded_summaries)
            all_target_summaries.extend(target_summaries)
        
        metric.add_batch(predictions=all_decoded_summaries, references=all_target_summaries)
        return metric.compute()
    
    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        config = AutoConfig.from_pretrained(self.config.model_path)
        config.forced_bos_token_id = 0
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.model_path,
            config = config
        ).to(device)
        model.eval()
        
        generation_config = GenerationConfig(
        max_length=128,
        min_length=40,
        length_penalty=1.2,
        num_beams=8,
        early_stopping=True,
        no_repeat_ngram_size=3,
        do_sample = True,
        forced_bos_token_id=0
        )
        
        # Load dataset and metric
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        
        rouge_metric = load('rouge', use_stemmer=True)
        
        # Calculate scores
        score = self.calculate_metric_on_test_ds(
            dataset_samsum_pt['test'],
            rouge_metric,
            model,
            tokenizer,generation_config,
            batch_size=8,
            
        )
        
        # Process and save results
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        rouge_dict = {rn: float(score[rn]) for rn in rouge_names}

        
        df = pd.DataFrame(rouge_dict, index=['bart'])
        df.to_csv(self.config.metric_file_name, index=False)