import streamlit as st
from util.nextButton import nextButton
from util.dataFrame import dataFrame
from routes.dataRoutes.target import get_choosing_messages
from routes.dataRoutes.drop import removed_cols_df
from routes.dataRoutes.filter import split_cols_numerical_and_non
from routes.dataRoutes.impute import imputed_df
from routes.dataRoutes.encode import cols_with_many_values


def reviewPage():

  st.subheader("8- Review")

  st.subheader("a- Initial dataset:")
  df=st.session_state.df
  dataFrame(df)

  st.subheader("b- Target:")
  label=st.session_state.label
  is_regression=st.session_state.is_regression



  st.write("**Name:** "+label)
  st.write("**Type:** "+('Regression' if is_regression else 'Classification'))
  if not is_regression:
    choice=get_choosing_messages(df,label)[st.session_state.choice]
    st.write("**Encoding choice:** "+choice)

  st.subheader("c- Removed features:")
  cols_to_remove=st.session_state.cols_to_remove

  if len(cols_to_remove)>0:
    st.write(", ".join(cols_to_remove))
  else:
    st.write("No removed features.")

  st.subheader("d- Filters:")
  remove_outliers=st.session_state.remove_outliers
  remove_singleval_col=st.session_state.remove_singleval_col

  filters=st.session_state.filter

  if len(filters)==0:
    st.write("**No Filters**")
  else:
    removed_cols_df2=removed_cols_df()
    num_cols,non_num_cols=split_cols_numerical_and_non(removed_cols_df2)
    for col in num_cols:
      min_key='min '+col
      min_val=st.session_state.filter[min_key] if min_key in st.session_state.filter else None
      max_key='max '+col
      max_val=st.session_state.filter[max_key] if max_key in st.session_state.filter else None

      if min_val and max_val:
        st.write(f"**{col}** between **{min_val}** and **{max_val}**")
      elif min_val:
        st.write(f"**{col}** more than **{min_val}**")
      elif max_val:
        st.write(f"**{col}** less than **{max_val}**")

    for col in non_num_cols:
      in_key='in '+col
      in_val=st.session_state.filter[in_key] if in_key in st.session_state.filter else None
      not_in_key='not in '+col
      not_in_val=st.session_state.filter[not_in_key] if not_in_key in st.session_state.filter else None

      if in_val and not_in_val:
        st.write(f"**{col}** should contain '**{format_string_filter(in_val)}**' and shouldn't contain '**{format_string_filter(not_in_val)}**'")
      elif in_val:
        st.write(f"**{col}** should contain '**{format_string_filter(in_val)}**'")
      elif not_in_val:
        st.write(f"**{col}** shouldn't contain '**{format_string_filter(not_in_val)}**'")


  st.write("**Remove outliers:** "+("Yes" if remove_outliers else "No"))
  st.write("**Remove single value features:** " + ("Yes" if remove_singleval_col else "No"))


  st.subheader("e- Missing Values:")
  imputation_method=st.session_state.imputation_method

  st.write("**Replace with:** "+imputation_method)
  imputed_df2=imputed_df()
  st.subheader("f- Non-numerical features encoding:")
  num_cols,non_num_cols=split_cols_numerical_and_non(imputed_df2)

  if len(non_num_cols)==0:
    st.markdown("**No non-numerical features**")
  else:
    encoded_cols=cols_with_many_values(imputed_df2,non_num_cols)

    cols_to_drop = list(set(non_num_cols) - set(encoded_cols)) if encoded_cols else non_num_cols

    if cols_to_drop:
      st.write("**"+", ".join(cols_to_drop) +"** will be dropped for having more than 20 value.")

    for col in encoded_cols:
      enc_method=st.session_state.encoding[col] if col in st.session_state.encoding else None

      st.write(f"**{col}**: "+ str(enc_method))




  st.subheader("g- Additionnal Configurations:")
  test_size=st.session_state.test_size
  with_scaler=st.session_state.with_scaler
  with_pca=st.session_state.with_pca
  st.write("**Test sample size:** "+str(test_size*100)+"%")
  st.write("**Apply Standard Scaler:** "+("Yes" if with_scaler else "No"))
  st.write("**Apply PCA:** "+("Yes" if with_pca else "No"))



  nextButton()



def format_string_filter(val):
  return "' or '".join(val.split("/##/"))