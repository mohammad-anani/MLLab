import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame


def uploadPage():
  st.subheader("1-Upload you data(csv only)")

  upload_file_ui() if 'df' not in st.session_state else loaded_dataset_ui()


def upload_file_ui():
  uploaded_file= st.file_uploader("", type="csv",
  key="uploaded_file",
  on_change=on_change,
  label_visibility="collapsed")


def loaded_dataset_ui():
  df=st.session_state.df
  row_count,col_count=df.shape
  
  dataFrame(df)

  st.error("Dataset should have at least 2 columns") if col_count<2 else nextButton()


def on_change():
  uploaded_file = st.session_state["uploaded_file"]
  if uploaded_file:
    try:
      df = pd.read_csv(uploaded_file)
      st.session_state.df = df
    except Exception as e:
      st.error("Error in file uploading. Try again")