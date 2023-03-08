class Posting:
    def __init__(self, url, freq):
        #url name
        self.url = url

        #frequency of the number of pages appeared
        self.freq = freq
        self.importantWord = False
    
    #updating freqency
    def updateFreq(self):
        self.freq += 1
    
    def getFreq(self):
        return self.freq
    
    def getURL(self):
        return self.url
    
    def hasImportantWord(self):
        self.importantWord = True
    
    def getImportantWord(self):
        return self.importantWord