import streamlit as st
from routes.dataRoutes.impute import imputed_df
from routes.dataRoutes.filter import split_cols_numerical_and_non
from routes.dataRoutes.encode import cols_with_few_values
from util.button import button
from routes.dataRoutes.data_state import data_state
from routes.dataRoutes.target import get_label_values
from routes.modelRoutes.train import predict_new_data

def predictPage():
  
  df = imputed_df()
  label=data_state().label

  df=df.drop(label,axis=1)

  num_cols, non_num_cols = split_cols_numerical_and_non(df)

  non_num_cols = cols_with_few_values(df, non_num_cols)

  st.subheader("Enter values for prediction:")


  input_data = {}

  for col in num_cols:
    c1, c2 = st.columns([1, 2])
    with c1:
      st.write(f"{col}:")
    with c2:
      input_data[col] = st.number_input(
        label="",
        value=float(df[col].mean()),
        step=1.0,
        label_visibility="collapsed"
      )

  for col in non_num_cols:
    unique_vals = sorted(df[col].dropna().unique().tolist())
    c1, c2 = st.columns([1, 2])
    with c1:
      st.write(f"{col}:")
    with c2:
      input_data[col] = st.selectbox(
        label="",
        options=unique_vals,
        label_visibility="collapsed"
      )
  submit = button("Predict",'right')

  if submit:
    result = predict_new_data(st.session_state.trained_model, input_data)
    
    if data_state().is_regression:
      st.header(f"{label}: {result:.2f}")
    else:
      choice=data_state().get('choice',None)
      if choice!=None:
        values=get_label_values()
        st.header(f"{label}: {values[result^choice]}")
      else:
        st.header(f"{label}: {result}")
