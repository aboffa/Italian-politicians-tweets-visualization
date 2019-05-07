import sys, os, subprocess, json
import datetime

from time import sleep

import myUtils

test = ["ant_boff"]

fromDateTime = datetime.datetime(2018, 6, 1)
jsonPoliticians = open('./d3/politicians.json', 'r')
politiciansObject = json.load(jsonPoliticians)

# With statuses/user_timeline
for name, politicianValue in politiciansObject.items():
    print(name)
    exists = os.path.isfile('allTweets/' + politicianValue['twetterName'] + ".json")
    if not exists:
        totalTweet = 0
        resultObjectTotal = []
        toExecute = "twurl \"/1.1/users/show.json?screen_name=" + politicianValue['twetterName'] + "\" "
        print("Executing -> " + toExecute)
        result = subprocess.run(toExecute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.stderr.decode("utf8") != "\n":
            resultText = result.stdout.decode("utf8")
            resultObject = json.loads(resultText)
            maxNumOfTweet = min(3200, resultObject['statuses_count'])
            print(maxNumOfTweet)
            while (totalTweet < maxNumOfTweet):
                sleep(1)
                if totalTweet == 0:
                    toExecute = "twurl \"/1.1/statuses/user_timeline.json?screen_name=" + politicianValue['twetterName'] + "&count=200&include_rts=true\" "
                else:
                    toExecute = "twurl \"/1.1/statuses/user_timeline.json?screen_name=" + politicianValue['twetterName'] + "&count=200&include_rts=true&max_id=" + str(
                        last_ID + 1) + "\" "
                print("Executing -> " + toExecute)
                result = subprocess.run(toExecute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                if result.stderr.decode("utf8") != "\n":
                    resultText = result.stdout.decode("utf8")
                    resultObject = json.loads(resultText)
                    resultObjectTotal.extend(resultObject)
                    totalTweet = totalTweet + len(resultObject)
                    print("TOTAL TWEET = " + str(totalTweet) + ", this amount of tweet = " + str(len(resultObject)))
                    last_ID = resultObject[-1]['id']
                    created_date = datetime.datetime.strptime(resultObject[-1]['created_at'],
                                                              '%a %b %d %H:%M:%S +0000 %Y')
                    if created_date < fromDateTime:
                        break;
                else:
                    print(result.stderr.decode("utf8"))
                    exit(1)
            f = open('allTweets/' + politicianValue['twetterName'] + ".json", "w+")
            f.write(json.dumps(resultObjectTotal))
            f.flush()
            f.close()

        else:
            print(result.stderr.decode("utf8"))
            exit(1)
    else:
        # Update with newer Tweet
        f = open("./allTweets/" + politicianValue['twetterName'] + ".json", "r")
        tweetsObject = json.loads(f.read())
        first_ID = tweetsObject[0]['id']
        resultObjectTotal = []
        toExecute = "twurl \"/1.1/statuses/user_timeline.json?screen_name=" + politicianValue['twetterName'] + "&count=200&include_rts=true&since_id=" + str(
            first_ID - 1) + "\" "
        result = subprocess.run(toExecute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.stderr.decode("utf8") != "\n":
            resultText = result.stdout.decode("utf8")
            resultObject = json.loads(resultText)
            if len(resultObject) != 0:
                for newtweet in resultObject:
                    tweetsObject.insert(0, newtweet)
                f = open('allTweets/' + politicianValue['twetterName'] + ".json", "w+")
                f.write(json.dumps(tweetsObject))
                f.flush()
                f.close()
        else:
            print(result.stderr.decode("utf8"))
            exit(1)
# ./allTweets/"+name+".json


# With Search
# for name in myUtils.tweetterNames:
#     print(name)
#     exists = os.path.isfile('allTweets/'+name+".json")
#     if not exists:
#         # Retrieve all tweets
#         toExecute = "twurl " \
#                     "\"/1.1/tweets/search/fullarchive/datacollecting.json\" " \
#                     "-A \"Content-Type: application/json\" -d \'{\"query\":\"from:"+name+"\"," \
#                     "\"maxResults\":\"100\", \"fromDate\":\""+fromDate+"\",\"toDate\":\""+toDate+"\"}\' "
#         print("Executing -> " + toExecute)
#         result = subprocess.run(toExecute,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
#         if result.stderr.decode("utf8") != "\n":
#             resultText = result.stdout.decode("utf8")
#             resultObject = json.loads(resultText)
#             if 'error' not in resultObject:
#                 f = open('allTweets/' + name + ".json", "w+")
#                 #print(type(tweetsObject))
#                 while ('next' in resultObject):
#                     print("PRESENT")
#                     nextToken = resultObject['next']
#                     # Continue retrieve all tweets
#                     toExecute = "twurl " \
#                                 "\"/1.1/tweets/search/fullarchive/datacollecting.json\" " \
#                                 "-A \"Content-Type: application/json\" -d \'{\"query\":\"from:" + name + "\"," \
#                                 "\"maxResults\":\"100\", \"fromDate\":\"" + fromDate + "\",\"toDate\":\"" + toDate + "\" " \
#                                 " \"next\":\""+nextToken+"\" }\' "
#                     print("Executing -> " + toExecute)
#                     newResult = subprocess.run(toExecute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#                     resultText = resultText + newResult
#                     sleep(1)
#                 else:
#                     print("NOT PRESENT")
#                 f.write(resultText)
#                 f.flush()
#                 f.close()
#             sleep(10)
#         else:
#             print(result.stderr.decode("utf8"))
#             exit(1)
