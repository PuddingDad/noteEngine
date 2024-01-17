import streamlit as st
st.set_page_config(layout="wide")
from streamlit_ace import st_ace

from io import StringIO
import uuid #

from engine import *


st.header('Notes Engine')

schema = ini_schema()
ix = open_ix()


with st.expander("Note searcher", expanded=True):
    
    with ix.searcher() as s:
            docnums = s.document_numbers()
            keywords = [keyword for keyword, score in s.key_terms(docnums, "subgroup",numterms = 50)]
            st.write("Keywords for subgroup")
            st.text(keywords)
    
    ## Inputs
    factor = st.slider('factor scores', 0.0, 1.0, 0.05)
    option = st.selectbox('Field to parse',('title', 'group', 'subgroup', 'feature','content','comment','author'))
    query = st.text_input("Key words or phrase", "", help="Using AND, OR, ANDNOT, ANDMAYBE, and NOT for better matches.")
    og = qparser.OrGroup.factory(factor)
    ## Inputs
    
    ## Filter   
    q_f = st.selectbox('allowed field',
                       ('title', 'group', 'subgroup', 'feature','content','comment','author'))
    q_w = st.text_input("allowed keyword", value = "")
    q_allow = Term(q_f, q_w)        
    ## Filter
    
    ## Mask
    ## To-do
        
    ## commit
    if st.button('try!'):
        searcher = ix.searcher(weighting=scoring.TF_IDF())
        
        parser = qparser.QueryParser(option, ix.schema, group=og)
        parser.add_plugin(qparser.FuzzyTermPlugin())
        q = parser.parse(query)
        if len(q_w)>0:
            results = searcher.search(q,filter=q_allow)
        else:
            results = searcher.search(q)

        if len(results)==0:
            st.markdown("Try better key words, using hints!")
        else:
            
            for i in range(len(results[:10])):
                st.markdown(f"#### Result: {i+1}")
                st.markdown(f"##### Title: {results[i]['title']}")
                st.text(results[i]['path'])
                st.markdown(results[i]['content'],unsafe_allow_html=True)
                st.markdown(f"##### Comment: {results[i]['comment']}")
                st.divider()

        searcher.close()        
    ## commit

st.divider()

st.write("Note Modifier, passport required")
if check_password("modifier"):

    with st.expander("Note modifier"):
    
        st.markdown("""
        **1. Deleting Document:**
        
        ```python
        ix.delete_by_term('path', u'/a/b/c')
        ix.commit()
        ```
                
        **2. Updating Document:**
        
        ```python
        from whoosh.fields import Schema, ID, TEXT

        writer = ix.writer()
        # Because "path" is marked as unique, calling update_document with path="/a"
        # will delete any existing documents where the "path" field contains "/a".
        writer.update_document(path=u"/a", content="Replacement for the first document")
        writer.commit()
        ```     
    """)
    
        code = st_ace(language="python",
                  theme="tomorrow_night_bright",
                  keybinding="vscode",
                  font_size=14,
                  tab_size=4,
                  show_gutter=True,
                  min_lines=10,
                  key="ace")
        if code:
            redirected_output = sys.stdout = StringIO()
            try:
                exec(code)
                result = str(redirected_output.getvalue())
                st.code(result)
            except Exception as e:
                st.code(str(e))


st.divider()

st.write("Note Recorder, passport required")
if check_password("recorder"):
    with st.expander("Note recorder"):
    
        ## Inputs
        st.session_state['title'] = st.text_input('Title', 'Default')
        st.session_state['group'] = st.selectbox('Group',('Math', 'Music', 'Movie', 'Miscellaneous'))
        st.session_state['subgroup'] = st.text_input('Subgroup', '')
        st.session_state['feature'] = st.multiselect('feature',
                             ['Theory', 'Application', 'Proof', 'Algorithm', 'Solving', 
                              'Knowledge', 'Interesting', 'Writers', 'RocknRoll', 'Chinese', 
                              'A-level', 'OpenMind', 'Linkage', 'abstract', 'technique'])
        st.session_state['content'] = st.text_area("Content",'',height=30)
        st.session_state['comment'] = st.text_input('Comment', '')
        st.session_state['author'] = st.text_input('Author', '')
        ## Inputs
    
        ## commit
        if st.button('submit'):
            writer = ix.writer()
            writer.add_document(title=st.session_state['title'],
                            path = str(uuid.uuid1()),
                            group=st.session_state['group'], 
                            subgroup = st.session_state['subgroup'],
                            feature = st.session_state['feature'],
                            content = st.session_state['content'],
                            comment = st.session_state['comment'],
                            author = st.session_state['author'])
            writer.commit()
            st.write("Notes submitted!")
            st.markdown(content,unsafe_allow_html=True)
        else:
            st.markdown(content,unsafe_allow_html=True)
    ## commit
        


