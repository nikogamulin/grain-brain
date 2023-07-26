import os
import sys
import streamlit as st
import time
import numpy as np
from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict

# setting path
sys.path.append('../utils')
import utils

FAISS_INDICES_FOLDER = '../data/articles_indices_faiss'
PDF_ARTICLES_FOLDER = '../data/raw/articles'
TXT_ARTICLES_FOLDER = '../data/raw/articles_txt'

def read_pdf(file_path):
    elements = partition(file_path)
    return elements

st.set_page_config(page_title="Bibliography", page_icon="📚")

indices = utils.list_subfolders(FAISS_INDICES_FOLDER)
article_titles = list(set(indices))
article_titles.sort()

markdow_bibliography = "\n".join(list(map(lambda title: f"* {title}", article_titles)))


st.markdown("# Bibliography")
st.sidebar.header("Bibliography")
st.sidebar.markdown(f"This is a list of all the articles ({len(article_titles)} total) that are currently available in the database.")
st.sidebar.markdown("""---""")
st.sidebar.markdown("## Upload new articles")
uploaded_files = st.sidebar.file_uploader("Choose a PDF files", accept_multiple_files=True, type="pdf")
with st.spinner(text='Uploading files...'):
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.sidebar.write("filename:", uploaded_file.name)
        # st.sidebar.write(bytes_data)
        pdf_file_path = os.path.join(PDF_ARTICLES_FOLDER, uploaded_file.name)
        txt_file_path = os.path.join(TXT_ARTICLES_FOLDER, uploaded_file.name.replace('.pdf', '.txt'))
        with open(pdf_file_path, 'wb') as f:
            f.write(bytes_data)
        elements = read_pdf(os.path.join(PDF_ARTICLES_FOLDER, uploaded_file.name))
        elements_dict = convert_to_dict(elements)
        article_txt = "\n\n".join([str(el) for el in elements])         
        with open(txt_file_path, 'w') as f:
            f.write(article_txt)
        st.sidebar.success("File uploaded successfully!")
        
txt_files = os.listdir(TXT_ARTICLES_FOLDER)
article_titles_txt = list(set(map(lambda path: os.path.splitext(str(os.path.basename(path)))[0], txt_files)))
unprocessed_articles = list(set(article_titles_txt) - set(article_titles))
if len(unprocessed_articles) > 0:
    str_unprocessed_articles = "\n".join(list(map(lambda title: f"* {title}", unprocessed_articles)))
    st.sidebar.markdown("## Unprocessed articles")
    st.sidebar.markdown(str_unprocessed_articles)
st.markdown(markdow_bibliography)
