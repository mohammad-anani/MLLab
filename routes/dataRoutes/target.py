import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame



def targetPage():
  st.subheader("2-Specify your target column (aka Label)")
  select_label_ui()
  if 'label' in st.session_state:
    confirm_label_ui()


def select_label_ui():
  df=st.session_state.df
  cols=filter_cols(df)
  index =cols.index(st.session_state.label) if 'label' in st.session_state and st.      session_state.label in cols else None

  st.selectbox("",cols,index=index,    key="my_input",
  on_change=on_target_change,label_visibility="collapsed")


def confirm_label_ui():
  df=st.session_state.df
  label=st.session_state.label
  is_reg=st.session_state.is_regression

  st.subheader(f"Based on your label( {label} ), your problem will be treated as a {'Regression' if is_reg else 'Classification'} problem")
  if (not is_reg) and not pd.api.types.is_numeric_dtype(df[label]):
    choose_encoding_ui()
  nextButton()


def choose_encoding_ui():
  df=st.session_state.df
  label=st.session_state.label
  choosing_messages=get_choosing_messages(df,label)
  if 'choice' not in st.session_state:
    st.session_state.choice=0
  default_choice = st.session_state.choice

  st.subheader("Your label is not binary (0/1). Please choose how you want it to be encoded.")
  choice=st.radio('',choosing_messages,index=default_choice,label_visibility="collapsed",on_change=on_encoding_change,args=(choosing_messages,), key='radio_input')
  dataFrame(encoded_label_df())


def on_encoding_change(choosing_messages):
  st.session_state.choice=choosing_messages.index(st.session_state['radio_input'])


def encoded_label_df():
  df=st.session_state.df.copy()
  is_regression=st.session_state.is_regression
  label=st.session_state.label

  if is_regression:
    return st.session_state.df.copy()
  df[label]=df[label].apply(target_encoding_callback)
  return df


def target_encoding_callback(x):
  if pd.isna(x) or pd.isnull(x):
    return x
  df=st.session_state.df
  label=st.session_state.label
  label_values=df[label].unique()
  choice=st.session_state.get('choice',0)
  if(choice==1):
    if x==label_values[0]: 
      return 0 
    elif x==label_values[1]:
      return 1
  else:
    if x==label_values[1]: 
      return 0 
    elif x==label_values[0]:
      return 1


def is_regression(label_df):
  if label_df.nunique() == 2:
    return False
  return True


def on_target_change():
  df=st.session_state.df
  label = st.session_state["my_input"]
  st.session_state.label =label
  st.session_state.is_regression=is_regression(df[label])


def filter_cols(df):
  cols = []
  for col in df.columns:
    n_unique = df[col].nunique()
    dtype = df[col].dtype
    if pd.api.types.is_numeric_dtype(dtype):
      if n_unique >= 2:
        cols.append(col)
    else:
      if n_unique == 2: 
        cols.append(col)
  return cols


def get_choosing_messages(df,label):
  label_values=df[label].unique()
  choosing_messages=[f'0 for {label_values[0]}, 1 for {label_values[1]}',f'0 for {label_values[1]}, 1 for {label_values[0]}']
  return choosing_messages