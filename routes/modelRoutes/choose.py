import streamlit as st
from routes.dataRoutes.data_state import data_state
from routes.modelRoutes.model_state import model_state
from util.nextButton import nextButton

regression_models = [
  'Linear Regression',
  'Support Vector Regression (SVR)',
  'K-Nearest Neighbors Regressor',
  'Decision Tree Regressor'
]

classification_models = [
  'Logistic Regression',
  'Support Vector Classifier (SVC)',
  'K-Nearest Neighbors Classifier',
  'Decision Tree Classifier'
]


def choosePage():
  ds = data_state()
  ms = model_state()

  is_regression = ds.is_regression
  current_models = regression_models if is_regression else classification_models

  if 'model' not in ms or (
      (ms.model in classification_models and is_regression) or 
      (ms.model in regression_models and not is_regression)
  ):
    ms.model = current_models[0]

  st.subheader("1- Choose your model:")
  st.selectbox(
    '',
    options=current_models,
    key='model_input',
    index=current_models.index(ms.model),
    on_change=on_change,
    label_visibility='collapsed'
  )
  nextButton()


def on_change():
  """Callback for model selection change"""
  model_state().model = st.session_state['model_input']
