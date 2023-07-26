import os


def similarity_search(query, index, k=4):
    matched_docs = index.similarity_search(query, k=k)
    sources = []
    for doc in matched_docs:
        sources.append(
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            }
        )

    return matched_docs, sources

def list_subfolders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

def get_article_titles(folders):
    return list(set(map(lambda path: os.path.splitext(str(os.path.basename(path)))[0], folders)))