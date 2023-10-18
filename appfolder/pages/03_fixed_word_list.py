#!/usr/bin/env python
# coding: utf-8

# # Inspiser en word2vec-modell
# 
# Installer gensim og test

# In[1]:

import streamlit as st
from gensim.models import KeyedVectors
import pandas as pd
#from gensim import model

# Last ned modellen og ta den inn i notebooken

# In[4]:

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.session_state.update(st.session_state)

st.title("Ordlikheter")
st.write("### med [Gensims](https://radimrehurek.com/gensim/) ordmodeller konstruert med data fra [dhlab](https://dh.nb.no)")

if 'model' not in st.session_state: 
    st.write(st.session_state)
    model_file = 'fifth_capital_ddc.model' # eller annet filnavn - pass på sti
    model = KeyedVectors.load(model_file)    #load_word2vec_format(model_file, binary=True)
    d = model.wv
    st.session_state['model'] = d
else:
    d = st.session_state['model']


def check(word, list_of_words):
    def test(x,y):
        try:
            return d.rank(x,y)
        except:
            return 1000000
    res = {w: test(word, w) for w in list_of_words}
    return pd.DataFrame.from_dict(res, orient='index', columns=[word]).sort_values(by=word)

def mcheck(these_words, list_of_words):
    res = pd.concat([check(w, list_of_words) for w in these_words], axis = 1)
    res = res.astype(int)
    return res
    
# Test med most_similar for forskjellige ord for evaluering.
word_col, word_list_col = st.columns([2, 5])

if "ordliste" not in st.session_state:
    st.session_state.ordliste = "første"
if "sjekkliste" not in st.session_state:
    st.session_state.sjekkliste = "sjekk"
    
with word_col:
    words = st.text_input("Ordene som skrives her sammenlignes med de i den andre listen", st.session_state.ordliste,key="ordliste")
    if ',' in words:
        words = [x.strip() for x in words.split(',')]
    else:
        words = words.split()
        

with word_list_col:
    word_list = st.text_input("Sjekk ordene her med de i den første listen", "", key="sjekkliste")
    if ',' in words:
        word_list = [x.strip() for x in word_list.split(',')]
    else:
        words_list = word_list.split()

if words != [] and words_list != []:
    T = mcheck(words, words_list)
    
    st.dataframe(T)
    
st.session_state.update()
