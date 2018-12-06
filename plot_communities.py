#!/usr/bin/env python3
"""
Create JSON file of links and nodes that will be used to plot the graph in D3
"""
import json
from collections import defaultdict

links = []
nodes = []
months = ['may', 'oct']

def org_source_targets(month):
    # Returns a list of dicts containing the source and target ids

    with open("./links-"+month+'/links-'+month+'.csv', "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            links.append({'source': line[0], 'target': line[1]})
    return links

def org_communities(month):   
    """
    Return a list of dicts with keys: 'id', 'domain' and 'community'
    """
    with open("./communities-"+month+'/communities-'+month+'.csv', "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            nodes.append({'id': line[0], 'domain': line[1], 'community': line[2]})
    return nodes

def load_popular_labels(month):   
    """
    Return a dict of domains as values with labels as keys: 'domain' and 'community labels'
    """
    popular_dict = {}
    with open("./top10-"+month+'/top10-'+month+'.csv', "r") as lines:
        for line in lines:
            line = line.rstrip('\n').split(',')
            if line[2] in popular_dict:
                popular_dict[line[2]].append(line[1])
            else:
                popular_dict[line[2]] = [line[1]]

    json_dump = json.dumps(popular_dict, indent=1, sort_keys=True)
    json_out = open('./public/top10-'+month+'.json', 'w')
    json_out.write(json_dump)

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

def main(output_path):

    for m in months:
        # Write out JSON file for D3
        links = org_source_targets(m)
        nodes = org_communities(m)
        popular_labels = load_popular_labels(m)
        json_content = json_loader(links, nodes)
        json_dump = json.dumps(json_content, indent=1, sort_keys=True)
        json_out = open(output_path+'-'+m+'.json', 'w')
        json_out.write(json_dump)

if __name__ == "__main__":
    output_path = './public/community-cluster'
    main(output_path)
