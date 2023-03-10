import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_config = Variable.get("my_dag_config", deserialize_json=True)

# Define the DAGs
dags = []

for dag_file in os.listdir(os.path.dirname(__file__)):
    if dag_file.endswith(".py") and not dag_file.startswith("_"):
        module_name = os.path.splitext(dag_file)[0]
        dag_module = __import__(
            f"{os.path.basename(__file__).replace('.py', '')}.{module_name}",
            fromlist=['dag']
        )
        dag = dag_module.dag
        dag_id = dag.dag_id
        if dag_id in dag_config:
            dag_config[dag_id]['schedule_interval'] = dag.schedule_interval
            dag_config[dag_id]['default_args'] = dag.default_args
        dags.append(dag)

# Update the configuration in Airflow Variables
Variable.set("my_dag_config", dag_config, serialize_json=True)
