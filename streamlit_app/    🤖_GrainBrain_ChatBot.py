import os
import sys
import streamlit as st
from streamlit_chat import message
import pyperclip

from langchain import PromptTemplate, LLMChain
from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import GPT4All
from langchain.vectorstores.faiss import FAISS

# setting path
sys.path.append('../utils')
import utils

FAISS_INDEX_FOLDER = '../data/articles_index_faiss'

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(script_dir)

@st.cache_resource
def initialize_model():
    gpt4all_path = '../models/gpt4all-converted.bin' 
    llama_path = '../models/ggml-model-q4_0.bin' 

    embeddings = LlamaCppEmbeddings(model_path=llama_path)
    llm = GPT4All(model=gpt4all_path, verbose=True)
    index = FAISS.load_local(FAISS_INDEX_FOLDER, embeddings)
    return llm, index


def get_formatted_answer_with_references(answer, references):
    str_references = "\n".join(list(set(map(lambda ref: f"* {os.path.splitext(str(os.path.basename(ref['metadata']['source'])))[0]}", references))))
    markdown = f"""### Answer\n{answer}\n### References\n{str_references}"""
    return markdown

def get_clipboard_string(answer, references):
    str_references = "\n".join(list(set(map(lambda ref: f"{os.path.splitext(str(os.path.basename(ref['metadata']['source'])))[0]}", references))))
    formatted_string = f"""Answer\n{answer}\n\nReferences\n{str_references}"""
    return formatted_string
    

def on_input_change():
    user_input = st.session_state.user_input
    
    # Set your query here manually
    matched_docs, sources = utils.similarity_search(user_input, index)

    template = """
    Please use the following context to answer questions.
    Context: {context}
    ---
    Question: {user_input}
    Answer: Let's think step by step."""

    context = "\n".join([doc.page_content for doc in matched_docs])
    prompt = PromptTemplate(template=template, input_variables=["context", "user_input"]).partial(context=context)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    st.session_state.past.append(user_input)
    answer = llm_chain.run(user_input)
    str_formatted_response = get_formatted_answer_with_references(answer, sources)
    st.session_state.last_answer = get_clipboard_string(answer, sources)
    
    str_prompt_debug = f"""
    Please use the following context to answer questions.
    Context: {context}
    ---
    Question: {user_input}
    Answer: Let's think step by step."""
    
    st.session_state.prompt_debug = str_prompt_debug
    
    st.session_state.generated.append({'type': 'normal', 'data': f'{str_formatted_response}'})
    st.session_state.user_input = ''
    

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


# Initialization
st.set_page_config(page_title='GrainBrain ChatBot', page_icon="🤖", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.session_state.setdefault(
    'past', 
    []
)
st.session_state.setdefault(
    'generated', 
    []
)

st.session_state.setdefault(
    'similarity_count', 4
)

st.title("GrainBrain Chatbot")

with st.sidebar:
    st.sidebar.header("GrainBrain Chatbot")
    with st.spinner("Loading LLM and vectorstore index..."):
        llm, index = initialize_model()
    st.success("LLM and vectorstore index loaded successfully!")
    
    st.session_state['similarity_count'] = int(st.text_input("Number of top-matching references to take into account:", key="input_similarity_count", value=st.session_state['similarity_count']))

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)
    if 'prompt_debug' in st.session_state:
        with st.expander("See the prompt"):
            st.text(st.session_state.prompt_debug)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")
    if 'last_answer' in st.session_state:
        if st.button("Copy answer to clipboard"):
            pyperclip.copy(st.session_state.last_answer)
            st.success("Answer copied to clipboard!")