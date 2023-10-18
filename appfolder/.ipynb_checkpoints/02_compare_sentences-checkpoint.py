#!/usr/bin/env python
# coding: utf-8

# # Inspiser en word2vec-modell
# 
# Installer gensim og test

# In[1]:
import numpy as np
import streamlit as st
from gensim.models import KeyedVectors
from dhlab.nbtokenizer import tokenize

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


#from gensim import model

# Last ned modellen og ta den inn i notebooken

# In[4]:

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.session_state.update()

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



# Test med most_similar for forskjellige ord for evaluering.
sentence_col, cluster_num_col = st.columns([5, 2])

with sentence_col:
    sentences = st.text_area("Angi noen setninger eller små tekster skilt med retur (ny linje)", "", key="text")
    sentences = sentences.split('\n')

with cluster_num_col:
    cluster_num = st.number_input("Hvor mange clustre?", min_value=2, max_value=20, value=5, key="cluster_num")




# Load model

def sentence_vector(sentence, model):
    """
    Compute the average vector of a sentence based on word vectors from the model.
    """
    words = [word for word in sentence.split() if word in model.key_to_index]
    if len(words) == 0:
        return np.zeros(model.vector_size)
    return np.mean([model[word] for word in words], axis=0)

def cluster_sentences(sentences, model, num_clusters=2):
    """
    Cluster sentences based on their average vector representations.
    """
    # Compute average vectors for each sentence
    sentence_vectors = [sentence_vector(sentence, model) for sentence in sentences]
    
    # Use KMeans clustering (here, you might want to find the best number of clusters for your data)
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_assignments = kmeans.fit_predict(sentence_vectors)
    
    # Group sentences by their assigned cluster
    clusters = {}
    for i, cluster_id in enumerate(cluster_assignments):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(sentences[i])

    return clusters

### Graph method

# 1. Represent sentences as nodes
G = nx.Graph()

# Adding nodes
for i, sentence in enumerate(sentences):
    G.add_node(i, sentence=sentence)

# 2. Compute cosine similarities and add edges
sentence_vectors = [sentence_vector(sentence, d) for sentence in sentences]
cosine_matrix = cosine_similarity(sentence_vectors)

# Only add edges above a certain threshold if you want to reduce connections
threshold = 0.5 
for i in range(len(sentences)):
    for j in range(len(sentences)):
        if i != j and cosine_matrix[i][j] > threshold:
            G.add_edge(i, j, weight=cosine_matrix[i][j])

# 3. Apply Louvain algorithm
partition = community_louvain.best_partition(G)

# Display clusters
clusters = {}
for node, cluster_id in partition.items():
    if cluster_id not in clusters:
        clusters[cluster_id] = []
    clusters[cluster_id].append(sentences[node])

for cluster_id, cluster_sentences in clusters.items():
    st.write(f"Cluster {cluster_id}:")
    for sentence in cluster_sentences:
        st.write(f" - {sentence}")
 

st.session_state.update()
