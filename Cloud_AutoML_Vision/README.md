This repository contains code and steps to train a image classifier model on Google Cloud AutoML Vision

Cloud ML Vision is trained on Kaggle Cassava Leaf Disease detection dataset - https://www.kaggle.com/c/cassava-leaf-disease-classification

Kaggle Data Download.ipynb - contains code to pull data from Kaggle and move the data to google cloud storage

Data Preparation.ipynb - contains code to prepare csv file containing image file and label information. This file will be used for training Cloud AutoML Vision models

On how to use google cloud UI to create AutoML vision model you can check this video - https://youtu.be/XZMU9uNbQvs

Once model is train you can deploy it and use predict.ipynb file to predict new instances of input

