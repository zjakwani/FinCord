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
import calculator


@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    text = '{0.content}'.format(message).split()
    print(text)
    stext = ' '.join(text)
    ttext = vectorizer.transform([stext]) # transformed text
    dact = classifier.predict(ttext)[0] # get dialog act of stext

    twoFound = False
    span = 2
    doubleOne = [" ".join(text[i:i+span]) for i in range(0, len(text), span)]
    doubleTwo = [" ".join(text[i:i+span]) for i in range(1, len(text), span)]

    if dact == 'whQuestion':

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
    await bot.process_commands(message)
    
        
@bot.command(name='retire', help='How much money do I need to retire? Input monthly budget.')
async def retire(ctx, monthly_budget: int):
    res = calculator.total_retirement_monthly(monthly_budget)
    await ctx.send(res)

@bot.command(name='compound', help="Calculate compound interest. Input principal balance (initial amount in dollars) and number of years. Optionally input interest rate in percent and/or number of times interest applied per year.")
async def compound(ctx, principal: int, years: int, interest_rate: int = 6, n: int = 1):
    res = calculator.compound_interest(principal, years, interest_rate, n)
    await ctx.send(res)

@bot.command(name='when', help="How many years until I can retire? Input monthly budget, amount you can save annually, amount already saved, and current age. Optionally input annual interest rate (for your savings) as a percent and/or desired retirement age.")
async def compound(ctx, monthly_budget: int, save_annually: int, amount_saved: int, cur_age: int, interest_rate: int = 6, retire_age: int = 65):
    res = calculator.retirement_age(monthly_budget, save_annually, amount_saved, cur_age, interest_rate, retire_age)
    await ctx.send(res)

key = open('key.txt').read()
bot.run(key)

