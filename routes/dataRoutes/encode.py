import streamlit as st
import pandas as pd
import numpy as np
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from .impute import imputed_df
from .filter import split_cols_numerical_and_non
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from routes.dataRoutes.data_state import data_state

def encodePage():
    ds = data_state()  
    ds.encoding = ds.get('encoding', {})
    ds.encoding_order = ds.get('encoding_order', {})
    for col in ds.get('cols_to_remove', []):
        ds.encoding.pop(col, None)
        ds.encoding_order.pop(col, None)
    df = imputed_df()
    num_cols, non_num_cols = split_cols_numerical_and_non(df)
    st.subheader("6- Encode non-numerical features")
    if len(non_num_cols) == 0:
        st.subheader("You have no non-numerical features!")
    else:
        for col in non_num_cols:
            choose_col_encode_ui(df[col])
        new_df = encoded_df()
        st.subheader("Dataset before encoding features:")
        dataFrame(df)
        st.subheader("Dataset after encoding features:")
        dataFrame(new_df)
    nextButton()


def choose_col_encode_ui(col):
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader(f"{col.name}:")
    with c2:
        if col.nunique() > 20:
            st.write("This feature has more than 20 unique values! It will be automatically removed.")
        else:
            encoder_input_ui(col)
    st.divider()


def encoder_input_ui(col):
    ds = data_state()
    encoding_methods = ['One Hot', 'Ordinal']
    key = col.name
    if key not in ds.encoding:
        ds.encoding[key] = encoding_methods[0]
    input_key = f'input {key}'
    default_index = encoding_methods.index(ds.encoding[key])
    st.selectbox('', options=encoding_methods, key=input_key, on_change=on_change, args=(input_key,), index=default_index, label_visibility='collapsed')
    if ds.encoding[key] == "Ordinal":
        ordering_input_ui(col)


def ordering_input_ui(col):
    ds = data_state()
    key = col.name
    input_key = f'e_input {key}'
    if key not in ds.encoding_order:
        ds.encoding_order[key] = list(col.unique())
    st.subheader("Arrange the values in order (first selection is 0, then 1, ...).")
    st.multiselect('', options=list(col.unique()), default=ds.encoding_order[key], key=input_key, on_change=on_order_change, args=(input_key,), label_visibility='collapsed')
    if len(ds.encoding_order[key]) != col.nunique():
        st.error("Some values are missing; they’ll be filled automatically.")


def on_change(key):
    ds = data_state()
    ds.encoding[key[6:]] = st.session_state[key]


def on_order_change(key):
    ds = data_state()
    ds.encoding_order[key[8:]] = st.session_state[key]


def encode_df(df, encoding_map, encoding_order, fit=True, encoders=None):
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    cat_cols=cols_with_few_values(df,cat_cols)
    if not cat_cols:
        return (df, encoders) if fit else df
    encoded_df = df[num_cols].copy()
    if fit:
        encoders = {}
    for col in cat_cols:
        enc_type = encoding_map.get(col, "One Hot")
        if enc_type == "One Hot":
            if fit:
                enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
                enc.fit(df[[col]])
                encoders[col] = enc
            else:
                enc = encoders[col]
            transformed = enc.transform(df[[col]])
            transformed_df = pd.DataFrame(transformed, columns=enc.get_feature_names_out([col]), index=df.index)
            encoded_df = pd.concat([encoded_df, transformed_df], axis=1)
        elif enc_type == "Ordinal":
            if fit:
                user_order = encoding_order.get(col, [])
                all_values = df[col].dropna().unique().tolist()
                full_order = user_order + [v for v in all_values if v not in user_order]
                enc = OrdinalEncoder(categories=[full_order], handle_unknown="use_encoded_value", unknown_value=-1)
                enc.fit(df[[col]])
                encoders[col] = enc
            else:
                enc = encoders[col]
            encoded_df[col] = enc.transform(df[[col]])
    return (encoded_df, encoders) if fit else encoded_df

def encoded_df():
    df = imputed_df()
    ds = data_state()
    return encode_df(df, ds.encoding, ds.encoding_order)[0]

def cols_with_few_values(df, non_num_cols):
    return [col for col in non_num_cols if df[col].nunique() <= 20]