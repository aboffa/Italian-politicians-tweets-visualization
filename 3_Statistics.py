import pprint

import numpy
from nltk.probability import FreqDist
import json
import myUtils

fwrite = open("first_statistics.csv", "w+")
fwrite.write("names")
for topic in myUtils.topics.keys():
    fwrite.write(" , "+topic)
fwrite.write("\n")
forForceGraph = {}
forForceGraph["nodes"] = []
forForceGraph["links"] = []

for topic in myUtils.topics.keys():
    forForceGraph["nodes"].append({"id":topic, "group":1, "size":6})
    #forForceGraph["nodes"].append({"name": topic, "group": 1, "size": 6})
for i, name in enumerate(myUtils.tweetterNames[0:10]):
    forForceGraph["nodes"].append(({"id":name, "group":2, "size":9}))
    #forForceGraph["nodes"].append(({"name": name, "group": 2, "size": 9}))
    print(str(i) + ") " + name)
    f = open('allWords/' + name + ".json", "r")
    words = json.loads(f.read())
    print("Plotting " +str(len(words))+ " words")
    mytopic = myUtils.topics.copy()
    for topic in mytopic.keys():
        for word in words:
            if topic in word:
                mytopic[topic] +=1
    print(mytopic)
    fwrite.write(name)
    for k, topic in enumerate(mytopic.keys()):
        ratio = (mytopic[topic] / len(words))
        #if mytopic[topic] == 0:
            #fwrite.write(" , 0")
            #forForceGraph["links"].append({"source": name, "target": topic, "value": -1})
        if ratio < 0.0001:
            fwrite.write(" , 0")
        else:
            fwrite.write(" , "+str(ratio))
            #forForceGraph["links"].append({"source":k  , "target":i+ len(mytopic), "value":ratio*50})
            forForceGraph["links"].append({"source": name, "target": topic, "value": ratio * 50})

    fwrite.write("\n")

    #for i in range(0,len(mytopic.keys())):
    #    for j in range (i+1,len(mytopic.keys())):
     #       forForceGraph["links"].append({"source": i, "target": j, "value": 1})
fGraph = open("d3/politicians3.json", "w+")
fGraph.write(json.dumps(forForceGraph))
fGraph.close()

print(forForceGraph)
    #freq = FreqDist(words)
    #freq.plot(60)
