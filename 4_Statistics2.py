import json
import myUtils

from nltk.probability import FreqDist

fwrite = open("first_statistics.csv", "w+")
fwrite.write("names")
for topic in myUtils.topics.keys():
    fwrite.write(" , " + topic)
fwrite.write("\n")
forForceGraph = {}
forForceGraph["nodes"] = []
forForceGraph["links"] = []

for k, topic in enumerate(myUtils.topics.keys()):
    mytopic = myUtils.topics.copy()
    sumRatio = 0
    politicians =[]
    for i, name in enumerate(myUtils.tweetterNames[0:2]):
        # forForceGraph["nodes"].append(({"id":name, "group":2, "size":9}))
        #forForceGraph["nodes"].append(({"name": name, "group": 2, "size": 9}))
        print(str(i) + ") " + name)
        f = open('allWords/' + name + ".json", "r")
        words = json.loads(f.read())
        print("Plotting " + str(len(words)) + " words")
        #NOT SMART THINK IT AGAIN
        thisTopic = 0
        for word in words:
            if topic in word:
                thisTopic += 1
        ratio = (thisTopic / len(words))
        # if mytopic[topic] == 0:
        # fwrite.write(" , 0")
        # forForceGraph["links"].append({"source": name, "target": topic, "value": -1})
        sumRatio += ratio
        print()
        fdist1 = FreqDist(words)
        print(fdist1.most_common(100))
        politicians.append({"value":ratio, "politic":name })

    for politic in politicians:
        politic["value"] = round(politic["value"] / sumRatio * 100)

    #politicians.sort(key = lambda x : x["value"] )

    forForceGraph["nodes"].append({"id": topic, "group": 1, "size": sumRatio, "politicians":politicians })

print(forForceGraph)
# for i in range(0,len(mytopic.keys())):
#    for j in range (i+1,len(mytopic.keys())):
#       forForceGraph["links"].append({"source": i, "target": j, "value": 1})
fGraph = open("d3/politiciansNEW.json", "w+")
fGraph.write(json.dumps(forForceGraph))
fGraph.close()
