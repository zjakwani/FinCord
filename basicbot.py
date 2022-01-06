import discord
import csv
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        

    async def on_message(self, message):
        mydict = {}
        reader = csv.reader(open("financial_terms.csv", "r"))
        for rows in reader:
            k = rows[0].lower()
            v = rows[1]
            mydict[k] = v
        text = '{0.content}'.format(message).split()
        print(text)
        for word in text:
            if word.lower() in mydict:
                print('FinBot recognized ' + word  +': ' + mydict[word])
        


client = MyClient()
client.run(key)
