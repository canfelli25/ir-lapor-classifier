class Document:
    def __init__(self, number, title, text):
        self.number = number
        self.title = title
        self.text = text

    def getNumber(self):
        return self.number

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text
