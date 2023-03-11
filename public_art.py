import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import os
import openai
import json
import pandas as pd

openai.api_key = 'OPEN_API_KEY'

st.title('Syracuse Public Art Challenge')

DATA_URL = ('Syracuse_Public_Art.csv')
def load_data(nrows):
    public_art = pd.read_csv(DATA_URL, nrows=nrows)
    public_art = public_art.rename(columns={"X": "longitude", "Y": "latitude"}, errors="raise").sample(40)
    public_art_string = public_art.to_string()
    return public_art_string

data = load_data(40)
question = """based on the following csv, please suggest what a  new  work of syracuse public art  would be and recommend and list out the following information - only list this information do not give me an introduction about the piece:
- name
- location
- latitude
- longitude
- material used to create the piece
- description of what the piece looks like"""

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant that recommends and lists the name, location, latitude, longitude, type of material, and description of a new art piece in Syracuse, NY."},
        {"role": "user", "content": question + data},
        {"role": "user", "content": 'Please recommend and list the name, location, latitude, longitude, type of material, and description'}

    ]
)
chunks = response["choices"][0]["message"]["content"].split('\n')

df = pd.DataFrame(chunks)
df[['Type','Description']] = df[0].str.split(':',expand=True)

df = df.replace("<br>"," ", regex=True)
Longitude = float(df['Description'][df['Type']=='Longitude'].iloc[0])
Latitude = float(df['Description'][df['Type']=='Latitude'].iloc[0])
st_map = pd.DataFrame([[Latitude, Longitude]], columns=['lat', 'lon'])

st.write(df[df['Type']=='Name']['Description'].iloc[0])
st.write(df[df['Type']=='Location']['Description'].iloc[0])
st.write(df[df['Type']=='Material']['Description'].iloc[0])
st.write(df[df['Type']=='Description']['Description'].iloc[0])
st.map(st_map)