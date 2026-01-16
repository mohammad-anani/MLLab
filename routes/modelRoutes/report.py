import streamlit as st
from datetime import datetime
from routes.modelRoutes.train import train_model, needs_retraining,test_model
from routes.dataRoutes.data_state import data_state
import pandas as pd
from util.button import button
from util.nextButton import nextButton

import pickle

def reportPage():
  st.subheader("5- Model Report")
  retrain = 'trained_model' not in st.session_state or needs_retraining()

  if retrain:
    st.info("Training model...")
    model, Y_predict, Y_test = train_model()
    st.session_state.trained_model = model
    st.session_state.Y_predict = Y_predict
    st.session_state.Y_test = Y_test
    st.session_state.last_retrain_time = datetime.now()
    st.success("Training Finished!")
  else:
    model = st.session_state.trained_model
    Y_predict = st.session_state.Y_predict
    Y_test = st.session_state.Y_test
    st.success("Using previously trained model")

  if 'last_retrain_time' in st.session_state:
    st.write(f"*Last trained:* {st.session_state.last_retrain_time.strftime('%Y-%m-%d %H:%M:%S')}")

  metrics = test_model(model, Y_predict, Y_test)
  
  st.subheader("Model Performance Metrics")
  for metric, value in metrics.items():
    st.write(f"**{metric}:** {round(value, 4) if not isinstance(value, str) else value}")


  if 'trained_model' in st.session_state:
    st.subheader('Export Model:')
    c1,c2=st.columns([1,1])
    model_bytes = get_model_bytes(st.session_state.trained_model)
    with c1:
      file_name=st.text_input('',label_visibility='collapsed',placeholder='Enter File Name')
    with c2:
      st.download_button(
    label="Download Trained Model",
    data=model_bytes,type='primary',
    file_name=(file_name or "MLLab_trained_model")+".pkl",
    mime="application/octet-stream"
  )
    nextButton()


def get_model_bytes(model):
  return pickle.dumps(model)


