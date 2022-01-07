import csv
import os
import pickle

import discord
import nltk
from nltk import ngrams
from nltk.util import pr

from utils.calculator import *
from utils.calculator2 import *
from utils.creditinfo import *
from utils.stock_info import *
from utils.Database import read_data

nltk.download('wordnet')

from discord.ext import commands
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

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

card_info = get_card_info('data/credit_info.csv')

@bot.command(name='stock', help="# View information about a specific stock given it's ticker (ex: \"COF\" = Capital One)")
async def stockInfo_(ctx, ticker: str):
    res = stockInfo(ticker)
    print(res)
    e=discord.Embed(title="Stock Information")
    e.set_thumbnail(url = res.get("logo_url"))
    e.add_field(name="Company Name: ", value=res.get("longName") + " (" + ticker + ")", inline=False)
    e.add_field(name="Current Price", value=res.get("regularMarketPrice"), inline=True)
    e.add_field(name="Market Cap", value="{:.2f}B".format(int(res.get("marketCap")) / 1000000000.00), inline=True)
    e.add_field(name="Sector", value=res.get("sector"), inline=True)
    pe_ratio = res.get("trailingPE")

    if (pe_ratio != None):
        pe_ratio = round(float(pe_ratio), 2)
    e.add_field(name="PE (TTM)", value=pe_ratio, inline=True)
    e.add_field(name="EPS (TTM)", value=res.get("trailingEps"), inline=True)
    div_yield = res.get("dividendYield")

    if (div_yield != None):
        div_yield = str(round(float(div_yield)) * 100, 2) + "%"
    e.add_field(name="Dividend (%)", value= div_yield, inline=True)
    e.add_field(name= "Day High", value=res.get("dayHigh"), inline=True)
    e.add_field(name="52-wk High", value=res.get("fiftyTwoWeekHigh"), inline=True)
    e.add_field(name="52-wk Change (%)", value=str(round(float(res.get("52WeekChange")) * 100, 2)) + "%", inline=True)
    e.add_field(name="Day Low", value=res.get("dayLow"),inline=True)
    e.add_field(name="52-wk Low", value=res.get("fiftyTwoWeekLow"), inline=True)
    e.add_field(name="Beta",value="{:.2f}".format(res.get("beta")), inline=True)

    await ctx.send(embed=e)

@bot.command(name='compare', help='Compare capital one credit cards. Input card names seperated by /')
async def compare(ctx, *, message):
    c1, c2 = message.split('/')
    res = compare_cards(c1, c2, card_info)
    await ctx.send(embed =res)
        
@bot.command(name='retire', help='How much money do I need to retire? Input monthly budget.')
async def retire_(ctx, monthly_budget: int):
    res = total_retirement_monthly(monthly_budget)
    await ctx.send(res)

@bot.command(name='compound', help="Calculate compound interest. Input principal balance (initial amount in dollars) and number of years. Optionally input interest rate in percent and/or number of times interest applied per year.")
async def compound_(ctx, principal: int, years: int, interest_rate: int = 6, n: int = 1):
    res = compound_interest(principal, years, interest_rate, n)
    await ctx.send(res)

@bot.command(name='when', help="How many years until I can retire? Input monthly budget, amount you can save annually, amount already saved, and current age. Optionally input annual interest rate (for your savings) as a percent and/or desired retirement age.")
async def when_(ctx, monthly_budget: int, save_annually: int, amount_saved: int, cur_age: int, interest_rate: int = 6, retire_age: int = 65):
    res = retirement_age(monthly_budget, save_annually, amount_saved, cur_age, interest_rate, retire_age)
    await ctx.send(res)

@bot.command(name='loan', help="Calculates total cost of a loan. Inputs: Starting loan amount (principal), interest rate (% APR as a decimal), and length of the loan term in months.")
async def loanCalculator_(ctx, principal: int, apr: int, term_in_months: int):
    res = loanCalculator(principal, apr, term_in_months)
    await ctx.send(res)

@bot.command(name='loancomp', help="Compares two loans. Loan terms in years. Returns the total cost of Loan 1, total cost of Loan 2, and then the dollar difference between the loans' totals.")
async def loanComparison_(ctx, loanAmt: int, loanInterest1: int, loanTerm1: int, loanInterest2: int, loanTerm2: int):
    res = loanComparison(loanAmt, loanInterest1, loanTerm1, loanInterest2, loanTerm2)
    await ctx.send(res)

@bot.command(name='credit', help="How long until my credit card is paid off? Assumes that payments are made at the end of each month, after interest has been accrued. Inputs: Starting credit card balance, card interest rate (% APY), expected payment per-month.")
async def credit_(ctx, card_balance: int, interest_rate: int, ppm: int):
    res = creditCardPayoff(card_balance, interest_rate, ppm)
    await ctx.send(res)

@bot.command(name='max401k', help="401k retirement planner. Assumption: All contributions, including match, are made at the end of the year. Inputs: Current Account Value, Salary, Expected Annual Raise (in %), Expected Annual Contribution, Employer 401k Match (in %), Expected Investment Return (in %), and number of total years.")
async def max401kcalc_(ctx, age: int):
    res = maxContributions401k(age)
    await ctx.send(res)

@bot.command(name='returns', help="Calculates 'real' investment returns given an initial value, and average annual growth rate, an average annual inflation rate, a fee amount as percent, and a tax rate as percent. Essentially, values are used to calculate 'real' investment returns, after inflation, fees, and taxes.")
async def realInvestmentReturns_(ctx, value: int, growth_rate: int, inflation_rate: int, fee: int, tax_rate: int, years: int):
    res = realInvestmentReturns(value, growth_rate, inflation_rate, fee, tax_rate, years)
    await ctx.send(res)

@bot.command(name='cagr', help="Calculate annual rate of return of investment based on beginning amount, final amount and number of years. Inputs: Starting amount, ending amount, total time in years.")
async def investmentCAGRCalculator_(ctx, principal: int, final_amt: int, time_in_years: int):
    res = investmentCAGRCalculator(principal, final_amt, time_in_years)
    await ctx.send(res)

@bot.command(name='401k', help="401k retirement planner. Assumption: All contributions, including match, are made at the end of the year. Inputs: Current Account Value, Salary, Expected Annual Raise (in %), Expected Annual Contribution, Employer 401k Match (in %), Expected Investment Return (in %), and number of total years.")
async def retirement401kcalc_(ctx, current_amt: int, salary: int, annual_raise: int, contribution: int, employer_match: int, investment_return: int, years: int):
    annual_raise /= 100
    employer_match /= 100
    investment_return /= 100
    res = retirement401kcalc(current_amt, salary, annual_raise, contribution, employer_match, investment_return, years, [])
    e=discord.Embed(title="401k Retirement Planner", description=res[0])
    e.set_image(url=res[1])
    await ctx.send(embed=e)

@bot.command(name='inflation', help="Calculates inflation over time. Given a rate of inflation, calculates the 'real' value of dollar amount after a given number of years. Inputs: Starting value, given inflation rate (as a %), and number of years")
async def futureInflationCalculator_(ctx, value: int, given_inflation_rate: int, years: int):
    res = futureInflationCalculator(value, given_inflation_rate, years, [])
    e=discord.Embed(title="The real value of your money after inflation", description=res[0])
    e.set_image(url=res[1])
    await ctx.send(embed=e)

@bot.command(name='roth', help="Max annual Roth IRA contributions. Returns the maximum amount of yearly contributions allowed to a Roth IRA based on age and income (based on 2022). Inputs: Age, Household Income")
async def maxContributionsRothIRA_(ctx, age: int, household_income: int):
    res = maxContributionsRothIRA(age, household_income)
    await ctx.send(res)

@bot.command(name='college', help="How should I pay off my college loans? Returns the percent of income put towards loans in order to pay them off within a given number of years. Assumes interest still accumulates while in school and that payments only begin after graduation. Inputs: College savings, tuition cost per year, expected years of school attendance, desired years after school until loan is payed off, and expected salary after graduation. Outputs: Estimated yearly cost of loans, estimated percent of salary put towards student loans.")
async def collegeAffordibilityCalculator_(ctx, balance: int, tuition_rate: int, years_of_school: int, loan_interest: int, years_until_paid: int, expected_postgrad_salary: int):
    res = collegeAffordibilityCalculator(balance, tuition_rate, years_of_school, loan_interest, years_until_paid, expected_postgrad_salary)
    await ctx.send(res)

@bot.command(name='list', help="Lists all commands.")
async def realInvestmentReturns_(ctx):
    res = all_commands()
    await ctx.send(res)

key = open('key.txt').read()
bot.run(key)

