
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "models", "ad_model"))

MODEL_PATH = OUTPUT_DIR
BASE_MODEL = "distilgpt2"

# Global variables for model caching
_tokenizer = None
_model = None
_model_loaded = False

def _load_model():
    """Load model once and cache it for subsequent requests"""
    global _tokenizer, _model, _model_loaded
    
    if not _model_loaded:
        # Check if we have a trained model, otherwise use base
        target_model = MODEL_PATH if os.path.exists(MODEL_PATH) else BASE_MODEL
        print(f"Loading model from: {target_model}")

        _tokenizer = AutoTokenizer.from_pretrained(target_model)
        _model = AutoModelForCausalLM.from_pretrained(target_model)
        _model_loaded = True
        print("Model loaded and cached successfully")
    
    return _tokenizer, _model

def generate_ad(product_name):
    """Generate an ad for the given product name"""
    tokenizer, model = _load_model()
    
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