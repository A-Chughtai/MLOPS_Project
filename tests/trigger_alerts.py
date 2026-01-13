import requests
import time
import concurrent.futures

BASE_URL = "http://localhost:8000"

def send_error_request():
    """Triggers HighErrorRate by causing an internal exception (500)"""
    # Sending a non-string to product_name might cause a crash in the tokenizer/model logic
    # which will be caught by the try-except and return a 500.
    payload = {"product_name": None} 
    try:
        requests.post(f"{BASE_URL}/generate", json=payload)
    except:
        pass

def send_heavy_request():
    """Triggers HighAPILatency by saturating the API"""
    payload = {"product_name": "Triggering a very long generation sequence to increase latency " * 5}
    try:
        requests.post(f"{BASE_URL}/generate", json=payload)
    except:
        pass

def trigger_high_error_rate(duration_mins=6):
    print(f"--- Triggering HighErrorRate (Target: > 0.1 err/s for 5m) ---")
    end_time = time.time() + (duration_mins * 60)
    while time.time() < end_time:
        # Send ~1 request per second (0.1 threshold is easily hit)
        send_error_request()
        time.sleep(1)
        print(f"Error packets sent. Time remaining: {int(end_time - time.time())}s", end="\r")

def trigger_high_latency(duration_mins=6):
    print(f"\n--- Triggering HighAPILatency (Target: > 2s for 5m) ---")
    end_time = time.time() + (duration_mins * 60)
    # Using thread pool to saturate the Gunicorn workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while time.time() < end_time:
            executor.submit(send_heavy_request)
            time.sleep(0.1)
            print(f"Latency stress ongoing. Time remaining: {int(end_time - time.time())}s", end="\r")

if __name__ == "__main__":
    print("Which alert do you want to trigger?")
    print("1. High Error Rate (Critical)")
    print("2. High API Latency (Warning)")
    choice = input("Enter 1 or 2: ")
    
    if choice == "1":
        trigger_high_error_rate()
    elif choice == "2":
        trigger_high_latency()
    else:
        print("Invalid choice.")