import csv
import os

import discord
import nltk

nltk.download('wordnet')
from discord.ext import commands
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

bot = commands.Bot(command_prefix='!')

import calculator


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
    for word in text:
        lemma = lemmatizer.lemmatize(word.lower())
        if lemma in mydict:
            reply = 'FinBot recognized ' + word  +': ' + mydict[lemma]
            await message.reply(reply, mention_author=True)
            print("recognized")
    await bot.process_commands(message)
        
@bot.command(name='retire', help='How much money do I need to retire? Using the 25x baseline. Input monthly budget.')
async def retire(ctx, monthly_budget: int):
    res = calculator.total_retirement_monthly(monthly_budget)
    await ctx.send(res)

@bot.command(name='compound', help="Calculate compound interest. Input principal balance (initial amount in dollars) and number of years. Optionally input interest rate in percent and number of times interest applied per year.")
async def compound(ctx, principal: int, years: int, interest_rate: int = 6, n: int = 1):
    res = calculator.compound_interest(principal, years, interest_rate, n)
    await ctx.send(res)

key = open('key.txt').read()
bot.run(key)

