from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'andre_vieira',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 3),
}

dag = DAG('dag_airlines_reviews_batch_extraction_sentiment_analysis', 
	  description='Hello World DAG',
	  default_args=args,
	  dagrun_timeout=timedelta(seconds=360),
          catchup=False)
          
hello_operator = BashOperator(task_id='dag_airlines_reviews_batch_extraction_sentiment_analysis', 
				bash_command="""
				cd /home/andre/airflow/dags/batch &&
				python3 ./airlines_reviews_batch_extraction_sentiment_analysis.py
				""", 
				dag=dag
				)

hello_operator
