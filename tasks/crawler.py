from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

"""Игнорирование элементов страницы"""
def ignore_tag(element):
    if (element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']) or isinstance(element, Comment):
        return False
    else:
        return True

"""Сохранение текста страницы в файл"""
def save(path, text):
    file = open(path, "w", encoding="utf-8")
    file.write(text)
    file.close()

class Crawler:
    def __init__(self, urls=[]):
        """
        :param urls: массив url-адресов веб-сайтов

        visited_urls : массив, посещенных страниц
        urls_to_visit : массив, страниц в очереди для посещения
        index : индекс страницы
        output : словарь, записанных страниц, ключ - индекс страницы, значение - адрес страницы
        """
        self.visited_urls = []
        self.urls_to_visit = urls
        self.index = 0
        self.output = dict()

    """Загрузить текст со страницы"""
    def download_url(self, url):
        try:
            return requests.get(url).text
        except Exception:
            return None

    """Получить все ссылки на текущей странице"""
    def get_linked_urls(self, soup, url):
        try:
            for link in soup.find_all('a'):
                path = link.get('href')
                if path and (path.startswith('/news') or path.startswith('/list')):
                    path = urljoin(url, path)
                    yield path
        except Exception:
            return None

    """Добавить страницу в очередь"""
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    """Обход страниц"""
    def crawl(self, url):
        html = self.download_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.find_all(text=True)
        visible_texts = list(filter(ignore_tag, texts))
        self.visited_urls.append(url)
        if len(visible_texts) >= 1000:
            text = u" ".join(t.strip() for t in visible_texts)
            save('{}/{}.txt'.format("output/text", self.index), text)
            self.output[self.index] = url
            self.index += 1
        for url in self.get_linked_urls(soup, url):
            self.add_url_to_visit(url)

    """Обход страниц из очереди
        Запись посещенных страниц в файл"""
    def run(self):
        while self.urls_to_visit and self.index < 100:
            url = self.urls_to_visit.pop()
            try:
                self.crawl(url)
            except Exception:
                print(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

        with open("output/index.txt", "w", encoding="utf-8") as f:
            for key, value in self.output.items():
                f.write('%s - %s\n' % (key, value))


if __name__ == '__main__':
    Crawler(urls=['https://journal.tinkoff.ru/list']).run()