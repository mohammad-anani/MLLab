import streamlit as st
from routes.modelRoutes.model_state import model_state
from util.nextButton import nextButton

def ensemblePage():
  if 'ensemble' not in model_state():
    model_state().ensemble = {
      'method': 'None',
      'n_estimators': 50,
      'learning_rate': 1.0,
      'max_samples': 1.0
    }
  ensemble_options = ['None', 'Bagging', 'Boosting (AdaBoost)']
  default_method = model_state().ensemble.get('method', 'None')

  st.subheader("3- Choose ensemble method:")
  st.selectbox('',label_visibility='collapsed',options=ensemble_options,index=ensemble_options.index(default_method),on_change=on_ensemble_method_change,key='ensemble_method')

  selected_method=model_state().ensemble['method']

  if selected_method!='None':
    st.subheader("Tune your ensemble method:")
  if selected_method == 'Boosting (AdaBoost)':
    st.slider("Number of Estimators (n_estimators):",min_value=10, max_value=500, step=10,value=model_state().ensemble['n_estimators'],on_change=on_ens_n_estimators_change,key='ens_n_estimators')
    st.slider("Learning Rate (Speed):",min_value=0.01, max_value=2.0, step=0.01,value=model_state().ensemble['learning_rate'],on_change=on_learning_rate_change,key='learning_rate')
  elif selected_method == 'Bagging':
    st.slider("Number of Estimators (n_estimators):",min_value=10, max_value=200, step=10,value=model_state().ensemble['n_estimators'],on_change=on_ens_n_estimators_change,key='ens_n_estimators')
    st.slider("Max Samples (Data Diversity):",min_value=0.1, max_value=1.0, step=0.05,value=model_state().ensemble['max_samples'],on_change=on_max_samples_change,key='max_samples')
  nextButton()


def on_ensemble_method_change():
  model_state().ensemble['method'] = st.session_state.ensemble_method

def on_ens_n_estimators_change():
  model_state().ensemble['n_estimators'] = st.session_state.ens_n_estimators

def on_learning_rate_change():
  model_state().ensemble['learning_rate'] = st.session_state.learning_rate

def on_max_samples_change():
  model_state().ensemble['max_samples'] = st.session_state.max_samples