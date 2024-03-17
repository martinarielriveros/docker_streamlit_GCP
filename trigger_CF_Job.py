from google.cloud import storage
from google.cloud import dataproc_v1 as dataproc

def trigger_dataproc(event, context):
    
    # Extract the bucket and file information from the event
    bucket_name = event['bucket']
    file_name = event['name']

    # Specify the Dataproc job parameters
    PROJECT_ID = 'dataproc-grupo5-test'
    REGION = 'us-central1'  # Replace with the actual Dataproc region
    CLUSTER_NAME = 'cluster-9f2c'  # Replace with the actual Dataproc cluster name
    MAIN_PYSPARK_FILE_URI = 'gs://path/to/your/pyspark/file'  # Update with the actual Cloud Storage URI of your main PySpark file

    # Create a Dataproc client
    client = dataproc.JobControllerClient()

    # Specify the new job to be submitted
    job = {
        'placement': {'cluster_name': CLUSTER_NAME},
        'pyspark_job': {
            'main_python_file_uri': MAIN_PYSPARK_FILE_URI
        }
    }

    # Submit the new job on Dataproc
    operation = client.submit_job(project_id=PROJECT_ID, region=REGION, job=job)
    result = operation.result()

    # Print the result or log it as needed
    print(f'Dataproc job triggered: {result.job.job_id}')
