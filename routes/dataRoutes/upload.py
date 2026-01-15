import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from routes.dataRoutes.data_state import data_state

def uploadPage():
  st.subheader("1-Upload you data(csv only)")
  upload_file_ui() if 'df' not in data_state() else loaded_dataset_ui()


def upload_file_ui():
  uploaded_file= st.file_uploader("", type="csv",
  key="uploaded_file",
  on_change=on_change,
  label_visibility="collapsed")


def loaded_dataset_ui():
  df=data_state()['df']
  row_count,col_count=df.shape
  
  dataFrame(df)

  if col_count<2: 
    st.error("Dataset should have at least 2 columns") 
  else:
    nextButton()


def on_change():
  uploaded_file = st.session_state["uploaded_file"]
  if uploaded_file:
    try:
      df = pd.read_csv(uploaded_file)
      data_state()['df'] = df
    except Exception as e:
      st.error("Error in file uploading. Try again")