import urllib.request, json
from collections import deque


def cites(doi):
    link = "https://api.crossref.org/works/" + doi
    cites_list = []
    try:
        with urllib.request.urlopen(link) as url:
            data = json.load(url)
            if data:
                if "message" in data:
                    if "references" in data["message"]:
                        for ele in data["message"]["references"]:
                            cites_list.append(ele["DOI"])
        return cites_list
    except:
        return []


