import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from util.dataFrame import dataFrame


def filterPage():

  routeButton("Back","left","drop")

  st.title("I-Data")

  st.subheader("4- Filter data")

  df=st.session_state.df
  label=st.session_state.label
  cols_to_remove=st.session_state.cols_to_remove

  x_df=df.drop([label,*cols_to_remove],axis=1)
  cols=x_df.columns

  for col in cols:
    render_col_filter(x_df[col])

  st.subheader("Resulting Dataset:")
  dataFrame(x_df)

  routeButton("Next","right",'target')


def render_col_filter(col):
  
  dtype=col.dtype

  if pd.api.types.is_numeric_dtype(dtype):
    c1, c2, c3, c4,c5 = st.columns(5)
    with c1:
      min_val=st.number_input('',label_visibility="collapsed",key='min '+col.name)
    with c2:
      st.write("<")
    with c3:
      st.write(col.name)
    with c4:
      st.write("<")
    with c5:
      max_val=st.number_input('',label_visibility="collapsed",key='max '+col.name)
    
    if min_val>max_val:
      st.error("Min value can't be greater than Max value")


# def get_non_numerical_cols(x_df):
#   return [col for col in x_df.columns
#             if not pd.api.types.is_numeric_dtype(x_df[col])
#             and not pd.api.types.is_bool_dtype(x_df[col])]