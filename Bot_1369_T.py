#import libraries
import random
import sqlite3
import tweepy
import time
import sched
import sys

#twitter authentication
auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)

#connect to database
conn = sqlite3.connect("Database.db")
c = conn.cursor()
print("Connected to database")

#runs every few hours (spamming will cause twitter to take your dev account)
scheduler = sched.scheduler(time.time, time.sleep)


def insult():
    randInsult = random.randint(1, 60)
    randUser = random.randint(1, 4)
    c.execute('SELECT handle FROM Users WHERE ID={}'.format(randUser))
    user = str(c.fetchall())

    userArray = list(user)
    userLength = len(user)
    del userArray[userLength - 4:userLength]
    del userArray[:3]
    user = "".join(userArray)
    tweet = user + " "

    print(randInsult)
    c.execute('SELECT insult FROM insults WHERE ID={}'.format(randInsult))
    insult = str(c.fetchall())
    
    insultArray = list(insult)
    length = len(insult)
    del insultArray[length - 4:length]
    del insultArray[:3]
    insult = "".join(insultArray)

    tweet += insult
    print(tweet)
    api.update_status(tweet)

#loops through each tweet, random intervals (1-24 hours between a tweet)
def loop():

    while True:
        delay = random.randint(1, 24) * 60 * 60
        #does not tweet between 8 and 12 (cause that is just plain rude)
        if (time.strftime("%H") + delay > 8):
            print( delay / 3600, " hrs")
            scheduler.enter(delay, 1, insult, ())
        else:
            deltaDelay = 8 - time.strftime("%H") + delay
            delay += deltaDelay
            if delay < 0:
                delay += 12
            print( delay / 3600, " hrs")
            scheduler.enter(delay, 1, insult, ())
            scheduler.run()


loop()
