import urllib.request, json
from collections import deque

def get_cited_by(doi):
    link = "https://opencitations.net/index/coci/api/v1/citations/" + doi
    doi_list = []
    try:
        with urllib.request.urlopen(link) as url:
            data = json.load(url)
            if data:
                for cited_by in data:
                    doi_list.append(cited_by["citing"])
    except:
        return []
            
    return doi_list

