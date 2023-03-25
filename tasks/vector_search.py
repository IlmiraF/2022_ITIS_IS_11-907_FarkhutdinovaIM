import os
from sklearn.metrics.pairwise import cosine_similarity
from tf_idf import tf_idf_calculation, calculate
import operator
from tokenizer import tokens

def search(query):
    exp = tokens(query)

    if len(exp) == 0:
        print("Empty query")
        return

    all_filenames = os.listdir('output/tokens')
    query_vector = []
    temp = calculate()

    for token in exp:
        doc_with_terms_count = len(temp[token])
        _, _, tf_idf = tf_idf_calculation(token, exp, len(all_filenames), doc_with_terms_count)
        query_vector.append(tf_idf)

    d = {}
    with open("output/index.txt", "r", encoding="utf-8") as f:
        for line in f:
            (key, val) = line.strip().split(" - ")
            d[key] = val

    distances = {}

    for index in d.keys():
        document_vector = []

        for token in exp:
            try:
                tf_idf = temp[token][index]["TF-IDF"]
                document_vector.append(tf_idf)
            except KeyError:
                document_vector.append(0.0)

        distances[index] = cosine_similarity([query_vector], [document_vector])[0][0]

    searched_indices = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)

    for index in searched_indices:
        doc_id, tf_idf = index

        if tf_idf < 0.05:
            continue

        url = d[doc_id]
        print("Index: {}\nURL:{}\nCosine:{}\n".format(doc_id, url, tf_idf))

if __name__ == '__main__':
    search('Удачный крепкий брак')