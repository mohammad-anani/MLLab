import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from .filter import filtered_df
from sklearn.impute import SimpleImputer, KNNImputer
from routes.dataRoutes.data_state import data_state


def imputePage():
  ds = data_state()
  if 'imputation_method' not in ds:
    ds.imputation_method = 'mean'

  df = filtered_df()
  has_na = df.isna().any().any()

  st.subheader("5- Handle missing values")
  if not has_na:
    st.subheader("Your data has no missing values!")
    nextButton()
  else:
    choose_imputation_ui()


def choose_imputation_ui():
  ds = data_state()
  df = filtered_df()

  na_df = pd.DataFrame({
    "na count": df.isna().sum(),
    "total count": len(df),
    "na percent": df.isna().mean() * 100
  })
  na_df = na_df[na_df["na count"] > 0]

  imputation_methods = ['mean', 'median', 'most_frequent', 'knn']
  default_val = imputation_methods.index(ds.imputation_method) if 'imputation_method' in ds else 0

  st.write(na_df)
  st.subheader("Choose the imputation method for the missing values in your dataset:")
  st.selectbox(
    '',
    options=imputation_methods,
    on_change=on_change,
    key='select_input',
    index=default_val,
    label_visibility='collapsed'
  )

  df_missing = df[df.isna().any(axis=1)]
  df_imputed_rows = imputed_rows_df()

  st.subheader("Data with missing values before imputing:")
  st.write(df_missing)
  st.subheader("Data with missing values after imputing:")
  st.write(df_imputed_rows)

  nextButton()



def missing_values_row_indices():
  df = filtered_df()
  return df.index[df.isna().any(axis=1)]


def imputed_rows_df():
  return imputed_df().loc[missing_values_row_indices()].copy()


def impute_df(df, method):
  num_cols = df.select_dtypes(include=['number']).columns
  cat_cols = df.select_dtypes(exclude=['number']).columns
  df_new = df.copy()

  if method in ["mean", "median", "most_frequent"]:
    if len(num_cols) > 0:
      df_new[num_cols] = SimpleImputer(strategy=method).fit_transform(df_new[num_cols])
    if len(cat_cols) > 0:
      df_new[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df_new[cat_cols])

  elif method == "knn":
    if len(num_cols) > 0:
      df_new[num_cols] = KNNImputer(n_neighbors=5).fit_transform(df_new[num_cols])
    if len(cat_cols) > 0:
      df_new[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df_new[cat_cols])

  else:
    print(f"Unknown imputation method: {method}")

  return pd.DataFrame(df_new, columns=df.columns)


def imputed_df():
  ds = data_state()
  df = filtered_df()
  method = ds.imputation_method
  return impute_df(df, method)


def on_change():
  ds = data_state()
  ds.imputation_method = st.session_state['select_input']
