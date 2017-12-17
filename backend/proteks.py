import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from crawler.crawler import Crawler
from crawler.document import Document

ADDED_STOPWORDS = ["saya", "yth", "yg", "terima", "kasih", "mohon", "ditindaklanjuti", "pak"]

class TextProcessor:
    def __init__(self):
        self.stemmer_factory = StemmerFactory()
        self.remover_factory = StopWordRemoverFactory()
        self.stopword = self.remover_factory.create_stop_word_remover()
        self.stemmer = self.stemmer_factory.create_stemmer()

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

    def clean_word(self, d):
        d.title = self._clean_word(d.getTitle())
        d.text = self._clean_word(d.getText())
        return d
    
    def _clean_word(self, s1):
        # remove double character
        s1 = self.clean_format(s1)
        s1 = self.remove_double_character(s1)

        # stemming process
        s1   = self.stemmer.stem(s1)
        s1 = self.stopword.remove(s1)

        for w in ADDED_STOPWORDS:
            s1 = s1.replace(w, "")

        s1 = self.find_bigrams(s1)
        return s1

    def remove_double_character(self, s1):
        s1_ = re.sub(r'([^gnk])\1+', r'\1', s1)
        s1_ = re.sub(r'[^a-zA-z- ]', '', s1)
        return s1_

    def clean_format(self, s1):
        s1_ = re.sub(r'(<br />|<br>)', '', s1 )
        return s1_
    
    def find_bigrams(self, s1):
        input_list = s1.split()
        bigram_list = []
        for i in range(len(input_list)-1):
            bigram_list.append((input_list[i] + "-" + input_list[i+1]))
        bigram = " ".join(bigram_list)
        return bigram

# tp = TextProcessor()
# c = Crawler()
# documents = c.get_document()
# for d in documents:
#     tp.clean_word(d)
#     print(d.title)
#     print(d.text)