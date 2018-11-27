# Todo refactor this to be more efficient
import json

links = []
nodes = []

with open("./links/links.csv", "r") as lines:
    for line in lines:
        line = line.rstrip('\n').split(',')
        links.append({'source': line[0], 'target': line[1]})
        
with open("./groups/groups.csv", "r") as lines:
    for line in lines:
        line = line.rstrip('\n').split(',')
        nodes.append({'id': line[0], 'name': line[1], 'group': line[2]})

for i in range(len(links)):
    for j in range(len(nodes)):
        if links[i]["source"] == nodes[j]["id"]:
            links[i]["source"] = j
        if links[i]["target"] == nodes[j]["id"]:
            links[i]["target"] = j

json_prep = {"nodes":nodes, "links":links}

json_prep.keys()

json_dump = json.dumps(json_prep, indent=1, sort_keys=True)
# print(json_dump)

json_out = open('./public/community-graph.json','w')
json_out.write(json_dump)
json_out.close()