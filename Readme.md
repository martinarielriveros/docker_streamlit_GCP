# Objective

"i need an app running a simple pyhton fron-end on the cloud (not a special host like Streamlit Community Cloud). That app will allow me to select some settings to perform a SQL search also on data stored on the cloud. The files to search/analyze are  big, in terms of houndreds of Gb, although the results are tiny. I need to get those results on my browser".

This statement triggers the following steps (this is how i did it, i may be wrong or maybe you can think of other, nevertheless it works fine)

Some tasks need to be done locally and some on the cloud (of course...):

1) On the cloud:

Create a Project.\
Create a Billing Account linked to the Project.\
Create IAM roles needed according to the task.\
Enable Artifact Registry and Container Registry.\
Enable Google Storage and upload the files to analize/search on a Bucket.\
Enable Google Big Query and link it to the Buckets.
Get the .json file to connect to BigQuery.\

2) Locally on your machine:


Create your app (in my case using Stremlit library for front-end).\
Create a requiremets.txt mandatory file.\
Create a Docker File to wrap it up and crate the image.\
Tag your image.\
Upload it to the cloud (Artifact Registry).

3) Again on the cloud

Enable Google Cloud Run (you could have done it in step one also).\
Create a new service ponting to the uploaded image in Artifact Registry.\
This last step will give you the public (if so) endopoint to your app.

**And that's it.**

Now we will go step by step with relavent issues, not necesary in the same order as some tasks are not shown here or even a complete list.

### Guide to create a Streamlit App (simple web interface)

This is a step by step guide to remind me how i did to create a streamlit app and then deploy it to GCP.
There are some steps to skip if already done

Install the framework (simple use front-end tool specialized for data visualization)

    pip install streamlit

Create your awesome python + streamleit app. Save it like a .py file:

    crap.py

To run your app, you type:

    streamlit run crap.py

A message like this is shown in the terminal, and a web browser is opened:


**You can now view your Streamlit app in your browser.**

**Local URL**: http://localhost:8501

**Network URL**: http://192.168.1.11:8501

You can refer to [markdown cheatsheet](https://markdownguide.offshoot.io/cheat-sheet/) to enhance/change your text part of the app inside the **`.markdown()`** method:

    sl.markdown("bla-bla")

For LatEx support you can visit [katex.org](https://katex.org/docs/supported.html)

You can install an extension on VSC "**Fast Unicode Math Characters**" to create some superindex, subindex, and other stuff in visualization.

This is just the tip of the iceberg, many more functionalities to investigate on.


### Create a Dockerized app


Go to [Streamlit official way of doing this](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker), although i will cover the steps here.

There are 3 steps once you have your app in streamlit ready:

1) Create a Docker image of your app with all the necesary files in it.

To test your Docker file you can run:

Check Port Mapping:\

If you are using port mapping

    e.g., -p 8080:8080 to map host port 8080 to container port 8080

verify that the mapping is correctly set in the docker run command or in your Docker Compose file.

    docker run -p 8080:8080 your_app_image_name (in my case, i previously created the martin_final image)
    

Take into account that 8080 is the Exposed port in the Dockerfile and streamlit2 is the name of the container.

2) Upload it to Google Cloud
    
    a) Create a new project or select a previously created one.

    b) Add the following permissions to the project, to get the permissions that you need to set up gcr.io repositories, ask your administrator to grant you the following IAM roles:
        [roles](https://cloud.google.com/artifact-registry/docs/transition/gcr-on-ar?hl=en). In my case, i created a Role with them.

    - Artifact Registry Administrator
    - Cloud Asset Viewer
    - Organization Administrator
    - Project IAM Admin
    - Storage Admin
    - Storage Folder Admin

    c) Enable Artifact Registry API: With Artifact Registry you can store and manage your build artifacts (e.g. Docker images, Maven packages, npm packages), in a scalable and integrated repository service built on Google infrastructure). Also, you need to enable Container Registry as this two somehow coexist...(Container Registry will be out by May 2024)

    d) Maybe in step c) you need to create or asociate a Billing Account.


    - Enable Artifact Registry

    - Enable Container Registry

3) Run the container in the cloud so it can be accesed by a public URL
We will go step by step:

1) Create a Docker Image of your app with all the necesary files in it:

a) Create a **Dockerfile** like the following:


    FROM python:3.9-slim

    WORKDIR /final_app

    COPY ./web_interface /final_app

    RUN pip install -r /final_app/requirements.txt

    EXPOSE 8080

    ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]



b) Create a **requirements.txt** file

Inside the file, your need to state all dependencies that your app needs.
In my case i used:


    google-cloud-bigquery
    google-cloud-storage
    streamlit-on-Hover-tabs
    streamlit_folium
    python-dotenv
    scikit-learn
    streamlit
    slack_sdk
    folium
    pandas
    numpy
    flask
    db-dtypes
    aiohttp

There is a caveat here:
Some libraries are directly called or used deom within the app. But there are others (last two of the list) that are not "used" aparentyly in your code. The fact is that other libraries, like GCP BigQuery or Pandas for instance, need some libraries that are part of the "standard python" libraries, and as the runtime is the "slim 3.9 python" nor in "pandas" as stated in the Dockerfile, the container will fail to build. This trial and error lead me to pip install them as they were requested. Did not find a better way. 


c) Build the **image**

To build the Docker image after creating the Dockerfile, run:
(in this case **final** is the name you want to call the image)

    docker build -t LOCAL_DOCKER_IMAGE_NAME_YOU_LIKE .   (general)

    docker build -t martin_final .                             (my case)

The `-t` flag is used to tag the image with a specific name (ahead you will tag again for GCP upload, altough you coud do this here....but you wouldn't understand why...nevermind...)

The `.` (dot) at the end specifies the build context. In this context, it represents the current directory as the build context. Docker uses the specified directory to find the Dockerfile and all files and directories in the current directory (including the Dockerfile) will be sent to the Docker daemon, allowing it to build the image.

Tree of files shoud look something like:

    final_app/
    ├── Dockerfile
    ├── .dockerignore (optional)
    └── requirements.txt
    └── source/
        ├── main.py
        └── utils.py

Create the repository in Artifact Registry

Enable Container Registry (AKA Artifact Registry as CR will be deprecated)
Enabeling requires a Billing Account. Create one (Manage Billing Accounts)

# Prerequisites

If this is the first time you install GCP CLI you should download it and create link your gmail account to it.


### Install Google Cloud CLI

    gcloud init

Select and enter a valid google account and select a project. Verify it through:

    gcloud config list

Set the property of `compute` in this case `region`

    gcloud config set compute/regios

Add credentials helpers

    gcloud auth configure-docker gcr.io

**If you have more than one project, you should select it by it's Id** 

Authenticate if you have already created the project

    gcloud auth login

Set the destination project

    gcloud config set project DESTINATION_PROJECT_ID

The docker tag command in Docker is used to assign a new name, optionally including a new tag, to an existing Docker image. This is commonly done before pushing the image to a container registry:

    docker tag LOCAL_DOCKER_IMAGE_NAME_YOU_LIKE [REPOSITORY_DOMAIN_ON_ARTIFACT_REGISTRY]/[PROJECT_ID]/[NAME_TO_ASSIGN_TO_CONTAINER_ON_CLOUD]

* Brackets are mine, do not include in the command.

Note: the destination route is a combination of REPOSITORY_DOMAIN_ON_ARTIFACT_REGISTRY, a PROJECT_ID you choose, and a NAME_TO_ASSIGN_TO_CONTAINER_ON_CLOUD

**Note regarding REPOSITORY_DOMAIN_ON_ARTIFACT_REGISTRY** (remember May 2024 i told you upwards)

    - You can choose between gcr.io and pkg.dev domains when creating repositories in Cloud Artifact Registry.
    - gcr.io is still supported for existing GCR users and offers a familiar experience.
    - pkg.dev is the recommended domain for new repositories as it provides additional features and better reflects the broader functionality of Cloud Artifact Registry.


In my case i used:
    
    docker tag martin_final:latest gcr.io/dataproc-grupo5-test/martin_final:latest

Then push it to the cloud:

    docker push gcr.io/dataproc-grupo5-test/martin_final:latest

Now go to Cloud Run and create a **New Service**.
Select the image uploaded and get the public URL to visit it.

## Enable Continous Deployment on GC (TODO)

## Connect Streamlit to Google Big Query

There is an oficial [step by step guide](https://docs.streamlit.io/knowledge-base/tutorials/databases/bigquery), but i'll paste it here for completness.

### Enable the BigQuery API

### Create a service account & key file

To use the BigQuery API from Streamlit Community Cloud, you need a Google Cloud Platform service account (a special account type for programmatic data access).

Go to the Service Accounts page (inside IAM) and create an account with the **Viewer** permission (this will let the account access data but not change it).

After clicking **DONE**, you should be back on the service accounts overview.
Create a `.json` key file for the new account (**KEYS --> ADD KEY**).The key will automatically be downloaded.

Inside the `.json` file (automatically downloaded), there is an object like (do not try this at home):

{
  "type": "service_account",  
  "project_id": "test3-henry-bigquery",
  "private_key_id": "58e668c10f69321",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBA7i7xQqO5ZqEB\n-----END PRIVATE KEY-----\n",
  "client_email": "service-acc@test3-henry-bigquery.iam.gserviceaccount.com",
  "client_id": "104494240012529666325",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-acc%40test3-henry-bigquery.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

### Add the key file to your local app secrets

Your local Streamlit app will read secrets from a file `.streamlit/secrets.toml` in your app's root directory. Create this file if it doesn't exist yet and add the content of the key file you just downloaded to it as shown below:

[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"
    
    Add this file to .gitignore and don't commit it to your GitHub repo!

### Copy your app secrets to the Streamlit Cloud

As the `secrets.toml` file above is not committed to GitHub, you need to pass its content to your deployed app (on Streamlit Community Cloud) separately. Go to the app dashboard and in the app's dropdown menu, click on Edit Secrets. Copy the content of `secrets.toml` into the text area

If you reached here, it's because you folowed up. Drop me a wapp message to + 5  4  9 3  4  2  6 1 4 2 1 60 with "hey! keep up on readme!" and i'll do.

But this is to upload the Streamlit app to Streamlit Community Cloud, but as i am creating a Docker container, i can insert the `Secrets.toml` inside it and no one would see it.

### Add google-cloud-bigquery to your requirements file

