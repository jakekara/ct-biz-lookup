import requests
from BeautifulSoup import BeautifulSoup

# http://searchctbusiness.ctdata.org/search_results?
# query_limit=
# &page=1
# &query=Pizza
# &start_date=1900-01-01
# &end_date=2016-08-01
# &index_field=business_name
# &sort_order=asc
# &sort_by=nm_name
# &active=False
# &business_type=All+Entities

def advanced_search(term,business_type="All+Entities",active="False"):
    adv_search_url = "http://searchctbusiness.ctdata.org/advanced_search"
    adv_results_url = "http://searchctbusiness.ctdata.org/search_results"
    user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}

    # Persist session
    s = requests.Session()
    r = s.get(adv_search_url, headers=user_agent)

    # Session id
    sesh = r.cookies.get_dict()["session"]    
    html = r.content
    soup = BeautifulSoup(html)
    token = ""
    data = {}

    # Get all the input fields
    for inp in soup.findAll("input"):
        data[inp["id"]] = inp["value"]
        # print "Input field: ", (inp["id"],inp["value"])

    # Get all the selection fields
    for sel in soup.findAll("select"):
        # query[inp["id"]] = inp["value"]
        # print "Selection field: " + sel["name"] + ":"
        opts = []
        for opt in sel.findAll("option"):
            # print "\t", opt["value"]
            opts.append(opt["value"])
        data[sel["name"]] = opts[0]

    user_agent["Referer"] = adv_search_url
    html = s.get(adv_search_url, headers=user_agent, data=data)
    search(term,s,sesh,data["csrf_token"])
        
def search(term,s,session,token,business_type="All+Entities"):

    # print "session:", session
    # print "csrf_token:", token
    
    base_url = "http://searchctbusiness.ctdata.org/search_results?"
    params = {
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
        # "csrf_token":token,
    }

    def make_url():
        ret = base_url;
        keys = params.keys()
        
        for i in range(len(keys)):
            k = keys[i];
            pref = ""
            
            if i > 0:
                pref = "&"

            pair = pref + k + "=" + params[k]
            ret +=  pair
            
        return ret

    # print make_url()

    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}
    cookies = {"session":session}

    # html =  s.get(make_url(),headers=headers,cookies=cookies).content
    # soup = BeautifulSoup(html)

    adv_download_url = "http://searchctbusiness.ctdata.org/download"
    headers["Referer"] = make_url()
    headers["Origin"] = "http://searchctbusiness.ctdata.org"
    headers["Host"] = "searchctbusiness.ctdata.org"
    headers["Cookie"] = "session=" + session
    params2 = {
        "index_field":params["index_field"],
        "query":params["query"],
        "query_limit":"",
        "start_date":params["start_date"],
        "end_date":params["end_date"],
        "active":"y",
        "csrf_token":token,
        "sort_by":"nm_name",
        "sort_order":"asc"}

    # r = requests.Session()
    s.headers.update({'referer': make_url})

    r = s.post(adv_download_url, headers=headers, cookies=cookies,data=params2)
    print r

    print r.headers
    print r.cookies
    content = r.content
    fh = open(term + ".csv","w")
    fh.write(content)
    fh.close()
    
    # print requests.get("http://searchctbusiness.ctdata.org/search_results?query_limit=&page=1&query=pizza&start_date=1900-01-01&end_date=2016-08-01&index_field=business_name&sort_order=asc&sort_by=nm_name&active=False",headers=headers,cookies=cookies).content
# Search("pizza")
# advanced_search("pizza")
# advanced_search("firearm")
# advanced_search("consulting")


advanced_search("analytics")
