import os
import mlflow
import mlflow.transformers
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "distilgpt2"
# Use a specific name for your model in the registry
REGISTERED_MODEL_NAME = "AdGeneratorModel"
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "models", "ad_model"))


import pandas as pd

DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data"))
CSV_PATH = os.path.join(DATA_DIR, "ads.csv") 

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find the CSV file at: {path}")
    
    print(f"Loading data from {path}...")
    
    # fix: on_bad_lines='skip' will ignore rows with too many commas 
    # instead of crashing.
    df = pd.read_csv(path, on_bad_lines='skip', encoding='utf-8')
    
    # Ensure no empty values
    df = df.dropna(subset=['Product', 'Ad'])
    
    formatted_data = [
        f"Product: {row['Product']}\nAd: {row['Ad']}" 
        for _, row in df.iterrows()
    ]
    
    return formatted_data

data = load_data(CSV_PATH)

class AdDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length=64):
        self.input_ids = []
        for txt in txt_list:
            enc = tokenizer(txt, truncation=True, max_length=max_length, padding="max_length")
            self.input_ids.append(torch.tensor(enc['input_ids']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {'input_ids': self.input_ids[idx], 'labels': self.input_ids[idx]}

def train():
    # 1. SETUP DATABASE BACKEND (Required for Registry)
    # ... inside train() ...

    # Build the absolute path to the DB file
    # SCRIPT_DIR is /app/train, so this goes up to /app/mlflow.db
    DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "mlflow.db"))

    # Note: SQLite URIs for absolute paths in Linux (Docker) need 4 slashes: sqlite:////path
    mlflow.set_tracking_uri(f"sqlite:///{DB_PATH}")
    
    
    
    mlflow.set_experiment("Ad_Generator_Experiment")
    
    # 2. AUTOLOGGING CONFIG
    # We set log_models=True so MLflow handles the heavy lifting
    mlflow.transformers.autolog(log_models=True)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    dataset = AdDataset(data, tokenizer)

    args = TrainingArguments(
        output_dir="./tmp_checkpoints",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        use_cpu=True,
        report_to="mlflow"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    with mlflow.start_run(run_name="training_run") as run:
        trainer.train()
        
        # 3. PUSH TO MODEL REGISTRY
        model_data = {"model": model, "tokenizer": tokenizer}
        
        print(f"--- Registering model as '{REGISTERED_MODEL_NAME}' ---")
        
        # Explicitly passing 'task' and avoiding auto-signature inference
        mlflow.transformers.log_model(
            transformers_model=model_data,
            artifact_path="model",
            registered_model_name=REGISTERED_MODEL_NAME,
            task="text-generation"  # This is the key fix
        )
        
        # Also save locally as you wanted
        model.save_pretrained(OUTPUT_DIR)
        tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    train()