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
  is_regression=data_state().is_regression

  current_models=regression_models if is_regression else classification_models

  if 'model' not in model_state() or model_state().model in classification_models and  is_regression or model_state().model in regression_models and not is_regression:
    model_state()['model']=current_models[0]

  st.subheader("1- Choose your model:")
  st.selectbox('',options=current_models,label_visibility='collapsed',key='model_input',index=current_models.index(model_state()['model']),on_change=on_change)
  nextButton()


def on_change():
  model_state().model=st.session_state['model_input']