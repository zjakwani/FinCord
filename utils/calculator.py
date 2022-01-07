
# functions for retirement calculations
# in reality these would be replaced with custom made Capital One formulas

# How much money do I need to retire? 
# Description (output this through the bot) - 
#   This is the 25x rule, a common estimate used by experts
# Inputs - monthly budget 
# source: https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/
# working test case - total_retirement_monthly(4000) and total_retirement_annual(48000)-> 1200000
def total_retirement_month(monthly_budget):
    return monthly_budget * 12 * 25
def total_retirement_monthly(monthly_budget):
    res = total_retirement_month(monthly_budget)
    output = "You need about $" + str(res) + " for retirement!\n"
    output += "\nThis is according to the 25x rule of thumb for expected retirement expenditures."
    output += "\nSource: <https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/>"
    return output

# Compound interest 
# Description (output this through the bot) - 
#   Wikipedia - Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, interest on interest. It is the result of reinvesting interest, rather than paying it out, so that interest in the next period is then earned on the principal sum plus previously accumulated interest.
# inputs - initial principal balance, time in years
# optional inputs - annual interest rate as a percent (default 6%), number of times interest applied per time period (default 1)
# source - https://en.wikipedia.org/wiki/Compound_interest
# working test case - compound_interest(30000, 3, 4, 365) -> 33154
def compound(principal, years, interest_rate=6, n=1):
    interest_decimal = interest_rate / 100
    res = int(principal * ((1 + (interest_decimal / n)) ** (n * years)))
    return res
def compound_interest(principal, years, interest_rate=6, n=1):
    res = compound(principal, years, interest_rate, n)
    output = "Your return is exactly $" + str(res) + "!\n"
    output += "\nThe formula used was Principal * (1 + interest rate / n) ^ n * years."
    output += "\nWikipedia - Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, interest on interest. It is the result of reinvesting interest, rather than paying it out, so that interest in the next period is then earned on the principal sum plus previously accumulated interest."
    output += "\nSource: <https://en.wikipedia.org/wiki/Compound_interest>"
    return output

# What age can I retire?
# Description (output this through the bot) -
#   This uses the 25x rule, current savings, and compound interest result to calculate the age of retirement. 
# Inputs - monthly budget, amount you can save per year, current age, amount already saved
# Optional inputs -  annual interest rate as a percent (default 6%), retirement age (default 65)
# source: https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/
# working test case: retirement_age(3000, 12000, 35, 75000, 5, 75) -> 24
def retirement_age(monthly_budget, save_annually, amount_saved, cur_age, interest_rate=6, retire_age=65):
    years = retire_age - cur_age
    target = total_retirement_month(monthly_budget) - amount_saved
    compound_i = compound(amount_saved, years, interest_rate)
    target -= compound_i
    res = int(target // save_annually)
    output = "You can retire in about " + str(res) + " years!\n"
    output += "\nThis was calculated using the 25x rule as a target, then accounting for current savings and assuming compound interest over time, and finally dividing by amount saved per year."
    output += "\nDuring the " + str(years) + " years until your retirement, your savings compounded to about $" + str(compound_i) + "."
    output += "\nSource: <https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/>"
    return output

def all_commands():
    output = "Use !help followed by any command to show details on its usage.\n"
    output += "\nRetirement Predictions: !retire !when"
    output += "\nRetirement Savings Calculations: !401k !max401k !roth"
    output += "\nCredit card calculation: !credit"
    output += "\nInvestment focused calculations: !returns !inflation !cagr"
    output += "\nLoan focused calculations: !loan !loancomp !college"
    return output
