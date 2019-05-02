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

jsonPoliticians = open('./d3/politicians.json', 'r')
politiciansObject = json.load(jsonPoliticians)

jsonTopics = open('./d3/topics.json', 'r')
topicsObject = json.load(jsonTopics)

for k, topic in enumerate(myUtils.topics.keys()):
    mytopic = myUtils.topics.copy()
    sumRatio = 0
    politicians ={}
    for name, value in politiciansObject.items():
        print(name)
        f = open('allWords/' + value['twetterName'] + ".json", "r")
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
        #sumRatio += ratio
        print()
        #fdist1 = FreqDist(words)
        #print(fdist1.most_common(100))
        if (ratio < 0.0002):
            politicians[name] = 0
        else :
            politicians[name] = ratio

    #for politic in politicians:
    #   politic["value"] = round(politic["value"] / sumRatio * 100)

    #politicians.sort(key = lambda x : x["value"] )

    forForceGraph["nodes"].append({"id": topic, "group": 1,  "politicians":politicians })

print(forForceGraph)
# for i in range(0,len(mytopic.keys())):
#    for j in range (i+1,len(mytopic.keys())):
#       forForceGraph["links"].append({"source": i, "target": j, "value": 1})
fGraph = open("d3/politiciansNEW.json", "w+")
fGraph.write(json.dumps(forForceGraph))
fGraph.close()
