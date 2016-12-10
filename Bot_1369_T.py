import random
import sqlite3
import tweepy
import time
import sched
import sys

auth = tweepy.OAuthHandler('xPrQuyFZchSsPZPNPaxGPswOJ', 'gKbylT2vQ5FrW5LN4TVGeDuAJGUG7OeZaZ0xlO8t4CP7ukhBtU')
auth.set_access_token('807662546035609600-TsM9nFnNSROw6MaekK5tULzWNk4qYgh', 'XYPctUGSHETmNT7p3nfnqCdDJIjPnuzeusXVZ8rDr7mzl')
api = tweepy.API(auth)

conn = sqlite3.connect("Database.db")
c = conn.cursor()
print("Connected to database")

scheduler = sched.scheduler(time.time, time.sleep)


def status(tweet):
    api.update_status(tweet)

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
    #status(tweet)

#status(insult())
#insult()
def loop():

    while True:
        delay = random.randint(1, 34) * 60 * 60
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