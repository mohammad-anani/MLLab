import streamlit as st
from datetime import datetime
from routes.modelRoutes.train import train_model, needs_retraining,test_model
from routes.dataRoutes.data_state import data_state
import pandas as pd

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
