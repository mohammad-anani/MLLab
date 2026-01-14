import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from .target import encoded_label_df
from routes.dataRoutes.data_state import data_state


def dropPage():
  df=encoded_label_df()
  label=data_state().label
  x_df=df.drop(label,axis=1)
  cols=x_df.columns
  col_count=x_df.shape[1]
  if 'cols_to_remove' not in data_state():
    data_state().cols_to_remove=[]
  default_cols = [c for c in data_state().get("cols_to_remove", []) if c != label]

  st.subheader("3- Remove unwanted features")
  st.multiselect("",cols,default=default_cols,max_selections=col_count-1,label_visibility="collapsed",on_change=on_change,key='drop_input' )
  st.subheader("Resulting Dataset:")
  dataFrame(removed_cols_df())
  nextButton()


def removed_cols_df():
  df=encoded_label_df()
  if 'cols_to_remove' not in data_state():
    return df 
  cols_to_remove=data_state().cols_to_remove
  return df.drop(columns=cols_to_remove, errors='ignore')


def on_change():
  data_state().cols_to_remove = st.session_state['drop_input']