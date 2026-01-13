from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import os

# Define paths
DATA_PATH = "/opt/airflow/data/ads.csv"

def fetch_and_push_to_feature_store():
    """
    Simulates fetching new product entries and pushing to 'feature store' (CSV)
    """
    # 1. Simulate fetching new data (e.g., from an API or temporary file)
    new_entries = [
        {"Product": "Smart Watch", "Ad": "Stay connected on the go with our new Smart Watch!"},
        {"Product": "Gaming Chair", "Ad": "Level up your comfort with the Ultimate Gaming Chair."}
    ]
    df_new = pd.DataFrame(new_entries)
    
    # 2. Push to 'Feature Store' (Append to local CSV)
    if os.path.exists(DATA_PATH):
        df_new.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df_new.to_csv(DATA_PATH, index=False)
    
    print(f"Pushed {len(new_entries)} new records to the feature store (CSV).")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ad_generator_ml_pipeline',
    default_args=default_args,
    description='Fetch data, update feature store, and retrain model',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Fetch and Push Data
    fetch_data = PythonOperator(
        task_id='fetch_new_data',
        python_callable=fetch_and_push_to_feature_store,
    )

    # Task 2: Retrain Model (Orchestrates your existing script)
    # We use BashOperator to run the exact command you use manually
    retrain_model = BashOperator(
        task_id='retrain_model_mlflow',
        bash_command='python /opt/airflow/train/train.py',
    )

    fetch_data >> retrain_model