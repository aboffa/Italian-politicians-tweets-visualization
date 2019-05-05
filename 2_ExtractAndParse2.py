import treetaggerwrapper
import json
import pprint

import myUtils

tagger = treetaggerwrapper.TreeTagger(TAGLANG="it", TAGDIR="/home/boffa/PycharmProjects/tweets/venv1/bin/tree-tagger")

typesToConsider = ["NOM", "ADJ", "NPR"]

jsonPoliticians = open('./d3/politicians.json', 'r')
politiciansObject = json.load(jsonPoliticians)
nTweets = 0
nTotalWords = 0
for name, politicianValue in politiciansObject.items():
    toPlot = []
    toWrite = {}
    toWrite["idsAndWords"] = {}
    f = open("./allTweets/" + politicianValue['twetterName'] + ".json", "r")
    tweetsObject = json.loads(f.read())
    f.close()
    for j, tweet in enumerate(tweetsObject):
        toConsider = ""
        NotToConsider = ""
        tweetText = tweet['text']
        # print(tweetText)
        tweetText = tweetText.replace("’", " ")
        finalTwertText = ""
        for word in tweetText.split():
            if "http" not in word:
                if word[0] == "#":
                    finalTwertText += " " + word[1:]
                else:
                    finalTwertText += " " + word

        tags = tagger.tag_text(finalTwertText)
        tags2 = treetaggerwrapper.make_tags(tags)
        for tag in tags2:
            if len(tag) == 3:
                if tag[1] in typesToConsider and len(tag[0]) > 1 and tag[0].isalpha():
                    # print(tag)
                    toConsider += " " + tag[2].lower()
                    nTotalWords += 1
                else:
                    NotToConsider += " " + tag[2].lower()
            else:
                NotToConsider += tag[0].lower()
        #print(toConsider[0:2110])
        #print()
        #print(NotToConsider[0:2110])
        if toConsider != "":
            toWrite["idsAndWords"][tweet["id"]] = toConsider
            nTweets += 1
    toWrite["nTweets"] = nTweets
    toWrite["nTotalWords"] = nTotalWords
    fw = open('allTweetsAndWords/' + politicianValue['twetterName'] + ".json", "w+")
    fw.write(json.dumps(toWrite, ensure_ascii=False))
    fw.flush()
    fw.close()
