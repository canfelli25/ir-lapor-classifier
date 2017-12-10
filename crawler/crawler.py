import requests, time
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
        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data)
        for option in soup.findAll('option'):
            self.id_kategori.append(option['value'])

    def make_corpus(self):
        stream="1488764654"
        count = 0
        file = open('corpus.txt','a') #write in a file
        while True:
            if count == 30:
                time.sleep(30)
                count = 0
            url_stream = 'http://lapor.go.id/home/streams/{}/{}/old/beranda'.format(stream,self.id_kategori[0])
            stat = requests.get(url_stream, verify=True)
            try:
                stat.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Timeout on parameter {}".format(stream))
            raw = stat.text
            data = json.loads(raw)
            if len(data) == 0:
                stream="0"
                break
            for d in range(len(data)):
                #doc = Document(data[d]['nid'],data[d]['subject'],data[d]['content']) #making object
                #self.document.append(doc)
                file.write("{}\n".format(data[d]['nid']))
                file.write("{}\n".format(data[d]['subject']))
                file.write("{}\n\n".format(data[d]['content']))
            stream=data[len(data)-1]['last_activity']
            count += 1
            print("{}".format(stream)) #check berhenti sampai mana

        file.close()

    def get_document(self):
        return self.document

c = Crawler()
c.gather_id_category()
c.make_corpus()
