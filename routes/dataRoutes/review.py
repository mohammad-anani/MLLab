import streamlit as st

from util.nextButton import nextButton

from util.dataFrame import dataFrame

from routes.dataRoutes.target import get_choosing_messages

from routes.dataRoutes.drop import removed_cols_df

from routes.dataRoutes.filter import split_cols_numerical_and_non

from routes.dataRoutes.impute import imputed_df

from routes.dataRoutes.encode import cols_with_few_values

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

  nextButton()




def review_initial_dataset():

  st.subheader("a- Initial dataset:")

  dataFrame(data_state().df)



def review_target():

  ds = data_state() 

  st.subheader("b- Target:")

  st.write(markdown_bold("Name:") + " " + ds.label)

  st.write(markdown_bold("Type:") + " " + ('Regression' if ds.is_regression else 'Classification'))


  if not ds.is_regression and 'choice' in ds:

    choice_text = get_choosing_messages(ds.df, ds.label)[ds.choice]

    st.write(markdown_bold("Encoding choice:") + " " + choice_text)



def review_removed_features():

  ds = data_state()

  st.subheader("c- Removed features:")

  st.write(", ".join(ds.cols_to_remove) if ds.cols_to_remove else "No removed features.")



def review_filters():

  ds = data_state()

  st.subheader("d- Filters:")

  _display_filters()

  st.write(markdown_bold("Remove outliers:") + " " + yes_or_no(ds.remove_outliers))

  st.write(markdown_bold("Remove single value features:") + " " + yes_or_no(ds.remove_singleval_col))



def _display_filters():

  ds = data_state()

  filters = ds.filter

  if not filters:

    st.write(markdown_bold("No Filters"))
    return


  df = removed_cols_df()

  num_cols, non_num_cols = split_cols_numerical_and_non(df)

  _display_numeric_filters(num_cols)

  _display_non_numeric_filters(non_num_cols)



def _display_numeric_filters(num_cols):

  ds = data_state()

  for col in num_cols:

    min_val = ds.filter.get('min ' + col)

    max_val = ds.filter.get('max ' + col)

    if min_val is not None and max_val is not None:

      st.write(markdown_bold(col) + f" between {markdown_bold(str(min_val))} and {markdown_bold(str(max_val))}")

    elif min_val is not None:

      st.write(markdown_bold(col) + f" more than {markdown_bold(str(min_val))}")

    elif max_val is not None:

      st.write(markdown_bold(col) + f" less than {markdown_bold(str(max_val))}")



def _display_non_numeric_filters(non_num_cols):

  ds = data_state()

  for col in non_num_cols:

    in_val = ds.filter.get('in ' + col)

    not_in_val = ds.filter.get('not in ' + col)

    if in_val and not_in_val:
      st.write(

        markdown_bold(col) + " should contain " + markdown_bold(format_string_filter(in_val)) +

        " and shouldn't contain " + markdown_bold(format_string_filter(not_in_val))
      )

    elif in_val:

      st.write(markdown_bold(col) + " should contain " + markdown_bold(format_string_filter(in_val)))

    elif not_in_val:

      st.write(markdown_bold(col) + " shouldn't contain " + markdown_bold(format_string_filter(not_in_val)))



def review_missing_values():

  ds = data_state()

  st.subheader("e- Missing Values:")

  st.write(markdown_bold("Replace with:") + " " + ds.imputation_method)

  ds._imputed_df2 = imputed_df()



def review_encoding():

  ds = data_state()

  st.subheader("f- Non-numerical features encoding:")


  imputed_df2 = getattr(ds, '_imputed_df2', imputed_df())

  num_cols, non_num_cols = split_cols_numerical_and_non(imputed_df2)


  if len(non_num_cols) == 0:

    st.markdown(markdown_bold("No non-numerical features"))
    return


  encoded_cols = cols_with_few_values(imputed_df2, non_num_cols)

  cols_to_drop = list(set(non_num_cols) - set(encoded_cols)) if encoded_cols else non_num_cols


  if cols_to_drop:

    st.write(markdown_bold(", ".join(cols_to_drop)) + " will be dropped for having more than 20 values.")


  for col in encoded_cols:

    enc_method = ds.encoding.get(col)

    c1, c2 = st.columns([1, 4])

    with c1:

      st.write(markdown_bold(col + ":"))

    with c2:

      st.write(enc_method)

      if enc_method == 'Ordinal':

        order = ds.encoding_order[col]

        st.write(markdown_bold("Order:") + " " + ", ".join(order))



def review_additional_configurations():

  ds = data_state()

  st.subheader("g- Additional Configurations:")

  st.write(markdown_bold("Test sample size:") + f" {ds.test_size * 100}%")

  st.write(markdown_bold("Apply Standard Scaler:") + " " + yes_or_no(ds.with_scaler))

  st.write(markdown_bold("Apply PCA:") + " " + yes_or_no(ds.with_pca))



def format_string_filter(val):

  return "' or '".join(val.split("/##/"))



def markdown_bold(text):

  return f"**{text}**"



def yes_or_no(bl):

  return "Yes" if bl else "No"

