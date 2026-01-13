import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from .filter import filtered_df
from sklearn.impute import SimpleImputer, KNNImputer


#mean median mode knn dropcols droprows

def imputePage():
  routeButton("Back","left","filter")
  st.title("I- Data")
  st.subheader("5- Handle missing values")

  df=filtered_df()

  has_na=df.isna().any().any()

  if not has_na:
    st.subheader("Your data has no missing values!")
    routeButton("Next","right","encode")
  else:
    choose_imputation_ui()

def choose_imputation_ui():
  df=filtered_df()

  na_df = pd.DataFrame({
    "na count": df.isna().sum(),
    "total count": len(df),
    "na percent": df.isna().mean() * 100
})

  na_df = na_df[na_df["na count"] > 0]

  st.write(na_df)
  imputation_methods=['mean','median','most_frequent','knn']


  st.subheader("Choose the imputation method for the missing values in your dataset:")

  default_val=imputation_methods.index(st.session_state.imputation_method) if 'imputation_method' in st.session_state else 0

  st.selectbox('',options=imputation_methods,on_change=on_change,key='select_input',index=default_val)


  df_missing = df[df.isna().any(axis=1)]
  df_imputed_rows=imputed_rows_df()

  st.subheader("Data with missing values before imputing:")  
  st.write(df_missing)

  st.subheader("Data with missing values after imputing:")  
  st.write(df_imputed_rows)
  routeButton("Next","right","encode")

def missing_values_row_indices():
  df=filtered_df()
  return df.index[df.isna().any(axis=1)]

def imputed_rows_df():
  return imputed_df().loc[missing_values_row_indices()].copy()

def imputed_df():
  df=filtered_df()
  method=st.session_state.imputation_method

  num_cols = df.select_dtypes(include="number").columns
  cat_cols = df.select_dtypes(exclude="number").columns

  df_new = df.copy()

  if method in ["mean", "median", "most_frequent"]:
    if num_cols.any():
      df_new[num_cols] = SimpleImputer(strategy=method).fit_transform(df_new[num_cols])
      if cat_cols.any():
        cat_strategy = "most_frequent"
        df_new[cat_cols] = SimpleImputer(strategy=cat_strategy).fit_transform(df_new[cat_cols])

  elif method == "knn":
    if num_cols.any():
      df_new[num_cols] = KNNImputer(n_neighbors=5).fit_transform(df_new[num_cols])
      if cat_cols.any():
        df_new[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df_new[cat_cols])

  else:
    st.warning(f"Unknown imputation method: {method}")

  return pd.DataFrame(df_new)


def on_change():
  st.session_state.imputation_method=st.session_state['select_input']