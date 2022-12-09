import networkx as nx
import json
import pathlib, sys
from datetime import datetime
from datetime import timezone

p = pathlib.Path(__file__).parent.absolute().parent.absolute()
sys.path.insert(0, str(p) + "/saved")

f = open(str(p) + "/saved/test.json")

J = json.load(f)

f.close()
G = nx.node_link_graph(J)

def getOptions(category):
    
    global G
    all_subs = nx.get_node_attributes(G, category)

    new = set()
    for k,v in all_subs.items():
        a = v.split(";")
        for ele in a:
            if ele:
                new.add(ele)
    to_return = []
    for ele in new:
        if ele:
            a = {"label":ele, "value":ele}
            to_return.append(a)
    return to_return

def get_filter(subs, pubs, from_t, to):
    global G
    subs2 = []
    for ele in subs:
        subs2.append(ele["value"])

    pubs2 = []
    for ele in pubs:
        pubs2.append(ele["value"])

    def lamb(attr):
        if attr == {}:
            return False
        
        nonlocal subs2, pubs2
        subs_bool = False
        pubs_bool = False
        time_bool = False
        if "subjects" in attr:
            subs_bool = any(list(map(lambda x: x in attr["subjects"], subs2)))

        if "publisher" in attr:
            pubs_bool = any(list(map(lambda x: x in attr["publisher"], pubs2)))
        if "origin" in attr:
            curr = datetime.fromisoformat(attr["origin"][:-1]).astimezone(timezone.utc)
            time_bool = (from_t<=curr) and (curr<=to)
        return subs_bool and pubs_bool and time_bool

    # print(G.nodes["10.1001/.389"])
    

    newG = G.subgraph([n for n,v in G.nodes(data=True) if lamb(v)])
    toShow = nx.node_link_data(newG)
    with open(str(p)+ "/interface/demo/src/components/toShow.json", "w") as f:
        json.dump(toShow, f)
    return

    