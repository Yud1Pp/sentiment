import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import streamlit as st
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi stopword remover dan stemmer
stopword_remover = StopWordRemoverFactory()
stopwords = stopword_remover.get_stop_words()
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def preprocess_text(text_series):
    """
    Preprocessing teks: menghapus stopwords, stemming, dan membersihkan teks.
    """
    # Hilangkan NA, ubah ke lowercase, dan hapus karakter khusus
    cleaned_text = text_series.dropna().str.lower().apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))
    
    # Hapus stopwords dan lakukan stemming
    cleaned_text = cleaned_text.apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split() if word not in stopwords]))
    
    return cleaned_text

def perform_lda(texts, num_topics=5, num_words=10):
    """
    Melakukan Latent Dirichlet Allocation (LDA) untuk mengidentifikasi topik dari teks.
    """
    # Vektorisasi teks
    vectorizer = CountVectorizer(stop_words=stopwords)
    dtm = vectorizer.fit_transform(texts)
    
    # LDA model
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(dtm)

    # Ambil kata-kata teratas untuk tiap topik
    terms = vectorizer.get_feature_names_out()
    topics = []
    for idx, topic in enumerate(lda_model.components_):
        top_words = [terms[i] for i in topic.argsort()[-num_words:]]
        topics.append((f"Topik {idx+1}", top_words))
    
    return topics

def display_topics(topics):
    """
    Menampilkan topik-topik yang ditemukan oleh LDA
    """
    st.markdown("### 🔍 Topik LDA dari Komentar")
    for topic_name, words in topics:
        st.markdown(f"**{topic_name}**: {', '.join(words)}")
