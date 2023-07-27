GrainBrain
=====================

Overview
--------

GrainBrain is a chatbot project designed to provide answers based on scientific articles. It uses a mix of advanced NLP techniques and AI models to process, understand, and retrieve information from a variety of text documents. The project uses several technologies, including Streamlit for the user interface, gpt4all for language model, the LangChain framework for text processing, and FAISS for vector storage.

Getting Started
---------------

1.  **Clone the repository**:
    
    `git clone https://github.com/nikogamulin/grain-brain`
    
2.  **Download model files**: The model files can be downloaded from the provided link. After downloading, place the [model files](https://drive.google.com/drive/folders/1y3Ry94OHcu3V_hD2Y22Z_5K4IO9S27yV?usp=sharing) into the `models` folder in your local clone of the repository.
    
3.  **Install Dependencies**: Install all the required dependencies for the project. It is recommended to create a virtual environment first.
    
    ``python -m venv env source env/bin/activate  # On Windows use `env\Scripts\activate` pip install -r requirements.txt``
    

Usage
-----

1.  **Add your data**: Put your PDF documents (articles or other body of knowledge) into the `data/raw/articles` folder.
    
2.  **Parse the articles**: Run `articles_pdf_parser.py` to transform the articles into `.txt` files.
    
    `python articles_pdf_parser.py`
    
    This will create text files from your PDFs and store them in `data/raw/articles_txt`.
    
3.  **Build FAISS vector store**: After generating text files, run `faiss_vectorstore_builder.py` to create the index.
    
    `python faiss_vectorstore_builder.py`
    
4.  **Run the application**: After the index has been built, run the Streamlit application.
    
    `streamlit run app.py`
    

Notes
-----

Please note that index files are not included due to article sharing restrictions.

Contributing
------------

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

Links
-----

*   [Model Files](https://drive.google.com/drive/folders/1y3Ry94OHcu3V_hD2Y22Z_5K4IO9S27yV?usp=sharing)
*   Blog Post

Licensing
---------

The code in this project is licensed under MIT license.

