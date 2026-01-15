import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from routes.dataRoutes.data_state import data_state


def targetPage():
  st.subheader("2- Specify your target column (aka Label)")
  select_label_ui()
  if 'label' in data_state():
    confirm_label_ui()


def select_label_ui():
  ds = data_state()
  df = ds.df
  cols = filter_cols(df)
  index = cols.index(ds.label) if 'label' in ds and ds.label in cols else None

  st.selectbox(
    "",
    cols,
    index=index,
    key="target_column",
    on_change=on_target_change,
    label_visibility="collapsed"
  )


def confirm_label_ui():
  ds = data_state()
  df = ds.df
  label = ds.label
  is_reg = ds.is_regression

  st.subheader(
    f"Based on your label ({label}), your problem will be treated as a "
    f"{'Regression' if is_reg else 'Classification'} problem"
  )

  if not is_reg and not pd.api.types.is_numeric_dtype(df[label]):
    choose_encoding_ui()
  
  nextButton()


def choose_encoding_ui():
  ds = data_state()
  df = ds.df
  label = ds.label
  messages = get_choosing_messages(df, label)

  if 'choice' not in ds:
    ds.choice = 0
  default_choice = ds.choice

  st.subheader(
    "Your label is not binary (0/1). Please choose how you want it to be encoded."
  )

  st.radio(
    '',
    messages,
    index=default_choice,
    label_visibility="collapsed",
    on_change=on_encoding_change,
    args=(messages,),
    key='label_encoding_radio'
  )
  dataFrame(encoded_label_df())


def on_encoding_change(messages):
  data_state().choice = messages.index(st.session_state['label_encoding_radio'])


def encoded_label_df():
  ds = data_state()
  df = ds.df.copy()
  label = ds.label

  df = df.dropna(subset=[label])
  if ds.is_regression:
    return df

  df[label] = df[label].apply(lambda x: target_encoding_callback(x))
  return df


def target_encoding_callback(x):
  ds = data_state()
  df = ds.df
  label = ds.label
  label_values = df[label].unique()
  choice = ds.get('choice', 0)
  idx = 1 - choice
  return int(x == label_values[idx])


def determine_regression(label_series):
  return label_series.nunique() != 2


def on_target_change():
  ds = data_state()
  df = ds.df
  label = st.session_state["target_column"]
  ds.label = label
  ds.is_regression = determine_regression(df[label])


def filter_cols(df):
  return [
    col for col in df.columns
    if (pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() >= 2)
    or (not pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() == 2)
  ]

def get_label_values():
  df=data_state().df
  label=data_state().label
  return  df[label].unique()[:2]

def get_choosing_messages(df, label):
  val0, val1 = df[label].unique()[:2]
  return [f'0 for {val0}, 1 for {val1}', f'0 for {val1}, 1 for {val0}']
