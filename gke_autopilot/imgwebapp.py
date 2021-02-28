import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Bean Image Classifier")
st.text("Provide URL of bean Image for image classification")

@st.cache(allow_output_mutation=True)
def load_model():
  model = tf.keras.models.load_model('./models')
  return model

with st.spinner('Loading Model Into Memory....'):
  model = load_model()

classes=['angular_leaf_spot','bean_rust','healthy']

def scale(image):
  image = tf.cast(image, tf.float32)
  image /= 255.0

  return tf.image.resize(image,[224,224])

def decode_img(image):
  img = tf.image.decode_jpeg(image, channels=3)
  img = scale(img)
  return np.expand_dims(img, axis=0)

#path = st.text_input('Enter Image URL to Classify.. ','http://barmac.com.au/wp-content/uploads/sites/3/2016/01/Angular-Leaf-Spot-Beans1.jpg')
img_file_buffer = st.file_uploader("Upload Image to Classify....")

if img_file_buffer  is not None:
    image = img_file_buffer
    image_out = Image.open(img_file_buffer)
    image = image.getvalue()
else:
    test_image = 'http://barmac.com.au/wp-content/uploads/sites/3/2016/01/Angular-Leaf-Spot-Beans1.jpg'
    image = requests.get(test_image).content
    image_out = Image.open(BytesIO(image))

st.write("Predicted Class :")
with st.spinner('classifying.....'):
    label =np.argmax(model.predict(decode_img(image)),axis=1)
    st.write(classes[label[0]])    
st.write("")
st.image(image_out, caption='Classifying Bean Image', use_column_width=True)