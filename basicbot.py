import csv
import os
import pickle

import discord
import nltk
from nltk import ngrams
from nltk.util import pr

from Database import read_data

nltk.download('wordnet')

from discord.ext import commands
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

import creditinfo

lemmatizer = WordNetLemmatizer()

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(command_prefix='!', help_command = help_command)

mydict = read_data()

# Old way we were reading in the data. Can delete later 
# reader = csv.reader(open("financial_terms.csv", "r"))
# for rows in reader:
#     k = lemmatizer.lemmatize(rows[0].lower())
#     v = rows[1]
#     mydict[k] = v

f = open('nlp/classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

f = open('nlp/vectorizer.pickle', 'rb')
vectorizer = pickle.load(f)
f.close()
import calculator
import calculator2


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

    if dact == 'whQuestion':
        gram = 4
        for i in range(gram):
            ngram = ngrams(text,i)
            for gram in ngram:
                sgram = " ".join(gram)
                lemma = lemmatizer.lemmatize(sgram.lower())
                if lemma in mydict:
                    print("orig")
                    reply = 'FinBot recognized ' + sgram  +': ' + mydict[lemma]
                    await message.reply(reply, mention_author=True)
                    print("recognized")

            
    await bot.process_commands(message)

card_info = creditinfo.get_card_info('credit_info.csv')

@bot.command(name='compare', help='compare capital one credit cards')
async def compare(ctx, c1: str, c2: str):
    res = creditinfo.compare_cards(c1, c2, card_info)
    await ctx.send(embed=res)
        
@bot.command(name='retire', help='How much money do I need to retire? Input monthly budget.')
async def retire(ctx, monthly_budget: int):
    res = calculator.total_retirement_monthly(monthly_budget)
    await ctx.send(res)

@bot.command(name='compound', help="Calculate compound interest. Input principal balance (initial amount in dollars) and number of years. Optionally input interest rate in percent and/or number of times interest applied per year.")
async def compound(ctx, principal: int, years: int, interest_rate: int = 6, n: int = 1):
    res = calculator.compound_interest(principal, years, interest_rate, n)
    await ctx.send(res)

@bot.command(name='when', help="How many years until I can retire? Input monthly budget, amount you can save annually, amount already saved, and current age. Optionally input annual interest rate (for your savings) as a percent and/or desired retirement age.")
async def when(ctx, monthly_budget: int, save_annually: int, amount_saved: int, cur_age: int, interest_rate: int = 6, retire_age: int = 65):
    res = calculator.retirement_age(monthly_budget, save_annually, amount_saved, cur_age, interest_rate, retire_age)
    await ctx.send(res)

@bot.command(name='loan', help="Calculates total cost of a loan. Inputs: Starting loan amount (principal), interest rate (% APR as a decimal), and length of the loan term in months.")
async def loanCalculator(ctx, principal: int, apr: int, term_in_months: int):
    res = calculator2.loanCalculator(principal, apr, term_in_months)
    await ctx.send(res)

@bot.command(name='loancomp', help="Compares two loans. Loan terms in years. Returns the total cost of Loan 1, total cost of Loan 2, and then the dollar difference between the loans' totals.")
async def loanComparison(ctx, loanAmt: int, loanInterest1: int, loanTerm1: int, loanInterest2: int, loanTerm2: int):
    res = calculator2.loanComparison(loanAmt, loanInterest1, loanTerm1, loanInterest2, loanTerm2)
    await ctx.send(res)

@bot.command(name='credit', help="How long until my credit card is paid off? Assumes that payments are made at the end of each month, after interest has been accrued. Inputs: Starting credit card balance, card interest rate (% APY), expected payment per-month.")
async def credit(ctx, card_balance: int, interest_rate: int, ppm: int):
    res = calculator2.creditCardPayoff(card_balance, interest_rate, ppm)
    await ctx.send(res)

@bot.command(name='401k', help="401k retirement planner. Assumption: All contributions, including match, are made at the end of the year. Inputs: Current Account Value, Salary, Expected Annual Raise (in %), Expected Annual Contribution, Employer 401k Match (in %), Expected Investment Return (in %), and number of total years.")
async def retirement401kcalc(ctx, current_amt: int, salary: int, annual_raise: int, contribution: int, employer_match: int, investment_return: int, years: int):
    res = calculator2.retirement401kcalc(current_amt, salary, annual_raise, contribution, employer_match, investment_return, years, [])
    await ctx.send(res)

@bot.command(name='returns', help="Calculates 'real' investment returns given an initial value, and average annual growth rate, an average annual inflation rate, a fee amount as percent, and a tax rate as percent. Essentially, values are used to calculate 'real' investment returns, after inflation, fees, and taxes.")
async def realInvestmentReturns(ctx, value: int, growth_rate: int, inflation_rate: int, fee: int, tax_rate: int, years: int):
    res = calculator2.realInvestmentReturns(value, growth_rate, inflation_rate, fee, tax_rate, years)
    await ctx.send(res)

@bot.command(name='cagr', help="Calculate annual rate of return of investment based on beginning amount, final amount and number of years. Inputs: Starting amount, ending amount, total time in years.")
async def investmentCAGRCalculator(ctx, principal: int, final_amt: int, time_in_years: int):
    res = calculator2.investmentCAGRCalculator(principal, final_amt, time_in_years)
    await ctx.send(res)

@bot.command(name='max401k', help="# Returns the maximum amount of yearly contributions allowed to a 401k based on age (based on 2022). Inputs: Age")
async def retirement401kcalc(ctx, current_amt: int, salary: int, annual_raise: int, contribution: int, employer_match: int, investment_return: int, years: int):
    res = calculator2.retirement401kcalc(current_amt, salary, annual_raise, contribution, employer_match, investment_return, years, [])
    embed=discord.Embed(title="401k Retirement Planner", url=res[0])
    embed.image = res[1]
    await ctx.send(embed=embed)

key = open('key.txt').read()
bot.run(key)

