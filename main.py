from crawler.crawler import Crawler
from backend.proteks import TextProcessor
from backend.ldav2 import LDAAlgorithm
import csv, re, gc


lda = LDAAlgorithm()
c = Crawler()
tp = TextProcessor()
documents = c.get_document()
print("Doc length:", len(documents))
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