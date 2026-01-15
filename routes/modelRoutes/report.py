import streamlit as st
from routes.modelRoutes.train import train_model
from routes.dataRoutes.data_state import data_state

def reportPage():

  if 'trained_model' not in st.session_state:
    model,Y_predict,Y_test=train_model()

  st.session_state.trained_model=model
  is_regression=data_state().is_regression