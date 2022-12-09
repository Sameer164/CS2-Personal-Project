import urllib.request, json

def get_info(doi):
    to_return = {}
    link = "https://api.crossref.org/works/" + doi
    try:
        with urllib.request.urlopen(link) as url:
            data = json.load(url)
            if data and data["message"]:
                if "title" in data["message"]:
                    to_return["title"] = ";".join(data["message"]["title"])
                else:
                    to_return["title"] = ""

                if "subject" in data["message"]:
                    to_return["subjects"] = ";".join(data["message"]["subject"])
                else:
                    to_return["subjects"] = ""

                if "type" in data["message"]:
                    to_return["type"] = data["message"]["type"]
                else:
                    to_return["type"] = ""
                
                if "publisher" in data["message"]:
                    to_return["publisher"] = data["message"]["publisher"]
                else:
                    to_return["publisher"] = ""
                
                if "created" in data["message"] and "date-time" in data["message"]["created"]:
                    to_return["origin"] = data["message"]["created"]["date-time"]
                else:
                    to_return["origin"] = data["message"]["created"]["date-time"]

                if "author" in data["message"]:
                    new = ""
                    for ele in data["message"]["author"]:
                        new += ele["given"] + ele["family"]
                        new += ";"
                    to_return["authors"] = new[:len(new) - 1]
        return to_return
    except:
        return {}
    
