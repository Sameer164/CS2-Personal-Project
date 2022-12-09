import networkx as nx
from collections import deque
from pyvis.network import Network
import os
import gzip
import json
from cites import cites
from opencit import get_cited_by
from nodeInfo import get_info

import sys, pathlib
p = pathlib.Path(__file__).parent.absolute().parent.absolute()

graph = nx.DiGraph()
def start(start_doi):
    global graph
    queue = deque([start_doi])
    while queue:
        doi = queue.popleft()
        info = get_info(doi)
        node = graph.add_node(doi)
        for k,v in info.items():
            graph.nodes[doi][k] = v
        references = cites(doi)     
        cited_by = get_cited_by(doi)
        for ref_doi in references:
            if not graph.has_edge(doi, ref_doi):
                graph.add_edge(doi, ref_doi)
                queue.append(ref_doi)
        
        for cited_doi in cited_by:
            if not graph.has_edge(cited_doi, doi):
                graph.add_edge(cited_doi, doi)
                queue.append(cited_doi)



def main():
    global graph    
    try:
        with os.scandir("../dois/") as lstDoi:
            for doi in lstDoi:
                with gzip.open("../dois/" + doi.name, "rb") as j:
                    data = data = json.loads(j.read())
                    for paper in data["items"]:
                        start(paper["DOI"])
    except KeyboardInterrupt:
        data1 = nx.node_link_data(graph)
        with open(str(p) + "/saved/test.json", "w") as f:
            json.dump(data1, f)
    # nt = Network("1920px", "1080px")     
    # nt.from_nx(graph)
    # nt.show('nx.html')
    data1 = nx.node_link_data(graph)
    with open(str(p) + "/saved/test.json", "w") as f:
        json.dump(data1, f)




if __name__ == "__main__":
    main()
