import requests
from BeautifulSoup import BeautifulSoup

class BizSearch:

    def __init__(self, outfile):
        self.s = requests.Session()
        adv_search_url = "http://searchctbusiness.ctdata.org/advanced_search"
        user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}
        soup = BeautifulSoup(self.s.get(adv_search_url, headers=user_agent).content)
        for inp in soup.findAll("input"):
            if inp["id"] == "csrf_token":
                self.token = inp["value"]

        self.outfile = open(outfile,"w")
        

    def make_url(self, term):
            base_url = "http://searchctbusiness.ctdata.org/search_results?"
            self.params = {
                "query_limit":"",
                "query": term,
                "start_date": "1900-01-01",
                "end_date": "2016-08-01",
                "index_field": "business_name",
                "sort_order":"asc",
                "sort_by":"nm_name",
                "active":"y",
                "business_type":"All+Entities",
                "page":"1",
            }

            ret = base_url;
            keys = self.params.keys()

            for i in range(len(keys)):
                k = keys[i];
                pref = ""
                
                if i > 0:
                    pref = "&"

                pair = pref + k + "=" + self.params[k]
                ret +=  pair
            
            return ret
    
        
    def search(self, term):
        refer = self.make_url(term)
        params2 = {
            "index_field":self.params["index_field"],
            "query":self.params["query"],
            "query_limit":"",
            "start_date":self.params["start_date"],
            "end_date":self.params["end_date"],
            "active":"y",
            "csrf_token":self.token,
            "sort_by":"nm_name",
            "sort_order":"asc"}

        adv_download_url = "http://searchctbusiness.ctdata.org/download"
        content = self.s.post(adv_download_url,data=params2).content

        self.outfile.write(content)
        self.outfile.close()

        
