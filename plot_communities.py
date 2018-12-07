#!/usr/bin/env python3
"""
Create JSON file of links and nodes that will be used to plot the graph in D3
"""
import json
import argparse

links = []
nodes = []

def org_source_targets(path, outputs):
    # Returns a list of dicts containing the source and target ids

    with open("data/D3Input/"+path+"/links-"+outputs +".csv", "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            links.append({'source': line[0], 'target': line[1]})
    return links

def org_communities(path, outputs): 
    """
    Return a list of dicts with keys: 'id', 'domain' and 'community'
    """
    with open("data/D3Input/"+path+"/communities-"+outputs+".csv", "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            nodes.append({'id': line[0], 'domain': line[1], 'community': line[2]})
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

def main(output_path, path, outputs):
    # Write out JSON file for D3
    links = org_source_targets(path, outputs)
    nodes = org_communities(path, outputs)
    json_content = json_loader(links, nodes)
    json_dump = json.dumps(json_content, indent=1, sort_keys=True)
    json_out = open(output_path+'-'+path+'-'+outputs+'.json', 'w')
    json_out.write(json_dump)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot files for labelled communities')
    parser.add_argument('-o', '--outputs', type=str, nargs='?', help='Output name for files generated')
    parser.add_argument('-p', '--path', type=str, nargs='?', help='Output directory path name for focus domains')
    args = parser.parse_args()
    output_path = './public/files/community-cluster'
    main(output_path, args.path, args.outputs)
