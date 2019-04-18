import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.probability import FreqDist
import treetaggerwrapper
import json
import pprint

import myUtils


tagger = treetaggerwrapper.TreeTagger(TAGLANG="it",TAGDIR="/home/boffa/PycharmProjects/tweets/venv1/bin/tree-tagger")
stemmer = SnowballStemmer('italian')
# name = myUtils.tweetterNames[1]

default_stopwords = set(stopwords.words('italian'))
custom_stopwords = set(myUtils.notToConsider)

all_stopwords = default_stopwords | custom_stopwords

for i, name in enumerate(myUtils.tweetterNames):
    toPlot = []
    bigString = ""
    print(str(i) + ") " + name)
    f = open("./allTweets/" + name + ".json", "r")
    tweetsObject = json.loads(f.read())
    f.close()
    for j, tweet in enumerate(tweetsObject):
        # print(j)
        # print(tweet['text'])
        # No punctuoation
        splitted = word_tokenize(tweet['text'], "italian")
        # print(splitted)
        if 'retweeted_status' in tweet:
            splitted.extend(word_tokenize(tweet['retweeted_status']['text'], "italian"))
        if 'quoted_status' in tweet:
           splitted.extend(word_tokenize(tweet['quoted_status']['text'], "italian"))
        #Rebuild everything with only TreeTagger (test italian2)
        cleansplitted = [word.lower() for word in splitted
                         if word.isalpha()
                         and "http" not in word
                         and "//" not in word
                         and len(word) > 1
                         and not word.isnumeric()]

        for word in cleansplitted:
            tags = tagger.tag_text(word)
            tags2 = treetaggerwrapper.make_tags(tags)
            #print(tags2)
            if tags2[0][2] not in all_stopwords:
                #stemmed = stemmer.stem(word)
                if"NOM" in tags2[0][1] or "ADJ" in tags2[0][1] and "|" not in tags2[0][2] and tags2[0][2] not in myUtils.notToConsiderLemma:
                    #pprint.pprint(tags2)
                    toPlot.append(tags2[0][2])

            # print(stemmed)
            # print(clean_splitted)
    fw = open('allWords/' + name + ".json", "w+")
    fw.write(json.dumps(toPlot,ensure_ascii=False))
    fw.flush()
    fw.close()

