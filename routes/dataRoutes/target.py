import streamlit as st
import pandas as pd

styles="""
<style>      
div[data-testid="stButton"] > button {
  height: 3em;
  width: 7em;
  background-color: white
}

div[data-testid="stButton"] p {
  font-size: 20px;
}

div[data-testid="stButton"] {
  display: flex;
  justify-content: right;
}
</style>
"""

def targetPage():
  st.markdown(
styles,
      unsafe_allow_html=True
  )

  if st.button("Back"):
    st.session_state.page = "upload" 
    st.rerun() 

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
  args=["my_input"])
  

def confirm_label_ui():
  df=st.session_state.df
  label=st.session_state.label
  
  is_reg=is_regression(df[label])

  st.session_state.is_regression=is_reg
  st.subheader(f"Based on your label( {label} ), your problem will be treated as a {'Regression' if is_reg else 'Classification'} problem")

  if st.button("Next",width="stretch"):
    st.session_state.page = "drop" 
    st.rerun() 


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