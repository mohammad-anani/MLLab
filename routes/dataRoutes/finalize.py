import streamlit as st
from util.nextButton import nextButton
from routes.dataRoutes.data_state import data_state


def finalizePage():
  ds = data_state()

  ds.with_pca = ds.get('with_pca', False)
  ds.with_scaler = ds.get('with_scaler', False)
  ds.test_size = ds.get('test_size', 0.4)

  st.subheader("7- Final steps")

  st.slider(
    'Test Size (for train-test splitting)',
    min_value=0.1,
    max_value=0.5,
    value=ds.test_size,
    key='slider',
    on_change=slider_on_change
  )

  st.checkbox(
    "Apply Standard Scaler",
    value=ds.with_scaler,
    key='scaler_input',
    on_change=scaler_on_change
  )
  st.checkbox(
    "Apply PCA",
    value=ds.with_pca,
    key='pca_input',
    on_change=pca_on_change
  )
  
  nextButton()



def slider_on_change():
  ds = data_state()
  ds.test_size = st.session_state['slider']


def scaler_on_change():
  ds = data_state()
  ds.with_scaler = st.session_state['scaler_input']


def pca_on_change():
  ds = data_state()
  ds.with_pca = st.session_state['pca_input']
