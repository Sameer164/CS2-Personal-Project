
import pathlib,sys
p = pathlib.Path(__file__).parent.absolute().parent.absolute()
print(sys.path)
sys.path.insert(0, str(p) + "/networkx")


from collections import deque
from pyvis.network import Network
from opencit import get_cited_by
from cites import cites


# count is how many clusters do we want to add
def main(start_doi, count):
    all_edges = set()
    net = Network(directed=True)
    queue = deque([start_doi])
    start = 0
    broken = False
    while queue and start < count:
        doi = queue.popleft()
        node = net.add_node(doi, label = doi)
        start += 1
        print(f"{start} edge added")
        references = cites(doi)
        cited_by = get_cited_by(doi)
        ref = True
        ref_count = 0
        cite_count = 0
        while ref_count < len(references) and cite_count < len(cited_by) and start < count:
            if ref:
                if (doi, references[ref_count]) not in all_edges:
                    net.add_node(references[ref_count])
                    net.add_edge(doi, references[ref_count])
                    queue.append(references[ref_count])
                    start += 1
                    ref = False
                    all_edges.add((doi, references[ref_count]))
                    ref_count += 1
            else:
                if (cited_by[cite_count], doi) not in all_edges:
                    net.add_node(cited_by[cite_count])
                    net.add_edge(cited_by[cite_count], doi)
                    queue.append(cited_by[cite_count])
                    ref = True
                    start += 1
                    all_edges.add((cited_by[cite_count], doi))
                    cite_count += 1
            
            print(f"{start} edge added")
    
        # for i in range(counter, len(references)):
        #     if start >= count:
        #         break
        #     net.add_node(references[i])
        #     net.add_edge(doi, references[i])
        #     queue.append(references[i])
        #     start += 1
        #     print(f"{start} node added")
        
        for j in range(cite_count, len(cited_by)):
            if start >= count:
                break
            if (cited_by[j], doi) not in all_edges:
                net.add_node(cited_by[j])
                net.add_edge(cited_by[j], doi)
                queue.append(cited_by[j])
                start += 1
                all_edges.add((cited_by[j], doi))
                print(f"{start} edge added")
        
        for i in range(ref_count, len(references)):
            if start >= count:
                break
            if (doi, references[i]) not in all_edges:
                net.add_node(references[i])
                net.add_edge(doi, references[i])
                queue.append(references[i])
                start += 1
                all_edges.add((doi, references[i]))
                print(f"{start} edge added")
        
        
    

    net.toggle_physics(True)
    net.show('nx.html')


if __name__ == "__main__":
    main("10.1177/1369148118786043", 500)

