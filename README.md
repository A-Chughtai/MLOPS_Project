# 🎯 Ad Generator ML Pipeline

A production-ready Machine Learning pipeline for generating product advertisements using fine-tuned transformer models. This project demonstrates end-to-end ML operations including model training, deployment, monitoring, and orchestration.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Services Overview](#services-overview)
- [Usage](#usage)
- [Monitoring & Observability](#monitoring--observability)
- [Model Training](#model-training)
- [Testing](#testing)
- [Screenshots](#screenshots)

## ✨ Features

- **🤖 ML Model**: Fine-tuned DistilGPT2 model for ad generation
- **🚀 REST API**: Flask-based inference service with Prometheus metrics
- **📊 MLflow Integration**: Model versioning, tracking, and registry
- **📈 Monitoring Stack**: Prometheus + Grafana + Alertmanager
- **🔄 Workflow Orchestration**: Apache Airflow for automated training pipelines
- **🐳 Containerized**: Fully Dockerized deployment
- **📉 Real-time Metrics**: API latency, throughput, and error rate tracking
- **🚨 Alerting**: Automated alerts for high latency, errors, and service downtime

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Airflow   │────▶│  Training    │────▶│   MLflow    │
│ Orchestrator│     │   Pipeline    │     │   Registry  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Fine-tuned  │
                    │    Model     │
                    └──────────────┘
                            │
                            ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Grafana   │◀────│  Prometheus  │◀────│  Flask API │
│  Dashboards │     │   Scraper    │     │  Inference  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Alertmanager │
                    │   Alerts     │
                    └──────────────┘
```

## 📦 Prerequisites

- **Docker** & **Docker Compose** installed
- **Python 3.10+** (for local development/testing)
- At least **4GB RAM** available for Docker containers
- **Ports available**: 8000, 3000, 9090, 9093, 8080

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd new_project
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- **Inference API** (port 8000)
- **Prometheus** (port 9090)
- **Grafana** (port 3000)
- **Alertmanager** (port 9093)
- **Airflow** (port 8080)

### 3. Verify Services

```bash
# Check all containers are running
docker-compose ps

# View logs
docker-compose logs -f inference-api
```

### 4. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Inference API** | http://localhost:8000 | N/A |
| **Grafana** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9090 | N/A |
| **Alertmanager** | http://localhost:9093 | N/A |
| **Airflow** | http://localhost:8080 | Check logs for credentials |

## 📁 Project Structure

```
new_project/
├── inference/              # Inference service
│   ├── app.py             # Flask API with Prometheus metrics
│   ├── inference.py       # Model inference logic with caching
│   └── Dockerfile         # Container definition
├── train/                 # Training pipeline
│   └── train.py          # MLflow-integrated training script
├── dags/                  # Airflow workflows
│   └── ml_pipeline_dag.py # Training orchestration DAG
├── prometheus/            # Prometheus configuration
│   ├── prometheus.yml     # Scrape configs
│   └── alerts.yml         # Alert rules
├── grafana/               # Grafana provisioning
│   ├── provisioning/      # Auto-configured datasources
│   └── dashboards/        # Pre-built dashboards
├── alertmanager/          # Alert routing
│   └── alertmanager.yml   # Alert configuration
├── tests/                 # Test scripts
│   ├── test_api.py       # Functional API tests
│   ├── load_test.py      # Load testing script
│   └── trigger_alerts.py # Alert testing script
├── data/                  # Training data
│   └── ads.csv           # Product-ad pairs dataset
├── models/                # Trained models
│   └── ad_model/         # Fine-tuned model artifacts
├── docker-compose.yml     # Multi-container orchestration
└── requirements.txt       # Python dependencies
```

## 🔧 Services Overview

### Inference API (`inference-api`)

Flask-based REST API for ad generation with built-in Prometheus metrics.

**Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /generate` - Generate ad for a product
- `GET /metrics` - Prometheus metrics endpoint

**Example Request:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Premium Coffee Beans"}'
```

**Response:**
```json
{
  "product_name": "Premium Coffee Beans",
  "generated_ad": "Product: Premium Coffee Beans\nAd: Experience the rich aroma..."
}
```

### Prometheus (`prometheus`)

Metrics collection and alerting engine. Scrapes metrics from the inference API every 10 seconds.

**Key Metrics:**
- `api_latency_seconds` - API response latency histogram
- `api_requests_total` - Total API requests (throughput)
- `http_requests_total` - HTTP request counter by status
- `http_request_duration_seconds` - HTTP latency histogram

### Grafana (`grafana`)

Visualization platform with pre-configured dashboards for:
- API Latency (95th percentile)
- Request Throughput (requests/second)
- Error Rates
- Service Health

**Pre-configured Dashboard:** `ML Inference API - System & Performance Dashboard`

### Alertmanager (`alertmanager`)

Routes alerts from Prometheus based on severity:
- **Critical**: Service down, high error rate, very high latency
- **Warning**: High latency, low throughput

### Airflow (`airflow`)

Workflow orchestration for automated model retraining.

**DAG:** `ad_generator_ml_pipeline`
- **Schedule**: Daily (`@daily`)
- **Tasks**:
  1. `fetch_new_data` - Fetch and append new product entries to feature store
  2. `retrain_model_mlflow` - Retrain model using MLflow

## 📊 Monitoring & Observability

### Metrics Exposed

The inference API exposes the following Prometheus metrics:

```prometheus
# API-specific metrics
api_latency_seconds_bucket{endpoint="generate"}    # Latency histogram
api_requests_total{endpoint="generate"}            # Request counter

# HTTP-level metrics
http_requests_total{method, endpoint, status}     # Request counter
http_request_duration_seconds_bucket{...}         # Latency histogram
```

### Alert Rules

Configured alerts in `prometheus/alerts.yml`:

| Alert | Condition | Severity | Duration |
|-------|-----------|----------|----------|
| HighAPILatency | 95th percentile > 2s | Warning | 5m |
| VeryHighAPILatency | 95th percentile > 5s | Critical | 2m |
| HighErrorRate | Error rate > 0.1 req/s | Critical | 5m |
| ServiceDown | Service unavailable | Critical | 1m |
| LowThroughput | Throughput < 0.1 req/s | Warning | 10m |

### Viewing Metrics

1. **Prometheus UI**: http://localhost:9090
   - Query: `rate(api_requests_total[5m])`
   - Query: `histogram_quantile(0.95, api_latency_seconds_bucket)`

2. **Grafana Dashboard**: http://localhost:3000
   - Navigate to Dashboards → ML Inference API

3. **Raw Metrics**: http://localhost:8000/metrics

## 🎓 Model Training

### Manual Training

```bash
# Train the model locally
python train/train.py
```

The training script:
- Loads data from `data/ads.csv`
- Fine-tunes DistilGPT2 model
- Logs metrics to MLflow
- Saves model to `models/ad_model/`

### MLflow UI

Start MLflow tracking server:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Access at: http://localhost:5000

### Automated Training (Airflow)

The Airflow DAG automatically:
1. Fetches new product entries
2. Appends to feature store (`data/ads.csv`)
3. Triggers model retraining
4. Logs to MLflow

**Trigger Manually:**
- Go to http://localhost:8080
- Find `ad_generator_ml_pipeline` DAG
- Click "Play" button

## 🧪 Testing

### Functional Tests

```bash
python tests/test_api.py
```

Tests:
- Health endpoint
- Successful ad generation
- Error handling
- Metrics endpoint

### Load Testing

Generate traffic to populate metrics:

```bash
python tests/load_test.py
```

This sends 30 requests with 0.2s delay between each.

### Alert Testing

Trigger alerts to test monitoring:

```bash
python tests/trigger_alerts.py
```

Choose:
- `1` - Trigger High Error Rate alert
- `2` - Trigger High Latency alert

## 📸 Screenshots

### MLflow Model Registry
![MLflow Model](ss/mlflow_model.png)

### MLflow Training Runs
![MLflow Runs](ss/mlflow_runs.png)

### MLflow Metrics
![MLflow Metrics](ss/mlflow_metrics.png)

### Grafana Dashboard
![Grafana](ss/Grafana.png)

### Prometheus Targets
![Prometheus](ss/Prometheus.png)

### Prometheus Alerts
![Alerts](ss/Alerts.png)

### Alertmanager
![Alert Manager](ss/Alert-Manager.png)

### Airflow DAGs
![Airflow](ss/airflow_dags.png)

## 🔍 Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Metrics Not Appearing in Grafana

1. Verify Prometheus is scraping: http://localhost:9090/targets
2. Check metrics endpoint: http://localhost:8000/metrics
3. Ensure Grafana datasource is configured: http://localhost:3000/connections/datasources

### Model Not Loading

1. Check model files exist: `ls models/ad_model/`
2. Verify model path in `inference/inference.py`
3. Check container logs: `docker-compose logs inference-api`

### Airflow DAG Not Showing

1. Check DAG file syntax: `python dags/ml_pipeline_dag.py`
2. Verify DAG folder is mounted: Check `docker-compose.yml` volumes
3. Check Airflow logs: `docker-compose logs airflow`

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
cd inference
python app.py

# Run training locally
python train/train.py
```

### Adding New Metrics

Edit `inference/app.py` to add custom Prometheus metrics:

```python
from prometheus_client import Counter, Histogram

MY_METRIC = Counter('my_metric_total', 'Description')
MY_METRIC.inc()
```

### Modifying Alert Rules

Edit `prometheus/alerts.yml` and reload Prometheus:

```bash
# Reload Prometheus config
curl -X POST http://localhost:9090/-/reload
```

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using Flask, MLflow, Prometheus, Grafana, and Airflow**
