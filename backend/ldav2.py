import gensim
from gensim import corpora
from crawler.crawler import Crawler
from .proteks import TextProcessor
import csv
import re, gc

class LDAAlgorithm:
	def __init__(self):
		self.input = []
		self.ldamodel = None

	def add_doc(self, doc):
		# Combine title and text into 1 list
		full_doc = doc.getTitle() + " " + doc.getText()
		self.input.append(full_doc.split())

	def _prepare_document(self):
		self.dictionary = corpora.Dictionary(self.input)
		self.dtm = [self.dictionary.doc2bow(doc) for doc in self.input]

	def lda(self):
		self._prepare_document()
		Lda = gensim.models.ldamodel.LdaModel
		# Gua set dulu jadi 5 ntar ganti aja
		self.ldamodel = Lda(self.dtm, num_topics=10, id2word=self.dictionary, passes=1)
		return self.ldamodel.print_topics()

lda = LDAAlgorithm()
c = Crawler()
tp = TextProcessor()
documents = c.get_document()
print(len(documents))
for d in documents:
	d = tp.clean_word(d)
	lda.add_doc(d)
gc.collect()

output = lda.lda()
data = [["num_of_cluster", "word", "weights"]]

counter = 1
for _, topic in output:
	_topic = re.split("\*|\s\+\s", topic)
	for i in range(0,len(_topic),2):
		data.append([counter, _topic[i+1].replace("\"", ""), _topic[i]])
	counter += 1

with open('output.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerows(data)