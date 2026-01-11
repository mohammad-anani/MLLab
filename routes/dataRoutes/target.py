import streamlit as st
import pandas as pd
from util.routeButton import routeButton


def targetPage():

  routeButton("Back","left","upload")

  st.title("I-Data")

  st.subheader("2-Specify your target column (aka Label)")

  select_label_ui()

  if 'label' in st.session_state:
    confirm_label_ui()


def select_label_ui():
  
  df=st.session_state.df
  cols=filter_cols(df)

  if 'label' in st.session_state and st.      session_state.label in cols:
    index = cols.index(st.session_state.label)
  else:
    index = None

  st.selectbox("",cols,index=index,    key="my_input",
  on_change=on_change,
  args=["my_input"],label_visibility="collapsed")


def confirm_label_ui():
  df=st.session_state.df
  label=st.session_state.label
  
  is_reg=is_regression(df[label])

  st.session_state.is_regression=is_reg

  st.subheader(f"Based on your label( {label} ), your problem will be treated as a {'Regression' if is_reg else 'Classification'} problem")

  if (not is_reg) and not pd.api.types.is_numeric_dtype(df[label]):
    choose_encoding_ui()

  routeButton("Next","right",'drop')


def choose_encoding_ui():
  df=st.session_state.df
  label=st.session_state.label

  label_values=df[label].unique()

  choosing_messages=[f'0 for {label_values[0]}, 1 for {label_values[1]}',f'0 for {label_values[1]}, 1 for {label_values[0]}']

  if 'choice' in st.session_state:
    default_choice = st.session_state.choice
  else:
    default_choice = 0

  st.subheader("Your label is not binary (0/1). Please choose how you want it to be encoded.")
  choice=st.radio('',choosing_messages,index=default_choice,label_visibility="collapsed")

  st.session_state.choice=choosing_messages.index(choice)


def is_regression(label_df):
  if label_df.nunique() == 2:
    return False

  return True


def on_change(key):
  st.session_state.label = st.session_state[key]


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