import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from routes.dataRoutes.data_state import data_state

def finalizePage():

  if 'with_pca' not in data_state():
    data_state().with_pca=False

  if 'with_scaler' not in data_state():
    data_state().with_scaler=False

  if 'test_size' not in data_state():
    data_state().test_size=0.4


  st.subheader("7- Final steps")


  st.slider('Test Size(for train test splitting)',0.1,0.5,on_change=slider_on_change,key='slider',value=data_state().test_size)  
  st.checkbox("Apply Standard Scaler",on_change=scaler_on_change,key='scaler',value=data_state().with_scaler)
  st.checkbox("Apply PCA",on_change=pca_on_change,key='pca',value=data_state().with_pca)

  nextButton()


def slider_on_change():
  data_state().test_size=st.session_state['slider']

def scaler_on_change():
  data_state().with_scaler=st.session_state['scaler']

def pca_on_change():
  data_state().with_pca=st.session_state['pca']
