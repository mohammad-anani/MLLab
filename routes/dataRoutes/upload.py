import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from util.dataFrame import dataFrame


def uploadPage():

  routeButton("Back","left","home")

  st.title("I-Data")

  st.subheader("1-Upload you data(csv only)")

  if 'df' not in st.session_state:
    upload_file_ui()
  else:
    loaded_dataset_ui()


def upload_file_ui():
  uploaded_file= st.file_uploader("", type="csv",
  key="uploaded_file",
  on_change=on_change,
  args=["uploaded_file"])


def loaded_dataset_ui():
  df=st.session_state.df
  row_count,col_count=df.shape
  
  dataFrame(df)


  if col_count<2:
    st.error("Dataset should have at least 2 columns")
  else:
    routeButton("Next","right",'target')


def on_change(key):
  uploaded_file = st.session_state[key]
  if uploaded_file:
    try:
      df = pd.read_csv(uploaded_file)
      st.session_state.df = df
    except Exception as e:
      st.error("Error in file uploading. Try again")