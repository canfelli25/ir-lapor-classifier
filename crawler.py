import requests
import json
from bs4 import BeautifulSoup
from document import Document

url = 'http://lapor.go.id/beranda'

class Crawler:
    def __init__(self, url=url):
        self.url = url
        self.id_kategori = []
        self.document = []

    def gather_id_category(self):
        soup = BeautifulSoup(self.url)
        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data)
        for option in soup.findAll('option'):
            self.id_kategori.append(option['value'])

    def make_corpus(self):
        stream="0"
        #file = open('corpus.txt','w') #write in a file
        for cat in range(len(self.id_kategori)):
            while True:
                url_stream = 'https://lapor.go.id/home/streams/{}/{}/old/beranda'.format(stream,id_kategori[cat])
                raw = requests.get(url_stream).text
                data = json.loads(raw)
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
                #print(stream) #check berhenti sampai mana
        #file.close()

    def get_document(self):
        return self.document

#gather_id_category(url)
