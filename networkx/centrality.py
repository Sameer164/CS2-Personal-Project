import sys, pathlib, json
import networkx as nx

p = pathlib.Path(__file__).parent.absolute().parent.absolute()
to_use = str(p) + "/saved/"

def main(name):
    json_f = to_use + name
    with open(json_f) as f:
        json_data = json.loads(f.read())
    
    G = nx.node_link_graph(json_data)
    print(G)
    centrals = nx.eigenvector_centrality(G)
    centrals = dict(sorted(centrals.items(), key = lambda x: x[1]))
    count = 0
    vs = set()
    same = 0
    for k, v in centrals.items():
        if v in vs:
            same += 1
        vs.add(v)
        count += 1
    print((same/count) * 100)

if __name__ == "__main__":
    
    main(str("large") + ".json")