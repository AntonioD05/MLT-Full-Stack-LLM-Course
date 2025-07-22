import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}

        headers = {'user-agent' : 'Antonio Diaz adiaz01022005@gmail.com'}
        r = requests.get(self.fileurl, headers=headers)

        self.filejson = r.json()

        #print(r.text)
        #print(self.filejson)
        #print(type(self.filejson))

        for entry in self.filejson.values():
            self.namedict[entry['title']] = (entry['cik_str'], entry['title'], entry['ticker'])
            self.tickerdict[entry['ticker']] = (entry['cik_str'], entry['title'], entry['ticker'])
        

    def name_to_cik(self, title):
        if title not in self.namedict:
            return "Not found"
        return self.namedict[title]
    
    def ticker_to_cik(self, ticker):
        if ticker not in self.tickerdict:
            return "Not found"
        return self.tickerdict[ticker]
            

sec = SecEdgar('https://www.sec.gov/files/company_tickers.json')

print(sec.ticker_to_cik('NVDA'))
print(sec.name_to_cik('Apple Inc.'))
       