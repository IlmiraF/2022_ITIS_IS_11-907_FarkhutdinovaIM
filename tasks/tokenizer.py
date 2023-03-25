import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
import pymorphy2
lemma = pymorphy2.MorphAnalyzer()
import os
import re

"""Сохранить текст в файл"""
def save(path, text):
    file = open(path, "w", encoding="utf-8")
    file.write(text)
    file.close()

"""Токенизация, лемматизация, удаление лишних символов"""
def tokens(text):
    tokens1 = nltk.word_tokenize(text)
    tokens2 = [lemma.parse(word)[0].normal_form for word in tokens1]
    tokens3 = [re.sub(r"\W", "", token, flags=re.I) for token in tokens2]

    stop_words = stopwords.words('russian')
    only_cyrillic_letters = re.compile('[а-яА-Я]')

    tokens3 = [token.lower() for token in tokens3 if (token not in stop_words)
               and only_cyrillic_letters.match(token)
               and not token.isdigit()
               and token != '']
    return tokens3

if __name__ == '__main__':
    all_files = os.listdir('output/text/')
    for file_name in all_files:
        input = 'output/text/' + file_name
        with open(input, "r", encoding="utf-8") as file:
            text = file.read()
            token = tokens(text)
            save('output/tokens/{}'.format(file_name), ' '.join(token))