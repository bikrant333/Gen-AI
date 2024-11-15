import os
import pathlib
import textwrap
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
load_dotenv()                           #Load all environment variables

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if image:
        response = model.generate_content([input,image[0],prompt])
    else:
        print(f'Please upload valid image')
    return response.text

def input_image_setup(uploaded_file):
     # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Construction Safety Assessment")

st.header("Construction Safety Application")

input=st.text_input("Input Prompt: ",key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Analyse the Image for Safety/Hazard Risk")

input_prompt = """
               You are an expert in Construction Engineering Health and Safety Management.
               You will receive input images from constructions sites &
               you will have to identify the potential safety/hazard risk (e.g., missing guardrails, cluttered pathways, Contact with live electrical wires, faulty equipment) based on the input image and 
               provide suggestions to avoid the safety/hazard risk (e.g., clearing pathways, installing safety barriers)
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
