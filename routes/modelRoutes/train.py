from routes.modelRoutes.model_state import model_state
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from routes.dataRoutes.data_state import data_state
from routes.dataRoutes.filter import filtered_df 
from sklearn.model_selection import train_test_split
from routes.dataRoutes.impute import impute_df
from routes.dataRoutes.encode import encode_df 
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import BaggingClassifier, BaggingRegressor, AdaBoostClassifier, AdaBoostRegressor
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier


def preprocess_data():
  label=data_state().label
  imputation_method=data_state().imputation_method
  encoding=data_state().encoding
  encoding_order=data_state().encoding_order
  test_size=data_state().test_size
  with_scaler=data_state().with_scaler
  with_pca=data_state().with_pca

  df=filtered_df()

  Y=df[label]
  X=df.drop(label,axis=1)

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size,random_state=42)

  X_train=impute_df(X_train,imputation_method)
  X_test=impute_df(X_test,imputation_method)

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
  is_regression=data_state().is_regression
  model=model_state().model
  tuning=model_state().tuning.copy()

  if 'model' in tuning:
    tuning.pop('model')


  if is_regression:
    models_map = {
      'Linear Regression': LinearRegression,
      'Support Vector Regression (SVR)': SVR,
      'K-Nearest Neighbors Regressor': KNeighborsRegressor,
      'Decision Tree Regressor': DecisionTreeRegressor
    }

  else:
    models_map = {
      'Logistic Regression': LogisticRegression,
      'Support Vector Classifier (SVC)': SVC,
      'K-Nearest Neighbors Classifier': KNeighborsClassifier,
      'Decision Tree Classifier': DecisionTreeClassifier
    }

  model_class = models_map[model]
  
  if 'gamma_choice' in tuning and ('SVR' in model or 'SVC' in model):
    choice = tuning.pop('gamma_choice')
    if choice != 'manual':
     tuning['gamma'] = choice


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
    if is_regression:
      return BaggingRegressor(estimator=base_model, n_estimators=n_estimators, max_samples=max_samples)
    else:
      return BaggingClassifier(estimator=base_model, n_estimators=n_estimators, max_samples=max_samples)

  elif method == 'Boosting (AdaBoost)':
    learning_rate = ensemble_config.get('learning_rate', 1.0)
    if is_regression:
      return AdaBoostRegressor(estimator=base_model, n_estimators=n_estimators, learning_rate=learning_rate)
    else:
      return AdaBoostClassifier(estimator=base_model, n_estimators=n_estimators, learning_rate=learning_rate)

  return base_model


def train_model():
  X_train, X_test, Y_train, Y_test=preprocess_data()
  model=build_model()
  final_model=apply_ensemble(model)
  final_model.fit(X_train,Y_train)
  Y_predict=final_model.predict(X_test)
  return final_model,Y_predict,Y_test


