## How to use Dataproc in GCP for a new project

Dataproc Serverless allows you to run PySpark batch workloads and sessions (notebooks) with auto-configured infrastructure and autoscaling. Dataproc Serverless is fully integrated with several Google Cloud services, including BigQuery, Cloud Storage, Vertex AI, and Dataplex.



1) Create a project in GCP

1.1) Enable necesary APIs:
    
- BigQuery API

- Cloud Dataproc API

2) Cloud Shell provides a shell environment inside the Google Cloud console.

Open Cloud Shell:

a) Chech if the project is set:

    echo ${GOOGLE_CLOUD_PROJECT}

b) If your project ID is not set, run the following command to set it:

    export \
    GOOGLE_CLOUD_PROJECT= `replace-this-with-your-project-id`

c) Run the following command to configure the gcloud commands to use your current project's ID (grupo5-dataproctest):


    gcloud config set project grupo5-dataproctest

3) Set a Compute Engine region for your resources, such as us-central1 or europe-west2.

    export REGION=us-central1

3) Check wich service accounts are in use

**A service account is a type of Google account that can be used by an application to access Google APIs programmatically via OAuth 2.0.**

    gcloud auth list

4) Go to Billing and link a Billing account to your project
5) Activate Dataproc and create a Cluster

under "select your infrastructure service" we choose **Cluster on Compute Engine**.

Choose the Compute Engine settings to your likes. In my case:

    gcloud dataproc clusters create grupo5-clustertest
    --region us-central1
    --master-machine-type n2-standard-4 --master-boot-disk-size 500
    --num-workers 2
    --worker-machine-type n2-standard-4 --worker-boot-disk-size 500
    --image-version 2.1-debian11
    --scopes 'https://www.googleapis.com/auth/cloud-platform' --project grupo5-dataproctest


6) Create a Bucket

    gsutil mb gs://grupo5-dataproctest-bucket

