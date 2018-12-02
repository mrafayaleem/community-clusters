#!/usr/bin/env python3
"""
Create JSON file of links and nodes that will be used to plot the graph in D3
"""
import json

links = []
nodes = []
def org_source_targets(link_path):
    # Returns a list of dicts containing the source and target ids
    with open(link_path, "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            links.append({'source': line[0], 'target': line[1]})
    return links

def org_communities(pagerank_path):   
    """
    Return a list of dicts with keys: 'id', 'domain', 'community' and 'pagerank' 
    """
    with open(pagerank_path, "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            nodes.append({'id': line[0], 'domain': line[1], 'community': line[2], 'pagerank': line[3]})
    return nodes

def json_loader(links, nodes):
    # Organize the 
    for i in range(len(links)):
        for j in range(len(nodes)):
            if links[i]["source"] == nodes[j]["id"]:
                links[i]["source"] = j
            if links[i]["target"] == nodes[j]["id"]:
                links[i]["target"] = j

    json_content = {"nodes":nodes, "links":links}
    return json_content

def main(link_path, pagerank_path, json_path):
    # Write out JSON file for D3
    links = org_source_targets(link_path)
    nodes = org_communities(pagerank_path)
    json_content = json_loader(links, nodes)

    json_content.keys()
    json_dump = json.dumps(json_content, indent=1, sort_keys=True)
    json_out = open(json_path, 'w')
    json_out.write(json_dump)

if __name__ == "__main__":
    link_path = "./links/links.csv"
    pagerank_path = "./communities/rankings.csv"
    json_path = './public/community-cluster.json'

    main(link_path, pagerank_path, json_path)
