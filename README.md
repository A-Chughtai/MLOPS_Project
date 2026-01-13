

# MLFLOW Setup

To start mlflow, use the following

```mlflow ui --backend-store-uri sqlite:///mlflow.db```

make sure **mlflow.db** is in the root

# Command Line Inference

```curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d "{\"product_name\": \"Dairy Chocolate\"}"```
