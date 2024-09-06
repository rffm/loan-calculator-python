import argparse
import math

parser = argparse.ArgumentParser(description="This a Loan Calculator.")

parser.add_argument("--interest")
parser.add_argument("--type")

parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")

args = parser.parse_args()

interest = float(args.interest) if args.interest is not None else None
P = int(args.principal) if args.principal is not None else None
n = int(args.periods) if args.periods is not None else None
A = float(args.payment) if args.payment is not None else None
T = args.type

if T is None or T not in ["annuity", "diff"] or \
        (T == "diff" and A is not None) or \
        interest is None or \
        (P is not None and P < 0) or \
        (n is not None and n < 0) or \
        (A is not None and A < 0) or \
        interest < 0:
    print("Incorrect parameters")
    exit(0)


def get_monthly_interest_rate(annual_interest_rate):
    return annual_interest_rate*0.01/12


i = get_monthly_interest_rate(interest)

S = 0
if A is None:
    if T == "annuity":
        A = math.ceil(P * (i * (1 + i)**n) / ((1+i)**n - 1))
        S = A * n
        print(f"Your annuity payment is = {A}!")
    elif T == "diff":
        for m in range(1, n + 1):
            A = math.ceil(P / n + i * (P - P * (m - 1) / n))
            S += A
            print(f"Month {m}: payment is {A}")
elif P is None:
    P = math.ceil(A / (i * (1+i)**n / ((1+i)**n - 1)))
    print(f"Your loan principal = {P}!")
    S = math.ceil(A * n)
elif n is None:
    n = math.ceil(math.log(A / (A - i*P), 1 + i))

    S = math.ceil(A * n)

    y = n // 12
    m = n % 12

    term_string = ""

    if y > 0:
        term_string = f"{y} year" if y == 1 else f"{y} years"
        if m > 0:
            term_string += f" and {m} month" if m == 1 else f" and {m} months"
    else:
        term_string = ""
        if m > 0:
            term_string += f"{m} month" if m == 1 else f"{m} months"

    print(f"It will take {term_string} to replay this loan!")

O = S - P
print(f"\nOverpayment = {O}")
