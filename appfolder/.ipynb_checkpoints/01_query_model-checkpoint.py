#!/usr/bin/env python
# coding: utf-8

# # Inspiser en word2vec-modell
# 
# Installer gensim og test

# In[1]:

import streamlit as st
from gensim.models import KeyedVectors
#from gensim import model

# Last ned modellen og ta den inn i notebooken

# In[4]:

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title("Ordlikheter")
st.write("### med [Gensims](https://radimrehurek.com/gensim/) ordmodeller konstruert med data fra [dhlab](https://dh.nb.no)")


if 'model' not in st.session_state: 

    model_file = 'fifth_capital_ddc.model' # eller annet filnavn - pass på sti
    model = KeyedVectors.load(model_file)    #load_word2vec_format(model_file, binary=True)
    d = model.wv
    st.session_state['model'] = d
else:
    d = st.session_state['model']


st.session_state.update(st.session_state)
    
# Test med most_similar for forskjellige ord for evaluering.
word_col, anta_col = st.columns([5, 2])
if "words" not in st.session_state:
    st.session_state.words = 'hallo'
    
with word_col:
    words = st.text_input("Listen med ord blir koblet de som ligger nærmest i bruk", st.session_state.words, key="words")
    if ',' in words:
        words = [x.strip() for x in words.split(',')]
    else:
        words = words.split()
        
with anta_col:
    antall_ord = st.number_input("Antall nærliggende ord", min_value=1, max_value=30, value=10, key="antall_ord")

T = ""
for x in words:
    try:
        text = f"### {x} \n {', '.join([x[0] for x in d.most_similar(x, topn=antall_ord)])}\n\n"
    except:
        text = f"### {x} \n"
    T += text
    
st.markdown(T)
    

st.session_state.update()