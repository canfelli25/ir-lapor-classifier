import Algorithmia
from crawler.crawler import Crawler
from .proteks import TextProcessor
import csv, gc, requests, time

# Your API Key
API_KEY = "simRzufrye0vElXGUbZHPYKm2sc1"

def retry(cooloff=5, exc_type=None):
    if not exc_type:
        exc_type = [requests.exceptions.ConnectionError]

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if e.__class__ in exc_type:
                        print("failed (?)")
                        time.sleep(cooloff)
                    else:
                        raise e
        return wrapper
    return real_decorator

class LDAAlgorithm:
	def __init__(self):
		self.client = Algorithmia.client(API_KEY)
		self.algo = self.client.algo('nlp/LDA/1.0.0')
		self.input = {"docsList" : []}

	def add_doc(self, doc):
		self.input["docsList"].append(doc.getTitle())
		self.input["docsList"].append(doc.getText())

	@retry()
	def lda(self):
		result = self.algo.pipe(self.input).result
		# output = {"result" : result}
		output = result
		return output

lda = LDAAlgorithm()
tp = TextProcessor()
c = Crawler()
documents = c.get_document()
for d in documents:
	d.title = tp.clean_word(d.title)
	d.text = tp.clean_word(d.text)
	lda.add_doc(d)
gc.collect()

output = lda.lda()
data = [["word", "frequency"]]
print(output)
for dic in output:
	for key, value in dic.items():
		data.append([key, value])

with open('output.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerows(data)
