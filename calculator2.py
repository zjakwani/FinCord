from quickchart import QuickChart

# Below are some financial calculator functions (Logan)
# At the bottom of this document is code related to QuickCharts functionality

# ------------------------
# LOAN FOCUSED CALCULATORS
# ------------------------

# Calculates total cost of a loan
# Inputs: Starting loan amount (principal), interest rate (% APR as a decimal), and length of the loan term in months
def loanCalculator(principal, apr, term_in_months):
    apr /= 100
    return "The estimated total cost of your loan is $" + str(int(principal * (1 + (apr/12))**term_in_months))

# Compares two loans. Loan terms in years. Returns the total cost of Loan 1, total cost of Loan 2, and then the dollar difference between the loans' totals.
# Inputs: 
def loanComparison(loanAmt, loanInterest1, loanTerm1, loanInterest2, loanTerm2):
    loanInterest1 /= 100
    loanInterest2 /= 100
    loanCost1 = loanAmt * (1 + loanInterest1)**loanTerm1
    loanCost2 = loanAmt * (1 + loanInterest2)**loanTerm2
    if loanCost1 < loanCost2:
        betterLoan = "The first loan"
    else:
        betterLoan = "The second loan"
    return "The total cost of the first loan is $" + str(int(loanCost1)) + ". The total cost of the second loan is $" + str(int(loanCost2)) +". The difference between the loans is $" + str(int(abs(loanCost1 - loanCost2))) + ". " + betterLoan + " cost less in total." 

# Returns the percent of income put towards loans in order to pay them off within a given number of years.
# Assumes interest still accumulates while in school and that payments only begin after graduation.
# Inputs: College savings, tuition cost per year, expected years of school attendance, desired years after school until loan is payed off, and expected salary after graduation
# Outputs: Estimated yearly cost of loans, estimated percent of salary put towards student loans.
def collegeAffordibilityCalculator(balance, tuition_rate, years_of_school, loan_interest, years_until_paid, expected_postgrad_salary):
    while (years_of_school > 0):
        if (balance > 0) and (balance > tuition_rate) and (years_until_paid != 0):
            balance -= tuition_rate
        elif (balance > 0) and (years_until_paid != 0):
            balance = balance - tuition_rate
            balance *= (1 + loan_interest)
        else:
            balance *= (1 + loan_interest)
        years_of_school -= 1
    yearly_cost = (balance * (1 + loan_interest)**years_until_paid) / 12
    percentCostOfSalary = yearly_cost / expected_postgrad_salary

    return yearly_cost, percentCostOfSalary

# ------------------------------
# INVESTMENT FOCUSED CALCULATORS
# ------------------------------

# Calculates "real" investment returns given an initial value, and average annual growth rate, an average annual inflation rate, a fee amount (% as decimal), and a tax rate (% as decimal)
# Essentially, values are used to calculate "real" investment returns, after inflation, fees, and taxes.
def realInvestmentReturns(value, growth_rate, inflation_rate, fee, tax_rate, years):
    if (years == 0):
        return value
    else:
        value = ((value * (1 + growth_rate)) - (value * (1 + inflation_rate))) * (1 - fee) * (1 - tax_rate)
        years -= 1
        realInvestmentReturns(value, growth_rate, inflation_rate, fee, tax_rate, years)


# Calculate annual rate of return of investment based on beginning amount, final amount and number of years.
# Inputs: Starting amount, ending amount, total time in years
def investmentCAGRCalculator(principal, final_amt, time_in_years):
    return ((final_amt / principal)**(1/time_in_years)) - 1

# Given a rate of inflation, calculates the "real" value of dollar amount after a given number of years.
# Inputs: Starting value, given inflation rate, and number of years
def futureInflationCalculator(value, given_inflation_rate, years, value_tracker):
    if (years == 0):
        return value, valueTimeCharting(value_tracker, "Dollar Value (Real)", "rgb(210, 46, 30)")
    else:
        value_tracker.append(value)
        value = value * (1 - given_inflation_rate)
        years -= 1
        return futureInflationCalculator(value, given_inflation_rate, years, value_tracker)

# -------------------------------
# -------------------------------



# -------------------------------
# CREDIT CARD FOCUSED CALCULATORS
# -------------------------------

# How long until my credit card is paid off?
# Assumes that payments are made at the end of each month, after interest has been accrued.
# Inputs: Starting credit card balance, card interest rate (% APY), expected payment per-month
def creditCardPayoff(card_balance, interest_rate, ppm):
    balance_tracker = []
    interest_rate /= 100
    if (ppm < card_balance * interest_rate / 12):
        return "Never Paid Off: Payment Less Than Interest"
    months = 0
    if (card_balance <= 0):
        balance_tracker.append(0)
        return months, valueTimeCharting(balance_tracker, "Credit Card Debt", "rgb(210, 46, 30)")
    else:
        card_balance = card_balance * (1 + (interest_rate / 12)) - ppm
        balance_tracker.append(card_balance)
        months += 1
        return creditCardPayoffSub(card_balance, interest_rate, ppm, balance_tracker, months)


def creditCardPayoffSub(card_balance, interest_rate, ppm, balance_tracker, months):
    if(card_balance <= 0):
        output = str(months) + " months."
        output += "\n" + valueTimeCharting(balance_tracker, "Credit Card Debt", "rgb(210, 46, 30)")
        return output
    else:
        card_balance = card_balance * (1 + (interest_rate / 12)) - ppm
        if (card_balance > 0):
            balance_tracker.append(card_balance)
        else:
            balance_tracker.append(0)
        months += 1
        return creditCardPayoffSub(card_balance, interest_rate, ppm, balance_tracker, months)


# -------------------------------
# -------------------------------



# ------------------------------
# RETIREMENT FOCUSED CALCULATORS
# ------------------------------
# The following section is all related to retirement accounts

# Returns the maximum amount of yearly contributions allowed to a 401k based on age (based on 2022)
# Inputs: Age
def maxContributions401k(age):
    if (age < 50):
        return 20,500
    else:
        return 27,000

# Returns the maximum amount of yearly contributions allowed to a Roth IRA based on age and income (based on 2022)
# Inputs: Age, Household Income
def maxContributionsRothIRA(age, household_income):
    if (age < 50) and (household_income < 193,000):
        return 6,000
    elif (household_income < 193,000):
        return 7,000
    else:
        return 0

# 401k retirement planner
# Assumption: All contributions, including match, are made at the end of the year.
# Inputs: Current Account Value, Salary, Expected Annual Raise (in %), Expected Annual Contribution, Employer 401k Match (in %), Expected Investment Return (in %),
#   and number of total years.
# CALL THIS FUNCTION INTITIALLY WITH annual_balances AS AN EMPTY ARRAY
def retirement401kcalc(current_amt, salary, annual_raise, contribution, employer_match, investment_return, years, annual_balances):
    annual_raise /= 100
    employer_match /= 100
    investment_return /= 100
    if (years == 0):
        # Returns the final account value, and a link to the graph for the account.
        output = "Final account value: $" + str(int(current_amt))
        output += "\n" + valueTimeCharting(annual_balances, "401k Account Value", "rgb(0, 72, 121)")
        return output
    else:
        if (contribution < (salary * employer_match)):
            match_amt = contribution
        else:
            match_amt = salary * employer_match
        current_amt = (current_amt * (1 + investment_return)) + contribution + match_amt
        salary *= (1 + annual_raise)
        annual_balances.append(current_amt)
        years = years - 1
        return retirement401kcalc(current_amt, salary, annual_raise, contribution, employer_match, investment_return, years, annual_balances)

# -------------------------------
# -------------------------------

# Graph Creation Tools

def valueTimeCharting(tracker, data_label, color):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0

    intervals = list(range(1, len(tracker) + 1))

    qc.config = {
    "type": "bar",
    "color": "Red",
    "data": {
        "labels": intervals,
        "datasets": [{
            "backgroundColor": color,
            "label": data_label,
            "data": tracker,
            }]
        }
    }
    return qc.get_short_url()


# working test cases
# print(loanCalculator(4000, 5, 12))
# print(loanComparison(5000, 4, 10, 6, 5))
# print(creditCardPayoff(200, 6,40))
# print(retirement401kcalc(40000, 60000, 3, 10000, 1, 5, 10, []))
