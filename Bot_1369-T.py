import random
import sqlite3
import tweepy
import time
import sched
import sys

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)

scheduler = sched.scheduler(time.time, time.sleep)

def getUser():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    print("Connected to database")

    randUser = random.randint(1, 6)
    c.execute('SELECT handle FROM Users WHERE ID={};'.format(randUser))
    user = str(c.fetchall())
    userArray = list(user)
    userLength = len(user)
    del userArray[userLength - 4:userLength]
    del userArray[:3]
    user = "".join(userArray)
    return user
    conn.close()

def catalog(insult):
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    print("Connected to database")

    print(time.strftime("%D : %H:%M:%S"))
    date = str(time.strftime("%D : %H:%M:%S"))
    c.execute('INSERT INTO Insult_Catalog (date, insult) VALUES (?, ?)',(date, insult,))
    conn.commit()
    conn.close()

def createInsult():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    print("Connected to database")

    endInsult = getUser() + " "
    randP1 = random.randint(1, 26)
    c.execute('SELECT phrase FROM phrase1 WHERE ID={};'.format(randP1))
    phrase1 = str(c.fetchall())
    phrase1Array = list(phrase1)
    p1length = len(phrase1Array)
    del phrase1Array[p1length - 4:p1length]
    del phrase1Array[:3]
    phrase1 = "".join(phrase1Array)
    endInsult += phrase1 + " "

    randP2 = random.randint(1, 26)
    c.execute('SELECT phrase FROM phrase2 WHERE ID={};'.format(randP2))
    phrase2 = str(c.fetchall())
    phrase2Array = list(phrase2)
    p2length = len(phrase2Array)
    del phrase2Array[p2length - 4:p2length]
    del phrase2Array[:3]
    phrase2 = "".join(phrase2Array)
    endInsult += phrase2 + " "

    randP3 = random.randint(1, 26)
    c.execute('SELECT phrase FROM phrase3 WHERE ID={};'.format(randP3))
    phrase3 = str(c.fetchall())
    phrase3Array = list(phrase3)
    p3length = len(phrase3Array)
    del phrase3Array[p3length - 4:p3length]
    del phrase3Array[:3]
    phrase3 = "".join(phrase3Array)
    endInsult += phrase3 + " "

    randP4 = random.randint(1, 20)
    c.execute('SELECT phrase FROM phrase4 WHERE ID={};'.format(randP4))
    phrase4 = str(c.fetchall())
    phrase4Array = list(phrase4)
    p4length = len(phrase4Array)
    del phrase4Array[p4length - 4:p4length]
    del phrase4Array[:3]
    phrase4 = "".join(phrase4Array)
    endInsult += phrase4 + " "

    randP5 = random.randint(1, 15)
    c.execute('SELECT phrase FROM phrase5 WHERE ID={};'.format(randP5))
    phrase5 = str(c.fetchall())
    phrase5Array = list(phrase5)
    p5length = len(phrase5Array)
    del phrase5Array[p5length - 4:p5length]
    del phrase5Array[:3]
    phrase5 = "".join(phrase5Array)
    endInsult += phrase5 + " "
    print(endInsult)
    print(len(endInsult))
    catalog(endInsult)
    conn.close()

def insult():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    print("Connected to database")
    randInsult = random.randint(1, 60)
    tweet = getUser() + " "

    print(randInsult)
    c.execute('SELECT insult FROM insults WHERE ID={};'.format(randInsult))
    insult = str(c.fetchall())
    
    insultArray = list(insult)
    length = len(insult)
    del insultArray[length - 4:length]
    del insultArray[:3]
    insult = "".join(insultArray)

    tweet += insult
    print(time.strftime("%H : %M : %S"), ": ", tweet)
    #api.update_status(tweet)
    conn.close()

def loop():

    while True:
        delay = random.randint(1, 24) * 60 * 60
        nextTweet = int(time.strftime("%H")) + delay
        if nextTweet > 23:
            nextTweet -= 24
        if nextTweet < 8 and nextTweet > 0:
            deltaTime = 8 - nextTweet
            nextTweet += deltaTime
            delay = nextTweet - int(time.strftime("%H"))

        print( delay / 3600, " hrs - Time now: ", time.strftime("%H : %M : %S"))
        scheduler.enter(delay, 1, insult, ())
        scheduler.run()

createInsult()
