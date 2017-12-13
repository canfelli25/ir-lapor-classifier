import Algorithmia
from crawler.crawler import Crawler
import csv

# Your API Key
API_KEY = "simRzufrye0vElXGUbZHPYKm2sc1"

class LDAAlgorithm:
	def __init__(self):
		self.client = Algorithmia.client(API_KEY)
		self.algo = self.client.algo('nlp/LDA/1.0.0')
		self.input = {"docsList" : []}

	def add_doc(self, doc):
		self.input["docsList"].append(doc.getTitle())
		self.input["docsList"].append(doc.getText())

	def lda(self):
		result = self.algo.pipe(self.input).result
		output = {"result" : result}
		return output

lda = LDAAlgorithm()
c = Crawler()
documents = c.get_document()
for d in documents:
	lda.add_doc(doc)

output = lda.lda()
data = [["word", "frequency"]]

for dic in output:
	for key, value in dic.items():
		data.append([key, value])

with open('output.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerows(data)