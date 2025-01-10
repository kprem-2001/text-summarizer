from textSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer
from transformers import pipeline

class PredictionPipelin:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
        
    
    def predict(self , text):
        tokenizer  = AutoTokenizer.from_pretrained("artifacts/model_trainer/tokenizer")
        gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": 128}
        
        pipe = pipeline("summarization",model="artifacts/model_trainer/bart-samsum-model" , tokenizer=tokenizer)
        
        print("Dialogue:")
        print(text)
        
        output = pipe(text , **gen_kwargs)[0]["summary_text"]
        print("\nmodel summary")
        print(output)
        
        return output
    
    