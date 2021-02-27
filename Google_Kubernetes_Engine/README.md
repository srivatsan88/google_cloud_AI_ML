This repository contains details and code for deploying machine learning models on Google Kubernetes Engine Engine

Details of the code and working is covered in detailed in my YouTube channel (AIEngineering) here - https://youtu.be/Hfgla4ViIwU

Before getting started with deployment the container expects trained models and also downloaded nltk corpus

For model files you are run associated notebook in this repository or else download the trained models and use it using below 2 command

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1m1bVxlUjrJ_tmWApYJHlk2q5bikGyIxr' -O complaints.booster

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WURdboJjF27g9bZG_CGCCGSYWi0EvxJR' -O tfvectroizer.pkl

If you want more details on model training you can check the video here - https://youtu.be/EHt_x8r1exU

For NLTK you have to download stopwords and tokenizer corpa. One can download it using nltk.download()


To deploy the model on Google Kubernetes Engine, execute the below commands
------------------------------------------------------------------------------------------

Building the container image - gcloud builds submit --tag gcr.io/<your GCP project>/complaintsapi .

List the image - gcloud builds list --filter complaints

Checking logs of built image - gcloud builds log <container id from list command above>

Create Kubernetes Cluster - gcloud container clusters create complaints-gke --zone "us-west1-b" --machine-type "n1-standard-1" --num-nodes "1" --service-account srivatsan-gke@srivatsan-project.iam.gserviceaccount.com (Change to your service account)

Create Kubernetes Deployment - kubectl apply -f deployment.yaml   

Get details on deployed application - kubectl get deployments

Get info of created pods via deployment - kubectl get pods

Decribe deployed pod - kubectl describe pod <pod info from above command>

Get pod logs - kubectl logs <pod info from above command>

Create service for deployment - kubectl apply -f service.yaml

Get service details - kubectl get services

Add nodes to cluster - gcloud container clusters resize complaints-gke --num-nodes 3 --zone us-west1-b

Get details on cluster - gcloud container clusters list

Scale pod replicas - kubectl scale deployment complaints --replicas 2

Auto Scale setting in deployment - kubectl autoscale deployment complaints --max 6 --min 2 --cpu-percent 50

Get details on horizontal pod autoscaler - kubectl get hpa
