import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from util.dataFrame import dataFrame


def dropPage():

  routeButton("Back","left","target")

  st.title("I-Data")

  st.subheader("2- Remove unwanted features")

  df=st.session_state.df
  label=st.session_state.label

  x_df=df.drop(label,axis=1)
  cols=x_df.columns
  col_count=x_df.shape[1]

  if "cols_to_remove" in st.session_state:
    default_cols=st.session_state.cols_to_remove

    if label in default_cols:
      default_cols.remove(label)
  else:
    default_cols=[]

  cols_to_remove=st.multiselect("",cols,default=default_cols,max_selections=col_count-1 )

  st.session_state.cols_to_remove=cols_to_remove

  new_x_df=x_df.drop(cols_to_remove,axis=1)

  st.subheader("Resulting Dataset:")
  dataFrame(new_x_df)

  routeButton("Next","right",'target')


# def get_non_numerical_cols(x_df):
#   return [col for col in x_df.columns
#             if not pd.api.types.is_numeric_dtype(x_df[col])
#             and not pd.api.types.is_bool_dtype(x_df[col])]