import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from .impute import imputed_df
from .filter import split_cols_numerical_and_non
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from routes.dataRoutes.data_state import data_state


def encodePage():
  if 'encoding' not in data_state():
    data_state().encoding={}
  if 'encoding_order' not in data_state():
    data_state().encoding_order={}

  for col in data_state()['cols_to_remove']:
    if col in data_state().encoding:
      del data_state().encoding[col]
      if col in data_state().encoding_order:
        del data_state().encoding_order[col]


  df=imputed_df()
  num_cols,non_num_cols=split_cols_numerical_and_non(df)


  st.subheader("6- Encode non-numerical features")
  if not non_num_cols.any():
    st.subheader("You have no non-numerical features!")
  else:
    for col in non_num_cols:
      choose_col_encode_ui(df[col])

    new_df=encoded_df()

    st.subheader("Dataset before encoding features:")
    dataFrame(df)
    st.subheader("Dataset after encoding features:")
    dataFrame(new_df)
  nextButton()


def choose_col_encode_ui(col):
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader(col.name+':')
  with c2:
    if col.nunique()>20:
      st.write("This feature has more that 20 unique value! It will be automatically removed. If needed, filter out values in the filter page.")
    else:
      encoder_input_ui(col)
  st.divider()


def encoder_input_ui(col):
  encoding_methods=['One Hot','Ordinal']
  key=col.name

  if key not in data_state().encoding:
    data_state().encoding[key]=encoding_methods[0]

  input_key='input '+key
  default_index=encoding_methods.index(data_state().encoding[key])

  st.selectbox('',options=encoding_methods,key=input_key,on_change=on_change,args=(input_key,),index=default_index,label_visibility='collapsed')

  if data_state().encoding[key]==encoding_methods[1]:
    ordering_input_ui(col)


def ordering_input_ui(col):
  key=col.name
  input_key='e_input '+key

  if key not in data_state().encoding_order:
    data_state().encoding_order[key]=list(col.unique())

  st.subheader("Arrange the values in the order you want(first selection is 0, then 1, ...).")
  st.multiselect('',options=list(col.unique()),default=data_state().encoding_order[key],key=input_key,on_change=on_order_change,args=(input_key,),label_visibility='collapsed')

  if len(data_state().encoding_order[key])!= col.nunique():
    st.error("Some values are missing; they’ll be filled automatically.")


def on_change(key):
  data_state().encoding[key[6:]]=st.session_state[key]


def on_order_change(key):
  data_state().encoding_order[key[8:]]=st.session_state[key]


def encoded_df():
  df = imputed_df()
  num_cols, non_num_cols = split_cols_numerical_and_non(df)

  if len(non_num_cols) == 0:
    return df
  
  low_card_cols = cols_with_many_values(df,non_num_cols)
  
  encoded_df = df[num_cols].copy() 
  
  if not low_card_cols:
    return encoded_df

  for col in low_card_cols:
    enc_type = data_state().encoding.get(col, "One Hot")
    
    if enc_type == "One Hot":
      ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
      transformed = ohe.fit_transform(df[[col]])
      transformed_df = pd.DataFrame(
        transformed,
        columns=ohe.get_feature_names_out([col]),
        index=df.index
      )
      encoded_df = pd.concat([encoded_df, transformed_df], axis=1)
    
    elif enc_type == "Ordinal":
      user_order = data_state().encoding_order.get(col, [])
      all_values = df[col].dropna().unique().tolist()
      
      missing = [v for v in all_values if v not in user_order]
      full_order = user_order + missing
      
      ord_enc = OrdinalEncoder(categories=[full_order], handle_unknown="use_encoded_value", unknown_value=-1)
      transformed = ord_enc.fit_transform(df[[col]])
      encoded_df[col] = transformed
  
  return encoded_df


def cols_with_many_values(df,non_num_cols):
  return [col for col in non_num_cols if df[col].nunique() <= 20] 
