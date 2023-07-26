import os
from tqdm import tqdm
from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(os.path.join(script_dir, '..'))

ARTICLES_FOLDER = 'data/raw/articles'
ARTICLES_TXT_FOLDER = 'data/raw/articles_txt'

if not os.path.exists(ARTICLES_TXT_FOLDER):
    # Create folder if it doesn't exist
    os.makedirs(ARTICLES_TXT_FOLDER)


def list_files(folder_path, extension):
    files = [file for file in os.listdir(
        folder_path) if file.endswith(f'.{extension}')]
    return files


def read_pdf(file_path):
    elements = partition(file_path)
    return elements

if __name__ == '__main__':
    pdf_files = list_files(ARTICLES_FOLDER, 'pdf')
    processed_files = list_files(ARTICLES_TXT_FOLDER, 'txt')
    with tqdm(total=len(pdf_files)) as pbar:
        for pdf_file in pdf_files:
            txt_file = pdf_file.replace('.pdf', '.txt')
            if txt_file not in processed_files:
                # print(f'Parsing {pdf_file}...')
                elements = read_pdf(os.path.join(ARTICLES_FOLDER, pdf_file))
                elements_dict = convert_to_dict(elements)
                article_txt = "\n\n".join([str(el) for el in elements])
                
                with open(os.path.join(ARTICLES_TXT_FOLDER, txt_file), 'w') as f:
                    f.write(article_txt)
            pbar.update(1)


