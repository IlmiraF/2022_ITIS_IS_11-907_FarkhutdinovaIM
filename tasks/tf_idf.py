import math
import os
from inverted_index import make_inverted_index

def calculate():
    all_filenames = os.listdir('output/tokens')

    __inverted_index = make_inverted_index()
    result = {}

    for term in __inverted_index.keys():
        docs_with_term = __inverted_index[term]
        for doc_index in docs_with_term:
            lem_file_path = "output/tokens/" + doc_index + ".txt"

            with open(lem_file_path, "r", encoding="utf-8") as file:
                tokens = file.read().split(' ')

            TF, IDF, TF_IDF = tf_idf_calculation(term, tokens, len(all_filenames), len(docs_with_term))

            try:
                result[term][doc_index] = {"TF": TF, "IDF": IDF, "TF-IDF": TF_IDF}
            except KeyError:
                result[term] = {doc_index: {"TF": TF, "IDF": IDF, "TF-IDF": TF_IDF}}

    with open("output/tf_idf.txt", "w", encoding="utf-8") as f:
        for key, value in result.items():
            f.write('%s - %s\n' % (key, value))

    return result

def tf_idf_calculation(term, document_tokens_list, documents_count, documents_with_term_count):
    TF = document_tokens_list.count(term) / len(document_tokens_list)
    IDF = math.log(documents_count / documents_with_term_count)

    return round(TF, 6), round(IDF, 6), round(TF * IDF, 6)

if __name__ == '__main__':
    calculate()