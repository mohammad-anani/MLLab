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

def uploadPage():
  st.markdown(
styles,
      unsafe_allow_html=True
  )

  if st.button("Back"):
    st.session_state.page = "home" 
    st.rerun() 

  st.title("I-Data")

  st.subheader("1-Upload you data(csv only)")

  if 'df' not in st.session_state:
    upload_file_ui()
  else:
    loaded_dataset_ui()


def upload_file_ui():
  uploaded_file= st.file_uploader("", type="csv",
  key="uploaded_file",
  on_change=on_change,
  args=["uploaded_file"])


def loaded_dataset_ui():
  df=st.session_state.df
  row_count,col_count=df.shape
  
  st.dataframe(df.head())
  st.text(f"{row_count} rows\n{col_count} columns")

  if col_count<2:
    st.error("Dataset should have at least 2 columns")
  else:
    if st.button("Next",width="stretch"):
      st.session_state.page = "target" 
      st.rerun() 


def on_change(key):
  uploaded_file = st.session_state[key]
  if uploaded_file:
    try:
      df = pd.read_csv(uploaded_file)
      st.session_state.df = df
    except Exception as e:
      st.error("Error in file uploading. Try again")