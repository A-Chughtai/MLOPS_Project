import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("--- Testing Ad Generator API ---")
    
    # 1. Test Health
    print("\n[1] Testing /health...")
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Status: {r.status_code}, Response: {r.json()}")
    except Exception as e:
        print(f"Failed: {e}")

    # 2. Test Success Case
    print("\n[2] Testing /generate (Success)...")
    payload = {"product_name": "Premium Dark Chocolate"}
    r = requests.post(f"{BASE_URL}/generate", json=payload)
    if r.status_code == 200:
        data = r.json()
        print(f"Status: 200")
        print(f"Product: {data['product_name']}")
        print(f"Ad: {data['generated_ad'][:100]}...")
    else:
        print(f"Failed: {r.status_code}, {r.text}")

    # 3. Test Error Case (Missing key)
    print("\n[3] Testing /generate (Error - 400 Bad Request)...")
    bad_payload = {"wrong_key": "data"}
    r = requests.post(f"{BASE_URL}/generate", json=bad_payload)
    print(f"Status: {r.status_code}, Response: {r.json()}")

    # 4. Check Metrics
    print("\n[4] Checking /metrics...")
    r = requests.get(f"{BASE_URL}/metrics")
    if r.status_code == 200:
        print("Metrics endpoint reachable.")
        # Check if our custom metric exists in the text output
        if "api_requests_total" in r.text:
            print("Confirmed: 'api_requests_total' metric is being exported.")
    else:
        print(f"Failed to reach metrics: {r.status_code}")

if __name__ == "__main__":
    test_endpoints()