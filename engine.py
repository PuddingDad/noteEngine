from whoosh.fields import *
from whoosh import qparser
#from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh import scoring
from whoosh.query import Term

import streamlit as st


def ini_schema():
    schema = Schema(
        title=TEXT(stored=True),
        path=ID(stored=True, unique=True),
        group=ID(stored=True), 
        subgroup=ID(stored=True),
        feature=KEYWORD(stored=True, scorable=True),
        content=TEXT(stored=True),
        comment=TEXT(stored=True),
        author=TEXT(stored=True)
    )
    return schema

def ini_ix(schema):
    ix = index.create_in("note_engine", schema)
    return ix

def open_ix():
    ix = index.open_dir("note_engine")
    return ix

def check_password(key):
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state[key] == "Betty2009_":
            st.session_state["password_correct"] = True
            del st.session_state[key]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key=key
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key=key
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True
    
    
  
