
# functions for retirement calculations
# in reality these would be replaced with custom made Capital One formulas

# How much money do I need to retire? 
# Description (output this through the bot) - 
#   This is the 25x rule, a common estimate used by experts
# Inputs - monthly budget or annual budget
# source: https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/
# working test case - total_retirement_monthly(4000) and total_retirement_annual(48000)-> 1200000
def total_retirement_monthly(monthly_budget):
    res = monthly_budget * 12 * 25
    print("You need about $" + str(res) + " for retirement.")
    return res
def total_retirement_annual(annual_budget):
    res = annual_budget * 25
    print("You need about $" + str(res) + " for retirement!")
    return res

# Compound interest 
# Description (output this through the bot) - 
#   Wikipedia - Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, interest on interest. It is the result of reinvesting interest, rather than paying it out, so that interest in the next period is then earned on the principal sum plus previously accumulated interest.
# inputs - initial principal balance, time in years
# optional inputs - annual interest rate as a percent (default 6%), number of times interest applied per time period (default 1)
# source - https://en.wikipedia.org/wiki/Compound_interest
# working test case - compound_interest(30000, 2.5, 4, 365) -> 33154
def compound_interest(principal, years, interest_rate=6, n=1):
    interest_decimal = interest_rate / 100
    res = int(principal * ((1 + (interest_decimal / n)) ** (n * years)))
    print("Your return is exactly $" + str(res) + "!")
    return res

# What age can I retire?
# Description (output this through the bot) -
#   This uses the 25x rule, current savings, and compound interest result to calculate the age of retirement. 
# Inputs - target (result from "How much money do I need to retire?"), amount you can save per year, current age, amount already saved
# Optional inputs -  annual interest rate as a percent (default 6%), retirement age (default 65)
# source: https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/
# working test case: retirement_age(900000, 12000, 35, 75000, 5, 75) -> 24
def retirement_age(target25, save_annually, cur_age, amount_saved, interest_rate=6, retire_age=65):
    target = target25 - amount_saved
    compound = compound_interest(amount_saved, retire_age - cur_age, interest_rate)
    target -= compound
    res = int(target // save_annually)
    print("You can retire in about " + str(res) + " years!")
    return res

