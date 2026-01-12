import streamlit as st
import pandas as pd
from util.routeButton import routeButton
from util.dataFrame import dataFrame
from .drop import removed_cols_df

styles="""
<style>
hr {
  margin: 0px !important;
  margin-bottom: 1em !important
}
</style>
"""


def filterPage():
  if 'filter' not in st.session_state:
    st.session_state.filter = {}

  if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter=0  

  if 'remove_outliers' not in st.session_state:
    st.session_state.remove_outliers=False  

  if 'remove_singleval_col' not in st.session_state:
    st.session_state.remove_singleval_col=False  

  st.markdown(styles, unsafe_allow_html=True)
  routeButton("Back", "left", "drop")
  st.title("I-Data")
  c1,c2=st.columns([1,2.5])
  with c1:
    st.subheader("4- Filter data")
  with c2:
    if st.button("Reset"):
      reset_form()

  df = removed_cols_df()
  label = st.session_state.label
  num_cols, non_num_cols = split_cols_numerical_and_non(df)

  for col in num_cols:
    render_num_col_filter(df[col])
  st.markdown("""
### 🔎 Multiple words rule

- Separate expressions using **`/##/`**
- This lets you match **any** of the words

**Examples:**

- **Should contain:** `apple banana`  
  → string must contain **exactly** `"apple banana"`

- **Should contain:** `apple/##/banana`  
  → string may contain **`apple` OR `banana` (or both)**
""")
  for col in non_num_cols:
    render_non_num_col_filter(df[col])
  st.checkbox("Remove outliers",key='remove_outliers_input',on_change=on_cb_outlier_change,value=st.session_state.remove_outliers)
  st.checkbox("Remove columns with single value",key='singleval_col_input',on_change=on_cb_singleval_col_change,value=st.session_state.remove_singleval_col)
  st.divider()
  st.subheader("Resulting Dataset:")
  dataFrame(filtered_df())
  routeButton("Next", "right", 'target')


def render_num_col_filter(col):
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader(col.name)
  with c2:
    c21, c22,c23 = st.columns([1, 4,1])
    with c21:
      st.write("From:")
      st.write("To:")
    with c22:
      min_filter_key='min '+col.name
      max_filter_key='max '+col.name
      min_key = 'input'+str(st.session_state.reset_counter)+' ' + min_filter_key
      max_key = 'input'+str(st.session_state.reset_counter)+' ' +  max_filter_key
      
      st.number_input('', label_visibility="collapsed", key=min_key, on_change=onchange, args=(min_key,))
      st.number_input('', label_visibility="collapsed", key=max_key, on_change=onchange, args=(max_key,))
    with c23:
      if st.button('Reset',key=min_key+" resetter") and min_filter_key in st.session_state.filter:
        st.session_state.filter.pop(min_filter_key)
      if st.button('Reset',key=max_key+" resetter") and max_filter_key in st.session_state.filter:
        st.session_state.filter.pop(max_filter_key)

  cur_min = st.session_state.get(min_key, 0.0)
  cur_max = st.session_state.get(max_key, 0.0)
  
  if cur_min > cur_max:
    st.error(f"Min value ({cur_min}) can't be greater than Max value ({cur_max})")
  st.divider()


def render_non_num_col_filter(col):
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader(col.name)
  with c2:
    c21, c22,c23 = st.columns([1.5, 2.5,1])
    with c21:
      st.write("Should Contain:")
      st.write("Shouldn't Contain:")
    with c22:
      in_filter_key='in '+col.name
      not_in_filter_key='not in '+col.name
      in_key = 'input'+str(st.session_state.reset_counter)+' ' +  in_filter_key
      not_in_key = 'input'+str(st.session_state.reset_counter)+' ' +  not_in_filter_key
      
      st.text_input('', label_visibility="collapsed", key=in_key, on_change=onchange, args=(in_key,))
      st.text_input('', label_visibility="collapsed", key=not_in_key, on_change=onchange, args=(not_in_key,))
    with c23:
      if st.button('Reset',key=in_key+" resetter") and in_filter_key in st.session_state.filter:
        st.session_state.filter.pop(in_filter_key)
      if st.button('Reset',key=not_in_key+" resetter") and not_in_filter_key in st.session_state.filter:
        st.session_state.filter.pop(not_in_filter_key)
  
  st.divider()


def split_cols_numerical_and_non(df):
  num_cols = []
  non_num_cols = []
  for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
      num_cols.append(col) 
    else:
      non_num_cols.append(col)
  return num_cols, non_num_cols


def onchange(key):
  filter_key = key[7:]
  
  if st.session_state[key] !='':
    st.session_state.filter[filter_key] = st.session_state[key]
  else:
    st.session_state.filter.pop(filter_key) 


def filtered_df():
  df=removed_cols_df()
  filters=st.session_state.filter
  remove_outliers=st.session_state.remove_outliers
  remove_singleval_col=st.session_state.remove_singleval_col
  mask = pd.Series(True, index=df.index)
  for key, value in filters.items():
    if key.startswith("min "):
      col = key[4:]
      mask &= df[col] >= value
    elif key.startswith("max "):
      col = key[4:]
      mask &= df[col] <= value
    elif key.startswith("in "):
      col = key[3:]
      if isinstance(value, str):
        or_values = value.split("/##/")
        mask_col = df[col].apply(lambda x: any(v in str(x) for v in or_values))
        mask &= mask_col
    elif key.startswith("not in "):
      col = key[7:]
      if isinstance(value, str):
        or_values = value.split("/##/")
        mask_col = df[col].apply(lambda x: all(v not in str(x) for v in or_values))
        mask &= mask_col
    else:
      mask &= df[key] == value

  df = df[mask]

  if remove_singleval_col:
    single_val_cols = [col for col in df.columns if df[col].nunique() <= 1]
    df = df.drop(columns=single_val_cols, errors='ignore')

  if remove_outliers:
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
      Q1 = df[col].quantile(0.25)
      Q3 = df[col].quantile(0.75)
      IQR = Q3 - Q1
      df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]

  return df


def reset_form():
  st.session_state.filter.clear()
  for k in list(st.session_state.keys()):
    if k.startswith("input"):
      del st.session_state[k]
  if st.session_state.reset_counter==9:
    st.session_state.reset_counter=0
  else:
    st.session_state.reset_counter+=1
  st.rerun()


def on_cb_outlier_change():
  st.session_state.remove_outliers=st.session_state['remove_outliers_input']


def on_cb_singleval_col_change():
  st.session_state.remove_singleval_col=st.session_state['singleval_col_input']
