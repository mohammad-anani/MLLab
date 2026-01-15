import streamlit as st

class DataState:
    def __getattr__(self, key):
        try:
            return st.session_state.data[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        st.session_state.data[key] = value

    def __getitem__(self, key):
        return st.session_state.data[key]

    def __setitem__(self, key, value):
        st.session_state.data[key] = value

    def __contains__(self, key):
        return key in st.session_state.data
    
    def get(self, key, default=None):
        return st.session_state.data.get(key, default)

def data_state():
  return DataState()