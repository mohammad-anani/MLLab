import streamlit as st
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from routes.dataRoutes.target import get_choosing_messages
from routes.dataRoutes.drop import removed_cols_df
from routes.dataRoutes.filter import split_cols_numerical_and_non
from routes.dataRoutes.impute import imputed_df
from routes.dataRoutes.encode import cols_with_many_values
from routes.dataRoutes.data_state import data_state


def reviewPage():
  st.subheader("8- Review")
  review_initial_dataset()
  review_target()
  review_removed_features()
  review_filters()
  review_missing_values()
  review_encoding()
  review_additional_configurations()
#  nextButton()


def review_initial_dataset():
  st.subheader("a- Initial dataset:")
  dataFrame(data_state().df)


def review_target():
  st.subheader("b- Target:")
  label = data_state().label
  is_regression = data_state().is_regression
  st.write(markdown_bold("Name:") + " " + label)
  st.write(markdown_bold("Type:") + " " + ('Regression' if is_regression else 'Classification'))
  if not is_regression:
    df = data_state().df
    choice = get_choosing_messages(df, label)[data_state().choice]
    st.write(markdown_bold("Encoding choice:") + " " + choice)


def review_removed_features():
  st.subheader("c- Removed features:")
  cols_to_remove = data_state().cols_to_remove
  st.write(", ".join(cols_to_remove) if cols_to_remove else "No removed features.")


def review_filters():
  st.subheader("d- Filters:")
  _display_filters()
  st.write(markdown_bold("Remove outliers:") + " " + yes_or_no(data_state().remove_outliers))
  st.write(markdown_bold("Remove single value features:") + " " + yes_or_no(data_state().remove_singleval_col))


def _display_filters():
  filters = data_state().filter
  if not filters:
    st.write(markdown_bold("No Filters"))
    return
  df = removed_cols_df()
  num_cols, non_num_cols = split_cols_numerical_and_non(df)
  _display_numeric_filters(num_cols)
  _display_non_numeric_filters(non_num_cols)


def _display_numeric_filters(num_cols):
  for col in num_cols:
    min_val = data_state().filter.get('min ' + col)
    max_val = data_state().filter.get('max ' + col)
    if min_val and max_val:
      st.write(markdown_bold(col) + " between " + markdown_bold(str(min_val)) + " and " + markdown_bold(str(max_val)))
    elif min_val:
      st.write(markdown_bold(col) + " more than " + markdown_bold(str(min_val)))
    elif max_val:
      st.write(markdown_bold(col) + " less than " + markdown_bold(str(max_val)))


def _display_non_numeric_filters(non_num_cols):
  for col in non_num_cols:
    in_val = data_state().filter.get('in ' + col)
    not_in_val = data_state().filter.get('not in ' + col)
    if in_val and not_in_val:
      st.write(markdown_bold(col) + " should contain " + markdown_bold(format_string_filter(in_val)) +
               " and shouldn't contain " + markdown_bold(format_string_filter(not_in_val)))
    elif in_val:
      st.write(markdown_bold(col) + " should contain " + markdown_bold(format_string_filter(in_val)))
    elif not_in_val:
      st.write(markdown_bold(col) + " shouldn't contain " + markdown_bold(format_string_filter(not_in_val)))


def review_missing_values():
  st.subheader("e- Missing Values:")
  imputation_method = data_state().imputation_method
  st.write(markdown_bold("Replace with:") + " " + imputation_method)
  data_state()._imputed_df2 = imputed_df()


def review_encoding():
  st.subheader("f- Non-numerical features encoding:")
  imputed_df2 = getattr(data_state(), '_imputed_df2', imputed_df())
  num_cols, non_num_cols = split_cols_numerical_and_non(imputed_df2)
  if len(non_num_cols)==0:
    st.markdown(markdown_bold("No non-numerical features"))
    return
  encoded_cols = cols_with_many_values(imputed_df2, non_num_cols)
  cols_to_drop = list(set(non_num_cols) - set(encoded_cols)) if encoded_cols else non_num_cols
  if len(cols_to_drop)>0:
    st.write(markdown_bold(", ".join(cols_to_drop)) + " will be dropped for having more than 20 value.")
  for col in encoded_cols:
    enc_method = data_state().encoding.get(col)
    st.write(markdown_bold(col) + ": " + str(enc_method))


def review_additional_configurations():
  st.subheader("g- Additionnal Configurations:")
  st.write(markdown_bold("Test sample size:") + " " + str(data_state().test_size * 100) + "%")
  st.write(markdown_bold("Apply Standard Scaler:") + " " + yes_or_no(data_state().with_scaler))
  st.write(markdown_bold("Apply PCA:") + " " + yes_or_no(data_state().with_pca))


def format_string_filter(val):
  return "' or '".join(val.split("/##/"))

def markdown_bold(str):
  return "**"+str+"**"

def yes_or_no(bl):
  return "Yes" if bl else "No"