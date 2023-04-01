import os
import nltk

operators = {'AND': '&', 'OR': '|', 'NOT': '!'}

"""Сохранение инвертированного списка"""
def save(__inverted_index):
    with open("output/inverted_index.txt", "w", encoding="utf-8") as f:
        for key, value in __inverted_index.items():
            f.write('%s - %s\n' % (key, value))

"""Создает инвертированный список на основе файлов из заданной директории"""
def make_inverted_index():
    __inverted_index = {}
    all_files = os.listdir('output/tokens')

    for (index, filename) in enumerate(all_files):
        input_file_path = 'output/tokens/' + filename
        with open(input_file_path, "r", encoding="utf-8") as file:
            index = filename.split('.')[0]
            text = file.read().split(' ')
            for word in text:
                try:
                    __inverted_index[word].add(index)
                except KeyError:
                    __inverted_index[word] = {index}

    return __inverted_index

"""Анализ ввода
    Результат - список списков с указанием приоритета логических операторов
    & = ! > |
    Внутренний список - (слово, инверсия)"""
def parse_input(input):
    tokens = nltk.word_tokenize(input)
    query_list = []
    boolean_operator = ''
    searched_expressions = list()
    for token in tokens:
        if token.lower() not in operators.values():
            if boolean_operator == operators['NOT']:
                negated = True
            else:
                negated = False
            query_list.append((token, negated))
        elif token.lower() == operators['OR']:
            boolean_operator = token.lower()
            searched_expressions.append(query_list)
            query_list = []
        else:
            boolean_operator = token.lower()
    searched_expressions.append(query_list)
    return searched_expressions

"""Пересечение и разность множеств"""
def evaluate_collection(collection):
    h = set()
    for i in range(100):
        h.add(str(i))

    result, negat = collection[0]
    if negat:
        result = h.difference(result)

    for file_list, negated in collection[1:]:
        if negated:
            result = result.difference(file_list)
        else:
            result = result.intersection(file_list)

    return result

"""Метод возвращает списки кортежей
    каждый кортеж, соответствующий искомому слову"""
def get_file_list(word_map, input_query):
    file_collection = []
    for word, to_find in input_query:
        word_id = word
        if word_id in word_map.keys():
            file_collection.append((word_map[word_id], to_find))
        else:
            file_collection.append(([], to_find))

    return file_collection


def search(input):
    __inverted_index = make_inverted_index()
    save(__inverted_index)
    searched_exp = parse_input(input)
    doc_id_list = []

    for expression in searched_exp:
        temp = get_file_list(__inverted_index, expression)
        doc_id_list.append(evaluate_collection(temp))

    union = doc_id_list[0]
    for item in doc_id_list[1:]:
        union = union.union(item)

    return sorted(union)


if __name__ == '__main__':
    exp = ['великолепный & особняк | сказка', 'великолепный | особняк | сказка', 'великолепный & !особняк | сказка', 'великолепный | !особняк | !сказка']
    for ind, query in enumerate(exp):
        result = search(query)
        file = open("output/inverted_index/inverted_index_search_{}.txt".format(ind), "w", encoding="utf-8")
        file.write(" ".join(str(item) for item in result))
        file.close()