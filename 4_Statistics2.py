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

# For all topics
for topic, topicValue in topicsObject.items():
    sumRatio = 0
    politicians = {}
    # For all politicians
    for name, politicianValue in politiciansObject.items():
        f = open('allTweetsAndWords/' + politicianValue['twetterName'] + ".json", "r")
        idsAndWords = json.loads(f.read())
        # NOT SMART THINK IT AGAIN
        tweetsIDsList = []
        ratio = 0
        thisTopic = 0
        # For all tweets
        for tweetId, words in idsAndWords["idsAndWords"].items():
            for keyword in topicValue["keywords"]:
                for word in words.split():
                    if keyword in word:
                        thisTopic += 1
                        if tweetId not in tweetsIDsList and len(tweetsIDsList) < 5:
                            tweetsIDsList.append(tweetId)
        ratio += (thisTopic / idsAndWords["nTotalWords"])
            # Check if useful
        print(ratio)
        politicians[name] = {}
        if (ratio < 0.00001):
            politicians[name]["ratio"] = 0
            politicians[name]["tweet_ids"] = []
        else:
            politicians[name]["ratio"] = '%.8f' % (ratio*2)
            politicians[name]["tweet_ids"] = tweetsIDsList
    forForceGraph["nodes"].append({"id": topic, "isTopic": 1, "group": 1, "politicians": politicians})

print(forForceGraph)
fGraph = open("d3/politiciansNEW.json", "w+")
fGraph.write(json.dumps(forForceGraph))
fGraph.close()
