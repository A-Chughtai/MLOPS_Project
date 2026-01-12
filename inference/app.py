from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from . import inference

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

API_LATENCY = Histogram(
    'api_latency_seconds',
    'API endpoint latency in seconds',
    ['endpoint']
)

REQUEST_THROUGHPUT = Counter(
    'api_requests_total',
    'Total number of API requests (throughput)',
    ['endpoint']
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Calculate request latency
    latency = time.time() - request.start_time
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown'
    ).observe(latency)
    
    # Record API-specific metrics for /generate endpoint
    if request.endpoint == 'generate_ad':
        API_LATENCY.labels(endpoint='generate').observe(latency)
        REQUEST_THROUGHPUT.labels(endpoint='generate').inc()
    
    return response

@app.route("/")
def root():
    return jsonify({"message": "Ad Generator API is running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/generate", methods=["POST"])
def generate_ad_endpoint():
    try:
        data = request.get_json()
        if not data or 'product_name' not in data:
            return jsonify({"error": "Missing 'product_name' in request body"}), 400
        
        product_name = data['product_name']
        generated_text = inference.generate_ad(product_name)  # Changed to use inference.generate_ad()
        
        return jsonify({
            "product_name": product_name,
            "generated_ad": generated_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)