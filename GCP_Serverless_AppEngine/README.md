This repository contains details and code for deploying machine learning models on Google Cloud Serverless platform and Google Cloud App Engine

Details of the code and working is covered in detailed in my YouTube channel (AIEngineering) here - https://youtu.be/kyQH71pB0vI 

Before getting started with deployment the container expects trained models and also downloaded nltk corpus

For model files you are run associated notebook in this repository or else download the trained models and use it using below 2 command

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1m1bVxlUjrJ_tmWApYJHlk2q5bikGyIxr' -O complaints.booster

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WURdboJjF27g9bZG_CGCCGSYWi0EvxJR' -O tfvectroizer.pkl

If you want more details on model training you can check the video here - https://youtu.be/EHt_x8r1exU

For NLTK you have to download stopwords and tokenizer corpa. One can download it using nltk.download()

To deploy the model on serverless infrastructure (Cloud Run), execute the below commands
