import requests
import time
import random

BASE_URL = "http://localhost:8000/generate"
PRODUCTS = [
    "Wireless Headphones", 
    "Organic Coffee", 
    "Running Shoes", 
    "Smart Watch", 
    "Yoga Mat"
]

def run_load_test(iterations=50, delay=0.5):
    print(f"Starting load test: {iterations} requests, {delay}s delay...")
    
    success_count = 0
    error_count = 0
    
    start_time = time.time()
    
    for i in range(iterations):
        # Occasionally send a bad request to test error metrics (10% of the time)
        if random.random() < 0.1:
            payload = {"invalid": "data"}
        else:
            payload = {"product_name": random.choice(PRODUCTS)}
            
        try:
            r = requests.post(BASE_URL, json=payload, timeout=10)
            if r.status_code == 200:
                success_count += 1
            else:
                error_count += 1
            
            print(f"Request {i+1}/{iterations} | Status: {r.status_code}", end="\r")
            
        except Exception as e:
            print(f"\nRequest {i+1} failed: {e}")
            error_count += 1
            
        time.sleep(delay)
    
    total_time = time.time() - start_time
    print(f"\n\n--- Load Test Finished ---")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Throughput: {iterations/total_time:.2f} requests/sec")
    print(f"Successes: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Check your Grafana dashboard now!")

if __name__ == "__main__":
    run_load_test(iterations=30, delay=0.2)