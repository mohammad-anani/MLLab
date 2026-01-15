import streamlit as st
import pandas as pd
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from .drop import removed_cols_df
from routes.dataRoutes.data_state import data_state

# Styles and guide (unchanged)
styles = """
<style>
hr {
  margin: 0px !important;
  margin-bottom: 1em !important
}
</style>
"""

string_guide = """
### 🔎 Multiple words rule

- Separate expressions using **`/##/`**
- This lets you match **any** of the words

**Examples:**

- **Should contain:** `apple banana`  
  → string must contain **exactly** `"apple banana"`

- **Should contain:** `apple/##/banana`  
  → string may contain **`apple` OR `banana` (or both)**
"""


def filterPage():
  ds = data_state()
  ds.filter = ds.get('filter', {})
  ds.reset_counter = ds.get('reset_counter', 0)
  ds.remove_outliers = ds.get('remove_outliers', False)
  ds.remove_singleval_col = ds.get('remove_singleval_col', False)

  df = removed_cols_df()
  label = ds.label
  num_cols, non_num_cols = split_cols_numerical_and_non(df)

  for col in ds.get('cols_to_remove', []):
    for prefix in ['min ', 'max ', 'in ', 'not in ']:
      ds.filter.pop(prefix + col, None)

  st.markdown(styles, unsafe_allow_html=True)
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader("4- Filter data")
  with c2:
    if st.button("Reset"):
      reset_form()

  for col in num_cols:
    render_num_col_filter(col)

  if len(non_num_cols) > 0:
    st.markdown(string_guide)
  for col in non_num_cols:
    render_non_num_col_filter(col)

  st.checkbox(
    "Remove outliers",
    key='remove_outliers_input',
    on_change=on_cb_outlier_change,
    value=ds.remove_outliers
  )
  st.checkbox(
    "Remove columns with single value",
    key='singleval_col_input',
    on_change=on_cb_singleval_col_change,
    value=ds.remove_singleval_col
  )

  st.divider()
  st.subheader("Resulting Dataset:")
  dataFrame(filtered_df())
  nextButton()


def render_num_col_filter(col):
  ds = data_state()
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader(f"{col.name}:")
  with c2:
    render_numeric_input(col.name, ds.reset_counter)
  st.divider()


def render_numeric_input(col_name, counter):
  ds = data_state()
  c1, c2, c3 = st.columns([1, 4, 1])

  min_key = f"input{counter} min {col_name}"
  max_key = f"input{counter} max {col_name}"
  default_min = ds.filter.get(f"min {col_name}", 0)
  default_max = ds.filter.get(f"max {col_name}", 0)

  with c1:
    st.write("From:")
    st.write("To:")

  with c2:
    st.number_input(
      '',
      label_visibility="collapsed",
      key=min_key,
      on_change=onchange,
      args=(f"min {col_name}",),
      value=default_min
    )
    st.number_input(
      '',
      label_visibility="collapsed",
      key=max_key,
      on_change=onchange,
      args=(f"max {col_name}",),
      value=default_max
    )

  with c3:
    if st.button('Reset', key=min_key + " resetter"):
      ds.filter.pop(f"min {col_name}", None)
    if st.button('Reset', key=max_key + " resetter"):
      ds.filter.pop(f"max {col_name}", None)


def render_non_num_col_filter(col):
  ds = data_state()
  c1, c2 = st.columns([1, 2.5])
  with c1:
    st.subheader(f"{col.name}:")
  with c2:
    render_string_input(col.name, ds.reset_counter)
  st.divider()


def render_string_input(col_name, counter):
  ds = data_state()
  c1, c2, c3 = st.columns([1.5, 2.5, 1])

  in_key = f"input{counter} in {col_name}"
  not_in_key = f"input{counter} not in {col_name}"
  default_in = ds.filter.get(f"in {col_name}", '')
  default_not_in = ds.filter.get(f"not in {col_name}", '')

  with c1:
    st.write("Should Contain:")
    st.write("Shouldn't Contain:")

  with c2:
    st.text_input(
      '',
      label_visibility="collapsed",
      key=in_key,
      on_change=onchange,
      args=(f"in {col_name}",),
      value=default_in
    )
    st.text_input(
      '',
      label_visibility="collapsed",
      key=not_in_key,
      on_change=onchange,
      args=(f"not in {col_name}",),
      value=default_not_in
    )

  with c3:
    if st.button('Reset', key=in_key + " resetter"):
      ds.filter.pop(f"in {col_name}", None)
    if st.button('Reset', key=not_in_key + " resetter"):
      ds.filter.pop(f"not in {col_name}", None)


def split_cols_numerical_and_non(df):
  num_cols = df.select_dtypes(include="number").columns
  non_num_cols = df.select_dtypes(exclude="number").columns
  return num_cols, non_num_cols


def onchange(filter_key):
  ds = data_state()
  value = st.session_state.get(f"input {filter_key}", '')
  if value != '':
    ds.filter[filter_key] = value
  else:
    ds.filter.pop(filter_key, None)


def filtered_df():
  ds = data_state()
  df = removed_cols_df()
  filters = ds.filter
  remove_outliers = ds.remove_outliers
  remove_singleval_col = ds.remove_singleval_col

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
        mask &= df[col].apply(lambda x: any(v in str(x) for v in or_values))
    elif key.startswith("not in "):
      col = key[7:]
      if isinstance(value, str):
        or_values = value.split("/##/")
        mask &= df[col].apply(lambda x: all(v not in str(x) for v in or_values))
    else:
      mask &= df[key] == value

  df = df[mask]

  if remove_outliers:
    for col in df.select_dtypes(include='number').columns:
      Q1 = df[col].quantile(0.25)
      Q3 = df[col].quantile(0.75)
      IQR = Q3 - Q1
      df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]

  if remove_singleval_col:
    single_val_cols = [col for col in df.columns if df[col].nunique() <= 1]
    df = df.drop(columns=single_val_cols, errors='ignore')

  return df


def reset_form():
  ds = data_state()
  ds.filter.clear()
  for k in list(st.session_state.keys()):
    if k.startswith("input"):
      del st.session_state[k]

  ds.reset_counter = (ds.reset_counter + 1) % 10
  st.rerun()


def on_cb_outlier_change():
  ds = data_state()
  ds.remove_outliers = st.session_state['remove_outliers_input']


def on_cb_singleval_col_change():
  ds = data_state()
  ds.remove_singleval_col = st.session_state['singleval_col_input']