import streamlit as st
from routes.dataRoutes.data_state import data_state
from routes.modelRoutes.model_state import model_state
from util.nextButton import nextButton

no_tuning_message="This model does not require hyperparameters tuning."


def linear_regression_tuning():
  st.subheader(no_tuning_message)


def svm_tuning():
  if 'kernel' not in model_state().tuning:
    model_state().tuning['kernel'] = 'rbf'
  if 'C' not in model_state().tuning:
    model_state().tuning['C'] = 1.0
  if 'epsilon' not in model_state().tuning:
    model_state().tuning['epsilon'] = 0.1
  if 'gamma_choice' not in model_state().tuning:
    model_state().tuning['gamma_choice'] = 'scale'
  if 'gamma' not in model_state().tuning:
    model_state().tuning['gamma']=0.01

  kernel_options = ['linear', 'poly', 'rbf', 'sigmoid']
  default_kernel = model_state().tuning.get('kernel',None)  

  C_options =[0.01,0.1,1,10,100,1000]
  default_C =  model_state().tuning.get('C',None) 

  epsilon_range = (0.001, 1.0)
  default_epsilon = model_state().tuning.get('epsilon',None) 

  gamma_options = ['scale', 'auto', 'manual']
  default_gamma =  model_state().tuning.get('gamma_choice',None) 

  st.selectbox(
    "Kernel:",
    options=kernel_options,
    index=kernel_options.index(default_kernel),
    on_change=on_kernel_change,key='kernel'
  )

  st.selectbox(
    "C (regularization):",
    options=C_options,
    index=C_options.index(default_C),
    on_change=on_C_change,key='C'
  )

  st.slider(
    "Epsilon (tube width):",
    min_value=epsilon_range[0],
    max_value=epsilon_range[1],
    value=default_epsilon,
    step=0.001,
    on_change=on_epsilon_change,key='epsilon'
  )

  st.selectbox(
    "Gamma:",
    options=gamma_options,
    index=gamma_options.index(default_gamma),
    on_change=on_gamma_choice_change,key='gamma_choice'
  )

  if model_state().tuning['gamma_choice'] == 'manual':
    gamma = st.slider(
      "Gamma value:",
      min_value=0.01,
      max_value=10.0,
      value= model_state().tuning['gamma'],
      step=0.01,
      on_change=on_gamma_value_change,key='gamma'
    )

def knn_tuning():
  if 'n_neighbors' not in model_state().tuning:
    model_state().tuning['n_neighbors'] = 5
  if 'weights' not in model_state().tuning:
    model_state().tuning['weights'] = 'uniform'
  if 'algorithm' not in model_state().tuning:
    model_state().tuning['algorithm'] = 'auto'

  n_neighbors_range = (1, 50)
  default_n_neighbors = model_state().tuning.get('n_neighbors')

  weights_options = ['uniform', 'distance']
  default_weights = model_state().tuning.get('weights')

  algorithm_options = ['auto', 'ball_tree', 'kd_tree', 'brute']
  default_algorithm = model_state().tuning.get('algorithm')

  st.slider(
    "Number of Neighbors (n_neighbors):",
    min_value=n_neighbors_range[0],
    max_value=n_neighbors_range[1],
    value=default_n_neighbors,
    step=1,
    on_change=on_n_neighbors_change,
    key='n_neighbors'
  )

  st.selectbox(
    "Weights:",
    options=weights_options,
    index=weights_options.index(default_weights),
    on_change=on_weights_change,
    key='weights'
  )

  st.selectbox(
    "Algorithm:",
    options=algorithm_options,
    index=algorithm_options.index(default_algorithm),
    on_change=on_algorithm_change,
    key='algorithm'
  )

def decision_tree_reg_tuning():
  if 'max_depth' not in model_state().tuning:
    model_state().tuning['max_depth'] = None
  if 'criterion' not in model_state().tuning:
    model_state().tuning['criterion'] = 'squared_error'

  max_depth_range = (1, 50)
  default_max_depth = model_state().tuning.get('max_depth', None)

  criterion_options = ['squared_error', 'friedman_mse', 'absolute_error']
  default_criterion = model_state().tuning.get('criterion', 'squared_error')

  st.slider(
    "Max Depth:",
    min_value=max_depth_range[0],
    max_value=max_depth_range[1],
    value=default_max_depth if default_max_depth is not None else max_depth_range[1],
    step=1,
    on_change=on_max_depth_change,
    key='max_depth'
  )

  st.selectbox(
    "Criterion:",
    options=criterion_options,
    index=criterion_options.index(default_criterion),
    on_change=on_criterion_change,
    key='criterion'
  )

def logistic_regression_tuning():
  if 'C' not in model_state().tuning:
    model_state().tuning['C'] = 1.0
  if 'penalty' not in model_state().tuning:
    model_state().tuning['penalty'] = 'l2'
  if 'solver' not in model_state().tuning:
    model_state().tuning['solver'] = 'lbfgs'

  C_options = [0.01, 0.1, 1, 10, 100, 1000]
  default_C = model_state().tuning.get('C', 1.0)

  penalty_options = ['l1', 'l2', 'elasticnet', 'none']
  default_penalty = model_state().tuning.get('penalty', 'l2')

  solver_options = ['lbfgs', 'liblinear', 'saga', 'newton-cg']
  default_solver = model_state().tuning.get('solver', 'lbfgs')

  st.selectbox(
    "Regularization strength (C):",
    options=C_options,
    index=C_options.index(default_C),
    on_change=on_logreg_C_change,
    key='C'
  )

  st.selectbox(
    "Penalty:",
    options=penalty_options,
    index=penalty_options.index(default_penalty),
    on_change=on_logreg_penalty_change,
    key='penalty'
  )

  st.selectbox(
    "Solver:",
    options=solver_options,
    index=solver_options.index(default_solver),
    on_change=on_logreg_solver_change,
    key='solver'
  )

def decision_tree_class_tuning():
  if 'max_depth' not in model_state().tuning:
    model_state().tuning['max_depth'] = None
  if 'criterion' not in model_state().tuning:
    model_state().tuning['criterion'] = 'gini'

  max_depth_range = (1, 50)
  default_max_depth = model_state().tuning.get('max_depth', None)

  criterion_options = ['gini', 'entropy', 'log_loss']
  default_criterion = model_state().tuning.get('criterion', 'gini')

  st.slider(
    "Max Depth:",
    min_value=max_depth_range[0],
    max_value=max_depth_range[1],
    value=default_max_depth if default_max_depth is not None else max_depth_range[1],
    step=1,
    on_change=on_tree_max_depth_change,
    key='max_depth'
  )

  st.selectbox(
    "Criterion:",
    options=criterion_options,
    index=criterion_options.index(default_criterion),
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
    'Linear Regression':linear_regression_tuning,
    'Support Vector Regression (SVR)':svm_tuning,
    'K-Nearest Neighbors Regressor':knn_tuning,
    'Decision Tree Regressor':decision_tree_reg_tuning
}


classification_models_tuning = {
    'Logistic Regression':logistic_regression_tuning,
    'Support Vector Classifier (SVC)':svm_tuning,
    'K-Nearest Neighbors Classifier':knn_tuning,
    'Decision Tree Classifier':decision_tree_class_tuning
}


def tunePage():
  st.subheader('2- Tune model hyperparameters:')

  if 'tuning' not in model_state():
    model_state().tuning={'model':model_state().model}
  elif model_state().tuning['model'] != model_state().model:
    model_state().tuning.clear()
    model_state().tuning={'model':model_state().model}

  if data_state().is_regression:
    regression_models_tuning[model_state().model]()
  else:
    classification_models_tuning[model_state().model]()
  nextButton()


