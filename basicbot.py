import discord
import csv
import os

import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
 
lemmatizer = WordNetLemmatizer()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        mydict = {}
        reader = csv.reader(open("financial_terms.csv", "r"))
        for rows in reader:
            k = lemmatizer.lemmatize(rows[0].lower())
            v = rows[1]
            mydict[k] = v
        text = '{0.content}'.format(message).split()
        print(text)
        for word in text:
            lemma = lemmatizer.lemmatize(word.lower())
            if lemma in mydict:
                reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
                await message.reply(reply, mention_author=True)
                print("recognized")
        


key = open('key.txt').read()
client = MyClient()
client.run(key)

