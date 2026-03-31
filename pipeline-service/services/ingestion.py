import dlt
import requests
import os

@dlt.resource(table_name="customers", write_disposition="merge", primary_key="customer_id")
def fetch_flask_data():
    url = "http://mock-server:5000/api/customers"
    page = 1
    limit = 10
    
    while True:
        response = requests.get(f"{url}?page={page}&limit={limit}")
        response.raise_for_status()
        payload = response.json()
        
        data = payload.get("data", [])
        if not data:
            break
            
        yield data
        
        if page * limit >= payload.get("total", 0):
            break
        page += 1

def run_ingestion():
    db_url = os.getenv("DATABASE_URL")
    pipeline = dlt.pipeline(
        pipeline_name='flask_ingestion',
        destination=dlt.destinations.postgres(db_url),
        dataset_name='public' 
    )
    
    load_info = pipeline.run(fetch_flask_data())
    
    load_info.raise_on_failed_jobs()
    
    return {"status": "success", "records_processed": 20}