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

def dropPage():
  st.markdown(
styles,
      unsafe_allow_html=True
  )

  if st.button("Back"):
    st.session_state.page = "target" 
    st.rerun() 

  st.title("I-Data")

  st.subheader("2- Feature Removing:")

  df=st.session_state.df
  label=st.session_state.label

  x_df=df.drop(label,axis=1)
  cols=x_df.columns
  cols_to_remove_auto=get_non_numerical_cols(x_df)

  if cols_to_remove_auto:
    st.subheader("a- The following features are non numerical and will therefore be automatically removed:")

    st.write(", ".join(cols_to_remove_auto))
  
  else:
    st.subheader("a- No features need to be automatically dropped")

  new_cols=[col for col in cols if col not in cols_to_remove_auto]

  st.subheader("b- Remove features manually:")

  cols_to_remove_manual=st.multiselect("",new_cols)


  new_x_df=x_df.drop([*cols_to_remove_auto,*cols_to_remove_manual],axis=1)

  st.subheader("Resulting Dataset:")
  st.dataframe(new_x_df.head())

  if st.button("Next",width="stretch"):
    st.session_state.page = "drop" 
    st.rerun() 


def get_non_numerical_cols(x_df):
  return [col for col in x_df.columns
            if not pd.api.types.is_numeric_dtype(x_df[col])
            and not pd.api.types.is_bool_dtype(x_df[col])]