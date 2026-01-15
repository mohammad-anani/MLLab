from routes.modelRoutes.model_state import model_state
from routes.dataRoutes.data_state import data_state
from routes.dataRoutes.filter import filtered_df
from routes.dataRoutes.impute import impute_df
from routes.dataRoutes.encode import encode_df

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import BaggingClassifier, BaggingRegressor, AdaBoostClassifier, AdaBoostRegressor
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

import streamlit as st

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)

def preprocess_data():
  ds = data_state()
  label = ds.label
  imputation_method = ds.imputation_method
  encoding = ds.encoding
  encoding_order = ds.encoding_order
  test_size = ds.test_size
  with_scaler = ds.with_scaler
  with_pca = ds.with_pca

  df = filtered_df()
  Y = df[label]
  X = df.drop(label, axis=1)

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=42)

  X_train = impute_df(X_train, imputation_method)
  X_test = impute_df(X_test, imputation_method)

  X_train, encoders = encode_df(X_train, encoding, encoding_order, fit=True)
  X_test = encode_df(X_test, encoding, encoding_order, fit=False, encoders=encoders)

  if with_scaler:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

  if with_pca:
    pca = PCA(n_components=0.95)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

  return X_train, X_test, Y_train, Y_test


def build_model():
  """Build the base model using selected type and tuned hyperparameters."""
  is_regression = data_state().is_regression
  model_name = model_state().model
  tuning = model_state().tuning.copy()

  tuning.pop('model', None)

  models_map = {
    'Linear Regression': LinearRegression,
    'Support Vector Regression (SVR)': SVR,
    'K-Nearest Neighbors Regressor': KNeighborsRegressor,
    'Decision Tree Regressor': DecisionTreeRegressor,
    'Logistic Regression': LogisticRegression,
    'Support Vector Classifier (SVC)': SVC,
    'K-Nearest Neighbors Classifier': KNeighborsClassifier,
    'Decision Tree Classifier': DecisionTreeClassifier
  }

  if 'gamma_choice' in tuning and ('SVR' in model_name or 'SVC' in model_name):
    choice = tuning.pop('gamma_choice')
    if choice != 'manual':
      tuning['gamma'] = choice

  model_class = models_map[model_name]
  clf = model_class(**tuning)
  return clf


def apply_ensemble(base_model):
  is_regression = data_state().is_regression
  ensemble_config = model_state().ensemble
  method = ensemble_config.get('method', 'None')

  if method == 'None':
    return base_model

  n_estimators = ensemble_config.get('n_estimators', 50)

  if method == 'Bagging':
    max_samples = ensemble_config.get('max_samples', 1.0)
    return BaggingRegressor(estimator=base_model, n_estimators=n_estimators, max_samples=max_samples) \
      if is_regression else \
      BaggingClassifier(estimator=base_model, n_estimators=n_estimators, max_samples=max_samples)

  if method == 'Boosting (AdaBoost)':
    learning_rate = ensemble_config.get('learning_rate', 1.0)
    return AdaBoostRegressor(estimator=base_model, n_estimators=n_estimators, learning_rate=learning_rate) \
      if is_regression else \
      AdaBoostClassifier(estimator=base_model, n_estimators=n_estimators, learning_rate=learning_rate)

  return base_model


def train_model():
  st.session_state.last_trained_state=store_current_state()
  X_train, X_test, Y_train, Y_test = preprocess_data()
  base_model = build_model()
  final_model = apply_ensemble(base_model)
  final_model.fit(X_train, Y_train)
  Y_predict = final_model.predict(X_test)
  return final_model, Y_predict, Y_test




def test_model(model, Y_predict, Y_test):
  is_regression = data_state().is_regression
  metrics = {}

  if is_regression:
    metrics["Mean Absolute Error"] = mean_absolute_error(Y_test, Y_predict)
    metrics["Mean Squared Error"] = mean_squared_error(Y_test, Y_predict)
    metrics["Root Mean Squared Error"] = mean_squared_error(Y_test, Y_predict)
    r2 = r2_score(Y_test, Y_predict)
    metrics["R2 Score"] = r2
    if r2 >= 0.8:
        performance = "Excellent"
    elif r2 >= 0.6:
        performance = "Good"
    elif r2 >= 0.4:
        performance = "Fair"
    elif r2 > 0:
        performance = "Poor"
    else:
        performance = "Baseline or Worse"
    metrics["Performance"] = performance 
  else:
    metrics["Accuracy"] = accuracy_score(Y_test, Y_predict)
    metrics["Precision"] = precision_score(Y_test, Y_predict, average='weighted', zero_division=0)
    metrics["Recall"] = recall_score(Y_test, Y_predict, average='weighted', zero_division=0)
    metrics["F1 Score"] = f1_score(Y_test, Y_predict, average='weighted', zero_division=0)

  return metrics


def store_current_state():
  ds = data_state()
  ms = model_state()
  
  return {
    # Data info
    "cols_to_remove": ds.cols_to_remove.copy(),
    "imputation": ds.imputation_method,
    "encoding": ds.encoding.copy(),
    "encoding_order": ds.encoding_order.copy(),
    "scaler": ds.with_scaler,
    "pca": ds.with_pca,
    "test_size": ds.test_size,
    "filter": {k: v for k, v in ds.filter.items()},
    "remove_outliers": ds.remove_outliers,
    "remove_singleval_col": ds.remove_singleval_col,
    "label": ds.label,
    "choice": ds.get("choice", None),

    # Model info
    "model": ms.model,
    "tuning": ms.tuning.copy(),
    "ensemble": ms.ensemble.copy()
  }


def needs_retraining():
  if 'last_trained_state' not in st.session_state:
    return True

  last_state = st.session_state.last_trained_state
  current_state = store_current_state()

  return current_state != last_state
