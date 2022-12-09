import networkx as nx
from collections import deque
import threading
import concurrent.futures
import os
import gzip
import json
from cites import cites
from opencit import get_cited_by
from nodeInfo import get_info

import sys, pathlib
p = pathlib.Path(__file__).parent.absolute().parent.absolute()

graph = nx.DiGraph()
sub = 0

def add_info(doi):
    global graph
    info = get_info(doi)
    for k,v in info.items():
        graph.nodes[doi][k] = v


def save():
    global graph

    
        
    
    data1 = nx.node_link_data(graph)
    with open(str(p) + "/saved/" + str("large") + ".json", "w") as f:
        json.dump(data1, f)
    quit()
    







def start(start_doi):
    global graph, sub
    queue = deque([start_doi])
    while queue:
        if sub > 300000:
            save()
        doi = queue.popleft()
        node = graph.add_node(doi)
        infos = threading.Thread(target = add_info, args= [doi])
        infos.start()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            ref = executor.submit(cites, doi)
            cit_by = executor.submit(get_cited_by, doi)

            for ref_doi in ref.result():
                if not graph.has_edge(doi, ref_doi):
                    graph.add_edge(doi, ref_doi)
                    queue.append(ref_doi)
                    print(sub, "edge added")
                    sub += 1
            
            for cited_doi in cit_by.result():
                if not graph.has_edge(cited_doi, doi):
                    graph.add_edge(cited_doi, doi)
                    queue.append(cited_doi)
                    print(sub, "edge added")
                    sub += 1



def main():
    global graph, sub

    with os.scandir(str(p) + "/dois/") as lstDoi:
        try:
            for doi in lstDoi:
                with gzip.open(str(p) + "/dois/" + doi.name, "rb") as j:
                    data = json.loads(j.read())
                    with concurrent.futures.ThreadPoolExecutor() as startDois:
                        for paper in data["items"]:
                            t = startDois.submit(start, paper["DOI"])
        except:
            pass
    






if __name__ == "__main__":
    main()
