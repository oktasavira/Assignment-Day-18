from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2
import json

def extract_openaq_data():

    url = 'https://api.openaq.org/v2/locations?limit=100&page=1&offset=0&sort=desc&radius=1000&country=ID&city=Jakarta%20Central&order_by=lastUpdated&dump_raw=false'

    headers = {"accept": 'application/json'}

    response = requests.get(url,headers=headers)
    data = response.json()
    return data

def transform_and_load_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_data_task')

    conn = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5433")
    cursor = conn.cursor()

    for item in data['results']:
        id =item['id']
        city = item['city']
        name= item['name']
        entity = item['entity']
        country = item['country']
        sources = item['sources']
        isMobile = item['isMobile']
        isAnalysis = item['isAnalysis']
        sensorType = item['sensorType']
        lastUpdated = item['lastUpdated']
        firstUpdated = item['firstUpdated']
        latitude = item['coordinates']['latitude']
        longitude= item['coordinates']['longitude']
        measurements= item['measurements']
        parameter=json.dumps(item['parameters']) 
        manufacturer = json.dumps(item['manufacturers']) 

  
        cursor.execute("INSERT INTO results (id, city, name, entity, country, sources, isMobile, isAnalysis, sensorType, lastUpdated, firstUpdated, measurements, latitude, longitude, parameter, manufacturer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (id, city, name, entity, country, sources, isMobile, isAnalysis, sensorType, lastUpdated, firstUpdated, measurements, latitude, longitude, parameter, manufacturer))

    conn.commit()
    conn.close()




default_args = {
    'owner': 'owner',
    'start_date': datetime(2023, 10, 25, 4, 0, 0),
    'schedule_interval': '0 4 * * *',  
}

dag = DAG('openaq_data_pipeline', default_args=default_args)

extract_data_task = PythonOperator(
    task_id='extract_data_task',
    python_callable=extract_openaq_data,
    dag=dag
)

transform_and_load_task = PythonOperator(
    task_id='transform_and_load_task',
    python_callable=transform_and_load_data,
    dag=dag
)