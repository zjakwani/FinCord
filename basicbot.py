import discord
import csv


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        

    async def on_message(self, message):
        mydict = {}
        reader = csv.reader(open("data.csv", "r"))
        for rows in reader:
            k = rows[0]
            v = rows[1]
            mydict[k] = v
        text = '{0.content}'.format(message).split()
        print(text)
        for word in text:
            if word in mydict:
                print('FinBot recognized ' + word  +': ' + mydict[word])
        


key = open('key.txt').read()
client = MyClient()
client.run(key)
