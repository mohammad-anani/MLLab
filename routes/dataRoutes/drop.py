import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from util.dataFrame import dataFrame
from .target import encoded_label_df


def dropPage():
  routeButton("Back","left","target")
  st.title("I- Data")
  st.subheader("3- Remove unwanted features")

  df=encoded_label_df()
  label=st.session_state.label

  x_df=df.drop(label,axis=1)
  cols=x_df.columns
  col_count=x_df.shape[1]

  default_cols = [c for c in st.session_state.get("cols_to_remove", []) if c != label]

  st.multiselect("",cols,default=default_cols,max_selections=col_count-1,label_visibility="collapsed",on_change=on_change,key='drop_input' )
  st.subheader("Resulting Dataset:")
  dataFrame(removed_cols_df())
  routeButton("Next","right",'filter')


def removed_cols_df():
  df=encoded_label_df()

  if 'cols_to_remove' not in st.session_state:
    return df 

  cols_to_remove=st.session_state.cols_to_remove
  return df.drop(columns=cols_to_remove, errors='ignore')


def on_change():
  st.session_state.cols_to_remove = st.session_state[drop_input]