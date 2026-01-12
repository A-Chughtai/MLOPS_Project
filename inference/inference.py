
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os


import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "models", "ad_model"))

MODEL_PATH = OUTPUT_DIR
BASE_MODEL = "distilgpt2"

def generate_ad(product_name):
    # Check if we have a trained model, otherwise use base
    target_model = MODEL_PATH if os.path.exists(MODEL_PATH) else BASE_MODEL
    print(f"Loading model from: {target_model}")

    tokenizer = AutoTokenizer.from_pretrained(target_model)
    model = AutoModelForCausalLM.from_pretrained(target_model)
    
    # Prompt formatting
    prompt = f"Product: {product_name}\nAd:"
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs, 
        max_new_tokens=40, 
        do_sample=True, 
        temperature=0.85,
        pad_token_id=tokenizer.eos_token_id
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    import sys
    # Allow command line argument for product name
    product = sys.argv[1] if len(sys.argv) > 1 else "Dairy Chocolate"
    print("\n" + "="*30)
    print(generate_ad(product))
    print("="*30 + "\n")