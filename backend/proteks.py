import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from crawler.crawler import Crawler

class TextProcessor:
    def __init__(self):
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

    def levenshtein_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def stem_word(self, s1):
        # remove double character
        s1 = self.clean_word(s1)
        s1 = self.remove_double_character(s1)

        # stemming process
        output   = self.stemmer.stem(s1)
        return output

    def remove_double_character(self, s1):
        s1_ = re.sub(r'([^gnk])\1+', r'\1', s1)
        return s1_

    def clean_word(self, s1):
        s1_ = re.sub(r'(<br />|<br>)', '', s1 )
        return s1_

tp = TextProcessor()
c = Crawler()
documents = c.get_document()
for d in documents:
    d.title = tp.stem_word(d.title)
    d.text = tp.stem_word(d.text)
    print("Judul: {}\nTeks: {}".format(d.title, d.text))