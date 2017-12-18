import requests, time, json
from bs4 import BeautifulSoup
from .document import Document

url = 'http://lapor.go.id/beranda'

class Crawler:
    def __init__(self, url=url):
        self.url = url
        self.id_kategori = []
        self.document = []

    def gather_id_category(self):
        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        for option in soup.findAll('option'):
            self.id_kategori.append(option['value'])

    def make_corpus(self):
        stream="0"
        #file = open('corpus.txt','a', encoding="utf-8") #write in a file
        for _ in range(2):
            url_stream = 'http://lapor.go.id/home/streams/{}/{}/old/beranda'.format(stream,self.id_kategori[0])
            try:
                stat = requests.get(url_stream, verify=True)
                stat.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Error {} on parameter {}".format(e, stream))
            except requests.exceptions.RequestException as ee:
                print("Error {} on parameter {}".format(ee, stream))
            except requests.exceptions.ConnectionError as er:
                print("Error {} on parameter {}".format(er, stream))
            except requests.exceptions.Timeout as err:
                print("Error {} on parameter {}".format(err, stream))
            except TimeoutError as te:
                print("Timeout on parameter {}".format(stream))
            data = json.loads(stat.text)
            if len(data) == 0:
                stream="0"
                break
            for d in range(len(data)):
                doc = Document(data[d]['nid'],data[d]['subject'],data[d]['content']) #making object
                self.document.append(doc)
                #file.write("{}\n".format(data[d]['nid']))
                #file.write("{}\n".format(data[d]['subject']))
                #file.write("{}\n\n".format(data[d]['content']))
            stream=data[len(data)-1]['last_activity']
            #print("{}".format(stream)) #check which param is in request

        #file.close()

    def get_document(self):
        if self.document == []:
            try:
                corpus = open('corpus.txt', 'r', encoding="utf-8")
                lines = corpus.readlines()
                number = ""
                title = ""
                text = ""
                is_text = 0
                for l in lines[:10339]:
                    if l == "\n":
                        doc = Document(number, title, text)
                        self.document.append(doc)
                        is_text = 0
                    elif is_text == 0:
                        number = l
                        is_text += 1
                    elif is_text == 1:
                        title = l
                        is_text += 1
                    elif is_text == 2:
                        text += l
            except FileNotFoundError:
                self.make_corpus()
        gc.collect()
        return self.document

# c = Crawler()
# c.gather_id_category()
# c.get_document()
