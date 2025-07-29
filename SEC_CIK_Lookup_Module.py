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

    def _get_submissions_data(self, cik): # helper function to fetch and return submission JSON
        cik = str(cik).zfill(10) #making sure it's 10 digits and use str since zfill is a string method
        headers = {'user-agent' : 'Antonio Diaz adiaz01022005@gmail.com'}
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        response = requests.get(url, headers=headers)
        data = response.json()
        return data['filings']['recent']
    
    def annual_filing(self,cik,year):
        filings_recent = self._get_submissions_data(cik)

        for i in range(len(filings_recent['form'])):
            form = filings_recent['form'][i]
            if (form == '10-K'):
                date = filings_recent['filingDate'][i]
                if date.startswith(str(year)):
                    accession = filings_recent['accessionNumber'][i].replace("-", "")
                    document = filings_recent['primaryDocument'][i]
                    file_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
                    return (form, date, file_url)
        
        return "No 10-K found for that year"
    
    def quarterly_filing(self, cik, year, quarter):
        filings_recent = self._get_submissions_data(cik)
        for i in range(len(filings_recent['form'])):
            form = filings_recent['form'][i]
            if (form == '10-Q' ):
                date = filings_recent['filingDate'][i]
                if date.startswith(str(year)):
                    month = int(date.split("-")[1])
                    if month in [1,2,3]:
                        this_quarter = 1
                    elif month in [4,5,6]:
                        this_quarter = 2
                    elif month in [7,8,9]:
                        this_quarter = 3
                    elif month in [10,11,12]:
                        this_quarter = 4
                    if this_quarter == quarter:
                        accession = filings_recent['accessionNumber'][i].replace("-", "")
                        document = filings_recent['primaryDocument'][i]
                        file_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
                        return (form, date, file_url)
                
        return "No 10-Q found for that year"
                


sec = SecEdgar('https://www.sec.gov/files/company_tickers.json')

print(sec.ticker_to_cik('NVDA'))
print(sec.name_to_cik('Apple Inc.'))
print(sec.name_to_cik('AMAZON COM INC'))
print(sec.annual_filing(320193, 2024))
print(sec.quarterly_filing(320193, 2024, 3))