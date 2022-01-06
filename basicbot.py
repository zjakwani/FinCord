import csv
import os

import discord
import nltk

nltk.download('wordnet')
from discord.ext import commands
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    mydict = {}
    reader = csv.reader(open("financial_terms.csv", "r"))
    for rows in reader:
        k = lemmatizer.lemmatize(rows[0].lower())
        v = rows[1]
        mydict[k] = v
    text = '{0.content}'.format(message).split()
    print(text)
    twoFound = False
    span = 2
    doubleOne = [" ".join(text[i:i+span]) for i in range(0, len(text), span)]
    doubleTwo = [" ".join(text[i:i+span]) for i in range(1, len(text), span)]

    for word in doubleOne:
        lemma = lemmatizer.lemmatize(word.lower())
        if lemma in mydict:
            print("doubleOne")
            reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
            await message.reply(reply, mention_author=True)
            print("recognized")
            twoFound = True
    
    if not twoFound:
        for word in doubleTwo:
            lemma = lemmatizer.lemmatize(word.lower())
            if lemma in mydict:
                print("doubleTwo")
                reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
                await message.reply(reply, mention_author=True)
                print("recognized")
                twoFound = True

    if not twoFound:
        for word in text:
            lemma = lemmatizer.lemmatize(word.lower())
            if lemma in mydict:
                print("orig")
                reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
                await message.reply(reply, mention_author=True)
                print("recognized")
                twoFound = True

key = open('key.txt').read()
bot.run(key)

