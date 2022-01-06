
# functions for retirement calculations
# in reality these would be replaced with custom made Capital One formulas

# How much money do I need to retire? 
# Description (output this through the bot) - 
#   This is the 25x rule, a common estimate used by experts
# Inputs - monthly budget or annual budget
# source: https://www.synchronybank.com/blog/ultimate-guide-to-retirement-calculations/
def total_retirement_monthly(monthly_budget):
    res = monthly_budget * 12 * 25
    print("You need about $" + str(res) + " for retirement.")
    return res
def total_retirement_annual(annual_budget):
    res = annual_budget * 25
    print("You need about $" + str(res) + " for retirement.")
    return res

