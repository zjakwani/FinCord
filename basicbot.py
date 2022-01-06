import csv
import os
import pickle

import discord
import nltk

nltk.download('wordnet')
from discord.ext import commands
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

lemmatizer = WordNetLemmatizer()
bot = commands.Bot(command_prefix='!')

mydict = {}
reader = csv.reader(open("financial_terms.csv", "r"))
for rows in reader:
    k = lemmatizer.lemmatize(rows[0].lower())
    v = rows[1]
    mydict[k] = v

f = open('nlp/classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

f = open('nlp/vectorizer.pickle', 'rb')
vectorizer = pickle.load(f)
f.close()

@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    text = '{0.content}'.format(message).split()
    
    stext = ' '.join(text)
    ttext = vectorizer.transform([stext]) # transformed text
    dact = classifier.predict(ttext)[0] # get dialog act of stext
    if dact == 'whQuestion':
        for word in text:
            lemma = lemmatizer.lemmatize(word.lower())
            if lemma in mydict:
                reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
                await message.reply(reply, mention_author=True)
                print("recognized")
        


key = open('key.txt').read()
bot.run(key)

