import streamlit as st
from routes.dataRoutes.data_state import data_state
from routes.modelRoutes.model_state import model_state
from util.nextButton import nextButton

no_tuning_message = "This model does not require hyperparameters tuning."


def linear_regression_tuning():
  st.subheader(no_tuning_message)


def svm_tuning():
  ms = model_state()
  tuning = ms.get('tuning',{})
  ms.tuning = tuning

  tuning.setdefault('kernel', 'rbf')
  tuning.setdefault('C', 1.0)
  tuning.setdefault('epsilon', 0.1)
  tuning.setdefault('gamma_choice', 'scale')
  tuning.setdefault('gamma', 0.01)

  kernel_options = ['linear', 'poly', 'rbf', 'sigmoid']
  st.selectbox(
    "Kernel:",
    options=kernel_options,
    index=kernel_options.index(tuning['kernel']),
    on_change=on_kernel_change,
    key='kernel'
  )

  C_options = [0.01, 0.1, 1, 10, 100, 1000]
  st.selectbox(
    "C (regularization):",
    options=C_options,
    index=C_options.index(tuning['C']),
    on_change=on_C_change,
    key='C'
  )

  st.slider(
    "Epsilon (tube width):",
    min_value=0.001,
    max_value=1.0,
    value=tuning['epsilon'],
    step=0.001,
    on_change=on_epsilon_change,
    key='epsilon'
  )

  gamma_options = ['scale', 'auto', 'manual']
  st.selectbox(
    "Gamma:",
    options=gamma_options,
    index=gamma_options.index(tuning['gamma_choice']),
    on_change=on_gamma_choice_change,
    key='gamma_choice'
  )

  if tuning['gamma_choice'] == 'manual':
    st.slider(
      "Gamma value:",
      min_value=0.01,
      max_value=10.0,
      value=tuning['gamma'],
      step=0.01,
      on_change=on_gamma_value_change,
      key='gamma'
    )


def knn_tuning():
  ms = model_state()
  tuning = ms.get('tuning', {})
  ms.tuning=tuning

  tuning.setdefault('n_neighbors', 5)
  tuning.setdefault('weights', 'uniform')
  tuning.setdefault('algorithm', 'auto')

  st.slider(
    "Number of Neighbors (n_neighbors):",
    min_value=1,
    max_value=50,
    value=tuning['n_neighbors'],
    step=1,
    on_change=on_n_neighbors_change,
    key='n_neighbors'
  )

  weights_options = ['uniform', 'distance']
  st.selectbox(
    "Weights:",
    options=weights_options,
    index=weights_options.index(tuning['weights']),
    on_change=on_weights_change,
    key='weights'
  )

  algorithm_options = ['auto', 'ball_tree', 'kd_tree', 'brute']
  st.selectbox(
    "Algorithm:",
    options=algorithm_options,
    index=algorithm_options.index(tuning['algorithm']),
    on_change=on_algorithm_change,
    key='algorithm'
  )


def decision_tree_reg_tuning():
  ms = model_state()
  tuning = ms.get('tuning', {})
  ms.tuning=tuning
  tuning.setdefault('max_depth', None)
  tuning.setdefault('criterion', 'squared_error')

  st.slider(
    "Max Depth:",
    min_value=1,
    max_value=50,
    value=tuning['max_depth'] if tuning['max_depth'] is not None else 50,
    step=1,
    on_change=on_max_depth_change,
    key='max_depth'
  )

  criterion_options = ['squared_error', 'friedman_mse', 'absolute_error']
  st.selectbox(
    "Criterion:",
    options=criterion_options,
    index=criterion_options.index(tuning['criterion']),
    on_change=on_criterion_change,
    key='criterion'
  )


def logistic_regression_tuning():
  ms = model_state()
  tuning = ms.get('tuning', {})
  ms.tuning=tuning
  tuning.setdefault('C', 1.0)
  tuning.setdefault('penalty', 'l2')
  tuning.setdefault('solver', 'lbfgs')

  C_options = [0.01, 0.1, 1, 10, 100, 1000]
  st.selectbox(
    "Regularization strength (C):",
    options=C_options,
    index=C_options.index(tuning['C']),
    on_change=on_logreg_C_change,
    key='C'
  )

  penalty_options = ['l1', 'l2', 'elasticnet', 'none']
  st.selectbox(
    "Penalty:",
    options=penalty_options,
    index=penalty_options.index(tuning['penalty']),
    on_change=on_logreg_penalty_change,
    key='penalty'
  )

  solver_options = ['lbfgs', 'liblinear', 'saga', 'newton-cg']
  st.selectbox(
    "Solver:",
    options=solver_options,
    index=solver_options.index(tuning['solver']),
    on_change=on_logreg_solver_change,
    key='solver'
  )


def decision_tree_class_tuning():
  ms = model_state()
  tuning = ms.get('tuning', {})
  ms.tuning=tuning
  tuning.setdefault('max_depth', None)
  tuning.setdefault('criterion', 'gini')

  st.slider(
    "Max Depth:",
    min_value=1,
    max_value=50,
    value=tuning['max_depth'] if tuning['max_depth'] is not None else 50,
    step=1,
    on_change=on_tree_max_depth_change,
    key='max_depth'
  )

  criterion_options = ['gini', 'entropy', 'log_loss']
  st.selectbox(
    "Criterion:",
    options=criterion_options,
    index=criterion_options.index(tuning['criterion']),
    on_change=on_tree_criterion_change,
    key='criterion'
  )



def on_tree_max_depth_change():
  model_state().tuning['max_depth'] = st.session_state.max_depth

def on_tree_criterion_change():
  model_state().tuning['criterion'] = st.session_state.criterion

def on_logreg_C_change():
  model_state().tuning['C'] = st.session_state.C

def on_logreg_penalty_change():
  model_state().tuning['penalty'] = st.session_state.penalty

def on_logreg_solver_change():
  model_state().tuning['solver'] = st.session_state.solver

def on_max_depth_change():
  model_state().tuning['max_depth'] = st.session_state.max_depth

def on_criterion_change():
  model_state().tuning['criterion'] = st.session_state.criterion

def on_n_neighbors_change():
  model_state().tuning['n_neighbors'] = st.session_state.n_neighbors

def on_weights_change():
  model_state().tuning['weights'] = st.session_state.weights

def on_algorithm_change():
  model_state().tuning['algorithm'] = st.session_state.algorithm

def on_kernel_change():
  model_state().tuning['kernel'] = st.session_state.kernel

def on_C_change():
  model_state().tuning['C'] = st.session_state.C

def on_epsilon_change():
  model_state().tuning['epsilon'] = st.session_state.epsilon

def on_gamma_choice_change():
  model_state().tuning['gamma_choice'] = st.session_state.gamma_choice

def on_gamma_value_change():
  model_state().tuning['gamma'] = st.session_state.gamma



regression_models_tuning = {
  'Linear Regression': linear_regression_tuning,
  'Support Vector Regression (SVR)': svm_tuning,
  'K-Nearest Neighbors Regressor': knn_tuning,
  'Decision Tree Regressor': decision_tree_reg_tuning
}

classification_models_tuning = {
  'Logistic Regression': logistic_regression_tuning,
  'Support Vector Classifier (SVC)': svm_tuning,
  'K-Nearest Neighbors Classifier': knn_tuning,
  'Decision Tree Classifier': decision_tree_class_tuning
}


def tunePage():
  """Page to tune model hyperparameters."""
  ds = data_state()
  ms = model_state()

  st.subheader('2- Tune model hyperparameters:')

  if 'tuning' not in ms or ms['tuning'].get('model') != ms.model:
    ms['tuning'] = {'model': ms.model}

  if ds.is_regression:
    regression_models_tuning[ms.model]()
  else:
    classification_models_tuning[ms.model]()

  nextButton()
